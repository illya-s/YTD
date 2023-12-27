try:
    from PyQt6 import uic, QtGui
    from PyQt6.QtWidgets import QMainWindow, QApplication, QFileDialog
    from PyQt6.QtCore import QRunnable, QThreadPool, QObject, pyqtSignal as Signal 
    from pytube import Playlist, YouTube

    from clearFileName import clearFileName
    import sys

    class DownloadWorkerSignals(QObject):
        progress_file = Signal(int)
        progress = Signal(int, str)
        nuul_progress = Signal()
        finished = Signal()
        error = Signal(str)

    class Progress(QRunnable):
        def __init__(self, link, path, mp, ot):
            super(Progress, self).__init__()
            self.link = link
            self.path = path
            self.mp = mp
            self.ot = ot
            self.signals = DownloadWorkerSignals()
            self.l = 0

        def progress_func(self, stream, chunk, bytes_remaining):
            size = stream.filesize
            progress = int(((size - bytes_remaining) / size) * 100)
            self.signals.progress_file.emit(progress)

        def run(self):
            try:
                if self.ot == 0:
                    self.signals.nuul_progress.emit()
                    youtube = YouTube(self.link, on_progress_callback=self.progress_func)
                    title = clearFileName(youtube.title)
                    if self.mp == 0:
                        stream = youtube.streams.get_highest_resolution()
                        stream.download(output_path=self.path, filename=f"{title}.mp4")
                    else:
                        stream = youtube.streams.filter(only_audio=True, file_extension="mp3").first()
                        stream.download(output_path=self.path, filename=f"{title}.mp3")
                    self.signals.progress.emit(100, f'1/1 {title}')
                    self.signals.finished.emit()
                elif self.ot == 1:
                    link = Playlist(self.link)
                    p = 0
                    for i in link.video_urls:
                        self.signals.nuul_progress.emit()
                        youtube = YouTube(i, on_progress_callback=self.progress_func)
                        title = clearFileName(youtube.title)
                        
                        if self.mp == 0:
                            stream = youtube.streams.filter(only_audio=False, file_extension="mp4").first()
                            stream.download(output_path=self.path, filename=f"{title}.mp4")
                        else:
                            stream = youtube.streams.filter(only_audio=True, file_extension="mp3").first()
                            stream.download(output_path=self.path, filename=f"{title}.mp3")
                        p += 1
                        self.l = (p * 100) / len(link)
                        self.signals.progress.emit(int(self.l), f'{p}/{len(link)} {title}')
                    self.signals.finished.emit()
                else:
                    self.signals.error.emit("Unknown error")
            except Exception as e:
                self.signals.error.emit(f"Error: {e}")



    class MainWindow(QMainWindow):
        def __init__(self):
            super(MainWindow, self).__init__()
            self.ui = uic.loadUi('design.ui', self)
            self.ui.browse.clicked.connect(self.open_folder)
            self.folderpath = ''
            self.model = QtGui.QStandardItemModel()
            self.threadpool = QThreadPool()
            self.ui.convert.clicked.connect(self.change)
            
        def open_folder(self):
            self.folderpath = QFileDialog.getExistingDirectory(self, 'Select Folder')
            self.ui.lineSrc.setText(self.folderpath)
        
        def change(self):
            link = self.ui.lineUrl.text()
            path = self.ui.lineSrc.text()
            if not link or not path:
                item = QtGui.QStandardItem('Please provide a valid URL and folder path.')
                self.model.appendRow(item)
                self.ui.listView.setModel(self.model)
                return
            mp = self.ui.TChange.currentIndex()
            ot = self.ui.QChange.currentIndex()

            worker = Progress(link, path, mp, ot)
            worker.signals.progress.connect(self.set_progress)
            worker.signals.progress_file.connect(self.set_progress_file)
            worker.signals.nuul_progress.connect(self.set_nuul_progress)
            worker.signals.finished.connect(self.thread_complete)
            worker.signals.error.connect(self.error_list)

            self.threadpool.start(worker)

        def set_progress_file(self, progress):
            self.ui.progressBarFile.setValue(progress)

        def set_progress(self, progress, work):
            self.ui.progressBar.setValue(progress)
            item = QtGui.QStandardItem(work)
            self.model.appendRow(item)
            self.ui.listView.setModel(self.model)

        def set_nuul_progress(self):
            self.ui.progressBarFile.setValue(0)

        def thread_complete(self):
            self.ui.progressBar.setValue(100)
            item = QtGui.QStandardItem('Download completed successfully!')
            self.model.appendRow(item)
            self.ui.listView.setModel(self.model)
        
        def error_list(self, error):
            item = QtGui.QStandardItem(error)
            self.model.appendRow(item)
            self.ui.listView.setModel(self.model)

except Exception as e:
    print(f"Error: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()