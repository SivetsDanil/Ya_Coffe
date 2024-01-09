import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
import sqlite3


class Coffe(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        result = cur.execute('select * from info').fetchall()
        header = ['ID', 'название сорта', 'степень обжарки', 'молотый/в зернах', 'описание вкуса', 'цена',
                  'объем упаковки']
        self.table.setRowCount(len(result))
        self.table.setColumnCount(len(result[0]))
        self.table.setVerticalHeaderLabels([''] * len(result))
        self.table.setHorizontalHeaderLabels(header)
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))


def exept(a, b, c):
    print(a, b, c)


if __name__ == '__main__':
    sys.excepthook = exept
    app = QApplication(sys.argv)
    ex = Coffe()
    ex.show()
    sys.exit(app.exec_())