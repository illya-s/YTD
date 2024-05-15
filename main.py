from PyQt6 import uic, QtGui
from PyQt6.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt6.QtCore import QRunnable, QUrl, QThreadPool, QStringListModel, QObject, pyqtSignal as Signal

from downloader import Download
from convertor import Convertor
from additionary import get_filename, is_audio, is_video

import sys, os


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = uic.loadUi('design.ui', self)

        self.ui.browse.clicked.connect(self.open_folder)
        self.ui.inBrowse.clicked.connect(self.open_file)

        self.folderpath = ''

        self.CONVERTOR_COD, self.DOWNLOADER_COD = "cnv", "dow"

        self.dwnModel = QtGui.QStandardItemModel()
        self.conModel = QtGui.QStandardItemModel()

        self.threadpool = QThreadPool()

        self.ui.download.clicked.connect(self.start_download)
        self.ui.convert.clicked.connect(self.start_convert)

    def messege(self, text, color, cod):
        if cod == "dow":
            item = QtGui.QStandardItem(text)
            self.dwnModel.appendRow(item)
            self.ui.listView.setModel(self.dwnModel)
        elif cod == "cnv":
            item = QtGui.QStandardItem(text)
            self.conModel.appendRow(item)
            self.ui.convertListView.setModel(self.conModel)

    def set_progress(self, progress, cod):
        if cod == "dow":
            self.ui.progressBar.setValue(progress)
        elif cod == "cnv":
            self.ui.convertorProgress.setValue(progress)

    def start_download(self):
        link, path = self.ui.lineUrl.text(), self.ui.lineSrc.text()
        if not link or not path:
            self.messege('Please provide a valid URL and folder path.', '#F00', self.DOWNLOADER_COD)
            return None

        worker = Download(link=link, path=path, mp=self.ui.AWChange.currentIndex())
        worker.signals.progress.connect(lambda progress: self.set_progress(progress, self.DOWNLOADER_COD))
        worker.signals.messege.connect(lambda text, color: self.messege(text, color, self.DOWNLOADER_COD))

        self.threadpool.start(worker)

    def open_folder(self):
        self.folderpath = QFileDialog.getExistingDirectory(self, 'Select Folder')
        self.ui.lineSrc.setText(self.folderpath)


    def open_file(self):
        f = QFileDialog.getOpenFileName(self, caption="File", filter="Files (*.avi *.mov *.mp4 *.mkv *.wmv *.flv *.webm *.mpeg *.mpg *.3gp *.ogg)")
        if f[0] == "":
            return
        fn, ext = get_filename(f[0])
        self.ui.inSrc.setText(f[0])
        if is_video(ext):
            items = ["Select extention", "avi", "mov", "mp4", "mkv", "wmv", "flv", "webm", "mpeg", "mpg", "3gp", "ogg"]
            items.remove(ext)
            model = QStringListModel()
            model.setStringList(items)
            self.ui.chengeOutExt.setModel(model)
        # elif is_audio(ext):
        #     items = ["Select extention", "mp3", "wav", "ogg", "webm", "wma"]
        #     items.remove(ext)
        #     model = QStringListModel()
        #     model.setStringList(items)
        #     self.ui.chengeOutExt.setModel(model)

    def start_convert(self):
        inFP, outExt = self.ui.inSrc.text(), self.ui.chengeOutExt.currentText()
        if self.ui.chengeOutExt.currentIndex() == 0 or not os.path.exists(inFP):
            self.messege('Please select extention or check file path!', "#f00", self.CONVERTOR_COD)
            return
        fn, ext = get_filename(inFP)
        self.messege(f'Start convert to {fn}.{outExt}!', '#FFF', self.CONVERTOR_COD)

        worker = Convertor(inFP=inFP, ext=outExt)
        worker.signals.progress.connect(lambda progress: self.set_progress(progress, self.CONVERTOR_COD))
        worker.signals.messege.connect(lambda text, color: self.messege(text, color, self.CONVERTOR_COD))

        self.threadpool.start(worker)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()