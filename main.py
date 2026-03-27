from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile, Signal, QThread
from PySide6.QtUiTools import QUiLoader
from Media_engine import Media_engine



#the actual searching function
class SearchTask(QThread):
    #signal used to carry the results of the search
    searchDone = Signal(object)

    def __init__(self, engine, query, count, source):
        super().__init__()
        self.engine = engine
        self.query = query
        self.count = count
        self.source = source
    
    def run(self):
        if self.source == 'YouTube':
            result = self.engine.search_yt(self.query, self.count)
        if self.source == 'SoundCloud':
            result = self.engine.search_sc(self.query, self.count)
        
        self.searchDone.emit(result)


#the actual downloading function!!
class DownloadTask(QThread):
    #signal used to carry the status of the download
    downloadDone = Signal(str)

    def __init__(self, engine ,index ,source):
        super().__init__()
        self.engine = engine
        self.index = index
        self.source = source

    def run(self):
        self.engine.download(self.index)
        self.downloadDone.emit('Done Downloading!')

#ui wrapper class
class Downloader_UI:
    def __init__(self):

        self.mediaEngine = Media_engine("~/Music/")

        #load ui from .ui file
        self.app = QApplication()

        self.loader = QUiLoader()

        self.file = QFile('gui.ui')

        self.file.open(QFile.ReadOnly)

        self.window = self.loader.load(self.file)

        self.file.close()
        ##

        #connects and other init stuff
        self.updateLabel('')

        self.window.search_bar.editingFinished.connect(self.enterPressed)

        self.window.results_list.doubleClicked.connect(self.itemSelected)
        ##

        #stuff shows on the screen
        self.window.show()   

        self.app.exec()
        ##


    #triggers when u press enter on the lineEdit
    def enterPressed(self):
        self.updateLabel('Searching...')
        
        self.window.results_list.clear()
        
        self.searchTask = SearchTask(self.mediaEngine, self.window.search_bar.text(), int(self.window.results_box.currentText()), self.window.source_box.currentText())
        
        self.searchTask.searchDone.connect(self.updateList)

        self.searchTask.start()

    #triggers when u double click on an item
    def itemSelected(self):
        self.updateLabel('Downloading...')

        self.downloadTask = DownloadTask(self.mediaEngine, self.window.results_list.currentRow(), self.window.source_box.currentText())

        self.downloadTask.downloadDone.connect(self.updateLabel)

        self.downloadTask.start()


    #updates the list based on the query results
    def updateList(self, result):
        for i in result:
            self.window.results_list.addItem(f"{i['title']}{' - ' i['channel'] if 'channel' in i else ''}")
        self.updateLabel('Done Searching!')
    

    #updates status label
    def updateLabel(self, message):
        self.window.status_label.setText(message)

#this may be run by itself or used as part of another app perhaps
if __name__ == '__main__':
    Downloader_UI()
