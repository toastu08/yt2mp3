from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import QFile, Signal, QThread
from PySide6.QtUiTools import QUiLoader
from Media_engine import Media_engine


class SearchTask(QThread):
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


class DownloadTask(QThread):
    downloadDone = Signal(str)

    def __init__(self, engine ,index ,source):
        super().__init__()
        self.engine = engine
        self.index = index
        self.source = source

    def run(self):
        self.engine.download(self.index)
        self.downloadDone.emit('Done Downloading!')

class Downloader_UI(QWidget):
    def __init__(self, path, parent=None):
        super().__init__(parent)
        self.path = path
        self.mediaEngine = Media_engine(path)

        self.loader = QUiLoader()

        self.file = QFile('downloader.ui')

        self.file.open(QFile.ReadOnly)

        self.ui = self.loader.load(self.file, self)

        self.file.close()

        self.updateLabel('')

        self.ui.search_bar.returnPressed.connect(self.enterPressed)

        self.ui.results_list.doubleClicked.connect(self.itemSelected)

        self.ui.show()


    def enterPressed(self):
        self.updateLabel('Searching...')
        
        self.ui.results_list.clear()
        
        self.searchTask = SearchTask(self.mediaEngine, self.ui.search_bar.text(), int(self.ui.results_box.currentText()), self.ui.source_box.currentText())
        
        self.searchTask.searchDone.connect(self.updateList)

        self.searchTask.start()

    def itemSelected(self):
        self.updateLabel('Downloading...')

        self.downloadTask = DownloadTask(self.mediaEngine, self.ui.results_list.currentRow(), self.ui.source_box.currentText())

        self.downloadTask.downloadDone.connect(self.updateLabel)

        self.downloadTask.start()


    def updateList(self, result):
        for i in result:
            self.ui.results_list.addItem(f"{i['title']}{' - ' +  i['channel'] if 'channel' in i else ''}")
        self.updateLabel('Done Searching!')
    

    def updateLabel(self, message):
        self.ui.status_label.setText(message)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    dialog = Downloader_UI("~/Music/")
    dialog.show()
    app.exec()
