# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'register.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QWidget)

class Ui_Registration(object):
    def setupUi(self, Registration):
        if not Registration.objectName():
            Registration.setObjectName(u"Registration")
        Registration.resize(441, 641)
        Registration.setMinimumSize(QSize(441, 641))
        Registration.setMaximumSize(QSize(541, 641))
        Registration.setStyleSheet(u"*\n"
"{\n"
"	font-family:sans-serif;\n"
"	font-size:24px;\n"
"}\n"
"\n"
"#frame\n"
"{\n"
"	background:#333;\n"
"	border-radius:22px;\n"
"}\n"
"\n"
"#frame_2\n"
"{\n"
"	background:url(C:\\Users\\Wester35\\Downloads\\sgustok_fraktal_sirenevyj_132619_1600x1200.jpg);\n"
"	border-radius:10px;\n"
"}\n"
"\n"
"#pushButton\n"
"{\n"
"color:white;\n"
"background:#4B0082;\n"
"border-radius:15px;\n"
"transition: background 1s;\n"
"}\n"
"\n"
"#pushButton:hover\n"
"{\n"
"	color:#4B0082;\n"
"	background:#696969;\n"
"	border-radius:15px;\n"
"\n"
"}\n"
"\n"
"#pushButton:pressed\n"
"{\n"
"background-color: #483D8B;\n"
"transform: scale(0.9);\n"
"}\n"
"\n"
"QToolButton\n"
"{\n"
"background:#4B0082;\n"
"border-radius:60px;\n"
"}\n"
"\n"
"QMainWindow\n"
"{\n"
"background:url('resources/sgustok_fraktal_sirenevyj_132619_1600x1200.jpg');\n"
"}\n"
"\n"
"QLineEdit\n"
"{\n"
"background:transparent;\n"
"border:none;\n"
"color:#717072;\n"
"border-bottom:1px solid #717072;\n"
"}\n"
"\n"
"#checkPassword\n"
"{\n"
"background:#333;\n"
"color:w"
                        "hite;\n"
"border-radius:15px;\n"
"transition: background 1s;\n"
"}\n"
"\n"
"#checkPassword:hover\n"
"{\n"
"background:#4B0082;\n"
"border-radius:15px;\n"
"}\n"
"\n"
"#checkPassword:pressed\n"
"{\n"
"background:#483D8B;\n"
"transform: scale(0.9);\n"
"}\n"
"\n"
"QCheckBox {\n"
"    font-size: 16px;\n"
"}\n"
"\n"
"#checkPassword\n"
"{\n"
"background:#333;\n"
"color:white;\n"
"border-radius:15px;\n"
"transition: background 1s;\n"
"}\n"
"\n"
"#checkPassword_2\n"
"{\n"
"background:#333;\n"
"color:white;\n"
"border-radius:15px;\n"
"transition: background 1s;\n"
"}\n"
"#checkPassword_2:hover\n"
"{\n"
"background:#4B0082;\n"
"border-radius:15px;\n"
"}\n"
"#checkPassword_2:pressed\n"
"{\n"
"background:#483D8B;\n"
"transform: scale(0.9);\n"
"}")
        self.frame_2 = QFrame(Registration)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setGeometry(QRect(0, 0, 441, 641))
        self.frame_2.setMinimumSize(QSize(0, 0))
        self.frame_2.setMaximumSize(QSize(541, 720))
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.frame = QFrame(self.frame_2)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(20, 20, 401, 591))
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(126, 50, 151, 41))
        self.label.setStyleSheet(u"")
        self.pushButton = QPushButton(self.frame)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(10, 470, 381, 61))
        self.usernameEdit = QLineEdit(self.frame)
        self.usernameEdit.setObjectName(u"usernameEdit")
        self.usernameEdit.setGeometry(QRect(20, 130, 360, 30))
        self.passwordEdit = QLineEdit(self.frame)
        self.passwordEdit.setObjectName(u"passwordEdit")
        self.passwordEdit.setGeometry(QRect(20, 340, 360, 30))
        self.passwordEdit.setEchoMode(QLineEdit.EchoMode.Password)
        self.checkPassword_2 = QPushButton(self.frame)
        self.checkPassword_2.setObjectName(u"checkPassword_2")
        self.checkPassword_2.setGeometry(QRect(340, 400, 31, 31))
        self.fioEdit = QLineEdit(self.frame)
        self.fioEdit.setObjectName(u"fioEdit")
        self.fioEdit.setGeometry(QRect(20, 200, 360, 30))
        self.phoneEdit = QLineEdit(self.frame)
        self.phoneEdit.setObjectName(u"phoneEdit")
        self.phoneEdit.setGeometry(QRect(20, 270, 360, 30))
        self.passwordEdit_2 = QLineEdit(self.frame)
        self.passwordEdit_2.setObjectName(u"passwordEdit_2")
        self.passwordEdit_2.setGeometry(QRect(20, 410, 360, 30))
        self.passwordEdit_2.setEchoMode(QLineEdit.EchoMode.Password)
        self.yes_account = QLabel(self.frame)
        self.yes_account.setObjectName(u"yes_account")
        self.yes_account.setGeometry(QRect(20, 550, 161, 21))
        self.yes_account.setStyleSheet(u"*{font-size:14px;}")
        self.to_auth = QPushButton(self.frame)
        self.to_auth.setObjectName(u"to_auth")
        self.to_auth.setGeometry(QRect(330, 550, 51, 21))
        self.to_auth.setStyleSheet(u"*{\n"
"font-size:14px;\n"
"background:transparent;\n"
"border: none;\n"
"}")
        self.checkPassword = QPushButton(self.frame)
        self.checkPassword.setObjectName(u"checkPassword")
        self.checkPassword.setGeometry(QRect(340, 330, 31, 31))
        self.label.raise_()
        self.pushButton.raise_()
        self.usernameEdit.raise_()
        self.passwordEdit.raise_()
        self.fioEdit.raise_()
        self.phoneEdit.raise_()
        self.passwordEdit_2.raise_()
        self.yes_account.raise_()
        self.to_auth.raise_()
        self.checkPassword.raise_()
        self.checkPassword_2.raise_()
        QWidget.setTabOrder(self.usernameEdit, self.fioEdit)
        QWidget.setTabOrder(self.fioEdit, self.phoneEdit)
        QWidget.setTabOrder(self.phoneEdit, self.passwordEdit)
        QWidget.setTabOrder(self.passwordEdit, self.passwordEdit_2)
        QWidget.setTabOrder(self.passwordEdit_2, self.checkPassword)
        QWidget.setTabOrder(self.checkPassword, self.checkPassword_2)
        QWidget.setTabOrder(self.checkPassword_2, self.pushButton)
        QWidget.setTabOrder(self.pushButton, self.to_auth)

        self.retranslateUi(Registration)

        QMetaObject.connectSlotsByName(Registration)
    # setupUi

    def retranslateUi(self, Registration):
        Registration.setWindowTitle(QCoreApplication.translate("Registration", u"Registration", None))
        self.label.setText(QCoreApplication.translate("Registration", u"\u0420\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u044f", None))
        self.pushButton.setText(QCoreApplication.translate("Registration", u"\u0417\u0430\u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0438\u0440\u043e\u0432\u0430\u0442\u044c\u0441\u044f", None))
        self.usernameEdit.setText("")
        self.usernameEdit.setPlaceholderText(QCoreApplication.translate("Registration", u"Username", None))
        self.passwordEdit.setInputMask("")
        self.passwordEdit.setText("")
        self.passwordEdit.setPlaceholderText(QCoreApplication.translate("Registration", u"Password", None))
        self.checkPassword_2.setText("")
        self.fioEdit.setText("")
        self.fioEdit.setPlaceholderText(QCoreApplication.translate("Registration", u"Full name", None))
        self.phoneEdit.setText("")
        self.phoneEdit.setPlaceholderText(QCoreApplication.translate("Registration", u"Phone", None))
        self.passwordEdit_2.setInputMask("")
        self.passwordEdit_2.setText("")
        self.passwordEdit_2.setPlaceholderText(QCoreApplication.translate("Registration", u"Password again", None))
        self.yes_account.setText(QCoreApplication.translate("Registration", u"\u0415\u0441\u0442\u044c \u0430\u043a\u043a\u0430\u0443\u043d\u0442?", None))
        self.to_auth.setText(QCoreApplication.translate("Registration", u"\u0412\u043e\u0439\u0442\u0438", None))
        self.checkPassword.setText("")
    # retranslateUi

