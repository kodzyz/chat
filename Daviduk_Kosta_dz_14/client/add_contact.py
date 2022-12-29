from PyQt5.QtWidgets import QDialog, QPushButton, QLineEdit, QApplication, QLabel, qApp
from PyQt5.QtCore import QEvent


# Стартовый диалог с выбором имени пользователя
class AddContactDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.ok_pressed = False

        self.setWindowTitle('Добавление контакта!')
        self.setFixedSize(280, 93)

        self.label = QLabel('Имя контакта для добавления:', self)
        self.label.move(10, 5)
        self.label.setFixedSize(300, 20)

        self.client_name = QLineEdit(self)
        self.client_name.setFixedSize(150, 20)
        self.client_name.move(10, 30)

        self.btn_ok = QPushButton('Добавить', self)
        self.btn_ok.move(10, 60)
        #self.btn_ok.clicked.connect(self.click)

        self.btn_cancel = QPushButton('Выход', self)
        self.btn_cancel.move(90, 60)
        self.btn_cancel.clicked.connect(qApp.exit)

        # self.show()

    # Обработчик кнопки ОК, если поле вводе не пустое, ставим флаг и завершаем приложение.
    # def click(self):
    #     if self.client_name.text():
    #         self.ok_pressed = True
    #         qApp.exit()


if __name__ == '__main__':
    app = QApplication([])
    dial = AddContactDialog()
    app.exec_()



