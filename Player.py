from PySide6.QtWidgets import QApplication, QFileDialog
from PySide6.QtCore import QFile, Signal, QThread, QUrl
from PySide6.QtUiTools import QUiLoader
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
import os

class Player_UI:
    def __init__(self, path):

        #variables
        self.path = path
        ##


        #load ui form .ui file
        self.app = QApplication()

        self.loader = QUiLoader()

        self.file = QFile('player.ui')

        self.file.open(QFile.ReadOnly)

        self.window = self.loader.load(self.file)

        self.file.close()
        ##

        #audio player and audio output
        self.player = QMediaPlayer()

        self.audio_output = QAudioOutput()

        self.player.setAudioOutput(self.audio_output)
        ##

        #connects and other init stuff
        self.window.play_button.clicked.connect(self.play_music)

        self.window.song_list.doubleClicked.connect(self.set_source)

        self.window.select_source_button.clicked.connect(self.select_source)

        self.audio_output.setVolume(0.7)
        self.window.volume_slider.valueChanged.connect(lambda v: self.audio_output.setVolume(v / 100))

        #sync seek slider with song
        self.player.positionChanged.connect(self.window.seek_slider.setValue)
        self.player.durationChanged.connect(self.window.seek_slider.setMaximum)

        #manual seeking when you move the slider
        self.window.seek_slider.sliderMoved.connect(self.player.setPosition)
        ##

        #stuff shows on the screen
        self.window.show()

        self.app.exec()
        ##

    
    def select_source(self):
        source = QFileDialog.getExistingDirectory(self.window, "Select Directory")

        if source:
            print(source)
            self.change_path(source)

    def set_source(self):
        self.player.setSource(QUrl.fromLocalFile(f"{self.path}/{self.window.song_list.currentItem().text()}"))
        self.play_music()


    def play_music(self):
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
            
        else:
            self.player.play()
    
    def populate_list(self):
        self.window.song_list.clear()

        for file in os.listdir(self.path):
            if file.endswith(".mp3"):
                self.window.song_list.addItem(file)
    
    def change_path(self, path):
        self.path = path
        self.populate_list()

            




if __name__ == "__main__":
    Player_UI()