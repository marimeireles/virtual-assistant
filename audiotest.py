from PySide2.QtMultimedia import QMediaPlayer
from PySide2.QtCore import QObject, Signal, Slot, QUrl

player = QMediaPlayer()
player.setMedia(QUrl.fromLocalFile("tts_out.wav"))
player.setVolume(50);
player.play()

