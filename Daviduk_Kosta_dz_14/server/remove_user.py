from PyQt5.QtWidgets import QDialog, QPushButton, QLineEdit, QApplication, QLabel, QMessageBox
from PyQt5.QtCore import Qt
import hashlib
import binascii


class DelUserDialog(QDialog):
    def __init__(self, database, server):
        super().__init__()
        self.database = database
        self.server = server