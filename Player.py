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
        self.path = path #the variable of the path where our player will display the songs in the list widget and play them from -> string
        self.queue = deque() #used as a queue for storing the order of the upcoming songs, -> [(index, title)]
        self.history = deque() #used as a stack for storing the songs played prior, -> [(index, title)]
        self.current_song = None #touple of information of the current song -> (index, title)
        self.song_list = [] #list of the titles of the mp3 files -> [strings]
        
        ##


        #load ui form .ui file
        self.app = QApplication()

        loader = QUiLoader()

        file = QFile('player.ui')

        file.open(QFile.ReadOnly)

        self.window = loader.load(file)

        file.close()
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

        self.window.prev_button.clicked.connect(self.play_prev)

        self.audio_output.setVolume(0.7)
        self.window.volume_slider.valueChanged.connect(lambda v: self.audio_output.setVolume(v / 100)) #volume

        self.player.mediaStatusChanged.connect(lambda status: self.play_next() if  status == QMediaPlayer.MediaStatus.EndOfMedia else None) #when song ends

        self.window.download_button.clicked.connect(self.open_downloader)

        #sync seek slider with song
        self.player.positionChanged.connect(self.window.seek_slider.setValue)
        self.player.durationChanged.connect(self.window.seek_slider.setMaximum)

        #manual seeking when you move the slider
        self.window.seek_slider.sliderMoved.connect(self.player.setPosition)
        ##

        self.app.setDesktopFileName("resonance") #for testing purposes

        #stuff shows on the screen
        self.window.show()

        self.app.exec()
        ##

    
    #clears & populates the queue from the current selected song up untill the last song, in order, triggers when selecting a song
    def init_queue(self):
        self.queue.clear()
        start = self.window.list_widget.currentRow() + 1
        stop = self.window.list_widget.count()

        for i in range(start, stop):
            item = self.window.list_widget.item(i)
            self.queue.append((i, item.text()))


    #triggers when pressing the download button, creates an instance of the downloader as a separate window
    def open_downloader(self):
        downloader = Downloader_UI(self.path, self.window)
        downloader.show()



    #triggers when pressing select source, dialog window to select the folder from which we play music
    def select_source_folder(self):
        source = QFileDialog.getExistingDirectory(self.window, "Select Directory")

        if source:
            #print(source)
            self.change_path(source)


    
    #triggers when double clicked an element in the list widget
    def select_source(self):
        self.init_queue() #when the user selects a new song we automatically assume they want to forget the old queue

        index = self.window.list_widget.currentRow()
        title = self.window.list_widget.currentItem().text()

        self.set_source(index, title)

    
    #helper method for putting the audio player to work, provide an index for selection and a title for playing
    def set_source(self, index, title):
        self.player.setSource(QUrl.fromLocalFile(f"{self.path}/{title}"))

        if self.window.list_widget.currentRow() != index:
            self.window.list_widget.setCurrentRow(index)
        self.play_music()

    #playes next song in queue, only used when NOT manually selecting a song
    def set_next_source(self):
        index, title = self.queue.popleft()
        
        if self.current_song:
            self.history.append(self.current_song)
        
        self.current_song = (index, title)
        self.set_source(index, title)
    

    #triggered when prev button is pressed, if there is history, it goes back if not it replays the current song
    def play_prev(self):
        if len(self.history) > 0:
            if self.current_song:
                self.queue.appendleft(self.current_song)
            
            self.current_song = self.history.pop()
            index, title = self.current_song
            
            self.player.setSource(QUrl.fromLocalFile(f"{self.path}/{title}"))
            self.window.list_widget.setCurrentRow(index)
            self.play_music()
        
        elif self.current_song:
            index, title = self.current_song
            self.player.setSource(QUrl.fromLocalFile(f"{self.path}/{title}"))
            self.player.setPosition(0)
            self.window.list_widget.setCurrentRow(index)
            self.play_music()


    #triggers when the play button is pressed and also when a method has to play a new song
    def play_music(self):
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
            
        else:
            self.player.play()
    
    
    #triggers when the next button is pressed 
    def play_next(self):
        #self.window.list_widget.setCurrentRow(self.window.list_widget.currentRow() + 1)
        if self.queue:
            #self.queue.popleft()
            self.set_next_source()
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