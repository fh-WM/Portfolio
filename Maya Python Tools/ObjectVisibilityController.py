#For Autodesk Maya 2024, Encoding UTF-8
import maya.cmds as cmds
from PySide2 import QtWidgets
from maya.app.general import mayaMixin

class ObjectVisibilityController(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    def __init__(self):
        super(ObjectVisibilityController, self).__init__()
        self.toolUI()
        self.initialize_settings()


    def toolUI(self):
        self.setGeometry(500, 300, 460, 580)
        self.setWindowTitle("Object Visibility Controller")
        self.statusBar().showMessage("Last Updated: 2024.12.24   |   For: Maya 2024   |   Fuma Hara")

        label_setting01 = QtWidgets.QLabel("<b>設定01</b>")
        label_setting02 = QtWidgets.QLabel("<b>設定02</b>")
        label_setting03 = QtWidgets.QLabel("<b>設定03</b>")

        self.listArea_visibility01 = QtWidgets.QListWidget(selectionMode = QtWidgets.QAbstractItemView.ExtendedSelection)
        self.listArea_visibility02 = QtWidgets.QListWidget(selectionMode = QtWidgets.QAbstractItemView.ExtendedSelection)
        self.listArea_visibility03 = QtWidgets.QListWidget(selectionMode = QtWidgets.QAbstractItemView.ExtendedSelection)

        self.checkBox_persp01 = QtWidgets.QCheckBox("パースビュー")
        self.checkBox_left01 = QtWidgets.QCheckBox("左面ビュー")
        self.checkBox_right01 = QtWidgets.QCheckBox("右面ビュー")
        self.checkBox_front01 = QtWidgets.QCheckBox("前面ビュー")
        self.checkBox_top01 = QtWidgets.QCheckBox("上面ビュー")
        self.checkBox_bottom01 = QtWidgets.QCheckBox("下面ビュー")
        self.checkBox_back01 = QtWidgets.QCheckBox("後面ビュー")

        self.checkBox_persp02 = QtWidgets.QCheckBox("パースビュー")
        self.checkBox_left02 = QtWidgets.QCheckBox("左面ビュー")
        self.checkBox_right02 = QtWidgets.QCheckBox("右面ビュー")
        self.checkBox_front02 = QtWidgets.QCheckBox("前面ビュー")
        self.checkBox_top02 = QtWidgets.QCheckBox("上面ビュー")
        self.checkBox_bottom02 = QtWidgets.QCheckBox("下面ビュー")
        self.checkBox_back02 = QtWidgets.QCheckBox("後面ビュー")

        self.checkBox_persp03 = QtWidgets.QCheckBox("パースビュー")
        self.checkBox_left03 = QtWidgets.QCheckBox("左面ビュー")
        self.checkBox_right03 = QtWidgets.QCheckBox("右面ビュー")
        self.checkBox_front03 = QtWidgets.QCheckBox("前面ビュー")
        self.checkBox_top03 = QtWidgets.QCheckBox("上面ビュー")
        self.checkBox_bottom03 = QtWidgets.QCheckBox("下面ビュー")
        self.checkBox_back03 = QtWidgets.QCheckBox("後面ビュー")

        button_register01 = QtWidgets.QPushButton("登録", objectName = "Register01")
        button_exclusion01 = QtWidgets.QPushButton("除外", objectName = "Exclusion01")
        button_clear01 = QtWidgets.QPushButton("クリア", objectName = "Clear01")
        button_register01.clicked.connect(self.register_objectNames)
        button_exclusion01.clicked.connect(self.exclusion_objectNames)
        button_clear01.clicked.connect(self.clear_objectNames)

        button_register02 = QtWidgets.QPushButton("登録", objectName = "Register02")
        button_exclusion02 = QtWidgets.QPushButton("除外", objectName = "Exclusion02")
        button_clear02 = QtWidgets.QPushButton("クリア", objectName = "Clear02")
        button_register02.clicked.connect(self.register_objectNames)
        button_exclusion02.clicked.connect(self.exclusion_objectNames)
        button_clear02.clicked.connect(self.clear_objectNames)

        button_register03 = QtWidgets.QPushButton("登録", objectName = "Register03")
        button_exclusion03 = QtWidgets.QPushButton("除外", objectName = "Exclusion03")
        button_clear03 = QtWidgets.QPushButton("クリア", objectName = "Clear03")
        button_register03.clicked.connect(self.register_objectNames)
        button_exclusion03.clicked.connect(self.exclusion_objectNames)
        button_clear03.clicked.connect(self.clear_objectNames)

        button_hidden = QtWidgets.QPushButton("非表示")
        button_visible = QtWidgets.QPushButton("非表示を全て解除")
        button_hidden.clicked.connect(self.hidden_objectVisibility)
        button_visible.clicked.connect(self.visible_objectVisibility)

        spacer_setting01 = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        spacer_setting02 = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        spacer_setting03 = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        lyt_grid_setting01 = QtWidgets.QGridLayout() #ビュー選択、設定01用
        lyt_grid_setting01.addWidget(self.checkBox_persp01, 0, 0)
        lyt_grid_setting01.addWidget(self.checkBox_left01, 0, 1)
        lyt_grid_setting01.addWidget(self.checkBox_right01, 0, 2)
        lyt_grid_setting01.addWidget(self.checkBox_front01, 1, 0)
        lyt_grid_setting01.addWidget(self.checkBox_top01, 1, 1)
        lyt_grid_setting01.addWidget(self.checkBox_bottom01, 1, 2)
        lyt_grid_setting01.addWidget(self.checkBox_back01, 2, 0)

        lyt_grid_setting02 = QtWidgets.QGridLayout() #ビュー選択、設定02用
        lyt_grid_setting02.addWidget(self.checkBox_persp02, 0, 0)
        lyt_grid_setting02.addWidget(self.checkBox_left02, 0, 1)
        lyt_grid_setting02.addWidget(self.checkBox_right02, 0, 2)
        lyt_grid_setting02.addWidget(self.checkBox_front02, 1, 0)
        lyt_grid_setting02.addWidget(self.checkBox_top02, 1, 1)
        lyt_grid_setting02.addWidget(self.checkBox_bottom02, 1, 2)
        lyt_grid_setting02.addWidget(self.checkBox_back02, 2, 0)

        lyt_grid_setting03 = QtWidgets.QGridLayout() #ビュー選択、設定03用
        lyt_grid_setting03.addWidget(self.checkBox_persp03, 0, 0)
        lyt_grid_setting03.addWidget(self.checkBox_left03, 0, 1)
        lyt_grid_setting03.addWidget(self.checkBox_right03, 0, 2)
        lyt_grid_setting03.addWidget(self.checkBox_front03, 1, 0)
        lyt_grid_setting03.addWidget(self.checkBox_top03, 1, 1)
        lyt_grid_setting03.addWidget(self.checkBox_bottom03, 1, 2)
        lyt_grid_setting03.addWidget(self.checkBox_back03, 2, 0)

        lyt_grid_buttons01 = QtWidgets.QGridLayout() #設定01ボタン用
        lyt_grid_buttons01.addWidget(button_register01, 0, 0, 1, 2)
        lyt_grid_buttons01.addWidget(button_exclusion01, 1, 0)
        lyt_grid_buttons01.addWidget(button_clear01, 1, 1)

        lyt_grid_buttons02 = QtWidgets.QGridLayout() #設定02ボタン用
        lyt_grid_buttons02.addWidget(button_register02, 0, 0, 1, 2)
        lyt_grid_buttons02.addWidget(button_exclusion02, 1, 0)
        lyt_grid_buttons02.addWidget(button_clear02, 1, 1)

        lyt_grid_buttons03 = QtWidgets.QGridLayout() #設定03ボタン用
        lyt_grid_buttons03.addWidget(button_register03, 0, 0, 1, 2)
        lyt_grid_buttons03.addWidget(button_exclusion03, 1, 0)
        lyt_grid_buttons03.addWidget(button_clear03, 1, 1)

        lyt_vBox_setting01 = QtWidgets.QVBoxLayout() #設定01項目用
        lyt_vBox_setting01.addLayout(lyt_grid_buttons01)
        lyt_vBox_setting01.addLayout(lyt_grid_setting01)
        lyt_vBox_setting01.addItem(spacer_setting01)

        lyt_vBox_setting02 = QtWidgets.QVBoxLayout() #設定02項目用
        lyt_vBox_setting02.addLayout(lyt_grid_buttons02)
        lyt_vBox_setting02.addLayout(lyt_grid_setting02)
        lyt_vBox_setting02.addItem(spacer_setting02)

        lyt_vBox_setting03 = QtWidgets.QVBoxLayout() #設定03項目用
        lyt_vBox_setting03.addLayout(lyt_grid_buttons03)
        lyt_vBox_setting03.addLayout(lyt_grid_setting03)
        lyt_vBox_setting03.addItem(spacer_setting03)

        lyt_grid_main = QtWidgets.QGridLayout()
        lyt_grid_main.addWidget(label_setting01, 0, 0, 1, 2)
        lyt_grid_main.addWidget(self.listArea_visibility01, 1, 0)
        lyt_grid_main.addLayout(lyt_vBox_setting01, 1, 1)
        lyt_grid_main.addWidget(label_setting02, 2, 0, 1, 2)
        lyt_grid_main.addWidget(self.listArea_visibility02, 3, 0)
        lyt_grid_main.addLayout(lyt_vBox_setting02, 3, 1)
        lyt_grid_main.addWidget(label_setting03, 4, 0, 1, 2)
        lyt_grid_main.addWidget(self.listArea_visibility03, 5, 0)
        lyt_grid_main.addLayout(lyt_vBox_setting03, 5, 1)
        lyt_grid_main.addWidget(button_hidden, 6, 0, 1, 2)
        lyt_grid_main.addWidget(button_visible, 7, 0, 1, 2)

        lyt_widget = QtWidgets.QWidget()
        lyt_widget.setLayout(lyt_grid_main)
        self.setCentralWidget(lyt_widget)


    def initialize_settings(self):
        self.objectNames_setting01 = [] #非表示にするオブジェクト名、設定01用
        self.objectNames_setting02 = [] #非表示にするオブジェクト名、設定02用
        self.objectNames_setting03 = [] #非表示にするオブジェクト名、設定03用


    def register_objectNames(self):
        selected_objects = cmds.ls(sl = True)
        name_clickedButton = self.sender().objectName() #どのボタンをクリックしたか
        self.objectNames_setting01 = [self.listArea_visibility01.item(one_item).text() for one_item in range(self.listArea_visibility01.count())] #現在リストに表示中の項目
        self.objectNames_setting02 = [self.listArea_visibility02.item(one_item).text() for one_item in range(self.listArea_visibility02.count())]
        self.objectNames_setting03 = [self.listArea_visibility03.item(one_item).text() for one_item in range(self.listArea_visibility03.count())]

        if not selected_objects:
            cmds.confirmDialog(b = "OK", icn = 'critical', m = "何も選択されていません、登録に失敗しました。", t = "ERROR: Object Visibility Controller")
        else:
            for one_object in selected_objects:
                if one_object not in self.objectNames_setting01 and one_object not in self.objectNames_setting02 and one_object not in self.objectNames_setting03:
                    if name_clickedButton == "Register01":
                        self.objectNames_setting01.append(one_object) #全てのリストで未登録だった場合に追加

                    elif name_clickedButton == "Register02":
                        self.objectNames_setting02.append(one_object)

                    elif name_clickedButton == "Register03":
                        self.objectNames_setting03.append(one_object)
                else:
                    cmds.confirmDialog(b = "OK", icn = 'warning', m = f"{one_object}は既に登録済みのオブジェクトです。", t = "ERROR: Object Visibility Controller")
            else:
                self.listArea_visibility01.clear()
                self.listArea_visibility02.clear()
                self.listArea_visibility03.clear()
                self.listArea_visibility01.addItems(self.objectNames_setting01)
                self.listArea_visibility02.addItems(self.objectNames_setting02)
                self.listArea_visibility03.addItems(self.objectNames_setting03)


    def hidden_objectVisibility(self):
        checkBoxes_setting01 = [self.checkBox_persp01.isChecked(), self.checkBox_left01.isChecked(), self.checkBox_right01.isChecked(),
                                self.checkBox_front01.isChecked(), self.checkBox_top01.isChecked(), self.checkBox_bottom01.isChecked(), self.checkBox_back01.isChecked()] #チェック状態
        checkBoxes_setting02 = [self.checkBox_persp02.isChecked(), self.checkBox_left02.isChecked(), self.checkBox_right02.isChecked(),
                                self.checkBox_front02.isChecked(), self.checkBox_top02.isChecked(), self.checkBox_bottom02.isChecked(), self.checkBox_back02.isChecked()]
        checkBoxes_setting03 = [self.checkBox_persp03.isChecked(), self.checkBox_left03.isChecked(), self.checkBox_right03.isChecked(),
                                self.checkBox_front03.isChecked(), self.checkBox_top03.isChecked(), self.checkBox_bottom03.isChecked(), self.checkBox_back03.isChecked()]
        viewCameras = ['persp', 'left', 'side', 'front', 'top', 'bottom', 'back'] #ビュー用カメラ
        exist_cameras = cmds.listRelatives(cmds.ls(ca = True), p = True) #現在存在しているカメラ

        cmds.perCameraVisibility(ra = True) #全て表示

        for one_object in self.objectNames_setting01:
            for one_check01, one_camera in zip(checkBoxes_setting01, viewCameras):
                if one_check01 == True and one_camera in exist_cameras: #チェックが入っており、そのカメラが存在する場合
                    try:
                        cmds.perCameraVisibility(one_object, c = one_camera, hi = True) #非表示
                    except:
                        continue

        for one_object in self.objectNames_setting02:
            for one_check02, one_camera in zip(checkBoxes_setting02, viewCameras):
                if one_check02 == True and one_camera in exist_cameras:
                    try:
                        cmds.perCameraVisibility(one_object, c = one_camera, hi = True)
                    except:
                        continue

        for one_object in self.objectNames_setting03:
            for one_check03, one_camera in zip(checkBoxes_setting03, viewCameras):
                if one_check03 == True and one_camera in exist_cameras:
                    try:
                        cmds.perCameraVisibility(one_object, c = one_camera, hi = True)
                    except:
                        continue
    

    def visible_objectVisibility(self):
        cmds.perCameraVisibility(ra = True)


    def clear_objectNames(self):
        name_clickedButton = self.sender().objectName()

        if name_clickedButton == "Clear01":
            self.listArea_visibility01.clear()
            self.objectNames_setting01.clear()
        
        elif name_clickedButton == "Clear02":
            self.listArea_visibility02.clear()
            self.objectNames_setting02.clear()
        
        elif name_clickedButton == "Clear03":
            self.listArea_visibility03.clear()
            self.objectNames_setting03.clear()


    def exclusion_objectNames(self):
        selected_items01 = self.listArea_visibility01.selectedItems() #選択中の項目
        selected_items02 = self.listArea_visibility02.selectedItems()
        selected_items03 = self.listArea_visibility03.selectedItems()
        name_clickedButton = self.sender().objectName()

        if name_clickedButton == "Exclusion01":
            for one_item in selected_items01:
                self.listArea_visibility01.takeItem(self.listArea_visibility01.row(one_item))
            else:
                self.objectNames_setting01 = [self.listArea_visibility01.item(one_item).text() for one_item in range(self.listArea_visibility01.count())]
        
        elif name_clickedButton == "Exclusion02":
            for one_item in selected_items02:
                self.listArea_visibility02.takeItem(self.listArea_visibility02.row(one_item))
            else:
                self.objectNames_setting02 = [self.listArea_visibility02.item(one_item).text() for one_item in range(self.listArea_visibility02.count())]
        
        elif name_clickedButton == "Exclusion03":
            for one_item in selected_items03:
                self.listArea_visibility03.takeItem(self.listArea_visibility03.row(one_item))
            else:
                self.objectNames_setting03 = [self.listArea_visibility03.item(one_item).text() for one_item in range(self.listArea_visibility03.count())]


    def closeEvent(self, event):
        cmds.perCameraVisibility(ra = True)


toolWindow = ObjectVisibilityController()
toolWindow.show()
