#############################################################################
##
## Copyright (C) 2019 The Qt Company Ltd.
## Contact: http://www.qt.io/licensing/
##
## This file is part of the Qt for Python examples of the Qt Toolkit.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of The Qt Company Ltd nor the names of its
##     contributors may be used to endorse or promote products derived
##     from this software without specific prior written permission.
##
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
##
## $QT_END_LICENSE$
##
#############################################################################

import sys
import random
import numpy as np
import queue
import threading
import logging

from deepspeech import Model

from PySide2.QtCore import QObject, Signal, Slot, QUrl
from PySide2.QtWidgets import QPushButton, QWidget, QVBoxLayout, QSpacerItem
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
        self.model = Model( os.path.join(os.path.dirname(__file__), "deepspeech-0.5.1-models/output_graph.pbmm"), N_FEATURES, N_CONTEXT,  os.path.join(os.path.dirname(__file__), "deepspeech-0.5.1-models/alphabet.txt"), BEAM_WIDTH)
        self.model.enableDecoderWithLM( os.path.join(os.path.dirname(__file__), "deepspeech-0.5.1-models/alphabet.txt"),  os.path.join(os.path.dirname(__file__), "deepspeech-0.5.1-models/lm.binary"),  os.path.join(os.path.dirname(__file__), "deepspeech-0.5.1-models/trie"), LM_ALPHA, LM_BETA)
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
                    self.model.feedAudioContent(stream, np.frombuffer(data[0].data(), np.int16))
            elif cmd == "finish":
                # "finish" means the caller wants the result of the current stream
                transcript = self.model.finishStream(stream)
                self.finished.emit(transcript)
                stream = None
                logging.debug("Finishes to process sound")


class AudioRecorder(QWidget):
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
