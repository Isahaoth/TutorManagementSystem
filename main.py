from PySide6.QtGui import QIcon, QPixmap, QFontDatabase, QFont
from PySide6.scripts.project_lib import Singleton

from databaseoperator import DataOperator
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, \
    QTableWidget, QTableWidgetItem, QStackedWidget, QLineEdit, QComboBox, QFrame, QDateTimeEdit, QHeaderView, QAbstractItemView
from PySide6.QtCore import Qt, QDateTime, Signal

db = DataOperator()
db.make_table()
uczniowie = db.return_students()

#STUDENTS SIDEWINDOW

class AddTutoringWidget(QWidget):
    addedsignal = Signal()
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)

        card = QFrame()
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(25,20,25,20)
        card_layout.setSpacing(10)

        heading = QLabel("DODAJ ZAJĘCIA")
        heading.setAlignment(Qt.AlignCenter)
        heading.setObjectName("heading")
        card_layout.addWidget(heading)


        card_layout.addWidget(QLabel("Id ucznia:"))
        self.studentidInput = QLineEdit()
        card_layout.addWidget(self.studentidInput)

        card_layout.addWidget(QLabel("Data zajęć:"))
        self.dateInput = QDateTimeEdit()
        self.dateInput.setCalendarPopup(True)
        self.dateInput.setDateTime(QDateTime.currentDateTime())
        self.dateInput.setDisplayFormat("yyyy-MM-dd HH:mm")
        card_layout.addWidget(self.dateInput)

        card_layout.addWidget(QLabel("Stawka:"))
        self.moneyInput = QLineEdit()
        card_layout.addWidget(self.moneyInput)

        card_layout.addWidget(QLabel("Typ zajęć:"))
        self.typeInput = QComboBox()
        self.typeInput.addItems(["Przygotowanie do E8", "Przygotowanie do Matury", "Powtórki do zajęć","Nadrobienie zaległości","Inne"])
        card_layout.addWidget(self.typeInput)

        card_layout.addSpacing(15)

        self.confirmButton = QPushButton("Zatwierdź")
        self.confirmButton.setCursor(Qt.PointingHandCursor)
        card_layout.addWidget(self.confirmButton)

        self.confirmButton.clicked.connect(self.saveTutoring)
        layout.addWidget(card)

    def saveTutoring(self):
       typeid = self.typeInput.currentIndex()+1
       money = self.moneyInput.text()
       date = self.dateInput.dateTime().toString("yyyy-MM-dd HH:mm")
       studentid = self.studentidInput.text()

       db.add_zajecia(studentid, typeid, date, money)
       self.addedsignal.emit()

       self.moneyInput.clear()
       self.dateInput.setDateTime(QDateTime.currentDateTime())
       self.studentidInput.clear()


class YourStudentsWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)

        card = QFrame()
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(25, 20, 25, 20)
        card_layout.setSpacing(10)

        heading = QLabel("LISTA TWOICH UCZNIÓW")
        heading.setObjectName("heading")
        heading.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(heading)

        self.table = QTableWidget()

        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Imię", "Nazwisko", "Klasa", "Rodzaj szkoły"])
        self.table.verticalHeader().setVisible(False)
        header = self.table.horizontalHeader()
        # Przypasowane do rozmiaru
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)

        # Rozwalone
        for num in range(1,5):
            header.setSectionResizeMode(num, QHeaderView.Stretch)

        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        card_layout.addWidget(self.table)
        self.callOutStudents()

        layout.addWidget(card)

    def callOutStudents(self):
        values = db.return_students()
        print("Pobrani uczniowie:", values)

        self.table.setRowCount(0)

        for row_pos, row_data in enumerate(values):
            self.table.insertRow(row_pos)
            for col_pos, col_data in enumerate(row_data):
                self.table.setItem(row_pos, col_pos, QTableWidgetItem(str(col_data)))


class AddStudentWidget(QWidget):
    seesignal = Signal()
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)

        card = QFrame()
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(25, 20, 25, 20)
        card_layout.setSpacing(10)

        heading = QLabel("DODAJ NOWEGO UCZNIA")
        heading.setObjectName("heading")
        card_layout.addWidget(heading)
        heading.setAlignment(Qt.AlignCenter)

        card_layout.addWidget(QLabel("Imię ucznia:"))
        self.nameInput = QLineEdit()
        card_layout.addWidget(self.nameInput)

        card_layout.addWidget(QLabel("Nazwisko ucznia:"))
        self.lastnameInput = QLineEdit()
        card_layout.addWidget(self.lastnameInput)

        card_layout.addWidget(QLabel("Klasa:"))
        self.classInput = QLineEdit()
        card_layout.addWidget(self.classInput)

        card_layout.addWidget(QLabel("Rodzaj szkoły:"))
        self.typeInput = QComboBox()
        self.typeInput.addItems(
            ["Liceum", "Technikum", "Branżowa I stopnia", "Branżowa II stopnia", "Podstawówka"])
        card_layout.addWidget(self.typeInput)

        card_layout.setSpacing(20)

        self.confirmButton = QPushButton("Zatwierdź")
        self.confirmButton.setCursor(Qt.PointingHandCursor)
        card_layout.addWidget(self.confirmButton)

        self.confirmButton.clicked.connect(self.saveStudents)
        layout.addWidget(card)

    def saveStudents(self):
        name = self.nameInput.text()
        lastname = self.lastnameInput.text()
        sclass = self.classInput.text()
        stype = self.typeInput.currentText()

        db.add_student(name, lastname, sclass, stype)
        self.seesignal.emit()

        self.nameInput.clear()
        self.lastnameInput.clear()
        self.classInput.clear()

