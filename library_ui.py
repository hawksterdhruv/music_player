# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'library.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(542, 268)
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(0, 0, 541, 261))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.search_label = QtWidgets.QLabel(self.widget)
        self.search_label.setObjectName("search_label")
        self.horizontalLayout_2.addWidget(self.search_label)
        self.search_input = QtWidgets.QLineEdit(self.widget)
        self.search_input.setObjectName("search_input")
        self.horizontalLayout_2.addWidget(self.search_input)
        self.clear_search_button = QtWidgets.QPushButton(self.widget)
        self.clear_search_button.setObjectName("clear_search_button")
        self.horizontalLayout_2.addWidget(self.clear_search_button)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.albums = QtWidgets.QTableView(self.widget)
        self.albums.setObjectName("albums")
        self.horizontalLayout_4.addWidget(self.albums)

        self.artists = QtWidgets.QTableView(self.widget)
        self.artists.setObjectName("artists")
        self.horizontalLayout_4.addWidget(self.artists)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.songs = QtWidgets.QTableView(self.widget)
        self.songs.setObjectName("songs")

        self.verticalLayout.addWidget(self.songs)
        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)
        self.library_button = QtWidgets.QPushButton(self.widget)
        self.library_button.setObjectName("library_button")
        self.gridLayout.addWidget(self.library_button, 1, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.play_now_button = QtWidgets.QPushButton(self.widget)
        self.play_now_button.setObjectName("play_now_button")
        self.horizontalLayout_3.addWidget(self.play_now_button)
        self.enqueue_button = QtWidgets.QPushButton(self.widget)
        self.enqueue_button.setObjectName("enqueue_button")
        self.horizontalLayout_3.addWidget(self.enqueue_button)
        self.status_label = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.status_label.sizePolicy().hasHeightForWidth())
        self.status_label.setSizePolicy(sizePolicy)
        self.status_label.setObjectName("status_label")
        self.horizontalLayout_3.addWidget(self.status_label)
        self.info_button = QtWidgets.QPushButton(self.widget)
        self.info_button.setObjectName("info_button")
        self.horizontalLayout_3.addWidget(self.info_button)
        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 1, 1, 1)
        self.sources = QtWidgets.QTreeView(self.widget)
        self.sources.setObjectName("sources")
        self.gridLayout.addWidget(self.sources, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.search_label.setText(_translate("Dialog", "Search :"))
        self.clear_search_button.setText(_translate("Dialog", "Clear Search"))
        self.library_button.setText(_translate("Dialog", "Library"))
        self.play_now_button.setText(_translate("Dialog", "Play"))
        self.enqueue_button.setText(_translate("Dialog", "Enqueue"))
        self.status_label.setText(_translate("Dialog", "TextLabel"))
        self.info_button.setText(_translate("Dialog", "Info"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
