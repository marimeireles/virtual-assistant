import sys
import random
import numpy as np
from deepspeech import Model
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtMultimedia import *
from dialog import Dialog

class AudioRecorder(QWidget):
    def __init__(self, dialog):
        super(AudioRecorder, self).__init__()

        self.format = QAudioFormat()
        self.format.setSampleRate(16000)
        self.format.setChannelCount(1)
        self.format.setSampleSize(16)
        self.format.setCodec("audio/pcm")
        self.format.setByteOrder(QAudioFormat.LittleEndian)
        self.format.setSampleType(QAudioFormat.SignedInt)

        self.recorder = QAudioInput(self.format, self)
        self.isRecording = False

        self.recordButton = QPushButton("Record")
        self.recordingLayout = QVBoxLayout()
        self.recordingLayout.addWidget(self.recordButton)
        self.setLayout(self.recordingLayout)

        self.recordButton.clicked.connect(self.toggleRecord)

        self.createDSModel()
        self.dialog = dialog

    def createDSModel(self):
        N_FEATURES = 26
        N_CONTEXT = 9
        BEAM_WIDTH = 500
        LM_ALPHA = 0.75
        LM_BETA = 1.85

        self.ds = Model('deepspeech-0.5.1-models/output_graph.pbmm', N_FEATURES, N_CONTEXT, 'deepspeech-0.5.1-models/alphabet.txt', BEAM_WIDTH)
        self.ds.enableDecoderWithLM('deepspeech-0.5.1-models/alphabet.txt', 'deepspeech-0.5.1-models/lm.binary', 'deepspeech-0.5.1-models/trie', LM_ALPHA, LM_BETA)

    @Slot()
    def toggleRecord(self):
        if self.isRecording == False:
            print('Recording on')
            self.isRecording = True
            self.sctx = self.ds.setupStream()
            self.recordedMessage = self.recorder.start()
            self.recordedMessage.readyRead.connect(self.DSPredict)
        else:
            print('Recording off')
            self.isRecording = False
            self.recorder.stop()
            self.dialog.setUserMessage(self.ds.finishStream(self.sctx))
            self.dialog.showUserMessage()
            print('Transcription: ', self.dialog.getUserMessage())

    @Slot()
    def DSPredict(self):
        self.ds.feedAudioContent(self.sctx, np.frombuffer(self.recordedMessage.readAll(), np.int16))