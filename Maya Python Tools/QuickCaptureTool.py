#For Autodesk Maya 2024, Encoding UTF-8
import maya.cmds as cmds
import datetime
import os
import platform
import subprocess
from PySide2 import QtWidgets
from PySide2 import QtCore
from maya.app.general import mayaMixin

class QuickCaptureTool(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    def __init__(self):
        super(QuickCaptureTool, self).__init__()
        self.toolUI()
        self.initialize_settings()


    def toolUI(self):
        self.setGeometry(500, 300, 490, 500)
        self.setWindowTitle("Quick Capture Tool")
        self.statusBar().showMessage("Last Updated: 2024.11.22   |   For: Maya 2024   |   Fuma Hara")

        label_fileName = QtWidgets.QLabel("ファイル名")
        label_filePath = QtWidgets.QLabel("保存先")
        label_fileFormat = QtWidgets.QLabel("ファイル形式", alignment = QtCore.Qt.AlignTop)
        label_displayMode = QtWidgets.QLabel("表示モード設定")
        label_lights = QtWidgets.QLabel("ライト設定")
        label_cameras = QtWidgets.QLabel("キャプチャを行うカメラ", alignment = QtCore.Qt.AlignTop)
        label_options = QtWidgets.QLabel("キャプチャに含める要素")

        self.txtLine_fileName = QtWidgets.QLineEdit(placeholderText = "ファイル名を入力", text = "「maya_年月日_時分秒_カメラ名」になります", enabled = False)
        self.txtLine_filePath = QtWidgets.QLineEdit(placeholderText = "保存先を入力")

        self.comboBox_fileName = QtWidgets.QComboBox(fixedWidth = 100)
        self.comboBox_filePath = QtWidgets.QComboBox(fixedWidth = 100)
        self.comboBox_displayMode = QtWidgets.QComboBox()
        self.comboBox_lights = QtWidgets.QComboBox()
        self.comboBox_fileName.addItems(["自動", "入力指定", "入力 & 連番"])
        self.comboBox_filePath.addItems(["入力指定", "デスクトップ", "ドキュメント", "ピクチャ"])
        self.comboBox_displayMode.addItems(["現在の表示モード", "ワイヤーフレーム (4番表示)", "スムースシェーディング (5番表示)",
                                            "スムースシェーディング & テクスチャ (6番表示)", "フラットシェーディング"])
        self.comboBox_lights.addItems(["現在のライト", "デフォルト", "全て表示", "全て非表示"])
        self.comboBox_fileName.currentIndexChanged.connect(self.change_comboBox_fileName)
        self.comboBox_filePath.currentIndexChanged.connect(self.change_comboBox_filePath)

        self.radioGroup_fileFormat = QtWidgets.QButtonGroup()
        radioButton_jpg = QtWidgets.QRadioButton("JPEG", self, checked = True)
        radioButton_png = QtWidgets.QRadioButton("PNG", self)
        radioButton_tif = QtWidgets.QRadioButton("TIFF", self)
        radioButton_webp = QtWidgets.QRadioButton("WebP", self)
        radioButton_heif = QtWidgets.QRadioButton("HEIF", self)
        radioButton_gif = QtWidgets.QRadioButton("GIF", self)
        radioButton_bmp = QtWidgets.QRadioButton("BMP", self)
        self.radioGroup_fileFormat.addButton(radioButton_jpg, 1)
        self.radioGroup_fileFormat.addButton(radioButton_png, 2)
        self.radioGroup_fileFormat.addButton(radioButton_tif, 3)
        self.radioGroup_fileFormat.addButton(radioButton_webp, 4)
        self.radioGroup_fileFormat.addButton(radioButton_heif, 5)
        self.radioGroup_fileFormat.addButton(radioButton_gif, 6)
        self.radioGroup_fileFormat.addButton(radioButton_bmp, 7)

        self.listArea_cameras = QtWidgets.QListWidget(selectionMode = QtWidgets.QAbstractItemView.ExtendedSelection) #Shift/Ctrlによる複数選択を有効化

        self.checkBox_defaultCamera = QtWidgets.QCheckBox("デフォルトの\nカメラを含める", checked = True)
        self.checkBox_hud = QtWidgets.QCheckBox("HUD", checked = True)
        self.checkBox_grid = QtWidgets.QCheckBox("グリッド", checked = True)
        self.checkBox_imagePlane = QtWidgets.QCheckBox("イメージプレーン", checked = True)
        self.checkBox_autoOpen = QtWidgets.QCheckBox("キャプチャ終了後に保存先を自動で開く", checked = True)

        button_register = QtWidgets.QPushButton("登録")
        button_exclusion = QtWidgets.QPushButton("除外")
        button_clear = QtWidgets.QPushButton("クリア")
        button_redetection = QtWidgets.QPushButton("再検出")
        button_capture = QtWidgets.QPushButton("キャプチャ")
        button_openDialog = QtWidgets.QPushButton("ダイアログボックスを開く")
        button_openExplorer = QtWidgets.QPushButton("エクスプローラー/Finderを開く")
        button_register.clicked.connect(self.register_cameras)
        button_exclusion.clicked.connect(self.exclusion_cameras)
        button_clear.clicked.connect(self.clear_cameras)
        button_redetection.clicked.connect(self.redetection_cameras)
        button_capture.clicked.connect(self.capture_viewport)
        button_openDialog.clicked.connect(self.open_dialog)
        button_openExplorer.clicked.connect(self.open_explorer)

        spacer_buttonLayout = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding) #伸縮可能なスペーサー

        lyt_hBox_fileName = QtWidgets.QHBoxLayout() #ファイル名用
        lyt_hBox_fileName.addWidget(self.comboBox_fileName)
        lyt_hBox_fileName.addWidget(self.txtLine_fileName)

        lyt_hBox_filePath = QtWidgets.QHBoxLayout() #保存先用
        lyt_hBox_filePath.addWidget(self.comboBox_filePath)
        lyt_hBox_filePath.addWidget(self.txtLine_filePath)

        lyt_grid_fileFormat = QtWidgets.QGridLayout() #ファイル形式用
        lyt_grid_fileFormat.addWidget(radioButton_jpg, 0, 0)
        lyt_grid_fileFormat.addWidget(radioButton_png, 0, 1)
        lyt_grid_fileFormat.addWidget(radioButton_tif, 0, 2)
        lyt_grid_fileFormat.addWidget(radioButton_webp, 0, 3)
        lyt_grid_fileFormat.addWidget(radioButton_heif, 1, 0)
        lyt_grid_fileFormat.addWidget(radioButton_gif, 1, 1)
        lyt_grid_fileFormat.addWidget(radioButton_bmp, 1, 2)

        lyt_vBox_button = QtWidgets.QVBoxLayout() #カメラ名リスト横ボタン用
        lyt_vBox_button.addWidget(button_register)
        lyt_vBox_button.addWidget(button_exclusion)
        lyt_vBox_button.addWidget(button_clear)
        lyt_vBox_button.addWidget(button_redetection)
        lyt_vBox_button.addWidget(self.checkBox_defaultCamera)
        lyt_vBox_button.addItem(spacer_buttonLayout)

        lyt_hBox_cameras = QtWidgets.QHBoxLayout() #カメラ名用
        lyt_hBox_cameras.addWidget(self.listArea_cameras, 3)
        lyt_hBox_cameras.addLayout(lyt_vBox_button, 1)

        lyt_hBox_options = QtWidgets.QHBoxLayout() #キャプチャに含める要素用
        lyt_hBox_options.addWidget(self.checkBox_hud)
        lyt_hBox_options.addWidget(self.checkBox_grid)
        lyt_hBox_options.addWidget(self.checkBox_imagePlane)

        lyt_hBox_button = QtWidgets.QHBoxLayout() #最下部ボタン用
        lyt_hBox_button.addWidget(button_openDialog)
        lyt_hBox_button.addWidget(button_openExplorer)

        lyt_grid_main = QtWidgets.QGridLayout()
        lyt_grid_main.addWidget(label_fileName, 0, 0)
        lyt_grid_main.addLayout(lyt_hBox_fileName, 0, 1)
        lyt_grid_main.addWidget(label_filePath, 1, 0)
        lyt_grid_main.addLayout(lyt_hBox_filePath, 1, 1)
        lyt_grid_main.addWidget(label_fileFormat, 2, 0)
        lyt_grid_main.addLayout(lyt_grid_fileFormat, 2, 1)
        lyt_grid_main.addWidget(label_displayMode, 3, 0)
        lyt_grid_main.addWidget(self.comboBox_displayMode, 3, 1)
        lyt_grid_main.addWidget(label_lights, 4, 0)
        lyt_grid_main.addWidget(self.comboBox_lights, 4, 1)
        lyt_grid_main.addWidget(label_cameras, 5, 0)
        lyt_grid_main.addLayout(lyt_hBox_cameras, 5, 1)
        lyt_grid_main.addWidget(label_options, 6, 0)
        lyt_grid_main.addLayout(lyt_hBox_options, 6, 1)

        lyt_vBox_main = QtWidgets.QVBoxLayout()
        lyt_vBox_main.addLayout(lyt_grid_main)
        lyt_vBox_main.addWidget(self.checkBox_autoOpen)
        lyt_vBox_main.addWidget(button_capture)
        lyt_vBox_main.addLayout(lyt_hBox_button)

        lyt_widget = QtWidgets.QWidget()
        lyt_widget.setLayout(lyt_vBox_main)
        self.setCentralWidget(lyt_widget)


    def initialize_settings(self):
        self.name_os = platform.system() #使用中のOS
        self.filePath_desktop = os.path.expanduser('~/Desktop') #デスクトップのファイルパス
        self.filePath_documents = os.path.expanduser('~/Documents') #ドキュメントのファイルパス
        self.filePath_pictures = os.path.expanduser('~/Pictures') #ピクチャのファイルパス
        self.listArea_cameras.addItems(cmds.listRelatives(cmds.ls(typ = 'camera'), p = True)) #ツール起動時に存在しているカメラ
        self.cameras_toBeCapture = [] #キャプチャを行うカメラ


    def register_cameras(self):
        selected_cameras = cmds.ls(sl = True)
        self.cameras_toBeCapture = [self.listArea_cameras.item(one_camera).text() for one_camera in range(self.listArea_cameras.count())] #リストに表示中の項目を取得

        if not selected_cameras:
            cmds.confirmDialog(b = "OK", icn = 'critical', m = "何も選択されていません、登録に失敗しました。", t = "ERROR: Quick Capture Tool")
        else:
            for one_camera in selected_cameras:
                if one_camera not in self.cameras_toBeCapture and cmds.nodeType(cmds.listRelatives(one_camera, f = True, s = True)) == 'camera':
                    self.cameras_toBeCapture.append(one_camera) #登録済みではなく、カメラであれば追加
            else:
                self.listArea_cameras.clear()
                self.listArea_cameras.addItems(self.cameras_toBeCapture)


    def capture_viewport(self):
        text_fileName = self.txtLine_fileName.text() #ファイル名
        text_filePath = self.txtLine_filePath.text() #保存先
        now_datetime = datetime.datetime.now() #現在の日時
        self.cameras_toBeCapture = [self.listArea_cameras.item(one_camera).text() for one_camera in range(self.listArea_cameras.count())]
        num_count = 0

        current_camera = cmds.modelEditor('modelPanel4', q = True, cam = True) #現在のカメラ
        current_displayMode = cmds.modelEditor('modelPanel4', q = True, da = True) #現在の表示モード
        current_lights = cmds.modelEditor('modelPanel4', q = True, dl = True) #現在のライト
        current_texture = cmds.modelEditor('modelPanel4', q = True, dtx = True) #現在のテクスチャ表示
        current_hud = cmds.modelEditor('modelPanel4', q = True, hud = True) #現在のHUD表示
        current_grid = cmds.modelEditor('modelPanel4', q = True, gr = True) #現在のグリッド表示
        current_imagePlane = cmds.modelEditor('modelPanel4', q = True, imp = True) #現在のイメージプレーン表示

        type_fileFormat = ["", ".jpg", ".png", ".tif", ".webp", ".heif", ".gif", ".bmp"]
        type_displayMode = [current_displayMode, 'wireframe', "smoothShaded", "smoothShaded", "flatShaded"]
        type_lights = [current_lights, "default", "all", "none"]
        type_texture = [current_texture, False, False, True, False]

        if not self.cameras_toBeCapture:
            cmds.confirmDialog(b = "OK", icn = 'critical', m = "カメラが登録されていません、キャプチャに失敗しました。", t = "ERROR: Quick Capture Tool")

        elif self.comboBox_fileName.currentIndex() == 1 and self.txtLine_fileName.text() == "":
            cmds.confirmDialog(b = "OK", icn = 'critical', m = "ファイル名が指定されていません、キャプチャに失敗しました。", t = "ERROR: Quick Capture Tool")

        elif self.comboBox_filePath.currentIndex() == 0 and self.txtLine_filePath.text() == "":
            cmds.confirmDialog(b = "OK", icn = 'critical', m = "保存先が指定されていません、キャプチャに失敗しました。", t = "ERROR: Quick Capture Tool")

        else:
            if self.comboBox_fileName.currentIndex() == 0: #自動
                text_fileName = f"maya_{now_datetime.year}{now_datetime.month:02d}{now_datetime.day:02d}_{now_datetime.hour:02d}{now_datetime.minute:02d}{now_datetime.second:02d}"

            for one_camera in self.cameras_toBeCapture:
                cmds.modelEditor('modelPanel4', e = True, cam = one_camera, da = type_displayMode[self.comboBox_displayMode.currentIndex()],
                                dl = type_lights[self.comboBox_lights.currentIndex()], dtx = type_texture[self.comboBox_displayMode.currentIndex()],
                                hud = self.checkBox_hud.isChecked(), gr = self.checkBox_grid.isChecked(), imp = self.checkBox_imagePlane.isChecked()) #撮影用に設定反映
                
                if self.comboBox_fileName.currentIndex() == 2:
                    cmds.refresh(fn = f"{text_filePath}/{text_fileName}_{num_count}{type_fileFormat[self.radioGroup_fileFormat.checkedId()]}") #撮影、入力&連番
                    num_count += 1
                else:
                    cmds.refresh(fn = f"{text_filePath}/{text_fileName}_{one_camera}{type_fileFormat[self.radioGroup_fileFormat.checkedId()]}") #撮影
            else:
                cmds.modelEditor('modelPanel4', e = True, cam = current_camera, da = current_displayMode, dl = current_lights, dtx = current_texture,
                                hud = current_hud, gr = current_grid, imp = current_imagePlane) #元に戻す
                
                if self.checkBox_autoOpen.isChecked() == True:
                    if self.name_os == "Windows":
                        os.startfile(text_filePath)

                    elif self.name_os == "Darwin":
                        subprocess.Popen(['open', text_filePath])
    

    def exclusion_cameras(self):
        selected_items = self.listArea_cameras.selectedItems()

        for one_item in selected_items:
            self.listArea_cameras.takeItem((self.listArea_cameras.row(one_item)))
    

    def clear_cameras(self):
        self.cameras_toBeCapture.clear()
        self.listArea_cameras.clear()


    def redetection_cameras(self):
        self.listArea_cameras.clear()
        cameras_exist = cmds.listRelatives(cmds.ls(typ = 'camera'), p = True)
        
        if self.checkBox_defaultCamera.isChecked() == False:
            self.listArea_cameras.addItems([one_camera for one_camera in cameras_exist if one_camera != 'persp' and
                                            one_camera != 'front' and one_camera != 'top' and one_camera != 'side' and
                                            one_camera != 'back' and one_camera != 'bottom' and one_camera != 'left']) #デフォルトのカメラを検出結果に含めない
        else:
            self.listArea_cameras.addItems(cameras_exist)
    

    def open_dialog(self):
        cmds.fileDialog2()
    

    def open_explorer(self):
        if self.name_os == "Windows":
            subprocess.Popen('explorer')

        elif self.name_os == "Darwin":
            subprocess.Popen(['open', '.'])
    

    def change_comboBox_fileName(self):
        if self.comboBox_fileName.currentIndex() == 0:
            self.txtLine_fileName.setEnabled(False)
            self.txtLine_fileName.setText("「maya_年月日_時分秒_カメラ名」になります")
        else:
            self.txtLine_fileName.setEnabled(True)
            self.txtLine_fileName.setFocus()
            self.txtLine_fileName.setText("")
    

    def change_comboBox_filePath(self):
        filePaths = ["", self.filePath_desktop, self.filePath_documents, self.filePath_pictures]

        if self.comboBox_filePath.currentIndex() == 0:
            self.txtLine_filePath.setEnabled(True)
            self.txtLine_filePath.setFocus()
        else:
            self.txtLine_filePath.setEnabled(False)
        
        self.txtLine_filePath.setText(filePaths[self.comboBox_filePath.currentIndex()])
    

toolWindow = QuickCaptureTool()
toolWindow.show()
