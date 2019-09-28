# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'player.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(610, 279)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.current_song_label = QtWidgets.QLabel(self.centralwidget)
        self.current_song_label.setGeometry(QtCore.QRect(220, 10, 67, 17))
        self.current_song_label.setObjectName("current_song_label")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(0, 220, 604, 27))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.previous_button = QtWidgets.QPushButton(self.widget)
        self.previous_button.setObjectName("previous_button")
        self.horizontalLayout.addWidget(self.previous_button)
        self.play_button = QtWidgets.QPushButton(self.widget)
        self.play_button.setObjectName("play_button")
        self.horizontalLayout.addWidget(self.play_button)
        self.pause_button = QtWidgets.QPushButton(self.widget)
        self.pause_button.setObjectName("pause_button")
        self.horizontalLayout.addWidget(self.pause_button)
        self.stop_button = QtWidgets.QPushButton(self.widget)
        self.stop_button.setObjectName("stop_button")
        self.horizontalLayout.addWidget(self.stop_button)
        self.next_button = QtWidgets.QPushButton(self.widget)
        self.next_button.setObjectName("next_button")
        self.horizontalLayout.addWidget(self.next_button)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.suffle_button = QtWidgets.QPushButton(self.widget)
        self.suffle_button.setObjectName("suffle_button")
        self.horizontalLayout.addWidget(self.suffle_button)
        self.loop_button = QtWidgets.QPushButton(self.widget)
        self.loop_button.setObjectName("loop_button")
        self.horizontalLayout.addWidget(self.loop_button)
        self.widget1 = QtWidgets.QWidget(self.centralwidget)
        self.widget1.setGeometry(QtCore.QRect(0, 160, 601, 27))
        self.widget1.setObjectName("widget1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.seek = QtWidgets.QSlider(self.widget1)
        self.seek.setOrientation(QtCore.Qt.Horizontal)
        self.seek.setObjectName("seek")
        self.horizontalLayout_2.addWidget(self.seek)
        self.volume = QtWidgets.QSlider(self.widget1)
        self.volume.setOrientation(QtCore.Qt.Horizontal)
        self.volume.setObjectName("volume")
        self.horizontalLayout_2.addWidget(self.volume)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.equilizer_button = QtWidgets.QPushButton(self.widget1)
        self.equilizer_button.setObjectName("equilizer_button")
        self.horizontalLayout_2.addWidget(self.equilizer_button)
        self.playlist_button = QtWidgets.QPushButton(self.widget1)
        self.playlist_button.setObjectName("playlist_button")
        self.horizontalLayout_2.addWidget(self.playlist_button)
        self.medialibrary_button = QtWidgets.QPushButton(self.widget1)
        self.medialibrary_button.setObjectName("medialibrary_button")
        self.horizontalLayout_2.addWidget(self.medialibrary_button)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.current_song_label.setText(_translate("MainWindow", "TextLabel"))
        self.previous_button.setText(_translate("MainWindow", "Previous"))
        self.play_button.setText(_translate("MainWindow", "Play"))
        self.pause_button.setText(_translate("MainWindow", "Pause"))
        self.stop_button.setText(_translate("MainWindow", "Stop"))
        self.next_button.setText(_translate("MainWindow", "Next"))
        self.suffle_button.setText(_translate("MainWindow", "Shuffle"))
        self.loop_button.setText(_translate("MainWindow", "Loop"))
        self.equilizer_button.setText(_translate("MainWindow", "EQ"))
        self.playlist_button.setText(_translate("MainWindow", "PL"))
        self.medialibrary_button.setText(_translate("MainWindow", "ML"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())