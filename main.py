from PySide6 import QtGui
from PySide6.QtUiTools import QUiLoader, loadUiType
from PySide6.QtWidgets import QMainWindow, QApplication, QFileDialog
from PySide6.QtCore import QThreadPool, QFile
from PySide6.QtGui import QColor, QTextCharFormat

from downloader import Download
from additionary import is_file
import sys, os, requests


def UiClass(path):
    formClass, widgetClass = loadUiType(path)
    name = os.path.basename(path).replace('.', '_')
    def __init__(self, parent=None):
        widgetClass.__init__(self, parent)
        self.ui = formClass()
        self.ui.setupUi(self)
    return type(name, (widgetClass, formClass), {'__init__': __init__})

class MainWindow(UiClass("design.ui")):
    def __init__(self):
        super().__init__()

        self.ui.browse.clicked.connect(self.open_folder)
        self.folderpath = ''

        self.dwnModel = QtGui.QStandardItemModel()

        self.threadpool = QThreadPool()

        self.ui.download.clicked.connect(self.start_download)

    def messege(self, text, color):
        cursor = self.ui.listView.textCursor()
        cursor.movePosition(QtGui.QTextCursor.MoveOperation.End)

        format = QTextCharFormat()
        format.setForeground(QColor(color))
        cursor.setCharFormat(format)
        
        cursor.insertText(f"{text}\n")
        self.ui.listView.setTextCursor(cursor)
        self.ui.listView.ensureCursorVisible()

    def set_progress(self, progress):
        if progress == 100:
            self.ui.download.setEnabled(True)
        self.ui.progressBar.setValue(progress)

    def url_exists(self, url):
        if is_file(url):
            return True
        else:
            try:
                response = requests.head(url)
                return True if response.status_code == 200 else False
            except requests.RequestException as e:
                self.messege(f"An error occurred: {e}", "#F00")
                return False

    def start_download(self):
        link, path = self.ui.lineUrl.text(), self.ui.lineSrc.text()

        if not self.url_exists(link) or not os.path.exists(path):
            self.messege('Please provide a valid URL and folder path.', '#F00')
            return None

        worker = Download(link=link, path=path, mp=self.ui.AWChange.currentIndex())
        worker.signals.progress.connect(lambda progress: self.set_progress(progress))
        worker.signals.messege.connect(lambda text, color: self.messege(text, color))

        self.threadpool.start(worker)
        self.ui.download.setEnabled(False)

    def open_folder(self):
        self.folderpath = QFileDialog.getExistingDirectory(self, 'Select Folder')
        self.ui.lineSrc.setText(self.folderpath)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()