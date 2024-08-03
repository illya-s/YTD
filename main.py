from PyQt6 import uic, QtGui
from PyQt6.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt6.QtCore import QThreadPool
from PyQt6.QtGui import QColor, QTextCharFormat

from downloader import Download
import sys, os, requests

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = uic.loadUi('design.ui', self)

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
        try:
            response = requests.head(url)
            if response.status_code == 200:
                return True
            else:
                return False
        except requests.RequestException as e:
            print(f"An error occurred: {e}")
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