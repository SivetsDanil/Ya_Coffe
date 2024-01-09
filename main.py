from PyQt5 import QtCore, QtWidgets
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
import sqlite3


class Coffe(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect("data\coffee.sqlite")
        self.cur = self.con.cursor()
        self.fill_table()
        self.change_btn.clicked.connect(self.open_change)

    def fill_table(self):
        result = self.cur.execute('select * from info').fetchall()
        header = ['ID', 'название сорта', 'степень обжарки', 'молотый/в зернах', 'описание вкуса', 'цена',
                  'объем упаковки']
        self.table.setRowCount(len(result))
        self.table.setColumnCount(len(result[0]))
        self.table.setVerticalHeaderLabels([''] * len(result))
        self.table.setHorizontalHeaderLabels(header)
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))

    def open_change(self):
        self.window = WorkWithBase()
        self.close()
        self.window.show()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.table = QtWidgets.QTableWidget(self.centralwidget)
        self.table.setGeometry(QtCore.QRect(70, 50, 641, 441))
        self.table.setObjectName("table")
        self.table.setColumnCount(0)
        self.table.setRowCount(0)
        self.change_btn = QtWidgets.QPushButton(self.centralwidget)
        self.change_btn.setGeometry(QtCore.QRect(70, 500, 141, 28))
        self.change_btn.setObjectName("change_btn")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Эспрессо"))
        self.change_btn.setText(_translate("MainWindow", "Изменить"))


class WorkWithBase(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect("data/coffee.sqlite")
        self.cur = self.con.cursor()
        self.fill_table()
        self.save_btn.clicked.connect(self.save_results)
        self.add_btn.clicked.connect(self.create_row)
        self.modified = {}
        self.changes = []
        self.row_sent = True
        self.row_created = False
        self.selected = False
        self.table.itemChanged.connect(self.item_changed)
        self.table.itemSelectionChanged.connect(self.item_selected)
        self.keys = {'ID': 'id', 'название сорта': 'sort', "степень обжарки": 'roasting',
                     "молотый/в зернах": 'condition', "описание вкуса": 'taste', "цена":
                         'price', "объем упаковки": 'volume'}

    def save_results(self):
        print(self.changes)
        for elem in self.changes:
            que = f"UPDATE info SET {self.keys[elem[1]]}='{elem[0].text()}'"
            que += f"WHERE id = {elem[2]}"
            self.cur.execute(que)
            self.con.commit()
        self.fill_table()
        self.statusBar().showMessage("Готово")
        self.changes.clear()

    def item_changed(self, item):
        try:
            if item.text() == self.select.text():
                self.changes.append((self.select, self.selected_key, self.selected_id))
        except Exception:
            pass

    def item_selected(self):
        try:
            self.selected = True
            self.select = self.table.selectedItems()[0]
            self.selected_key = self.table.horizontalHeaderItem(self.select.column()).text()
            self.selected_id = self.table.item(self.select.row(), 0).text()
            self.table.itemChanged.connect(self.item_changed)
        except IndexError:
            pass

    def create_row(self):
        self.row_created = True
        self.row_sent = False
        self.modified = {}
        self.cur.execute(f"insert into info(sort, roasting, condition, taste, price, volume) "
                         f"values('', '', '', '', '', '')")
        self.con.commit()
        self.fill_table()
        self.row_id = self.cur.execute(f"select id from info where taste=''").fetchall()[0][0]

    def fill_table(self):
        con = sqlite3.connect("data/coffee.sqlite")
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

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.table = QtWidgets.QTableWidget(self.centralwidget)
        self.table.setGeometry(QtCore.QRect(40, 30, 691, 401))
        self.table.setObjectName("table")
        self.table.setColumnCount(0)
        self.table.setRowCount(0)
        self.add_btn = QtWidgets.QPushButton(self.centralwidget)
        self.add_btn.setGeometry(QtCore.QRect(40, 470, 191, 28))
        self.add_btn.setObjectName("add_btn")
        self.save_btn = QtWidgets.QPushButton(self.centralwidget)
        self.save_btn.setGeometry(QtCore.QRect(270, 470, 171, 28))
        self.save_btn.setObjectName("save_btn")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.add_btn.setText(_translate("MainWindow", "Добавить"))
        self.save_btn.setText(_translate("MainWindow", "Сохранить"))


def exept(a, b, c):
    print(a, b, c)


if __name__ == '__main__':
    sys.excepthook = exept
    app = QApplication(sys.argv)
    ex = Coffe()
    ex.show()
    sys.exit(app.exec_())
