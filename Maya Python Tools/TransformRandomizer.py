#For Autodesk Maya 2024, Encoding UTF-8
import maya.cmds as cmds
import random
from PySide2 import QtWidgets
from PySide2 import QtCore
from maya.app.general import mayaMixin

class TransformRandomizer(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    def __init__(self):
        super(TransformRandomizer, self).__init__()
        self.toolUI()


    def toolUI(self):
        self.setGeometry(500, 300, 470, 550)
        self.setWindowTitle("Transform Randomizer")
        self.statusBar().showMessage("Last Updated: 2025.1.2   |   For: Maya 2024   |   Fuma Hara")

        label_move = QtWidgets.QLabel("<b>移動</b>")
        label_rotate = QtWidgets.QLabel("<b>回転</b>")
        label_scale = QtWidgets.QLabel("<b>スケール</b>")

        label_moveMethod = QtWidgets.QLabel("値の基準空間")
        label_rotateMethod = QtWidgets.QLabel("値の基準空間")
        label_scaleMethod = QtWidgets.QLabel("値の基準空間")

        label_moveX = QtWidgets.QLabel("ランダムの範囲   X", alignment = QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label_moveY = QtWidgets.QLabel("Y", alignment = QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label_moveZ = QtWidgets.QLabel("Z", alignment = QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label_rotateX = QtWidgets.QLabel("ランダムの範囲   X", alignment = QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label_rotateY = QtWidgets.QLabel("Y", alignment = QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label_rotateZ = QtWidgets.QLabel("Z", alignment = QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label_scaleX = QtWidgets.QLabel("ランダムの範囲   X", alignment = QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label_scaleY = QtWidgets.QLabel("Y", alignment = QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label_scaleZ = QtWidgets.QLabel("Z", alignment = QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        label_moveZero = QtWidgets.QLabel("ゼロ")
        label_rotateZero = QtWidgets.QLabel("ゼロ")
        label_scaleOne = QtWidgets.QLabel("イチ")

        label_moveMin = QtWidgets.QLabel("  最小値")
        label_moveMax = QtWidgets.QLabel(" 最大値")
        label_rotateMin = QtWidgets.QLabel("  最小値")
        label_rotateMax = QtWidgets.QLabel(" 最大値")
        label_scaleMin = QtWidgets.QLabel("  最小値")
        label_scaleMax = QtWidgets.QLabel(" 最大値")

        self.radioGroup_moveMethodSelect = QtWidgets.QButtonGroup()
        radioButton_moveWorld = QtWidgets.QRadioButton("World", self, checked = True)
        radioButton_moveRelative = QtWidgets.QRadioButton("Relative", self)
        self.radioGroup_moveMethodSelect.addButton(radioButton_moveWorld, 1)
        self.radioGroup_moveMethodSelect.addButton(radioButton_moveRelative, 2)

        self.radioGroup_rotateMethodSelect = QtWidgets.QButtonGroup()
        radioButton_rotateWorld = QtWidgets.QRadioButton("World", self, checked = True)
        radioButton_rotateRelative = QtWidgets.QRadioButton("Relative", self)
        self.radioGroup_rotateMethodSelect.addButton(radioButton_rotateWorld, 1)
        self.radioGroup_rotateMethodSelect.addButton(radioButton_rotateRelative, 2)

        self.radioGroup_scaleMethodSelect = QtWidgets.QButtonGroup()
        radioButton_scaleObject = QtWidgets.QRadioButton("Object", self, checked = True)
        radioButton_scaleRelative = QtWidgets.QRadioButton("Relative", self)
        self.radioGroup_scaleMethodSelect.addButton(radioButton_scaleObject, 1)
        self.radioGroup_scaleMethodSelect.addButton(radioButton_scaleRelative, 2)

        self.checkBox_moveZeroX = QtWidgets.QCheckBox(objectName = "Zero_MoveX")
        self.checkBox_moveZeroY = QtWidgets.QCheckBox(objectName = "Zero_MoveY")
        self.checkBox_moveZeroZ = QtWidgets.QCheckBox(objectName = "Zero_MoveZ")
        self.checkBox_sameMoveXYZ = QtWidgets.QCheckBox("XYZまとめて変更", objectName = "Same_MoveXYZ")
        self.checkBox_equalMoveXYZ = QtWidgets.QCheckBox("XYZ同じ値を適用", enabled = False)
        self.checkBox_rotateZeroX = QtWidgets.QCheckBox(objectName = "Zero_RotateX")
        self.checkBox_rotateZeroY = QtWidgets.QCheckBox(objectName = "Zero_RotateY")
        self.checkBox_rotateZeroZ = QtWidgets.QCheckBox(objectName = "Zero_RotateZ")
        self.checkBox_sameRotateXYZ = QtWidgets.QCheckBox("XYZまとめて変更", objectName = "Same_RotateXYZ")
        self.checkBox_equalRotateXYZ = QtWidgets.QCheckBox("XYZ同じ値を適用", enabled = False)
        self.checkBox_scaleOneX = QtWidgets.QCheckBox(objectName = "One_ScaleX")
        self.checkBox_scaleOneY = QtWidgets.QCheckBox(objectName = "One_ScaleY")
        self.checkBox_scaleOneZ = QtWidgets.QCheckBox(objectName = "One_ScaleZ")
        self.checkBox_sameScaleXYZ = QtWidgets.QCheckBox("XYZまとめて変更", objectName = "Same_ScaleXYZ")
        self.checkBox_equalScaleXYZ = QtWidgets.QCheckBox("XYZ同じ値を適用", enabled = False)
        self.checkBox_moveZeroX.stateChanged.connect(self.changed_checkBox_zeroOne)
        self.checkBox_moveZeroY.stateChanged.connect(self.changed_checkBox_zeroOne)
        self.checkBox_moveZeroZ.stateChanged.connect(self.changed_checkBox_zeroOne)
        self.checkBox_rotateZeroX.stateChanged.connect(self.changed_checkBox_zeroOne)
        self.checkBox_rotateZeroY.stateChanged.connect(self.changed_checkBox_zeroOne)
        self.checkBox_rotateZeroZ.stateChanged.connect(self.changed_checkBox_zeroOne)
        self.checkBox_scaleOneX.stateChanged.connect(self.changed_checkBox_zeroOne)
        self.checkBox_scaleOneY.stateChanged.connect(self.changed_checkBox_zeroOne)
        self.checkBox_scaleOneZ.stateChanged.connect(self.changed_checkBox_zeroOne)
        self.checkBox_sameMoveXYZ.stateChanged.connect(self.changed_checkBox_sameXYZ)
        self.checkBox_sameRotateXYZ.stateChanged.connect(self.changed_checkBox_sameXYZ)
        self.checkBox_sameScaleXYZ.stateChanged.connect(self.changed_checkBox_sameXYZ)

        self.spinBox_moveMinX = QtWidgets.QDoubleSpinBox(minimum = -500, maximum = 0, value = 0, fixedWidth = 80, objectName = "Sb_MoveMinX")
        self.spinBox_moveMaxX = QtWidgets.QDoubleSpinBox(minimum = 0, maximum = 500, value = 0, fixedWidth = 80, objectName = "Sb_MoveMaxX")
        self.spinBox_moveMinY = QtWidgets.QDoubleSpinBox(minimum = -500, maximum = 0, value = 0, fixedWidth = 80, objectName = "Sb_MoveMinY")
        self.spinBox_moveMaxY = QtWidgets.QDoubleSpinBox(minimum = 0, maximum = 500, value = 0, fixedWidth = 80, objectName = "Sb_MoveMaxY")
        self.spinBox_moveMinZ = QtWidgets.QDoubleSpinBox(minimum = -500, maximum = 0, value = 0, fixedWidth = 80, objectName = "Sb_MoveMinZ")
        self.spinBox_moveMaxZ = QtWidgets.QDoubleSpinBox(minimum = 0, maximum = 500, value = 0, fixedWidth = 80, objectName = "Sb_MoveMaxZ")
        self.spinBox_moveMinX.editingFinished.connect(self.valueUpdate_spinBoxToSlider)
        self.spinBox_moveMaxX.editingFinished.connect(self.valueUpdate_spinBoxToSlider)
        self.spinBox_moveMinY.editingFinished.connect(self.valueUpdate_spinBoxToSlider)
        self.spinBox_moveMaxY.editingFinished.connect(self.valueUpdate_spinBoxToSlider)
        self.spinBox_moveMinZ.editingFinished.connect(self.valueUpdate_spinBoxToSlider)
        self.spinBox_moveMaxZ.editingFinished.connect(self.valueUpdate_spinBoxToSlider)

        self.spinBox_rotateMinX = QtWidgets.QDoubleSpinBox(minimum = -180, maximum = 0, value = 0, fixedWidth = 80, objectName = "Sb_RotateMinX")
        self.spinBox_rotateMaxX = QtWidgets.QDoubleSpinBox(minimum = 0, maximum = 180, value = 0, fixedWidth = 80, objectName = "Sb_RotateMaxX")
        self.spinBox_rotateMinY = QtWidgets.QDoubleSpinBox(minimum = -180, maximum = 0, value = 0, fixedWidth = 80, objectName = "Sb_RotateMinY")
        self.spinBox_rotateMaxY = QtWidgets.QDoubleSpinBox(minimum = 0, maximum = 180, value = 0, fixedWidth = 80, objectName = "Sb_RotateMaxY")
        self.spinBox_rotateMinZ = QtWidgets.QDoubleSpinBox(minimum = -180, maximum = 0, value = 0, fixedWidth = 80, objectName = "Sb_RotateMinZ")
        self.spinBox_rotateMaxZ = QtWidgets.QDoubleSpinBox(minimum = 0, maximum = 180, value = 0, fixedWidth = 80, objectName = "Sb_RotateMaxZ")
        self.spinBox_rotateMinX.editingFinished.connect(self.valueUpdate_spinBoxToSlider)
        self.spinBox_rotateMaxX.editingFinished.connect(self.valueUpdate_spinBoxToSlider)
        self.spinBox_rotateMinY.editingFinished.connect(self.valueUpdate_spinBoxToSlider)
        self.spinBox_rotateMaxY.editingFinished.connect(self.valueUpdate_spinBoxToSlider)
        self.spinBox_rotateMinZ.editingFinished.connect(self.valueUpdate_spinBoxToSlider)
        self.spinBox_rotateMaxZ.editingFinished.connect(self.valueUpdate_spinBoxToSlider)

        self.spinBox_scaleMinX = QtWidgets.QDoubleSpinBox(minimum = 0.01, maximum = 1, value = 1, fixedWidth = 80, objectName = "Sb_ScaleMinX")
        self.spinBox_scaleMaxX = QtWidgets.QDoubleSpinBox(minimum = 1, maximum = 100, value = 1, fixedWidth = 80, objectName = "Sb_ScaleMaxX")
        self.spinBox_scaleMinY = QtWidgets.QDoubleSpinBox(minimum = 0.01, maximum = 1, value = 1, fixedWidth = 80, objectName = "Sb_ScaleMinY")
        self.spinBox_scaleMaxY = QtWidgets.QDoubleSpinBox(minimum = 1, maximum = 100, value = 1, fixedWidth = 80, objectName = "Sb_ScaleMaxY")
        self.spinBox_scaleMinZ = QtWidgets.QDoubleSpinBox(minimum = 0.01, maximum = 1, value = 1, fixedWidth = 80, objectName = "Sb_ScaleMinZ")
        self.spinBox_scaleMaxZ = QtWidgets.QDoubleSpinBox(minimum = 1, maximum = 100, value = 1, fixedWidth = 80, objectName = "Sb_ScaleMaxZ")
        self.spinBox_scaleMinX.editingFinished.connect(self.valueUpdate_spinBoxToSlider)
        self.spinBox_scaleMaxX.editingFinished.connect(self.valueUpdate_spinBoxToSlider)
        self.spinBox_scaleMinY.editingFinished.connect(self.valueUpdate_spinBoxToSlider)
        self.spinBox_scaleMaxY.editingFinished.connect(self.valueUpdate_spinBoxToSlider)
        self.spinBox_scaleMinZ.editingFinished.connect(self.valueUpdate_spinBoxToSlider)
        self.spinBox_scaleMaxZ.editingFinished.connect(self.valueUpdate_spinBoxToSlider)

        self.slider_moveMinX = QtWidgets.QSlider(QtCore.Qt.Horizontal, minimum = -50000, maximum = 0, value = 0, objectName = "Sli_MoveMinX")
        self.slider_moveMaxX = QtWidgets.QSlider(QtCore.Qt.Horizontal, minimum = 0, maximum = 50000, value = 0, objectName = "Sli_MoveMaxX")
        self.slider_moveMinY = QtWidgets.QSlider(QtCore.Qt.Horizontal, minimum = -50000, maximum = 0, value = 0, objectName = "Sli_MoveMinY")
        self.slider_moveMaxY = QtWidgets.QSlider(QtCore.Qt.Horizontal, minimum = 0, maximum = 50000, value = 0, objectName = "Sli_MoveMaxY")
        self.slider_moveMinZ = QtWidgets.QSlider(QtCore.Qt.Horizontal, minimum = -50000, maximum = 0, value = 0, objectName = "Sli_MoveMinZ")
        self.slider_moveMaxZ = QtWidgets.QSlider(QtCore.Qt.Horizontal, minimum = 0, maximum = 50000, value = 0, objectName = "Sli_MoveMaxZ")
        self.slider_moveMinX.valueChanged.connect(self.valueUpdate_sliderToSpinBox)
        self.slider_moveMaxX.valueChanged.connect(self.valueUpdate_sliderToSpinBox)
        self.slider_moveMinY.valueChanged.connect(self.valueUpdate_sliderToSpinBox)
        self.slider_moveMaxY.valueChanged.connect(self.valueUpdate_sliderToSpinBox)
        self.slider_moveMinZ.valueChanged.connect(self.valueUpdate_sliderToSpinBox)
        self.slider_moveMaxZ.valueChanged.connect(self.valueUpdate_sliderToSpinBox)

        self.slider_rotateMinX = QtWidgets.QSlider(QtCore.Qt.Horizontal, minimum = -18000, maximum = 0, value = 0, objectName = "Sli_RotateMinX")
        self.slider_rotateMaxX = QtWidgets.QSlider(QtCore.Qt.Horizontal, minimum = 0, maximum = 18000, value = 0, objectName = "Sli_RotateMaxX")
        self.slider_rotateMinY = QtWidgets.QSlider(QtCore.Qt.Horizontal, minimum = -18000, maximum = 0, value = 0, objectName = "Sli_RotateMinY")
        self.slider_rotateMaxY = QtWidgets.QSlider(QtCore.Qt.Horizontal, minimum = 0, maximum = 18000, value = 0, objectName = "Sli_RotateMaxY")
        self.slider_rotateMinZ = QtWidgets.QSlider(QtCore.Qt.Horizontal, minimum = -18000, maximum = 0, value = 0, objectName = "Sli_RotateMinZ")
        self.slider_rotateMaxZ = QtWidgets.QSlider(QtCore.Qt.Horizontal, minimum = 0, maximum = 18000, value = 0, objectName = "Sli_RotateMaxZ")
        self.slider_rotateMinX.valueChanged.connect(self.valueUpdate_sliderToSpinBox)
        self.slider_rotateMaxX.valueChanged.connect(self.valueUpdate_sliderToSpinBox)
        self.slider_rotateMinY.valueChanged.connect(self.valueUpdate_sliderToSpinBox)
        self.slider_rotateMaxY.valueChanged.connect(self.valueUpdate_sliderToSpinBox)
        self.slider_rotateMinZ.valueChanged.connect(self.valueUpdate_sliderToSpinBox)
        self.slider_rotateMaxZ.valueChanged.connect(self.valueUpdate_sliderToSpinBox)

        self.slider_scaleMinX = QtWidgets.QSlider(QtCore.Qt.Horizontal, minimum = 1, maximum = 100, value = 100, objectName = "Sli_ScaleMinX")
        self.slider_scaleMaxX = QtWidgets.QSlider(QtCore.Qt.Horizontal, minimum = 100, maximum = 10000, value = 100, objectName = "Sli_ScaleMaxX")
        self.slider_scaleMinY = QtWidgets.QSlider(QtCore.Qt.Horizontal, minimum = 1, maximum = 100, value = 100, objectName = "Sli_ScaleMinY")
        self.slider_scaleMaxY = QtWidgets.QSlider(QtCore.Qt.Horizontal, minimum = 100, maximum = 10000, value = 100, objectName = "Sli_ScaleMaxY")
        self.slider_scaleMinZ = QtWidgets.QSlider(QtCore.Qt.Horizontal, minimum = 1, maximum = 100, value = 100, objectName = "Sli_ScaleMinZ")
        self.slider_scaleMaxZ = QtWidgets.QSlider(QtCore.Qt.Horizontal, minimum = 100, maximum = 10000, value = 100, objectName = "Sli_ScaleMaxZ")
        self.slider_scaleMinX.valueChanged.connect(self.valueUpdate_sliderToSpinBox)
        self.slider_scaleMaxX.valueChanged.connect(self.valueUpdate_sliderToSpinBox)
        self.slider_scaleMinY.valueChanged.connect(self.valueUpdate_sliderToSpinBox)
        self.slider_scaleMaxY.valueChanged.connect(self.valueUpdate_sliderToSpinBox)
        self.slider_scaleMinZ.valueChanged.connect(self.valueUpdate_sliderToSpinBox)
        self.slider_scaleMaxZ.valueChanged.connect(self.valueUpdate_sliderToSpinBox)

        button_randomize = QtWidgets.QPushButton("適用")
        button_randomize.clicked.connect(self.randomize_objects)

        line_move = QtWidgets.QFrame(frameShape = QtWidgets.QFrame.HLine, frameShadow = QtWidgets.QFrame.Sunken)
        line_rotate = QtWidgets.QFrame(frameShape = QtWidgets.QFrame.HLine, frameShadow = QtWidgets.QFrame.Sunken)
        line_scale = QtWidgets.QFrame(frameShape = QtWidgets.QFrame.HLine, frameShadow = QtWidgets.QFrame.Sunken)

        lyt_form_moveHeader = QtWidgets.QFormLayout(fieldGrowthPolicy = QtWidgets.QFormLayout.AllNonFixedFieldsGrow) #移動の冒頭部
        lyt_form_moveHeader.addRow(label_move, line_move)

        lyt_hBox_moveMethod = QtWidgets.QHBoxLayout() #移動の基準空間用
        lyt_hBox_moveMethod.addWidget(radioButton_moveWorld)
        lyt_hBox_moveMethod.addWidget(radioButton_moveRelative)

        lyt_grid_moveSettings = QtWidgets.QGridLayout() #移動の設定用
        lyt_grid_moveSettings.addWidget(label_moveMethod, 0, 0)
        lyt_grid_moveSettings.addLayout(lyt_hBox_moveMethod, 0, 1, 1, 5)
        lyt_grid_moveSettings.addWidget(label_moveZero, 1, 1)
        lyt_grid_moveSettings.addWidget(label_moveMin, 1, 2)
        lyt_grid_moveSettings.addWidget(label_moveMax, 1, 5)
        lyt_grid_moveSettings.addWidget(label_moveX, 2, 0)
        lyt_grid_moveSettings.addWidget(self.checkBox_moveZeroX, 2, 1)
        lyt_grid_moveSettings.addWidget(self.spinBox_moveMinX, 2, 2)
        lyt_grid_moveSettings.addWidget(self.slider_moveMinX, 2, 3)
        lyt_grid_moveSettings.addWidget(self.slider_moveMaxX, 2, 4)
        lyt_grid_moveSettings.addWidget(self.spinBox_moveMaxX, 2, 5)
        lyt_grid_moveSettings.addWidget(label_moveY, 3, 0)
        lyt_grid_moveSettings.addWidget(self.checkBox_moveZeroY, 3, 1)
        lyt_grid_moveSettings.addWidget(self.spinBox_moveMinY, 3, 2)
        lyt_grid_moveSettings.addWidget(self.slider_moveMinY, 3, 3)
        lyt_grid_moveSettings.addWidget(self.slider_moveMaxY, 3, 4)
        lyt_grid_moveSettings.addWidget(self.spinBox_moveMaxY, 3, 5)
        lyt_grid_moveSettings.addWidget(label_moveZ, 4, 0)
        lyt_grid_moveSettings.addWidget(self.checkBox_moveZeroZ, 4, 1)
        lyt_grid_moveSettings.addWidget(self.spinBox_moveMinZ, 4, 2)
        lyt_grid_moveSettings.addWidget(self.slider_moveMinZ, 4, 3)
        lyt_grid_moveSettings.addWidget(self.slider_moveMaxZ, 4, 4)
        lyt_grid_moveSettings.addWidget(self.spinBox_moveMaxZ, 4, 5)
        lyt_grid_moveSettings.addWidget(self.checkBox_sameMoveXYZ, 5, 1, 1, 2)
        lyt_grid_moveSettings.addWidget(self.checkBox_equalMoveXYZ, 5, 3, 1, 3)

        lyt_form_rotateHeader = QtWidgets.QFormLayout(fieldGrowthPolicy = QtWidgets.QFormLayout.AllNonFixedFieldsGrow) #回転の冒頭部
        lyt_form_rotateHeader.addRow(label_rotate, line_rotate)

        lyt_hBox_rotateMethod = QtWidgets.QHBoxLayout() #回転の基準空間用
        lyt_hBox_rotateMethod.addWidget(radioButton_rotateWorld)
        lyt_hBox_rotateMethod.addWidget(radioButton_rotateRelative)

        lyt_grid_rotateSettings = QtWidgets.QGridLayout() #回転の設定用
        lyt_grid_rotateSettings.addWidget(label_rotateMethod, 0, 0)
        lyt_grid_rotateSettings.addLayout(lyt_hBox_rotateMethod, 0, 1, 1, 5)
        lyt_grid_rotateSettings.addWidget(label_rotateZero, 1, 1)
        lyt_grid_rotateSettings.addWidget(label_rotateMin, 1, 2)
        lyt_grid_rotateSettings.addWidget(label_rotateMax, 1, 5)
        lyt_grid_rotateSettings.addWidget(label_rotateX, 2, 0)
        lyt_grid_rotateSettings.addWidget(self.checkBox_rotateZeroX, 2, 1)
        lyt_grid_rotateSettings.addWidget(self.spinBox_rotateMinX, 2, 2)
        lyt_grid_rotateSettings.addWidget(self.slider_rotateMinX, 2, 3)
        lyt_grid_rotateSettings.addWidget(self.slider_rotateMaxX, 2, 4)
        lyt_grid_rotateSettings.addWidget(self.spinBox_rotateMaxX, 2, 5)
        lyt_grid_rotateSettings.addWidget(label_rotateY, 3, 0)
        lyt_grid_rotateSettings.addWidget(self.checkBox_rotateZeroY, 3, 1)
        lyt_grid_rotateSettings.addWidget(self.spinBox_rotateMinY, 3, 2)
        lyt_grid_rotateSettings.addWidget(self.slider_rotateMinY, 3, 3)
        lyt_grid_rotateSettings.addWidget(self.slider_rotateMaxY, 3, 4)
        lyt_grid_rotateSettings.addWidget(self.spinBox_rotateMaxY, 3, 5)
        lyt_grid_rotateSettings.addWidget(label_rotateZ, 4, 0)
        lyt_grid_rotateSettings.addWidget(self.checkBox_rotateZeroZ, 4, 1)
        lyt_grid_rotateSettings.addWidget(self.spinBox_rotateMinZ, 4, 2)
        lyt_grid_rotateSettings.addWidget(self.slider_rotateMinZ, 4, 3)
        lyt_grid_rotateSettings.addWidget(self.slider_rotateMaxZ, 4, 4)
        lyt_grid_rotateSettings.addWidget(self.spinBox_rotateMaxZ, 4, 5)
        lyt_grid_rotateSettings.addWidget(self.checkBox_sameRotateXYZ, 5, 1, 1, 2)
        lyt_grid_rotateSettings.addWidget(self.checkBox_equalRotateXYZ, 5, 3, 1, 3)

        lyt_form_scaleHeader = QtWidgets.QFormLayout(fieldGrowthPolicy = QtWidgets.QFormLayout.AllNonFixedFieldsGrow) #スケールの冒頭部
        lyt_form_scaleHeader.addRow(label_scale, line_scale)

        lyt_hBox_scaleMethod = QtWidgets.QHBoxLayout() #スケールの基準空間用
        lyt_hBox_scaleMethod.addWidget(radioButton_scaleObject)
        lyt_hBox_scaleMethod.addWidget(radioButton_scaleRelative)

        lyt_grid_scaleSettings = QtWidgets.QGridLayout() #スケールの設定用
        lyt_grid_scaleSettings.addWidget(label_scaleMethod, 0, 0)
        lyt_grid_scaleSettings.addLayout(lyt_hBox_scaleMethod, 0, 1, 1, 5)
        lyt_grid_scaleSettings.addWidget(label_scaleOne, 1, 1)
        lyt_grid_scaleSettings.addWidget(label_scaleMin, 1, 2)
        lyt_grid_scaleSettings.addWidget(label_scaleMax, 1, 5)
        lyt_grid_scaleSettings.addWidget(label_scaleX, 2, 0)
        lyt_grid_scaleSettings.addWidget(self.checkBox_scaleOneX, 2, 1)
        lyt_grid_scaleSettings.addWidget(self.spinBox_scaleMinX, 2, 2)
        lyt_grid_scaleSettings.addWidget(self.slider_scaleMinX, 2, 3)
        lyt_grid_scaleSettings.addWidget(self.slider_scaleMaxX, 2, 4)
        lyt_grid_scaleSettings.addWidget(self.spinBox_scaleMaxX, 2, 5)
        lyt_grid_scaleSettings.addWidget(label_scaleY, 3, 0)
        lyt_grid_scaleSettings.addWidget(self.checkBox_scaleOneY, 3, 1)
        lyt_grid_scaleSettings.addWidget(self.spinBox_scaleMinY, 3, 2)
        lyt_grid_scaleSettings.addWidget(self.slider_scaleMinY, 3, 3)
        lyt_grid_scaleSettings.addWidget(self.slider_scaleMaxY, 3, 4)
        lyt_grid_scaleSettings.addWidget(self.spinBox_scaleMaxY, 3, 5)
        lyt_grid_scaleSettings.addWidget(label_scaleZ, 4, 0)
        lyt_grid_scaleSettings.addWidget(self.checkBox_scaleOneZ, 4, 1)
        lyt_grid_scaleSettings.addWidget(self.spinBox_scaleMinZ, 4, 2)
        lyt_grid_scaleSettings.addWidget(self.slider_scaleMinZ, 4, 3)
        lyt_grid_scaleSettings.addWidget(self.slider_scaleMaxZ, 4, 4)
        lyt_grid_scaleSettings.addWidget(self.spinBox_scaleMaxZ, 4, 5)
        lyt_grid_scaleSettings.addWidget(self.checkBox_sameScaleXYZ, 5, 1, 1, 2)
        lyt_grid_scaleSettings.addWidget(self.checkBox_equalScaleXYZ, 5, 3, 1, 3)
        
        lyt_vBox_main = QtWidgets.QVBoxLayout()
        lyt_vBox_main.addLayout(lyt_form_moveHeader)
        lyt_vBox_main.addLayout(lyt_grid_moveSettings)
        lyt_vBox_main.addLayout(lyt_form_rotateHeader)
        lyt_vBox_main.addLayout(lyt_grid_rotateSettings)
        lyt_vBox_main.addLayout(lyt_form_scaleHeader)
        lyt_vBox_main.addLayout(lyt_grid_scaleSettings)
        lyt_vBox_main.addWidget(button_randomize)

        lyt_widget = QtWidgets.QWidget()
        lyt_widget.setLayout(lyt_vBox_main)
        self.setCentralWidget(lyt_widget)


    def randomize_objects(self):
        selected_objects = cmds.ls(sl = True)

        if not selected_objects:
            cmds.confirmDialog(b = "OK", icn = 'critical', m = "何も選択されていません、適用に失敗しました。", t = "ERROR: Transform Randomizer")
        else:
            for one_object in selected_objects:
                nums_transform = {"moveX":round(random.uniform(self.spinBox_moveMinX.value(), self.spinBox_moveMaxX.value()), 5),
                                  "moveY":round(random.uniform(self.spinBox_moveMinY.value(), self.spinBox_moveMaxY.value()), 5),
                                  "moveZ":round(random.uniform(self.spinBox_moveMinZ.value(), self.spinBox_moveMaxZ.value()), 5),
                                  "rotateX":round(random.uniform(self.spinBox_rotateMinX.value(), self.spinBox_rotateMaxX.value()), 5),
                                  "rotateY":round(random.uniform(self.spinBox_rotateMinY.value(), self.spinBox_rotateMaxY.value()), 5),
                                  "rotateZ":round(random.uniform(self.spinBox_rotateMinZ.value(), self.spinBox_rotateMaxZ.value()), 5),
                                  "scaleX":round(random.uniform(self.spinBox_scaleMinX.value(), self.spinBox_scaleMaxX.value()), 5),
                                  "scaleY":round(random.uniform(self.spinBox_scaleMinY.value(), self.spinBox_scaleMaxY.value()), 5),
                                  "scaleZ":round(random.uniform(self.spinBox_scaleMinZ.value(), self.spinBox_scaleMaxZ.value()), 5)}
                checkBoxes_nums = [[self.checkBox_moveZeroX, "moveX"], [self.checkBox_moveZeroY, "moveY"], [self.checkBox_moveZeroZ, "moveZ"],
                                   [self.checkBox_rotateZeroX, "rotateX"], [self.checkBox_rotateZeroY, "rotateY"], [self.checkBox_rotateZeroZ, "rotateZ"],
                                   [self.checkBox_scaleOneX, "scaleX"], [self.checkBox_scaleOneY, "scaleY"], [self.checkBox_scaleOneZ, "scaleZ"]] #0もしくは1を指定するCheckBoxと対応する文字列

                for one_index, one_item in zip(range(9), checkBoxes_nums):
                    if checkBoxes_nums[one_index][0].isChecked() == True:
                        if "scale" in one_item[1]: #Scaleの場合は1、それ以外は0
                            nums_transform[one_item[1]] = 1
                        else:
                            nums_transform[one_item[1]] = 0

                if self.checkBox_sameMoveXYZ.isChecked() == True:
                    if self.checkBox_equalMoveXYZ.isChecked() == True or self.checkBox_moveZeroX.isChecked() == True: #「まとめて変更」でXをゼロ指定した場合は「同じ値を適用」と結果が同一になる
                        nums_transform["moveZ"] = nums_transform["moveY"] = nums_transform["moveX"] #Xと同一の値を設定
                    else:
                        nums_transform["moveY"] = round(random.uniform(self.spinBox_moveMinX.value(), self.spinBox_moveMaxX.value()), 5) #Xに設定された範囲で再算出
                        nums_transform["moveZ"] = round(random.uniform(self.spinBox_moveMinX.value(), self.spinBox_moveMaxX.value()), 5)

                if self.checkBox_sameRotateXYZ.isChecked() == True:
                    if self.checkBox_equalRotateXYZ.isChecked() == True or self.checkBox_rotateZeroX.isChecked() == True:
                        nums_transform["rotateZ"] = nums_transform["rotateY"] = nums_transform["rotateX"]
                    else:
                        nums_transform["rotateY"] = round(random.uniform(self.spinBox_rotateMinX.value(), self.spinBox_rotateMaxX.value()), 5)
                        nums_transform["rotateZ"] = round(random.uniform(self.spinBox_rotateMinX.value(), self.spinBox_rotateMaxX.value()), 5)

                if self.checkBox_sameScaleXYZ.isChecked() == True:
                    if self.checkBox_equalScaleXYZ.isChecked() == True or self.checkBox_scaleOneX.isChecked() == True:
                        nums_transform["scaleZ"] = nums_transform["scaleY"] = nums_transform["scaleX"]
                    else:
                        nums_transform["scaleY"] = round(random.uniform(self.spinBox_scaleMinX.value(), self.spinBox_scaleMaxX.value()), 5)
                        nums_transform["scaleZ"] = round(random.uniform(self.spinBox_scaleMinX.value(), self.spinBox_scaleMaxX.value()), 5)

                if self.radioGroup_moveMethodSelect.checkedId() == 1: #World
                    cmds.move(nums_transform["moveX"], one_object, x = True, ws = True) #移動
                    cmds.move(nums_transform["moveY"], one_object, y = True, ws = True)
                    cmds.move(nums_transform["moveZ"], one_object, z = True, ws = True)
                else: #Relative
                    cmds.move(nums_transform["moveX"], one_object, x = True, r = True)
                    cmds.move(nums_transform["moveY"], one_object, y = True, r = True)
                    cmds.move(nums_transform["moveZ"], one_object, z = True, r = True)

                if self.radioGroup_rotateMethodSelect.checkedId() == 1: #World
                    cmds.rotate(nums_transform["rotateX"], one_object, x = True, ws = True) #回転
                    cmds.rotate(nums_transform["rotateY"], one_object, y = True, ws = True)
                    cmds.rotate(nums_transform["rotateZ"], one_object, z = True, ws = True)
                else: #Relative
                    cmds.rotate(nums_transform["rotateX"], one_object, x = True, r = True)
                    cmds.rotate(nums_transform["rotateY"], one_object, y = True, r = True)
                    cmds.rotate(nums_transform["rotateZ"], one_object, z = True, r = True)

                if self.radioGroup_scaleMethodSelect.checkedId() == 1: #Object
                    cmds.scale(nums_transform["scaleX"], one_object, x = True, os = True) #スケール
                    cmds.scale(nums_transform["scaleY"], one_object, y = True, os = True)
                    cmds.scale(nums_transform["scaleZ"], one_object, z = True, os = True)
                else: #Relative
                    cmds.scale(nums_transform["scaleX"], one_object, x = True, r = True)
                    cmds.scale(nums_transform["scaleY"], one_object, y = True, r = True)
                    cmds.scale(nums_transform["scaleZ"], one_object, z = True, r = True)


    def changed_checkBox_zeroOne(self):
        name_changedCheckBox = self.sender().objectName()
        affectedWidgets_pair = {"Zero_MoveX":[self.checkBox_moveZeroX, self.spinBox_moveMinX, self.spinBox_moveMaxX, self.slider_moveMinX, self.slider_moveMaxX], #値のリストの0番にobjectNameと同一のCheckBox
                                "Zero_MoveY":[self.checkBox_moveZeroY, self.spinBox_moveMinY, self.spinBox_moveMaxY, self.slider_moveMinY, self.slider_moveMaxY], #1-4番は影響を受けるウィジェット
                                "Zero_MoveZ":[self.checkBox_moveZeroZ, self.spinBox_moveMinZ, self.spinBox_moveMaxZ, self.slider_moveMinZ, self.slider_moveMaxZ],
                                "Zero_RotateX":[self.checkBox_rotateZeroX, self.spinBox_rotateMinX, self.spinBox_rotateMaxX, self.slider_rotateMinX, self.slider_rotateMaxX],
                                "Zero_RotateY":[self.checkBox_rotateZeroY, self.spinBox_rotateMinY, self.spinBox_rotateMaxY, self.slider_rotateMinY, self.slider_rotateMaxY],
                                "Zero_RotateZ":[self.checkBox_rotateZeroZ, self.spinBox_rotateMinZ, self.spinBox_rotateMaxZ, self.slider_rotateMinZ, self.slider_rotateMaxZ],
                                "One_ScaleX":[self.checkBox_scaleOneX, self.spinBox_scaleMinX, self.spinBox_scaleMaxX, self.slider_scaleMinX, self.slider_scaleMaxX],
                                "One_ScaleY":[self.checkBox_scaleOneY, self.spinBox_scaleMinY, self.spinBox_scaleMaxY, self.slider_scaleMinY, self.slider_scaleMaxY],
                                "One_ScaleZ":[self.checkBox_scaleOneZ, self.spinBox_scaleMinZ, self.spinBox_scaleMaxZ, self.slider_scaleMinZ, self.slider_scaleMaxZ]}
        
        for one_num in range(1, 5):
            affectedWidgets_pair[name_changedCheckBox][one_num].setEnabled(not affectedWidgets_pair[name_changedCheckBox][0].isChecked()) #Trueなら操作可、Falseなら操作不可
    

    def changed_checkBox_sameXYZ(self):
        name_changedCheckBox = self.sender().objectName()
        affectedWidgets_pair = {"Same_MoveXYZ":[self.checkBox_sameMoveXYZ, self.checkBox_moveZeroY, self.checkBox_moveZeroZ, #値のリストの0番にobjectNameと同一のCheckBox、1,2番に上記のdefで変更を司るCheckBox
                                                self.spinBox_moveMinY, self.spinBox_moveMaxY, self.slider_moveMinY, self.slider_moveMaxY, #3-10番は影響を受けるウィジェット
                                                self.spinBox_moveMinZ, self.spinBox_moveMaxZ, self.slider_moveMinZ, self.slider_moveMaxZ, self.checkBox_equalMoveXYZ], #11番は「XYZと同じ値を適用」のCheckBox
                                "Same_RotateXYZ":[self.checkBox_sameRotateXYZ, self.checkBox_rotateZeroY, self.checkBox_rotateZeroZ,
                                                  self.spinBox_rotateMinY, self.spinBox_rotateMaxY, self.slider_rotateMinY, self.slider_rotateMaxY,
                                                  self.spinBox_rotateMinZ, self.spinBox_rotateMaxZ, self.slider_rotateMinZ, self.slider_rotateMaxZ, self.checkBox_equalRotateXYZ],
                                "Same_ScaleXYZ":[self.checkBox_sameScaleXYZ, self.checkBox_scaleOneY, self.checkBox_scaleOneZ,
                                                 self.spinBox_scaleMinY, self.spinBox_scaleMaxY, self.slider_scaleMinY, self.slider_scaleMaxY,
                                                 self.spinBox_scaleMinZ, self.spinBox_scaleMaxZ, self.slider_scaleMinZ, self.slider_scaleMaxZ, self.checkBox_equalScaleXYZ]}
        
        if affectedWidgets_pair[name_changedCheckBox][1].isChecked() == False: #1番のチェックボックスの影響を受けるのは3-6番のウィジェット
            for one_num in range(3, 7):
                affectedWidgets_pair[name_changedCheckBox][one_num].setEnabled(not affectedWidgets_pair[name_changedCheckBox][0].isChecked())
        
        if affectedWidgets_pair[name_changedCheckBox][2].isChecked() == False: #2番のチェックボックスの影響を受けるのは7-10番のウィジェット
            for one_num in range(7, 11):
                affectedWidgets_pair[name_changedCheckBox][one_num].setEnabled(not affectedWidgets_pair[name_changedCheckBox][0].isChecked())

        affectedWidgets_pair[name_changedCheckBox][1].setEnabled(not affectedWidgets_pair[name_changedCheckBox][0].isChecked())
        affectedWidgets_pair[name_changedCheckBox][2].setEnabled(not affectedWidgets_pair[name_changedCheckBox][0].isChecked())
        affectedWidgets_pair[name_changedCheckBox][11].setEnabled(affectedWidgets_pair[name_changedCheckBox][0].isChecked())


    def valueUpdate_spinBoxToSlider(self):
        name_changedSpinBox = self.sender().objectName()
        widgets_values = {"Sb_MoveMinX":[self.slider_moveMinX, self.spinBox_moveMinX.value()], "Sb_MoveMaxX":[self.slider_moveMaxX, self.spinBox_moveMaxX.value()], #値のリストの0番はSpinBoxとペアになるSlider
                          "Sb_MoveMinY":[self.slider_moveMinY, self.spinBox_moveMinY.value()], "Sb_MoveMaxY":[self.slider_moveMaxY, self.spinBox_moveMaxY.value()], #1番はSpinBoxの現在の値
                          "Sb_MoveMinZ":[self.slider_moveMinZ, self.spinBox_moveMinZ.value()], "Sb_MoveMaxZ":[self.slider_moveMaxZ, self.spinBox_moveMaxZ.value()],
                          "Sb_RotateMinX":[self.slider_rotateMinX, self.spinBox_rotateMinX.value()], "Sb_RotateMaxX":[self.slider_rotateMaxX, self.spinBox_rotateMaxX.value()],
                          "Sb_RotateMinY":[self.slider_rotateMinY, self.spinBox_rotateMinY.value()], "Sb_RotateMaxY":[self.slider_rotateMaxY, self.spinBox_rotateMaxY.value()],
                          "Sb_RotateMinZ":[self.slider_rotateMinZ, self.spinBox_rotateMinZ.value()], "Sb_RotateMaxZ":[self.slider_rotateMaxZ, self.spinBox_rotateMaxZ.value()],
                          "Sb_ScaleMinX":[self.slider_scaleMinX, self.spinBox_scaleMinX.value()], "Sb_ScaleMaxX":[self.slider_scaleMaxX, self.spinBox_scaleMaxX.value()],
                          "Sb_ScaleMinY":[self.slider_scaleMinY, self.spinBox_scaleMinY.value()], "Sb_ScaleMaxY":[self.slider_scaleMaxY, self.spinBox_scaleMaxY.value()],
                          "Sb_ScaleMinZ":[self.slider_scaleMinZ, self.spinBox_scaleMinZ.value()], "Sb_ScaleMaxZ":[self.slider_scaleMaxZ, self.spinBox_scaleMaxZ.value()]}
        
        widgets_values[name_changedSpinBox][0].setValue(widgets_values[name_changedSpinBox][1] * 100) #Slider側に値を反映
    

    def valueUpdate_sliderToSpinBox(self):
        name_changedSlider = self.sender().objectName()
        widgets_values = {"Sli_MoveMinX":[self.spinBox_moveMinX, self.slider_moveMinX.value()], "Sli_MoveMaxX":[self.spinBox_moveMaxX, self.slider_moveMaxX.value()], #値のリストの0番はSliderとペアになるSpinBox
                          "Sli_MoveMinY":[self.spinBox_moveMinY, self.slider_moveMinY.value()], "Sli_MoveMaxY":[self.spinBox_moveMaxY, self.slider_moveMaxY.value()], #1番はSliderの現在の値
                          "Sli_MoveMinZ":[self.spinBox_moveMinZ, self.slider_moveMinZ.value()], "Sli_MoveMaxZ":[self.spinBox_moveMaxZ, self.slider_moveMaxZ.value()],
                          "Sli_RotateMinX":[self.spinBox_rotateMinX, self.slider_rotateMinX.value()], "Sli_RotateMaxX":[self.spinBox_rotateMaxX, self.slider_rotateMaxX.value()],
                          "Sli_RotateMinY":[self.spinBox_rotateMinY, self.slider_rotateMinY.value()], "Sli_RotateMaxY":[self.spinBox_rotateMaxY, self.slider_rotateMaxY.value()],
                          "Sli_RotateMinZ":[self.spinBox_rotateMinZ, self.slider_rotateMinZ.value()], "Sli_RotateMaxZ":[self.spinBox_rotateMaxZ, self.slider_rotateMaxZ.value()],
                          "Sli_ScaleMinX":[self.spinBox_scaleMinX, self.slider_scaleMinX.value()], "Sli_ScaleMaxX":[self.spinBox_scaleMaxX, self.slider_scaleMaxX.value()],
                          "Sli_ScaleMinY":[self.spinBox_scaleMinY, self.slider_scaleMinY.value()], "Sli_ScaleMaxY":[self.spinBox_scaleMaxY, self.slider_scaleMaxY.value()],
                          "Sli_ScaleMinZ":[self.spinBox_scaleMinZ, self.slider_scaleMinZ.value()], "Sli_ScaleMaxZ":[self.spinBox_scaleMaxZ, self.slider_scaleMaxZ.value()]}
        
        widgets_values[name_changedSlider][0].setValue(widgets_values[name_changedSlider][1] / 100) #SpinBox側に値を反映


toolWindow = TransformRandomizer()
toolWindow.show()
