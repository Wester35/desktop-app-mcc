# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_main.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(522, 398)
        MainWindow.setMinimumSize(QSize(522, 398))
        MainWindow.setMaximumSize(QSize(522, 398))
        MainWindow.setStyleSheet(u"QFrame\n"
"{\n"
"	border-radius:10px;\n"
"	background-color: transparent;\n"
"	border: 3px solid black;\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.profile_btn = QPushButton(self.centralwidget)
        self.profile_btn.setObjectName(u"profile_btn")
        self.profile_btn.setGeometry(QRect(30, 30, 181, 41))
        self.prokofiev_button = QPushButton(self.centralwidget)
        self.prokofiev_button.setObjectName(u"prokofiev_button")
        self.prokofiev_button.setGeometry(QRect(30, 170, 181, 41))
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(30, 80, 181, 41))
        self.frame_2 = QFrame(self.centralwidget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setGeometry(QRect(250, 10, 261, 231))
        self.frame_2.setStyleSheet(u"#frame\n"
"{\n"
"	border-radius:10px;\n"
"	background-color: transparent;\n"
"	border: 3px solid black;\n"
"}")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_3 = QFrame(self.centralwidget)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setGeometry(QRect(10, 150, 221, 181))
        self.frame_3.setStyleSheet(u"#frame\n"
"{\n"
"	border-radius:10px;\n"
"	background-color: transparent;\n"
"	border: 3px solid black;\n"
"}")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(10, 10, 221, 131))
        self.frame.setStyleSheet(u"")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_4 = QFrame(self.centralwidget)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setGeometry(QRect(250, 250, 261, 81))
        self.frame_4.setStyleSheet(u"#frame\n"
"{\n"
"	border-radius:10px;\n"
"	background-color: transparent;\n"
"	border: 3px solid black;\n"
"}")
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.pushButton = QPushButton(self.frame_4)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(20, 20, 221, 41))
        self.integral_charts = QPushButton(self.centralwidget)
        self.integral_charts.setObjectName(u"integral_charts")
        self.integral_charts.setGeometry(QRect(30, 220, 181, 41))
        self.interval_charts = QPushButton(self.centralwidget)
        self.interval_charts.setObjectName(u"interval_charts")
        self.interval_charts.setGeometry(QRect(30, 270, 181, 41))
        self.integral_window = QPushButton(self.centralwidget)
        self.integral_window.setObjectName(u"integral_window")
        self.integral_window.setGeometry(QRect(270, 130, 221, 41))
        self.analytics_btn = QPushButton(self.centralwidget)
        self.analytics_btn.setObjectName(u"analytics_btn")
        self.analytics_btn.setGeometry(QRect(270, 80, 221, 41))
        self.interval_window = QPushButton(self.centralwidget)
        self.interval_window.setObjectName(u"interval_window")
        self.interval_window.setGeometry(QRect(270, 180, 221, 41))
        self.data_input_btn = QPushButton(self.centralwidget)
        self.data_input_btn.setObjectName(u"data_input_btn")
        self.data_input_btn.setGeometry(QRect(270, 30, 221, 41))
        MainWindow.setCentralWidget(self.centralwidget)
        self.frame_2.raise_()
        self.frame_4.raise_()
        self.frame_3.raise_()
        self.frame.raise_()
        self.profile_btn.raise_()
        self.prokofiev_button.raise_()
        self.pushButton_2.raise_()
        self.integral_charts.raise_()
        self.interval_charts.raise_()
        self.integral_window.raise_()
        self.analytics_btn.raise_()
        self.interval_window.raise_()
        self.data_input_btn.raise_()
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 522, 33))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.profile_btn.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u043e\u0444\u0438\u043b\u044c", None))
        self.prokofiev_button.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u043e\u0433\u043d\u043e\u0437\u044b", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0445\u043e\u0434 \u0441 \u0430\u043a\u043a\u0430\u0443\u043d\u0442\u0430", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u044f", None))
        self.integral_charts.setText(QCoreApplication.translate("MainWindow", u"\u0418\u043d\u0442\u0435\u0433\u0440\u0430\u043b\u044c\u043d\u044b\u0435 \u0433\u0440\u0430\u0444\u0438\u043a\u0438", None))
        self.interval_charts.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0440./\u0441\u0443\u0442. \u0433\u0440\u0430\u0444\u0438\u043a\u0438", None))
        self.integral_window.setText(QCoreApplication.translate("MainWindow", u"\u041c\u043e\u0434\u0435\u043b\u044c \u0438\u043d\u0442\u0435\u0433\u0440\u0430\u043b\u044c\u043d\u043e\u0433\u043e \u043f\u043e\u043a\u0430\u0437\u0430\u0442\u0435\u043b\u044f", None))
        self.analytics_btn.setText(QCoreApplication.translate("MainWindow", u"\u0418\u043d\u0442\u0435\u0433\u0440\u0430\u043b\u044c\u043d\u044b\u0435 \u043f\u043e\u043a\u0430\u0437\u0430\u0442\u0435\u043b\u0438", None))
        self.interval_window.setText(QCoreApplication.translate("MainWindow", u"\u041c\u043e\u0434\u0435\u043b\u044c \u0441\u0440\u0435\u0434\u043d\u0435\u0441\u0443\u0442\u043e\u0447\u043d\u043e\u0433\u043e \u0438\u043d\u0442\u0435\u0440\u0432\u0430\u043b\u0430", None))
        self.data_input_btn.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0432\u043e\u0434 \u0434\u0430\u043d\u043d\u044b\u0445", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u0421\u043f\u0440\u0430\u0432\u043a\u0430", None))
    # retranslateUi

