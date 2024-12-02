#For Autodesk Maya 2024, Encoding UTF-8
import maya.cmds as cmds
from PySide2 import QtWidgets
from PySide2 import QtCore
from maya.app.general import mayaMixin

class OpenWindowsDetector(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    def __init__(self):
        super(OpenWindowsDetector, self).__init__()
        self.toolUI()


    def toolUI(self):
        self.setGeometry(500, 300, 400, 350)
        self.setWindowTitle("Open Windows Detector")
        self.statusBar().showMessage("Last Updated: 2024.11.07   |   For: Maya 2024   |   Fuma Hara")

        label_openWindow = QtWidgets.QLabel("現在開いているウィンドウ一覧", alignment = QtCore.Qt.AlignBottom)
        self.label_windowNum = QtWidgets.QLabel("ウィンドウ数: 0", alignment = QtCore.Qt.AlignRight)

        self.listArea_openWindows = QtWidgets.QListWidget()

        button_detection = QtWidgets.QPushButton("検出 / 更新",  fixedWidth = 100)
        button_showFront = QtWidgets.QPushButton("選択中の項目を手前に移動")
        button_close = QtWidgets.QPushButton("選択中の項目を閉じる")
        button_detection.clicked.connect(self.detection_openWindows)
        button_showFront.clicked.connect(self.showFront_selectedWindow)
        button_close.clicked.connect(self.close_selectedWindow)

        lyt_hBox_detection = QtWidgets.QHBoxLayout()
        lyt_hBox_detection.addWidget(label_openWindow)
        lyt_hBox_detection.addWidget(button_detection)

        lyt_hBox_button = QtWidgets.QHBoxLayout()
        lyt_hBox_button.addWidget(button_showFront)
        lyt_hBox_button.addWidget(button_close)

        lyt_vBox_main = QtWidgets.QVBoxLayout()
        lyt_vBox_main.addLayout(lyt_hBox_detection)
        lyt_vBox_main.addWidget(self.listArea_openWindows)
        lyt_vBox_main.addWidget(self.label_windowNum)
        lyt_vBox_main.addLayout(lyt_hBox_button)

        lyt_widget = QtWidgets.QWidget()
        lyt_widget.setLayout(lyt_vBox_main)
        self.setCentralWidget(lyt_widget)


    def detection_openWindows(self):
        titles_openWindows = [] #現在開いているウィンドウのタイトル全て
        widgets_openWindows = [] #現在開いているウィンドウ全て

        for one_window in QtWidgets.QApplication.topLevelWidgets():
            if one_window.isVisible() and not one_window.objectName() == "MayaWindow" and not one_window.windowTitle() == "Open Windows Detector": #Mayaのメインウィンドウと本ツールを除く
                titles_openWindows.append(one_window.windowTitle())
                widgets_openWindows.append(one_window)
        else:
            self.listArea_openWindows.clear()
            self.listArea_openWindows.addItems(sorted(titles_openWindows)) #並べ替えて表示
            self.label_windowNum.setText(f"ウィンドウ数: {self.listArea_openWindows.count()}")
            self.windows_openWindow = dict(zip(titles_openWindows, widgets_openWindows)) #まとめて辞書化
    

    def showFront_selectedWindow(self):
        selected_windowName = [one_item.text() for one_item in self.listArea_openWindows.selectedItems()]

        if not selected_windowName:
            cmds.confirmDialog(b = "OK", icn = 'warning', m = "何も選択されていません。", t = "ERROR: Open Windows Detector")
        else:
            if self.windows_openWindow[selected_windowName[0]].isMinimized():
                self.windows_openWindow[selected_windowName[0]].showNormal() #最小化している場合元のサイズに戻す
            else:
                self.windows_openWindow[selected_windowName[0]].raise_() #一番前に表示する


    def close_selectedWindow(self):
        selected_windowName = [one_item.text() for one_item in self.listArea_openWindows.selectedItems()]

        if not selected_windowName:
            cmds.confirmDialog(b = "OK", icn = 'warning', m = "何も選択されていません。", t = "ERROR: Open Windows Detector")
        else:
            self.windows_openWindow[selected_windowName[0]].close() #ウィンドウを閉じる
            self.detection_openWindows()


toolWindow = OpenWindowsDetector()
toolWindow.show()
