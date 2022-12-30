from PyQt5.QtWidgets import QDialog, QPushButton, QLineEdit, QApplication, QLabel, QMessageBox
from PyQt5.QtCore import Qt



class StatWindow(QDialog):
    def __init__(self, database):
        super().__init__()
        self.database = database
