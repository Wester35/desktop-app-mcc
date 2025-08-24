# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'auth.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QWidget)

class Ui_Authorization(object):
    def setupUi(self, Authorization):
        if not Authorization.objectName():
            Authorization.setObjectName(u"Authorization")
        Authorization.resize(401, 501)
        Authorization.setMinimumSize(QSize(401, 501))
        Authorization.setMaximumSize(QSize(501, 501))
        Authorization.setStyleSheet(u"*\n"
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
"#no_account{\n"
"font-size: 14px;\n"
"}\n"
"")
        self.frame_2 = QFrame(Authorization)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setGeometry(QRect(0, 0, 401, 501))
        self.frame_2.setMinimumSize(QSize(401, 501))
        self.frame_2.setMaximumSize(QSize(401, 501))
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.frame = QFrame(self.frame_2)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(20, 20, 361, 461))
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(110, 50, 141, 41))
        self.label.setStyleSheet(u"")
        self.pushButton = QPushButton(self.frame)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(10, 340, 341, 61))
        self.usernameEdit = QLineEdit(self.frame)
        self.usernameEdit.setObjectName(u"usernameEdit")
        self.usernameEdit.setGeometry(QRect(20, 150, 321, 22))
        self.passwordEdit = QLineEdit(self.frame)
        self.passwordEdit.setObjectName(u"passwordEdit")
        self.passwordEdit.setGeometry(QRect(20, 230, 321, 22))
        self.passwordEdit.setEchoMode(QLineEdit.EchoMode.Password)
        self.checkPassword = QPushButton(self.frame)
        self.checkPassword.setObjectName(u"checkPassword")
        self.checkPassword.setGeometry(QRect(300, 220, 31, 31))
        self.checkBox = QCheckBox(self.frame)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setGeometry(QRect(20, 290, 231, 20))
        self.checkBox.setAcceptDrops(False)
        self.no_account = QLabel(self.frame)
        self.no_account.setObjectName(u"no_account")
        self.no_account.setGeometry(QRect(20, 420, 161, 21))
        self.to_register = QPushButton(self.frame)
        self.to_register.setObjectName(u"to_register")
        self.to_register.setGeometry(QRect(200, 420, 151, 21))
        self.to_register.setStyleSheet(u"*{\n"
"font-size:14px;\n"
"background:transparent;\n"
"border: none;\n"
"}")
        self.pushButton.raise_()
        self.usernameEdit.raise_()
        self.passwordEdit.raise_()
        self.checkPassword.raise_()
        self.checkBox.raise_()
        self.no_account.raise_()
        self.to_register.raise_()
        self.label.raise_()

        self.retranslateUi(Authorization)

        QMetaObject.connectSlotsByName(Authorization)
    # setupUi

    def retranslateUi(self, Authorization):
        Authorization.setWindowTitle(QCoreApplication.translate("Authorization", u"Authorization", None))
        self.label.setText(QCoreApplication.translate("Authorization", u"\u0410\u0432\u0442\u043e\u0440\u0438\u0437\u0430\u0446\u0438\u044f", None))
        self.pushButton.setText(QCoreApplication.translate("Authorization", u"\u0410\u0432\u0442\u043e\u0440\u0438\u0437\u043e\u0432\u0430\u0442\u044c\u0441\u044f", None))
        self.usernameEdit.setText("")
        self.usernameEdit.setPlaceholderText(QCoreApplication.translate("Authorization", u"Username", None))
        self.passwordEdit.setInputMask("")
        self.passwordEdit.setText("")
        self.passwordEdit.setPlaceholderText(QCoreApplication.translate("Authorization", u"Password", None))
        self.checkPassword.setText("")
        self.checkBox.setText(QCoreApplication.translate("Authorization", u"\u0417\u0430\u043f\u043e\u043c\u043d\u0438\u0442\u044c \u043c\u0435\u043d\u044f?", None))
        self.no_account.setText(QCoreApplication.translate("Authorization", u"\u041d\u0435\u0442 \u0430\u043a\u043a\u0430\u0443\u043d\u0442\u0430?", None))
        self.to_register.setText(QCoreApplication.translate("Authorization", u"\u0417\u0430\u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0438\u0440\u043e\u0432\u0430\u0442\u044c\u0441\u044f", None))
    # retranslateUi

