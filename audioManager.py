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

import sys
import os
import random
import numpy as np
import queue
import threading
import logging

from deepspeech import Model

from PySide2.QtCore import QObject, Signal, Slot
from PySide2.QtMultimedia import QAudioInput, QAudioFormat

N_FEATURES = 25
N_CONTEXT = 9
BEAM_WIDTH = 500
LM_ALPHA = 0.75
LM_BETA = 1.85

class InferenceThread(QObject):
    finished = Signal(str)

    def __init__(self):
        super(InferenceThread, self).__init__()
        self.in_queue = queue.Queue()
        self.should_quit = False
        self.worker = threading.Thread(target=self.run)

    def send_cmd(self, cmd):
        ''' Insert command in queue to be processed by the thread '''
        self.in_queue.put(cmd)

    def setQuit(self):
        ''' Signal to the thread that it should stop running '''
        self.should_quit = True

    def start(self):
        self.worker.start()

    def run(self):
        # Creating the model
        self.model = Model( os.path.join(os.path.dirname(__file__),
                     "deepspeech-0.5.1-models/output_graph.pbmm"), N_FEATURES,
                     N_CONTEXT,  os.path.join(os.path.dirname(__file__),
                     "deepspeech-0.5.1-models/alphabet.txt"), BEAM_WIDTH)
        self.model.enableDecoderWithLM( os.path.join(os.path.dirname(__file__),
            "deepspeech-0.5.1-models/alphabet.txt"),
            os.path.join(os.path.dirname(__file__),
            "deepspeech-0.5.1-models/lm.binary"),
            os.path.join(os.path.dirname(__file__),
            "deepspeech-0.5.1-models/trie"), LM_ALPHA, LM_BETA)
        stream = None

        while True:
            # Try to get the next command from our queue, use a timeout to check
            # periodically for a quit signal so the application doesn't hang on
            # exit.
            try:
                cmd, *data = self.in_queue.get(timeout=0.3)
            except queue.Empty:
                if self.should_quit:
                    break
                # If we haven't received a quit signal just continue trying to
                # get a command from the queue indefinitely
                continue

            if cmd == "start":
                # "start" means create a new stream
                stream = self.model.setupStream()
                logging.debug("Starts to process sound")
            elif cmd == "data":
                # "data" means we received more audio data from the recorder
                if stream:
                    self.model.feedAudioContent(stream,
                        np.frombuffer(data[0].data(), np.int16))
            elif cmd == "finish":
                # "finish" means the caller wants the result of the current stream
                transcript = self.model.finishStream(stream)
                self.finished.emit(transcript)
                stream = None
                logging.debug("Finishes to process sound")


class AudioRecorder(QObject):
    def __init__(self, dialog, inference_thread):
        super(AudioRecorder, self).__init__()

        self.dialog = dialog
        self.inference_thread = inference_thread

        self.inference_thread.finished.connect(self.on_transcription_finished)

        self.format = QAudioFormat()
        self.format.setSampleRate(16000)
        self.format.setChannelCount(1)
        self.format.setSampleSize(16)
        self.format.setCodec("audio/pcm")
        self.format.setByteOrder(QAudioFormat.LittleEndian)
        self.format.setSampleType(QAudioFormat.SignedInt)
        self.recorder = QAudioInput(self.format, self)

        self.is_recording = False

    @Slot()
    def toggle_record(self):
        if self.is_recording == False:
            logging.info("Capturing sound")
            self.is_recording = True
            self.inference_thread.send_cmd(("start",))
            self.recorded_message = self.recorder.start()
            self.recorded_message.readyRead.connect(self.read_from_IO_devide)
        else:
            logging.info("Finished sound capturing")
            self.is_recording = False
            self.recorder.stop()
            self.inference_thread.send_cmd(("finish",))

    @Slot()
    def read_from_IO_devide(self):
        ''' Forward available audio data to the inference thread. '''
        # self.sender() is the IO device returned by QAudioInput.start()
        self.inference_thread.send_cmd(("data", self.sender().readAll()))

    @Slot(str)
    def on_transcription_finished(self, result):
        logging.info("Transcription: {result}")

        self.dialog.set_user_message(result)
        self.dialog.process_user_message()
        self.dialog.process_machine_message()
