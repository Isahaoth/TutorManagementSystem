from databaseoperator import DataOperator
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, \
    QTableWidget, QStackedWidget, QLineEdit, QComboBox
from PySide6.QtCore import Qt

db = DataOperator()
db.make_table()
uczniowie = db.return_students()
zarobki = db.overall_zarobki()


#STUDENTS SIDEWINDOW

class AddTutoringWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<h3>DODAJ ZAJĘCIA</h3>"))

        layout.addWidget(QLabel("<i>Id ucznia:</i>"))
        self.studentidInput = QLineEdit()
        layout.addWidget(self.studentidInput)

        layout.addWidget(QLabel("<i>Data zajęć (YYYY-MM-DD HH:MM):</i>"))
        self.dateInput = QLineEdit()
        layout.addWidget(self.dateInput)

        layout.addWidget(QLabel("<i>Stawka:</i>"))
        self.moneyInput = QLineEdit()
        layout.addWidget(self.moneyInput)

        layout.addWidget(QLabel("<i>Typ zajęć:</i>"))
        self.typeInput = QComboBox()
        self.typeInput.addItems(["Przygotowanie do E8", "Przygotowanie do Matury", "Powtórki do zajęć","Nadrobienie zaległości","Inne"])
        layout.addWidget(self.typeInput)

        self.confirmButton = QPushButton("Zatwierdź")
        layout.addWidget(self.confirmButton)

        self.confirmButton.clicked.connect(self.saveTutoring)

    def saveTutoring(self):
       typeid = self.typeInput.currentIndex()+1
       money = self.moneyInput.text()
       date = self.dateInput.text()
       studentid = self.studentidInput.text()

       db.add_zajecia(studentid, typeid, date, money)

       self.moneyInput.clear()
       self.dateInput.clear()
       self.studentidInput.clear()


class YourStudentsWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("LISTA TWOICH UCZNIÓW"))

class AddStudentWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<h3>DODAJ NOWEGO UCZNIA</h3>"))

        layout.addWidget(QLabel("<i>Imię ucznia:</i>"))
        self.nameInput = QLineEdit()
        layout.addWidget(self.nameInput)

        layout.addWidget(QLabel("<i>Nazwisko ucznia:</i>"))
        self.lastnameInput = QLineEdit()
        layout.addWidget(self.lastnameInput)

        layout.addWidget(QLabel("<i>Klasa:</i>"))
        self.classInput = QLineEdit()
        layout.addWidget(self.classInput)
        layout.addWidget(QLabel("<i>Aby móc w pełni korzystać ze statystyk uczniów klasę należy zakodować jako numer oraz literę (P/L/T).</i>"))

        self.confirmButton = QPushButton("Zatwierdź")
        layout.addWidget(self.confirmButton)

        self.confirmButton.clicked.connect(self.saveStudents)

    def saveStudents(self):
        name = self.nameInput.text()
        lastname = self.lastnameInput.text()
        sclass = self.classInput.text()

        db.add_student(name, lastname, sclass)

        self.nameInput.clear()
        self.lastnameInput.clear()
        self.classInput.clear()


#MAIN WINDOW
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tutoring Management Application")

        container = QWidget()
        self.setCentralWidget(container)

        layout = QHBoxLayout(container)

        inner_container = QWidget()
        navigationLayout = QVBoxLayout(inner_container)

        label1 = QLabel('Witaj Korepetytorze!')
        label1.setAlignment(Qt.AlignCenter)

        label2 = QLabel(f'Twoje zarobki wynoszą {zarobki[0]} zł.')
        label2.setAlignment(Qt.AlignCenter)

        button1 = QPushButton('Kliknij, aby wyświetlić swoich uczniów.')
        button2 = QPushButton('Kliknij, aby dodać nowego ucznia.')
        button3 = QPushButton('Kliknij, aby dodać zajęcia.')

        #NO 1 PANEL
        navigationLayout.addWidget(label1)
        navigationLayout.addWidget(label2)
        navigationLayout.addWidget(button3)
        navigationLayout.addWidget(button2)
        navigationLayout.addWidget(button1)

        #NO 2 PANEL
        workspace = QStackedWidget()

        #PODSTRONY
        pagestudents = YourStudentsWidget()
        pageadding = AddStudentWidget()
        pageaddtutoring = AddTutoringWidget()

        #DODAWANIE
        workspace.addWidget(pagestudents)
        workspace.addWidget(pageadding)
        workspace.addWidget(pageaddtutoring)

        #CONNECTION Z GUZIKAMI
        button1.clicked.connect(lambda:workspace.setCurrentIndex(0))
        button2.clicked.connect(lambda:workspace.setCurrentIndex(1))
        button3.clicked.connect(lambda: workspace.setCurrentIndex(2))

        #FINAL LAYOUT
        layout.addWidget(inner_container, stretch=1)
        layout.addWidget(workspace, stretch=3)


app = QApplication()

window = MainWindow()
window.show()

app.exec()

