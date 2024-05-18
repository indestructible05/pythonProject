import sqlite3
import sys

from PyQt5 import QtWidgets
import calc
import calcu

db = sqlite3.connect('database.db')
cursor = db.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users(
    login TEXT,
    password TEXT
)''')
db.commit()

for i in cursor.execute('SELECT * FROM users'):
    print(i)


class Registration(QtWidgets.QMainWindow, calc.Ui_MainWindow):
    def __init__(self):
        super(Registration, self).__init__()
        self.setupUi(self)
        self.label.setText('')
        self.lineEdit.setPlaceholderText('Введите Логин')
        self.lineEdit_2.setPlaceholderText('Введите Пароль')
        self.pushButton.setText('Регистрация')
        self.pushButton_2.setText('Вход')
        self.setWindowTitle('Регистрация')

        self.pushButton.pressed.connect(self.reg)
        self.pushButton_2.pressed.connect(self.login)

    def login(self):
        login_page = Login()
        login_page.show()
        self.hide()

    def reg(self):
        user_login = self.lineEdit.text()
        user_password = self.lineEdit_2.text()

        if len(user_login) == 0 or len(user_password) == 0:
            return

        cursor.execute(f'SELECT login FROM users WHERE login="{user_login}"')
        if cursor.fetchone() is None:
            cursor.execute(f'INSERT INTO users VALUES ("{user_login}", "{user_password}")')
            self.label.setText(f'Аккаунт {user_login} успешно зарегистрирован!')
            db.commit()
        else:
            self.label.setText('Такая запись уже имеется!')


class Login(QtWidgets.QMainWindow, calc.Ui_MainWindow):
    def __init__(self):
        super(Login, self).__init__()
        self.setupUi(self)
        self.label.setText('')
        self.lineEdit.setPlaceholderText('Введите логин')
        self.lineEdit_2.setPlaceholderText('Введите пароль')
        self.pushButton.setText('Вход')
        self.pushButton_2.setText('Регистрация')
        self.setWindowTitle('Вход')

        self.pushButton.pressed.connect(self.login)
        self.pushButton_2.pressed.connect(self.reg)

    def reg(self):
        reg_page = Registration()
        reg_page.show()
        self.hide()

    def login(self):
        user_login = self.lineEdit.text()
        user_password = self.lineEdit_2.text()

        if len(user_login) == 0 or len(user_password) == 0:
            return

        cursor.execute(f'SELECT password FROM users WHERE login="{user_login}"')
        check_pass = cursor.fetchone()

        if check_pass is not None and check_pass[0] == user_password:
            self.label.setText('Успешная авторизация!')

            self.main_window = MainWindow1(user_login)
            self.main_window.show()
            self.hide()
        else:
            self.label.setText('Ошибка авторизации')

class MainWindow1(QtWidgets.QMainWindow, calcu.Ui_MainWindow1):
            def __init__(self, user_login):
                super(MainWindow1, self).__init__()
                self.setupUi(self)
                self.label.setText(f"Добро пожаловать, {user_login}")
                self.setWindowTitle('Калькулятор')


app = QtWidgets.QApplication([])
window = Login()
window.show()
sys.exit(app.exec())