class ViewTutoring(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)

        card = QFrame()
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(25, 20, 25, 20)
        card_layout.setSpacing(10)

        heading = QLabel("LISTA TWOICH ZAJĘĆ")
        heading.setObjectName("heading")
        heading.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(heading)

        self.table = QTableWidget()

        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID","Data zajęć","Stawka" ,"Typ zajęć" ,"Imię", "Nazwisko"])
        self.table.verticalHeader().setVisible(False)
        header = self.table.horizontalHeader()
        # Przypasowane do rozmiaru
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        # Rozwalone
        for num in range(1, 7):
            header.setSectionResizeMode(num, QHeaderView.Stretch)

        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)

        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        card_layout.addWidget(self.table)
        self.callOutTutoring()

        layout.addWidget(card)

    def callOutTutoring(self):
        values = db.showZajecia()

        self.table.setRowCount(0)

        for row_pos, row_data in enumerate(values):
            self.table.insertRow(row_pos)
            for col_pos, col_data in enumerate(row_data):
                self.table.setItem(row_pos, col_pos, QTableWidgetItem(str(col_data)))


#MAIN WINDOW
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('gui/images/icon'))
        self.setWindowTitle("Tutoring Management Application")
        self.setFixedSize(1280, 640)

        container = QWidget()
        container.setObjectName("CentralWidget")
        self.setCentralWidget(container)
        layout = QHBoxLayout(container)

        inner_container = QFrame()
        inner_container.setObjectName("NavigationBar")
        inner_container.setFixedWidth(300)

        navigationLayout = QVBoxLayout(inner_container)
        navigationLayout.setContentsMargins(20, 25, 20, 25)
        navigationLayout.setSpacing(15)

        label1 = QLabel('Witaj Korepetytorze!')
        label1.setStyleSheet("""
            font-size: 25px;
            font-weight: bold;
        """)
        label1.setAlignment(Qt.AlignCenter)
        picture = QPixmap('gui/images/userkitty.png')
        label3 = QLabel()
        label3.setPixmap(picture)
        label3.setScaledContents(True)
        label3.setFixedSize(275, 275)
        self.label2 = QLabel()
        self.label2.setStyleSheet("""
                  font-size: 20px;
              """)
        self.label2.setAlignment(Qt.AlignCenter)
        self.label2.setWordWrap(True)
        self.updateEarnings()

        button1 = QPushButton(' Wyświetl swoich uczniów')
        button2 = QPushButton(' Dodaj nowego ucznia')
        button3 = QPushButton(' Dodaj zajęcia')
        button4 = QPushButton(' Wyświetl swoje zajęcia')

        #NO 1 PANEL
        navigationLayout.addWidget(label1)
        navigationLayout.addWidget(label3)
        navigationLayout.addWidget(self.label2)
        navigationLayout.addWidget(button1)
        navigationLayout.addWidget(button2)
        navigationLayout.addWidget(button3)
        navigationLayout.addWidget(button4)



        #NO 2 PANEL
        workspace = QStackedWidget()

        #PODSTRONY
        pagestudents = YourStudentsWidget()
        pageadding = AddStudentWidget()
        pageaddtutoring = AddTutoringWidget()
        pageviewtutoring = ViewTutoring()
        pageaddtutoring.addedsignal.connect(self.updateEarnings)
        pageadding.seesignal.connect(pagestudents.callOutStudents)
        pageaddtutoring.addedsignal.connect(pageviewtutoring.callOutTutoring)
        #DODAWANIE
        workspace.addWidget(pagestudents)
        workspace.addWidget(pageadding)
        workspace.addWidget(pageaddtutoring)
        workspace.addWidget(pageviewtutoring)

        #CONNECTION Z GUZIKAMI
        button1.clicked.connect(lambda:workspace.setCurrentIndex(0))
        button2.clicked.connect(lambda:workspace.setCurrentIndex(1))
        button3.clicked.connect(lambda: workspace.setCurrentIndex(2))
        button4.clicked.connect(lambda: workspace.setCurrentIndex(3))

        #FINAL LAYOUT
        layout.addWidget(inner_container, stretch=1)
        layout.addWidget(workspace, stretch=3)

    def updateEarnings(self):
        result = db.overall_zarobki()
        total = result
        self.label2.setText(f"Twoje całkowite zarobki wynoszą <b>{total:.2f} zł.</b>")



app = QApplication()
QFontDatabase.addApplicationFont("gui/fonts/Nunito-Regular.ttf")
QFontDatabase.addApplicationFont("gui/fonts/Nunito-Bold.ttf")
app.setFont(QFont("Nunito", 10))

with open("stylesheet.qss", "r") as file:
    app.setStyleSheet(file.read())

window = MainWindow()
window.show()


app.exec()

