from PyQt5.QtWidgets import (QMainWindow, QWidget,
                             QPushButton, QLineEdit, QInputDialog, QComboBox, QLabel,
                             QSpinBox, QCalendarWidget, QTableView, QVBoxLayout, QHBoxLayout)
import myDatabase


class MainWindow(QMainWindow):
    def __init__(self, dataBaseName):
        super().__init__()
        self._dataBase = myDatabase.MyDataBase(dataBaseName)
        self._dictexe = {"первый запрос": (self.firstQuery,
                                           self.firstExe), "второй запрос": (self.secondQuery,
                                                                             self.secondExe),
                         "третий запрос": (self.thirdQuery, self.thirdExe)}
        self._view = QTableView()
        self._buttonAdd = QPushButton("Добавить")
        self._buttonKek = QPushButton('kek')
        self._buttonAdd.clicked.connect(self.getItems)
        self._addSpinBox = QSpinBox()
        self._addComboBox = QComboBox()
        self._addComboBox.addItems(self._dataBase.dishes())
        self._layout = QHBoxLayout()
        self._qSpinBox = QSpinBox()
        self._qComboBox = QComboBox()
        self._qLineEdit = QLineEdit()
        self._qCalendarWidget = QCalendarWidget()
        self._queryDisc = QLabel()
        self._buttonExe = QPushButton("Выполнить")
        self._buttonExe.clicked.connect(self.onButtonExe)
        self._combox = QComboBox()
        self._combox.currentTextChanged.connect(self.comboChanged)
        self._combox.addItems(self._dictexe.keys())
        self.initUi()

    def initUi(self):
        self.setGeometry(300, 300, 200, 200)
        self.setWindowTitle('Рестораны')
        w = QWidget()
        mainLayout = QVBoxLayout()
        w.setLayout(mainLayout)
        self.setCentralWidget(w)
        mainLayout.addWidget(self._view)
        tmpLayout = QHBoxLayout()
        mainLayout.addLayout(tmpLayout)
        tmpLayout.addWidget(QLabel("Добавления ингредиента"))
        tmpLayout.addWidget(self._addSpinBox)
        tmpLayout.addWidget(self._addComboBox)
        tmpLayout.addWidget(self._buttonAdd)
        mainLayout.addWidget(self._queryDisc)
        tmpLayout = QHBoxLayout()
        mainLayout.addLayout(tmpLayout)
        tmpLayout.addWidget(self._combox)
        tmpLayout.addLayout(self._layout)
        tmpLayout.addWidget(self._buttonExe)
        self.adjustSize()

    def comboChanged(self, text):
        self._dictexe[text][0]()

    def clearLayout(self):
        while self._layout.count() > 0:
            self._layout.itemAt(0).widget().setParent(None)

    # Названия и калорийность блюд по рецептам автора X
    def firstQuery(self):
        self._queryDisc.setText('''Названия и калорийность блюд по рецептам автора X''')
        self.clearLayout()
        self._qComboBox.clear()
        self._qComboBox.addItems(self._dataBase.authors())
        self._layout.insertWidget(1, self._qComboBox)

    def firstExe(self):
        model = self._dataBase.first(self._qComboBox.currentText())
        self.setModel(model)

    def secondQuery(self):
        self._queryDisc.setText("Названия ресторанов, к которым")
        self.clearLayout()
        self._qLineEdit.clear()
        self._layout.insertWidget(1, self._qLineEdit)

    def secondExe(self):
        model = self._dataBase.second(self._qLineEdit.text())
        self.setModel(model)

    def thirdQuery(self):
        self._queryDisc.setText("Названия и количества")
        self.clearLayout()
        self._layout.insertWidget(1, self._qCalendarWidget)

        self._qSpinBox.setMaximum(self._dataBase.maxDrinkCount() * 10)
        self._qSpinBox.setValue(0)
        self._layout.insertWidget(1, self._qSpinBox)

    def thirdExe(self):
        model = self._dataBase.third(self._qSpinBox.value(),
                                     self._qCalendarWidget.selectedDate().toPyDate())
        self.setModel(model)

    def setModel(self, model):
        if model is None:
            return

        self._view.setVisible(False)
        self._view.setModel(model)
        for i in range(model.columnCount()):
            self._view.resizeColumnToContents(i)
        self._view.setVisible(True)
        self.adjustSize()

    def onButtonExe(self):
        self._dictexe[self._combox.currentText()][1]()

    def getItems(self):
        name, ok = QInputDialog.getText(self, "ингредиент",
                                        "введите название")

        if not ok:
            return self._dataBase.add(self._addSpinBox.value(), self._addComboBox.currentText(), name)
