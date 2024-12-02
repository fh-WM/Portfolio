#For Autodesk Maya 2024, Encoding UTF-8
import maya.cmds as cmds
import math
from PySide2 import QtWidgets
from PySide2 import QtCore
from maya.app.general import mayaMixin

class SurroundCameraSetupTool(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    def __init__(self):
        super(SurroundCameraSetupTool, self).__init__()
        self.toolUI()


    def toolUI(self):
        self.setGeometry(500, 300, 450, 250)
        self.setWindowTitle("Surround Camera Setup Tool")
        self.statusBar().showMessage("Last Updated: 2024.11.21   |   For: Maya 2024   |   Fuma Hara")

        label_methodSelect = QtWidgets.QLabel("配置するカメラ")
        label_placementNum = QtWidgets.QLabel("配置台数")
        label_placementRadius = QtWidgets.QLabel("配置半径")
        label_cameraName = QtWidgets.QLabel("カメラ名")
        label_directionSelect = QtWidgets.QLabel("カメラの向き")
        label_centralPosition = QtWidgets.QLabel("中心座標(XYZ)")

        self.radioGroup_methodSelect = QtWidgets.QButtonGroup()
        radioButton_new = QtWidgets.QRadioButton("新規作成", self, checked = True)
        radioButton_duplicate = QtWidgets.QRadioButton("選択中のカメラを複製", self)
        self.radioGroup_methodSelect.addButton(radioButton_new, 1)
        self.radioGroup_methodSelect.addButton(radioButton_duplicate, 2)

        self.radioGroup_directionSelect = QtWidgets.QButtonGroup()
        radioButton_inward = QtWidgets.QRadioButton("内向き(中心方向)", self, checked = True)
        radioButton_outward = QtWidgets.QRadioButton("外向き(中心の反対方向)", self)
        self.radioGroup_directionSelect.addButton(radioButton_inward, 1)
        self.radioGroup_directionSelect.addButton(radioButton_outward, 2)

        self.spinBox_placementNum = QtWidgets.QSpinBox(minimum = 4, maximum = 100, value = 8)
        self.spinBox_placementRadius = QtWidgets.QDoubleSpinBox(minimum = 1, maximum = 100, value = 5)
        self.spinBox_cameraNameNum = QtWidgets.QSpinBox(minimum = 0, maximum = 999, value = 1)
        self.spinBox_centralPositionX = QtWidgets.QDoubleSpinBox(minimum = -500, maximum = 500, value = 0)
        self.spinBox_centralPositionY = QtWidgets.QDoubleSpinBox(minimum = -500, maximum = 500, value = 0)
        self.spinBox_centralPositionZ = QtWidgets.QDoubleSpinBox(minimum = -500, maximum = 500, value = 0)
        self.spinBox_placementNum.valueChanged.connect(self.change_spinBox_placementNum)
        self.spinBox_placementRadius.editingFinished.connect(self.change_spinBox_placementRadius) #編集状態が終了したら反応、小数点以下の入力指定がスムーズになる

        self.slider_placementNum = QtWidgets.QSlider(QtCore.Qt.Horizontal, minimum = 4, maximum = 100, value = 8)
        self.slider_placementRadius = QtWidgets.QSlider(QtCore.Qt.Horizontal, minimum = 100, maximum = 10000, value = 5)
        self.slider_placementNum.valueChanged.connect(self.change_slider_placementNum)
        self.slider_placementRadius.valueChanged.connect(self.change_slider_placementRadius)

        self.txtLine_cameraName = QtWidgets.QLineEdit(placeholderText = "配置するカメラの名前を入力")

        self.checkBox_group = QtWidgets.QCheckBox("配置後グループにまとめる", checked = True)

        button_setup = QtWidgets.QPushButton("配置")
        button_setup.clicked.connect(self.setup_surroundCamera)

        lyt_hBox_methodSelect = QtWidgets.QHBoxLayout() #配置するカメラ用
        lyt_hBox_methodSelect.addWidget(radioButton_new)
        lyt_hBox_methodSelect.addWidget(radioButton_duplicate)

        lyt_hBox_placementNum = QtWidgets.QHBoxLayout() #配置台数用
        lyt_hBox_placementNum.addWidget(self.spinBox_placementNum, 1)
        lyt_hBox_placementNum.addWidget(self.slider_placementNum, 4)

        lyt_hBox_placementRadius = QtWidgets.QHBoxLayout() #配置半径用
        lyt_hBox_placementRadius.addWidget(self.spinBox_placementRadius, 1)
        lyt_hBox_placementRadius.addWidget(self.slider_placementRadius, 4)

        lyt_hBox_directionSelect = QtWidgets.QHBoxLayout() #カメラの向き用
        lyt_hBox_directionSelect.addWidget(radioButton_inward)
        lyt_hBox_directionSelect.addWidget(radioButton_outward)

        lyt_hBox_cameraName = QtWidgets.QHBoxLayout() #カメラ名用
        lyt_hBox_cameraName.addWidget(self.txtLine_cameraName, 4)
        lyt_hBox_cameraName.addWidget(self.spinBox_cameraNameNum, 1)

        lyt_hBox_centralPosition = QtWidgets.QHBoxLayout() #中心座標用
        lyt_hBox_centralPosition.addWidget(self.spinBox_centralPositionX)
        lyt_hBox_centralPosition.addWidget(self.spinBox_centralPositionY)
        lyt_hBox_centralPosition.addWidget(self.spinBox_centralPositionZ)

        lyt_grid_main = QtWidgets.QGridLayout()
        lyt_grid_main.addWidget(label_methodSelect, 0, 0)
        lyt_grid_main.addLayout(lyt_hBox_methodSelect, 0, 1)
        lyt_grid_main.addWidget(label_placementNum, 1, 0)
        lyt_grid_main.addLayout(lyt_hBox_placementNum, 1, 1)
        lyt_grid_main.addWidget(label_placementRadius, 2, 0)
        lyt_grid_main.addLayout(lyt_hBox_placementRadius, 2, 1)
        lyt_grid_main.addWidget(label_directionSelect, 3, 0)
        lyt_grid_main.addLayout(lyt_hBox_directionSelect, 3, 1)
        lyt_grid_main.addWidget(label_cameraName, 4, 0)
        lyt_grid_main.addLayout(lyt_hBox_cameraName, 4, 1)
        lyt_grid_main.addWidget(label_centralPosition, 5, 0)
        lyt_grid_main.addLayout(lyt_hBox_centralPosition, 5, 1)

        lyt_vBox_main = QtWidgets.QVBoxLayout()
        lyt_vBox_main.addLayout(lyt_grid_main)
        lyt_vBox_main.addWidget(self.checkBox_group)
        lyt_vBox_main.addWidget(button_setup)

        lyt_widget = QtWidgets.QWidget()
        lyt_widget.setLayout(lyt_vBox_main)
        self.setCentralWidget(lyt_widget)


    def setup_surroundCamera(self):
        num_placement = self.spinBox_placementNum.value() #配置台数
        radius_placement = self.spinBox_placementRadius.value() #配置半径
        name_surroundCamera = self.txtLine_cameraName.text() #カメラ名
        num_surroundCamera = self.spinBox_cameraNameNum.value() #カメラ名末尾の番号
        num_centralPositionX = self.spinBox_centralPositionX.value() #中心座標X
        num_centralPositionY = self.spinBox_centralPositionY.value() #Y
        num_centralPositionZ = self.spinBox_centralPositionZ.value() #Z
        selected_camera = cmds.ls(sl = True)
        angle_camera = 90 #最初に配置するカメラの角度
        placed_cameras = [] #配置済みのカメラ

        if self.radioGroup_methodSelect.checkedId() == 2 and not selected_camera:
            cmds.confirmDialog(b = "OK", icn = 'critical', m = "何も選択されていません、配置に失敗しました。", t = "ERROR: Surround Camera Setup Tool")

        elif self.radioGroup_methodSelect.checkedId() == 2 and len(selected_camera) > 1:
            cmds.confirmDialog(b = "OK", icn = 'critical', m = "選択は必ず1つに絞ってください、配置に失敗しました。", t = "ERROR: Surround Camera Setup Tool")

        elif self.radioGroup_methodSelect.checkedId() == 1 or len(selected_camera) == 1 and cmds.nodeType(cmds.listRelatives(selected_camera[0], f = True, s = True)) == 'camera':
            if self.txtLine_cameraName.text() == "":
                name_surroundCamera = "SurroundCamera"

                if self.radioGroup_methodSelect.checkedId() == 2:
                    name_surroundCamera = f"{name_surroundCamera}_{selected_camera[0]}" #カメラ名未指定 & カメラ複製

            if self.radioGroup_directionSelect.checkedId() == 2: #外向きのカメラ
                angle_camera = -90

            for one_num in range(num_placement):
                angle = 2 * math.pi * one_num / num_placement
                location_x = radius_placement * math.cos(angle)
                location_z = radius_placement * math.sin(angle)

                if self.radioGroup_methodSelect.checkedId() == 2:
                    surround_camera = cmds.duplicate(selected_camera[0], n = name_surroundCamera) #複製
                else:
                    surround_camera = cmds.camera(n = f"{name_surroundCamera}{num_surroundCamera + one_num}") #新規作成

                cmds.move(location_x, 0, location_z, surround_camera)
                cmds.rotate(angle_camera, surround_camera, y = True) #カメラを中央に向ける
                placed_cameras.append(surround_camera[0])
                angle_camera -= 360 / num_placement
            else:
                group_surroundCameras = cmds.group(placed_cameras, n = f"cams_{name_surroundCamera}")
                cmds.rotate(-90, group_surroundCameras, y = True) #1番目のカメラが正面に来るように回転
                cmds.move(num_centralPositionX, num_centralPositionY, num_centralPositionZ, group_surroundCameras)
                cmds.select(group_surroundCameras)

                if self.checkBox_group.isChecked() == False:
                    cmds.ungroup() #グループ化を解除
                    cmds.select(placed_cameras)

                cmds.rename(placed_cameras[0], f"{name_surroundCamera}{num_surroundCamera}") #一番最初に作成したカメラは必ず末尾番号が置き換えられてしまうため、正しい名称にリネーム
        else:
            cmds.confirmDialog(b = "OK", icn = 'critical', m = "カメラではないオブジェクトが選択されています、配置に失敗しました。", t = "ERROR: Surround Camera Setup Tool")
    

    def change_spinBox_placementNum(self):
        value_spinBox_placementNum = self.spinBox_placementNum.value()
        self.slider_placementNum.setValue(value_spinBox_placementNum)
    

    def change_spinBox_placementRadius(self):
        value_spinBox_placementRadius = self.spinBox_placementRadius.value() * 100
        self.slider_placementRadius.setValue(value_spinBox_placementRadius)
    

    def change_slider_placementNum(self):
        value_slider_placementNum = self.slider_placementNum.value()
        self.spinBox_placementNum.setValue(value_slider_placementNum)
    

    def change_slider_placementRadius(self):
        value_slider_placementRadius = self.slider_placementRadius.value() / 100
        self.spinBox_placementRadius.setValue(value_slider_placementRadius)


toolWindow = SurroundCameraSetupTool()
toolWindow.show()
