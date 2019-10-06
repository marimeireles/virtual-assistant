import sys
import random
import numpy as np
import queue
import threading

from deepspeech import Model

from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtMultimedia import *

N_FEATURES = 25
N_CONTEXT = 9
BEAM_WIDTH = 500
LM_ALPHA = 0.75
LM_BETA = 1.85

class InferenceThread(QObject):
    finished = Signal(str)

    def __init__(self):
        super(InferenceThread, self).__init__()
        self.inQueue = queue.Queue()
        self.shouldQuit = False
        self.worker = threading.Thread(target=self.run)

    def sendCmd(self, cmd):
        ''' Insert command in queue to be processed by the thread '''
        self.inQueue.put(cmd)

    def setQuit(self):
        ''' Signal to the thread that it should stop running '''
        self.shouldQuit = True

    def start(self):
        self.worker.start()

    def run(self):
        # Creating the model
        self.model = Model('deepspeech-0.5.1-models/output_graph.pbmm', N_FEATURES, N_CONTEXT, 'deepspeech-0.5.1-models/alphabet.txt', BEAM_WIDTH)
        self.model.enableDecoderWithLM('deepspeech-0.5.1-models/alphabet.txt', 'deepspeech-0.5.1-models/lm.binary', 'deepspeech-0.5.1-models/trie', LM_ALPHA, LM_BETA)
        stream = None

        while True:
            # Try to get the next command from our queue, use a timeout to check
            # periodically for a quit signal so the application doesn't hang on
            # exit.
            try:
                cmd, *data = self.inQueue.get(timeout=0.3)
            except queue.Empty:
                if self.shouldQuit:
                    break
                # If we haven't received a quit signal just continue trying to
                # get a command from the queue indefinitely
                continue

            if cmd == 'start':
                # 'start' means create a new stream
                stream = self.model.setupStream()
            elif cmd == 'data':
                # 'data' means we received more audio data from the recorder
                if stream:
                    self.model.feedAudioContent(stream, np.frombuffer(data[0].data(), np.int16))
            elif cmd == 'finish':
                # 'finish' means the caller wants the result of the current stream
                transcript = self.model.finishStream(stream)
                self.finished.emit(transcript)
                stream = None


class AudioRecorder(QWidget): #should it be like this?
    def __init__(self, dialog, inferenceThread):
        super(AudioRecorder, self).__init__()

        self.dialog = dialog

        self.inferenceThread = inferenceThread

        self.inferenceThread.finished.connect(self.onTranscriptionFinished)

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

    @Slot()
    def toggleRecord(self):
        if self.isRecording == False:
            self.isRecording = True
            self.inferenceThread.sendCmd(('start',))
            self.recordedMessage = self.recorder.start()
            self.recordedMessage.readyRead.connect(self.readFromIODevide)
            print('on')
        else:
            print('off')
            self.isRecording = False
            self.recorder.stop()
            self.inferenceThread.sendCmd(('finish',))

    @Slot()
    def readFromIODevide(self):
        ''' Forward available audio data to the inference thread. '''
        # self.sender() is the IO device returned by QAudioInput.start()
        self.inferenceThread.sendCmd(('data', self.sender().readAll()))

    @Slot(str)
    def onTranscriptionFinished(self, result):
        self.dialog.setUserMessage(result)
        self.dialog.showUserMessage()
        print('Transcription:', result)
