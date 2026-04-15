from PySide6.QtWidgets import QApplication, QFileDialog
from PySide6.QtCore import QFile, Signal, QThread, QUrl, Slot
from PySide6.QtUiTools import QUiLoader
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from Downloader import *
import os
from collections import deque

class Player_UI:
    def __init__(self, path):

        #variables
        self.path = path
        self.queue = deque()
        self.song_list = []
        #self.current_song_index
        
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

        self.window.list_widget.clicked.connect(self.select_source)

        self.window.select_source_button.clicked.connect(self.select_source_folder)

        self.window.next_button.clicked.connect(self.play_next)

        self.audio_output.setVolume(0.7)
        self.window.volume_slider.valueChanged.connect(lambda v: self.audio_output.setVolume(v / 100))

        self.player.mediaStatusChanged.connect(lambda status: self.play_next() if  status == QMediaPlayer.MediaStatus.EndOfMedia else None)

        self.window.download_button.clicked.connect(self.open_downloader)

        #sync seek slider with song
        self.player.positionChanged.connect(self.window.seek_slider.setValue)
        self.player.durationChanged.connect(self.window.seek_slider.setMaximum)

        #manual seeking when you move the slider
        self.window.seek_slider.sliderMoved.connect(self.player.setPosition)
        ##

        self.app.setDesktopFileName("resonance")

        #stuff shows on the screen
        self.window.show()

        self.app.exec()
        ##

    
    def init_queue(self):
        self.queue.clear()
        start = self.window.list_widget.currentRow()
        stop = self.window.list_widget.count()

        for i in range(start, stop):
            item = self.window.list_widget.item(i)
            self.queue.append((i, item.text()))

    def open_downloader(self):
        downloader = Downloader_UI(self.path, self.window)
        downloader.show()



    #dialog window to select the folder from which we play music
    def select_source_folder(self):
        source = QFileDialog.getExistingDirectory(self.window, "Select Directory")

        if source:
            #print(source)
            self.change_path(source)


    
    #when double clicked an element in the list
    def select_source(self):
        self.init_queue()
        self.set_source()
    
    def set_source(self):
        index, title = self.queue.popleft()

        self.player.setSource(QUrl.fromLocalFile(f"{self.path}/{title}"))
        self.window.list_widget.setCurrentRow(index)
        self.play_music()


    #when the play button is pressed
    def play_music(self):
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
            
        else:
            self.player.play()
    
    

    def play_next(self):
        #self.window.list_widget.setCurrentRow(self.window.list_widget.currentRow() + 1)
        if len(self.queue) != 0:
            #self.queue.popleft()
            self.set_source()
        else:
            self.window.list_widget.setCurrentRow(0)
            self.select_source()




    def populate_lists_widget(self, entries):
        self.window.list_widget.clear()

        for entry in entries:
            self.window.list_widget.addItem(entry)
    

    def populate_song_list(self, files):
        self.song_list.clear()

        for file in files:
            if file.endswith(".mp3"):
                self.song_list.append(file)
    
    
    def change_path(self, path):
        self.path = path
        self.populate_song_list(os.listdir(self.path))
        self.populate_lists_widget(self.song_list)

            




if __name__ == "__main__":
    Player_UI()