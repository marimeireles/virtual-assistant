#############################################################################
##
## Copyright (C) 2019 The Qt Company Ltd.
## Contact: https://www.qt.io/licensing/
##
## This file is part of the Qt for Python examples of the Qt Toolkit.
##
## $QT_BEGIN_LICENSE:LGPL$
## Commercial License Usage
## Licensees holding valid commercial Qt licenses may use this file in
## accordance with the commercial license agreement provided with the
## Software or, alternatively, in accordance with the terms contained in
## a written agreement between you and The Qt Company. For licensing terms
## and conditions see https://www.qt.io/terms-conditions. For further
## information use the contact form at https://www.qt.io/contact-us.
##
## GNU Lesser General Public License Usage
## Alternatively, this file may be used under the terms of the GNU Lesser
## General Public License version 3 as published by the Free Software
## Foundation and appearing in the file LICENSE.LGPL3 included in the
## packaging of this file. Please review the following information to
## ensure the GNU Lesser General Public License version 3 requirements
## will be met: https://www.gnu.org/licenses/lgpl-3.0.html.
##
## GNU General Public License Usage
## Alternatively, this file may be used under the terms of the GNU
## General Public License version 2.0 or (at your option) the GNU General
## Public license version 3 or any later version approved by the KDE Free
## Qt Foundation. The licenses are as published by the Free Software
## Foundation and appearing in the file LICENSE.GPL2 and LICENSE.GPL3
## included in the packaging of this file. Please review the following
## information to ensure the GNU General Public License requirements will
## be met: https://www.gnu.org/licenses/gpl-2.0.html and
## https://www.gnu.org/licenses/gpl-3.0.html.
##
## $QT_END_LICENSE$
##
#############################################################################

import requests
import os
import sys
import io
import json
import torch
import numpy as np
import logging
from collections import OrderedDict

from TTS.models.tacotron import Tacotron
from TTS.layers import *
from TTS.utils.data import *
from TTS.utils.audio import AudioProcessor
from TTS.utils.generic_utils import load_config
from TTS.utils.text import text_to_sequence
from TTS.utils.synthesis import synthesis
from utils.text.symbols import symbols, phonemes
from TTS.utils.visual import visualize

from PySide2.QtCore import Signal, QUrl, Qt
from PySide2.QtMultimedia import QSound

MODEL_PATH = os.path.join(os.path.dirname(__file__), "tts_model/best_model.pth.tar")
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "tts_model/config.json")
OUT_FILE = "tts_out.wav"
CONFIG = load_config(CONFIG_PATH)
use_cuda = False

class Dialog():
    def __init__(self, sqlConversationModel):
        super(Dialog, self).__init__()
        self.sqlConversationModel = sqlConversationModel

        self.userText = ""
        self.machineText = ""

        #Creates the TTS model
        self.tts = TTS()
        self.model, self.ap, MODEL_PATH, CONFIG, use_cuda  = self.tts.load_tts_model()

    def process_user_message(self):
        ''' Shows user's message in screen and send it to the ChatBot '''
        self.send_user_msg_to_chatbot(self.userText)
        logging.debug("User message: {self.textResponse}")

    def set_user_message(self, string):
        self.userText = string

    def send_user_msg_to_chatbot(self, message):
        self.sqlConversationModel.send_message("machine", message, "Me")
        headers = {"Content-type": "application/json"}
        data = "{\"sender\": \"user1\", \"message\": \" " + message + "\"}"
        self.response = requests.post("http://localhost:5002/webhooks/rest/webhook",
                        headers=headers, data=data)

    def process_machine_message(self):
        '''Shows machine's message and reproduce its voice'''
        if json.loads(self.response.text):
            self.textResponse = json.loads(self.response.text)[0]["text"]
            print(self.textResponse)
            self.sqlConversationModel.send_message("Me", self.textResponse, "machine")

            self.tts.tts_predict(self.model, MODEL_PATH, self.textResponse, CONFIG, use_cuda,
                                 self.ap, OUT_FILE)
            logging.debug("Machine message: {self.textResponse}")
            QSound.play(OUT_FILE);
        else:
            logging.error("An error happened in the Rasa Server and there's no message to display.")

class TTS():

    def tts(self, model, text, CONFIG, use_cuda, ap, OUT_FILE):
        waveform, alignment, spectrogram, mel_spectrogram, stop_tokens = synthesis(model, text,
                                                                         CONFIG, use_cuda, ap)
        ap.save_wav(waveform, OUT_FILE)
        wav_norm = waveform * (32767 / max(0.01, np.max(np.abs(waveform))))
        return alignment, spectrogram, stop_tokens, wav_norm

    def load_tts_model(self):
        CONFIG = load_config(CONFIG_PATH)

        model = Tacotron(len(phonemes), CONFIG.embedding_size, CONFIG.audio["num_freq"],
                CONFIG.audio["num_mels"], CONFIG.r, attn_windowing=False)

        # load the audio processor
        ap = AudioProcessor(**CONFIG.audio)

        # load model state
        cp = torch.load(MODEL_PATH, map_location=lambda storage, loc: storage)

        # load the model
        model.load_state_dict(cp["model"])

        model.decoder.max_decoder_steps = 650
        return model, ap, MODEL_PATH, CONFIG, use_cuda

    def tts_predict(self, model, MODEL_PATH, sentence, CONFIG, use_cuda, ap, OUT_FILE):
        align, spec, stop_tokens, wav_norm = self.tts(model, sentence, CONFIG, use_cuda, ap,
                                             OUT_FILE)
        return wav_norm
