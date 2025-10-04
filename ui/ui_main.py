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
from PySide6.QtWidgets import (QApplication, QPushButton, QSizePolicy, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(512, 383)
        self.pushButton = QPushButton(MainWindow)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(20, 310, 211, 41))
        self.pushButton_2 = QPushButton(MainWindow)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(280, 240, 211, 41))
        self.data_input_btn = QPushButton(MainWindow)
        self.data_input_btn.setObjectName(u"data_input_btn")
        self.data_input_btn.setGeometry(QRect(360, 30, 131, 41))
        self.analytics_btn = QPushButton(MainWindow)
        self.analytics_btn.setObjectName(u"analytics_btn")
        self.analytics_btn.setGeometry(QRect(170, 30, 171, 41))
        self.prokofiev_button = QPushButton(MainWindow)
        self.prokofiev_button.setObjectName(u"prokofiev_button")
        self.prokofiev_button.setGeometry(QRect(280, 170, 211, 41))
        self.integral_charts = QPushButton(MainWindow)
        self.integral_charts.setObjectName(u"integral_charts")
        self.integral_charts.setGeometry(QRect(20, 170, 211, 41))
        self.interval_charts = QPushButton(MainWindow)
        self.interval_charts.setObjectName(u"interval_charts")
        self.interval_charts.setGeometry(QRect(20, 240, 211, 41))
        self.profile_btn = QPushButton(MainWindow)
        self.profile_btn.setObjectName(u"profile_btn")
        self.profile_btn.setGeometry(QRect(20, 30, 131, 41))
        self.interval_window = QPushButton(MainWindow)
        self.interval_window.setObjectName(u"interval_window")
        self.interval_window.setGeometry(QRect(280, 100, 211, 41))
        self.integral_window = QPushButton(MainWindow)
        self.integral_window.setObjectName(u"integral_window")
        self.integral_window.setGeometry(QRect(20, 100, 211, 41))

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainApp", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u044f", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0445\u043e\u0434 \u0441 \u0430\u043a\u043a\u0430\u0443\u043d\u0442\u0430", None))
        self.data_input_btn.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0432\u043e\u0434 \u0434\u0430\u043d\u043d\u044b\u0445", None))
        self.analytics_btn.setText(QCoreApplication.translate("MainWindow", u"\u0418\u043d\u0442\u0435\u0433\u0440\u0430\u043b\u044c\u043d\u044b\u0435 \u043f\u043e\u043a\u0430\u0437\u0430\u0442\u0435\u043b\u0438", None))
        self.prokofiev_button.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u043e\u0433\u043d\u043e\u0437 \u0441\u0440./\u0441\u0443\u0442. \u0438\u043d\u0442\u0435\u0440\u0432\u0430\u043b\u0430", None))
        self.integral_charts.setText(QCoreApplication.translate("MainWindow", u"\u0418\u043d\u0442\u0435\u0433\u0440\u0430\u043b\u044c\u043d\u044b\u0435 \u0433\u0440\u0430\u0444\u0438\u043a\u0438", None))
        self.interval_charts.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0440./\u0441\u0443\u0442. \u0433\u0440\u0430\u0444\u0438\u043a\u0438", None))
        self.profile_btn.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u043e\u0444\u0438\u043b\u044c", None))
        self.interval_window.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0430\u0441\u0441\u0447\u0435\u0442 \u0438\u043d\u0442\u0435\u0440\u0432\u0430\u043b\u044c\u043d\u043e\u0439 \u043c\u043e\u0434\u0435\u043b\u0438", None))
        self.integral_window.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0430\u0441\u0441\u0447\u0435\u0442 \u0438\u043d\u0442\u0435\u0433\u0440\u0430\u043b\u044c\u043d\u043e\u0439 \u043c\u043e\u0434\u0435\u043b\u0438", None))
    # retranslateUi

