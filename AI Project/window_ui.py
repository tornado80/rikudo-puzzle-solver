# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'window.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from canvas import MplCanvas


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(832, 608)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.splitter_2 = QSplitter(self.centralwidget)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Horizontal)
        self.widget = QWidget(self.splitter_2)
        self.widget.setObjectName(u"widget")
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.draw_button = QPushButton(self.widget)
        self.draw_button.setObjectName(u"draw_button")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.draw_button.sizePolicy().hasHeightForWidth())
        self.draw_button.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.draw_button, 2, 0, 1, 2)

        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.spinBox = QSpinBox(self.widget)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMinimum(10)
        self.spinBox.setMaximum(100)
        self.spinBox.setValue(40)

        self.gridLayout.addWidget(self.spinBox, 1, 1, 1, 1)

        self.splitter_3 = QSplitter(self.widget)
        self.splitter_3.setObjectName(u"splitter_3")
        self.splitter_3.setOrientation(Qt.Vertical)
        self.verticalLayoutWidget = QWidget(self.splitter_3)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName(u"label_2")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy2)
        self.label_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout.addWidget(self.label_2)

        self.puzzle_plain_text_edit = QPlainTextEdit(self.verticalLayoutWidget)
        self.puzzle_plain_text_edit.setObjectName(u"puzzle_plain_text_edit")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.puzzle_plain_text_edit.sizePolicy().hasHeightForWidth())
        self.puzzle_plain_text_edit.setSizePolicy(sizePolicy3)
        font = QFont()
        font.setFamily(u"Code New Roman")
        self.puzzle_plain_text_edit.setFont(font)

        self.verticalLayout.addWidget(self.puzzle_plain_text_edit)

        self.splitter_3.addWidget(self.verticalLayoutWidget)
        self.verticalLayoutWidget_2 = QWidget(self.splitter_3)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.verticalLayoutWidget_2)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_2.addWidget(self.label_3)

        self.solved_cells_plain_text_edit = QPlainTextEdit(self.verticalLayoutWidget_2)
        self.solved_cells_plain_text_edit.setObjectName(u"solved_cells_plain_text_edit")
        sizePolicy3.setHeightForWidth(self.solved_cells_plain_text_edit.sizePolicy().hasHeightForWidth())
        self.solved_cells_plain_text_edit.setSizePolicy(sizePolicy3)

        self.verticalLayout_2.addWidget(self.solved_cells_plain_text_edit)

        self.splitter_3.addWidget(self.verticalLayoutWidget_2)

        self.gridLayout.addWidget(self.splitter_3, 0, 0, 1, 2)

        self.splitter_2.addWidget(self.widget)
        self.splitter = QSplitter(self.splitter_2)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Vertical)
        self.graphics_view = QGraphicsView(self.splitter)
        self.graphics_view.setObjectName(u"graphics_view")
        sizePolicy4 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy4.setHorizontalStretch(1)
        sizePolicy4.setVerticalStretch(1)
        sizePolicy4.setHeightForWidth(self.graphics_view.sizePolicy().hasHeightForWidth())
        self.graphics_view.setSizePolicy(sizePolicy4)
        font1 = QFont()
        font1.setPointSize(16)
        self.graphics_view.setFont(font1)
        self.splitter.addWidget(self.graphics_view)
        self.canvas = MplCanvas(self.splitter)
        self.canvas.setObjectName(u"canvas")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.canvas.sizePolicy().hasHeightForWidth())
        self.canvas.setSizePolicy(sizePolicy5)
        self.splitter.addWidget(self.canvas)
        self.splitter_2.addWidget(self.splitter)

        self.gridLayout_2.addWidget(self.splitter_2, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Rikudo Puzzle Solver", None))
        self.draw_button.setText(QCoreApplication.translate("MainWindow", u"Draw!", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Radius of Cells:", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Puzzle Representation:", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Solved Cells:", None))
    # retranslateUi

