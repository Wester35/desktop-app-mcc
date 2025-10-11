# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QPushButton, QSizePolicy,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(522, 374)
        MainWindow.setMinimumSize(QSize(522, 374))
        MainWindow.setMaximumSize(QSize(522, 374))
        MainWindow.setStyleSheet(u"QFrame\n"
"{\n"
"	border-radius:10px;\n"
"	background-color: transparent;\n"
"	border: 3px solid black;\n"
"}")
        self.integral_charts = QPushButton(MainWindow)
        self.integral_charts.setObjectName(u"integral_charts")
        self.integral_charts.setGeometry(QRect(30, 230, 181, 41))
        self.interval_charts = QPushButton(MainWindow)
        self.interval_charts.setObjectName(u"interval_charts")
        self.interval_charts.setGeometry(QRect(30, 280, 181, 41))
        self.frame = QFrame(MainWindow)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(10, 20, 221, 131))
        self.frame.setStyleSheet(u"")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_2 = QFrame(MainWindow)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setGeometry(QRect(250, 20, 261, 231))
        self.frame_2.setStyleSheet(u"#frame\n"
"{\n"
"	border-radius:10px;\n"
"	background-color: transparent;\n"
"	border: 3px solid black;\n"
"}")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.prokofiev_button = QPushButton(MainWindow)
        self.prokofiev_button.setObjectName(u"prokofiev_button")
        self.prokofiev_button.setGeometry(QRect(30, 180, 181, 41))
        self.pushButton_2 = QPushButton(MainWindow)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(30, 90, 181, 41))
        self.profile_btn = QPushButton(MainWindow)
        self.profile_btn.setObjectName(u"profile_btn")
        self.profile_btn.setGeometry(QRect(30, 40, 181, 41))
        self.data_input_btn = QPushButton(MainWindow)
        self.data_input_btn.setObjectName(u"data_input_btn")
        self.data_input_btn.setGeometry(QRect(270, 40, 221, 41))
        self.analytics_btn = QPushButton(MainWindow)
        self.analytics_btn.setObjectName(u"analytics_btn")
        self.analytics_btn.setGeometry(QRect(270, 90, 221, 41))
        self.interval_window = QPushButton(MainWindow)
        self.interval_window.setObjectName(u"interval_window")
        self.interval_window.setGeometry(QRect(270, 190, 221, 41))
        self.integral_window = QPushButton(MainWindow)
        self.integral_window.setObjectName(u"integral_window")
        self.integral_window.setGeometry(QRect(270, 140, 221, 41))
        self.frame_3 = QFrame(MainWindow)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setGeometry(QRect(10, 160, 221, 181))
        self.frame_3.setStyleSheet(u"#frame\n"
"{\n"
"	border-radius:10px;\n"
"	background-color: transparent;\n"
"	border: 3px solid black;\n"
"}")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_4 = QFrame(MainWindow)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setGeometry(QRect(250, 260, 261, 81))
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
        self.frame_3.raise_()
        self.frame_4.raise_()
        self.frame_2.raise_()
        self.frame.raise_()
        self.integral_charts.raise_()
        self.interval_charts.raise_()
        self.prokofiev_button.raise_()
        self.pushButton_2.raise_()
        self.profile_btn.raise_()
        self.data_input_btn.raise_()
        self.analytics_btn.raise_()
        self.interval_window.raise_()
        self.integral_window.raise_()

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainApp", None))
        self.integral_charts.setText(QCoreApplication.translate("MainWindow", u"\u0418\u043d\u0442\u0435\u0433\u0440\u0430\u043b\u044c\u043d\u044b\u0435 \u0433\u0440\u0430\u0444\u0438\u043a\u0438", None))
        self.interval_charts.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0440./\u0441\u0443\u0442. \u0433\u0440\u0430\u0444\u0438\u043a\u0438", None))
        self.prokofiev_button.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u043e\u0433\u043d\u043e\u0437\u044b", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0445\u043e\u0434 \u0441 \u0430\u043a\u043a\u0430\u0443\u043d\u0442\u0430", None))
        self.profile_btn.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u043e\u0444\u0438\u043b\u044c", None))
        self.data_input_btn.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0432\u043e\u0434 \u0434\u0430\u043d\u043d\u044b\u0445", None))
        self.analytics_btn.setText(QCoreApplication.translate("MainWindow", u"\u0418\u043d\u0442\u0435\u0433\u0440\u0430\u043b\u044c\u043d\u044b\u0435 \u043f\u043e\u043a\u0430\u0437\u0430\u0442\u0435\u043b\u0438", None))
        self.interval_window.setText(QCoreApplication.translate("MainWindow", u"\u041c\u043e\u0434\u0435\u043b\u044c \u0441\u0440\u0435\u0434\u043d\u0435\u0441\u0443\u0442\u043e\u0447\u043d\u043e\u0433\u043e \u0438\u043d\u0442\u0435\u0440\u0432\u0430\u043b\u0430", None))
        self.integral_window.setText(QCoreApplication.translate("MainWindow", u"\u041c\u043e\u0434\u0435\u043b\u044c \u0438\u043d\u0442\u0435\u0433\u0440\u0430\u043b\u044c\u043d\u043e\u0433\u043e \u043f\u043e\u043a\u0430\u0437\u0430\u0442\u0435\u043b\u044f", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u044f", None))
    # retranslateUi

