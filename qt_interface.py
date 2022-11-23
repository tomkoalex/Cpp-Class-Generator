import sys
import os
import subprocess
import pickle
import platform
from class_constructor import ClassConstructor
from PySide6 import QtCore, QtQuick
from PySide6.QtWidgets import *
from PySide6.QtGui import *

if platform.uname().system == 'Windows':
    NOTEPAD_APP = 'notepad.exe'
elif platform.uname().system == 'Darwin':
    NOTEPAD_APP = 'TextEdit'
else:
    NOTEPAD_APP = os.getenv('EDITOR')

print(NOTEPAD_APP)


app = QApplication([])

DEFAULTS = './templates/defaults'


def defaults_exist():
    return bool(os.stat(DEFAULTS).st_size)


def get_default_values():
    if defaults_exist():
        with open(DEFAULTS, "rb") as f:
            return pickle.load(f)
    return []


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("C++ Class Generator")
        self.setWindowIcon(QIcon('templates/img/cpp.png'))
        self.resize(500, 200)

        self.layout = QVBoxLayout(self)
        self.form = QFormLayout(self)
        self.h_box = QHBoxLayout(self)
        self.h_box2 = QHBoxLayout(self)
        data = get_default_values()
        self.labels = {
            'Creator': [data[0][0], 'Dev or company Name'],
            'Includes': [data[0][1], 'Lib or comma separated libs'],
            'Namespace': [data[0][2], 'Namespace/empty if not necessary'],
            'Base classes': [data[0][3], 'Class or comma separated classes'],
            'Class name': [data[0][4], 'Class name or names'],
        }

        self.ctor_cheques = ['Copy ctor', 'Copy Assign', 'Move ctor', 'Move assign', 'final', 'Dctor']

        for index, (text, vls) in enumerate(self.labels.items()):
            self.lbl = QLabel(self)
            self.lbl.setText(text)
            self.lbl.setToolTip(vls[1])
            self.qe = QLineEdit(self)
            self.qe.setText(vls[0])
            self.form.addRow(self.lbl, self.qe)

        for index, name in enumerate(self.ctor_cheques):
            self.qch = QCheckBox(name)
            self.qch.setChecked(data[1][index])
            self.h_box.addWidget(self.qch)

        self.clear = QPushButton('Clear', self)
        self.save = QPushButton('Save', self)
        self.load = QPushButton('Load', self)
        self.load.setEnabled(defaults_exist())
        self.clear.clicked.connect(self.clear_defaults)
        self.save.clicked.connect(self.save_defaults)
        self.load.clicked.connect(self.load_defaults)
        self.h_box2.addWidget(self.clear)
        self.h_box2.addWidget(self.save)
        self.h_box2.addWidget(self.load)

        self.form.addRow('Properties', self.h_box)
        self.form.addRow('Defaults', self.h_box2)
        self.generate = QPushButton('Generate', self)
        self.open = QPushButton('Open', self)
        self.open.setEnabled(False)

        self.form.addRow(self.open, self.generate)
        self.generate.clicked.connect(self.create_class)
        self.open.clicked.connect(self.open_file)
        self.layout.addLayout(self.form)
        self.show()
        sys.exit(app.exec())

    @QtCore.Slot()
    def clear_defaults(self):
        qes = self.form.parentWidget().findChildren(QLineEdit)
        cheques = self.h_box.parentWidget().findChildren(QCheckBox)
        [q.setText('') for q in qes]
        [cheque.setChecked(False) for cheque in cheques]

    def save_defaults(self):
        qes = self.form.parentWidget().findChildren(QLineEdit)
        cheques = self.h_box.parentWidget().findChildren(QCheckBox)
        data = [[q.text() for q in qes], [q.isChecked() for q in cheques]]
        with open(DEFAULTS, "wb") as f:
            pickle.dump(data, f)

    def load_defaults(self):
        data = get_default_values()
        qes = self.form.parentWidget().findChildren(QLineEdit)
        cheques = self.h_box.parentWidget().findChildren(QCheckBox)
        [qes[i].setText(j) for i, j in enumerate (data[0])]
        [cheques[i].setChecked(j) for i, j in enumerate (data[1])]

    def create_class(self):
        qes = self.form.parentWidget().findChildren(QLineEdit)
        cheques = self.h_box.parentWidget().findChildren(QCheckBox)
        creator = qes[0].text()
        includes = list(map(str.strip, qes[1].text().split(",")))
        namespace = qes[2].text()
        base_classes = list(map(str.strip, qes[3].text().split(",")))
        names = list(map(str.strip, qes[4].text().split(",")))
        copy_constructor = cheques[0].isChecked()
        copy_assignment = cheques[1].isChecked()
        move_constructor = cheques[2].isChecked()
        move_assignment = cheques[3].isChecked()
        is_final = cheques[4].isChecked()
        destructor = cheques[5].isChecked()
        class_constructor = ClassConstructor(creator,
                                             includes,
                                             namespace,
                                             base_classes,
                                             names,
                                             copy_constructor,
                                             copy_assignment,
                                             move_constructor,
                                             move_assignment,
                                             is_final,
                                             destructor)
        class_constructor.to_file('h')
        class_constructor.to_file('cpp')
        print(class_constructor)
        self.open.setEnabled(True)

    def open_file(self):
        qes = self.form.parentWidget().findChildren(QLineEdit)
        root = os.getcwd()
        for file_name in list(qes[4].text().split(", ")):
            for ext in ['.h', '.cpp']:
                file = file_name + ext
                file_to_open = os.path.join(root, "render", file)
                subprocess.run([NOTEPAD_APP, file_to_open], check=True)


if __name__ == "__main__":
    pass

