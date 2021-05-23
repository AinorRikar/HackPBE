import sys
import pymysql



from ue import *


# Интерфейс программы и обработчик событий внутри него
class Client(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Отключаем стандартные границы окна программы
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.center()

        # # Обработчики основных кнопок + кнопок с панели
        self.ui.pushButton_2.clicked.connect(self.but_page)
        self.ui.pushButton.clicked.connect(self.but_page_2)
        # self.ui.pushButton_2.clicked.connect(self.connect_to_server)
        self.ui.pushButton_3.clicked.connect(lambda: self.close())
        # self.ui.pushButton_4.clicked.connect(lambda: self.ui.listWidget.clear())
        self.ui.pushButton_5.clicked.connect(lambda: self.showMinimized())
        # self.ui.pushButton_7.clicked.connect(self.setting_panel)

        self.loaddata()
        self.ui.tableWidget_2.cellPressed[int, int].connect(self.clickedRowColumn)
    def but_page(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page)

    def but_page_2(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_2)
        self.ui.label.setText('')
    # Перетаскивание безрамочного окна
    # ==================================================================
    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        try:
            delta = QtCore.QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()
        except AttributeError:
            pass
    # ==================================================================




    # Открыть окно для настройки клиента
    def setting_panel(self):
        setting_win = SettingPanel(self, self.connect_monitor.mysignal)
        setting_win.show()

    def loaddata(self):
        con = pymysql.connect(host='localhost',
                              user='root',
                              password='1234',
                              db='hackathon',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)

        with con:

            cur = con.cursor()

            cur.execute("SELECT * FROM egeresults;")
            rows = cur.fetchall()

            tablerow = 0
            self.ui.tableWidget_2.setRowCount(len(rows))
            # print(rows)
            list_student = []
            # a = rows
            # for i in range(len(rows)):
            #     for j in range(i+1, len(rows)):
            #         if a[i]['ParticipantId'] == a[j]['ParticipantId']:
            #             list_student.insert([])
            for row in rows:
                self.ui.tableWidget_2.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(row['ParticipantId']))
                tablerow += 1
            cur.close()

    def clickedRowColumn(self, r):
        self.ui.tableWidget.cellPressed[int, int].connect(self.clickedRowColumn_2)

        con = pymysql.connect(host='localhost',
                             user='root',
                             password='1234',
                             db='hackathon',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

        with con:
            cur = con.cursor()

            cur.execute("SELECT * FROM egeresults;")


            rows = cur.fetchall()
            id_st = rows[r]['ParticipantId']
            a = str(rows[r]['MarkPercent'])
            cur.execute(f"SELECT * FROM egeresults WHERE ParticipantId = '{str(id_st)}';")
            inf = cur.fetchall()
            tablerow = 0
            self.ui.tableWidget.setRowCount(len(inf))

            self.list_ou = []
            for i in range(len(inf)):
                self.list_ou.insert(len(self.list_ou), [str(inf[i]['SubjectId']), str(inf[i]['MarkPercent'])])

            for i in range(len(inf)):
                cur.execute(f"SELECT * FROM subjects WHERE Id = '{str(inf[i]['SubjectId'])}';")
                popo = cur.fetchall()
                # cur.execute(f"SELECT * FROM subjects WHERE Id = '{str(inf[i]['MarkPercent'])}';")
                # yes = cur.fetchall()
                for h in range(len(popo)):

                    self.ui.tableWidget.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(popo[h]['Name'])))
                tablerow += 1


            # self.ui.label.setText(a)
            print(rows[r]['MarkPercent'])
            print("row={}".format(r))

    def clickedRowColumn_2(self, r):
        con = pymysql.connect(host='localhost',
                              user='root',
                              password='1234',
                              db='hackathon',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)

        with con:
            cur = con.cursor()
            a = str(self.list_ou[r][1])
            self.ui.label.setText(a)








if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = Client()
    myapp.show()
    sys.exit(app.exec_())