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

from PySide2.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide2.QtCore import Signal, QUrl, Qt
from PySide2.QtMultimedia import QSound

MODEL_PATH = "./tts_model/best_model.pth.tar"
CONFIG_PATH = "./tts_model/config.json"
OUT_FILE = "tts_out.wav"
CONFIG = load_config(CONFIG_PATH)
use_cuda = False

class Dialog(QWidget):
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
        self.response = requests.post("http://localhost:5002/webhooks/rest/webhook", headers=headers, data=data)

    def process_machine_message(self):
        '''Shows machine's message and reproduce its voice'''
        if json.loads(self.response.text):
            self.textResponse = json.loads(self.response.text)[0]["text"]
            print(self.textResponse)
            self.sqlConversationModel.send_message("Me", self.textResponse, "machine")

            self.tts.tts_predict(self.model, MODEL_PATH, self.textResponse, CONFIG, use_cuda, self.ap, OUT_FILE)
            logging.debug("Machine message: {self.textResponse}")
            QSound.play(OUT_FILE);
        else:
            logging.error("An error happened in the Rasa Server and there is no message to display.")

class TTS():

    def tts(self, model, text, CONFIG, use_cuda, ap, OUT_FILE):
        waveform, alignment, spectrogram, mel_spectrogram, stop_tokens = synthesis(model, text, CONFIG, use_cuda, ap)
        ap.save_wav(waveform, OUT_FILE)
        wav_norm = waveform * (32767 / max(0.01, np.max(np.abs(waveform))))
        return alignment, spectrogram, stop_tokens, wav_norm

    def load_tts_model(self):
        MODEL_PATH = "./tts_model/best_model.pth.tar"
        CONFIG_PATH = "./tts_model/config.json"
        CONFIG = load_config(CONFIG_PATH)
        use_cuda = False

        num_chars = len(phonemes) if CONFIG.use_phonemes else len(symbols)
        model = Tacotron(num_chars, CONFIG.embedding_size, CONFIG.audio["num_freq"], CONFIG.audio["num_mels"], CONFIG.r, attn_windowing=False)

        # load the audio processor
        # CONFIG.audio["power"] = 1.3
        CONFIG.audio["preemphasis"] = 0.97
        ap = AudioProcessor(**CONFIG.audio)

        # load model state
        if use_cuda:
            cp = torch.load(MODEL_PATH)
        else:
            cp = torch.load(MODEL_PATH, map_location=lambda storage, loc: storage)

        # load the model
        model.load_state_dict(cp["model"])
        if use_cuda:
            model.cuda()

        model.decoder.max_decoder_steps = 1000
        return model, ap, MODEL_PATH, CONFIG, use_cuda

    def tts_predict(self, model, MODEL_PATH, sentence, CONFIG, use_cuda, ap, OUT_FILE):
        align, spec, stop_tokens, wav_norm = self.tts(model, sentence, CONFIG, use_cuda, ap, OUT_FILE)
        return wav_norm