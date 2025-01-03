#For Autodesk Maya 2024, Encoding UTF-8
import maya.cmds as cmds
from PySide2 import QtWidgets
from PySide2 import QtCore
from maya.app.general import mayaMixin

class RigControllerGenerator(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    def __init__(self):
        super(RigControllerGenerator, self).__init__()
        self.toolUI()
        self.initialize_settings()


    def toolUI(self):
        self.setGeometry(500, 300, 530, 220)
        self.setWindowTitle("Rig Controller Generator")
        self.statusBar().showMessage("Last Updated: 2024.1.3   |   For: Maya 2024   |   Fuma Hara")

        label_presets = QtWidgets.QLabel("プリセット形状")
        label_methodSelect = QtWidgets.QLabel("作成方法")
        label_controllerColor = QtWidgets.QLabel("色")
        label_controllerScale = QtWidgets.QLabel("スケール")
        label_controllerName = QtWidgets.QLabel("コントローラー名")
        label_controllerPosition = QtWidgets.QLabel("配置座標(XYZ)")

        self.listArea_presets = QtWidgets.QListWidget()
        self.listArea_presets.addItems(["円形", "三角形", "四角形", "五角形", "六角形", "八角形", "直角三角形", "正符号 (プラス記号)", "正符号 (プラス記号): 線",
                                        "球体", "立方体", "三角錐", "四角錐", "正八面体", "1方向矢印", "1方向矢印: 線", "1方向曲折矢印", "1方向曲折矢印: 線",
                                        "双方向矢印", "双方向矢印: 線", "双方向曲折矢印", "双方向曲折矢印: 線", "4方向矢印", "4方向矢印: 線", "4方向矢印 + 円形",
                                        "8方向矢印", "8方向矢印: 線", "8方向矢印 + 円形", "平歯車", "星形", "Avicii ロゴ"])

        self.radioGroup_methodSelect = QtWidgets.QButtonGroup()
        radioButton_presets = QtWidgets.QRadioButton("プリセット形状", self, checked = True)
        radioButton_convert = QtWidgets.QRadioButton("選択中のメッシュを変換", self)
        self.radioGroup_methodSelect.addButton(radioButton_presets, 1)
        self.radioGroup_methodSelect.addButton(radioButton_convert, 2)
        self.radioGroup_methodSelect.buttonClicked.connect(self.changed_methodSelect)

        self.spinBox_controllerScale = QtWidgets.QSpinBox(minimum = 1, maximum = 100, value = 1)
        self.spinBox_controllerPositionX = QtWidgets.QDoubleSpinBox(minimum = -500, maximum = 500, value = 0)
        self.spinBox_controllerPositionY = QtWidgets.QDoubleSpinBox(minimum = -500, maximum = 500, value = 0)
        self.spinBox_controllerPositionZ = QtWidgets.QDoubleSpinBox(minimum = -500, maximum = 500, value = 0)
        self.spinBox_controllerScale.valueChanged.connect(self.valueUpdate_spinBox_controllerScale)

        self.slider_controllerScale = QtWidgets.QSlider(QtCore.Qt.Horizontal, minimum = 1, maximum = 100, value = 1)
        self.slider_controllerScale.valueChanged.connect(self.valueUpdate_slider_controllerScale)

        self.txtLine_controllerName = QtWidgets.QLineEdit(placeholderText = "作成するコントローラーの名前を入力", fixedWidth = 220)

        self.button_controllerColor = QtWidgets.QPushButton(styleSheet = "background-color: rgb(255, 0, 0)")
        button_generate = QtWidgets.QPushButton("作成 / 変換")
        self.button_controllerColor.clicked.connect(self.open_colorEditor)
        button_generate.clicked.connect(self.generate_rigController)

        spacer_layout = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        lyt_vBox_presets = QtWidgets.QVBoxLayout()
        lyt_vBox_presets.addWidget(label_presets)
        lyt_vBox_presets.addWidget(self.listArea_presets)

        lyt_grid_options = QtWidgets.QGridLayout()
        lyt_grid_options.addWidget(label_methodSelect, 0, 0)
        lyt_grid_options.addWidget(radioButton_presets, 0, 1, 1, 3)
        lyt_grid_options.addWidget(radioButton_convert, 1, 1, 1, 3)
        lyt_grid_options.addWidget(label_controllerColor, 2, 0)
        lyt_grid_options.addWidget(self.button_controllerColor, 2, 1, 1, 3)
        lyt_grid_options.addWidget(label_controllerScale, 3, 0)
        lyt_grid_options.addWidget(self.spinBox_controllerScale, 3, 1)
        lyt_grid_options.addWidget(self.slider_controllerScale, 3, 2, 1, 2)
        lyt_grid_options.addWidget(label_controllerName, 4, 0)
        lyt_grid_options.addWidget(self.txtLine_controllerName, 4, 1, 1, 3)
        lyt_grid_options.addWidget(label_controllerPosition, 5, 0)
        lyt_grid_options.addWidget(self.spinBox_controllerPositionX, 5, 1)
        lyt_grid_options.addWidget(self.spinBox_controllerPositionY, 5, 2)
        lyt_grid_options.addWidget(self.spinBox_controllerPositionZ, 5, 3)
        lyt_grid_options.addWidget(button_generate, 6, 0, 1, 4)
        lyt_grid_options.addItem(spacer_layout, 7, 0, 1, 4)

        lyt_hBox_main = QtWidgets.QHBoxLayout()
        lyt_hBox_main.addLayout(lyt_vBox_presets, 2)
        lyt_hBox_main.addLayout(lyt_grid_options, 1)

        lyt_widget = QtWidgets.QWidget()
        lyt_widget.setLayout(lyt_hBox_main)
        self.setCentralWidget(lyt_widget)


    def initialize_settings(self):
        self.color_rigController = [1, 0, 0] #RGB赤


    def generate_rigController(self):
        self.scale_rigController = self.spinBox_controllerScale.value() #スケール
        self.name_rigController = self.txtLine_controllerName.text() #コントローラー名

        if self.txtLine_controllerName.text() == "":
            self.name_rigController = "Controller"

        if self.radioGroup_methodSelect.checkedId() == 1: #プリセット形状
            self.create_fromSelectedPreset()

        elif self.radioGroup_methodSelect.checkedId() == 2: #選択中のメッシュを変換
            self.convert_fromSelectedMesh()


    def create_fromSelectedPreset(self):
        selected_presetItem = self.listArea_presets.currentItem().text() #リスト上で選択中のアイテム
        positionX_rigController = self.spinBox_controllerPositionX.value() #配置座標X
        positionY_rigController = self.spinBox_controllerPositionY.value() #Y
        positionZ_rigController = self.spinBox_controllerPositionZ.value() #Z
        presets_oneStroke = {"三角形":[(0, 0, -0.5), (0.433, 0, 0.25), (-0.433, 0, 0.25), (0, 0, -0.5)],
                             "四角形":[(0.5, 0, 0.5), (0.5, 0, -0.5), (-0.5, 0, -0.5), (-0.5, 0, 0.5), (0.5, 0, 0.5)],
                             "五角形":[(0, 0, -0.5), (-0.4755, 0, -0.1545), (-0.2939, 0, 0.4045), (0.2939, 0, 0.4045), (0.4755, 0, -0.1545), (0, 0, -0.5)],
                             "六角形":[(0.5, 0, 0), (0.25, 0, 0.433), (-0.25, 0, 0.433), (-0.5, 0, 0), (-0.25, 0, -0.433), (0.25, 0, -0.433), (0.5, 0, 0)],
                             "八角形":[(0.5, 0, 0), (0.3536, 0, 0.3536), (0, 0, 0.5), (-0.3536, 0, 0.3536), (-0.5, 0, 0),(-0.3536, 0, -0.3536), (0, 0, -0.5),
                                    (0.3536, 0, -0.3536), (0.5, 0, 0)],
                             "直角三角形":[(0.5, 0, 0.5), (-0.5, 0, 0.5), (-0.5, 0, -0.5), (0.5, 0, 0.5)],
                             "正符号 (プラス記号)":[(0.167, 0, -0.5), (0.167, 0, -0.167), (0.5, 0, -0.167), (0.5, 0, 0.167), (0.167, 0, 0.167), (0.167, 0, 0.5),(-0.167, 0, 0.5),
                                            (-0.167, 0, 0.167), (-0.5, 0, 0.167), (-0.5, 0, -0.167), (-0.167, 0, -0.167), (-0.167, 0, -0.5), (0.167, 0, -0.5)],
                             "1方向矢印":[(0.5, 0, 0), (0.25, 0, 0.25), (0.25, 0, 0.087), (-0.5, 0, 0.087), (-0.5, 0, -0.087), (0.25, 0, -0.087), (0.25, 0, -0.25), (0.5, 0, 0)],
                             "1方向矢印: 線":[(0.25, 0, -0.25), (0.5, 0, 0), (0.25, 0, 0.25), (0.5, 0, 0), (-0.5, 0, 0)],
                             "1方向曲折矢印":[(0.5, 0, -0.5), (0.424, 0, -0.117), (0.207, 0, 0.207), (-0.117, 0, 0.424), (-0.5, 0, 0.5), (-0.5, 0, 0.617), (-0.8, 0, 0.442),
                                        (-0.5, 0, 0.267), (-0.5, 0, 0.38), (-0.217, 0, 0.324), (0.107, 0, 0.107), (0.324, 0, -0.217), (0.38, 0, -0.5), (0.5, 0, -0.5)],
                             "1方向曲折矢印: 線":[(0.44, 0, -0.5), (0.374, 0, -0.167), (0.157, 0, 0.157), (-0.167, 0, 0.374), (-0.5, 0, 0.44), (-0.8, 0, 0.442), (-0.5, 0, 0.267),
                                           (-0.8, 0, 0.442), (-0.5, 0, 0.617)],
                             "双方向矢印":[(0.5, 0, 0), (0.25, 0, 0.25), (0.25, 0, 0.087), (-0.25, 0, 0.087), (-0.25, 0, 0.25), (-0.5, 0, 0), (-0.25, 0, -0.25),
                                      (-0.25, 0, -0.087), (0.25, 0, -0.087), (0.25, 0, -0.25), (0.5, 0, 0)],
                             "双方向矢印: 線":[(0.25, 0, -0.25), (0.5, 0, 0), (0.25, 0, 0.25), (0.5, 0, 0), (-0.5, 0, 0), (-0.25, 0, -0.25), (-0.5, 0, 0), (-0.25, 0, 0.25)],
                             "双方向曲折矢印":[(0.44, 0, -0.8), (0.615, 0, -0.5), (0.5, 0, -0.5), (0.424, 0, -0.117), (0.207, 0, 0.207), (-0.117, 0, 0.424), (-0.5, 0, 0.5),
                                        (-0.5, 0, 0.617), (-0.8, 0, 0.442), (-0.5, 0, 0.267), (-0.5, 0, 0.38), (-0.217, 0, 0.324), (0.107, 0, 0.107), (0.324, 0, -0.217),
                                        (0.38, 0, -0.5), (0.265, 0, -0.5), (0.44, 0, -0.8)],
                             "双方向曲折矢印: 線":[(0.265, 0, -0.5), (0.44, 0, -0.8), (0.615, 0, -0.5), (0.44, 0, -0.8), (0.44, 0, -0.5), (0.374, 0, -0.167), (0.157, 0, 0.157),
                                           (-0.167, 0, 0.374), (-0.5, 0, 0.44), (-0.8, 0, 0.442), (-0.5, 0, 0.267), (-0.8, 0, 0.442), (-0.5, 0, 0.617)],
                             "4方向矢印":[(0, 0, -0.5), (0.175, 0, -0.325), (0.061, 0, -0.325), (0.061, 0, -0.061), (0.325, 0, -0.061), (0.325, 0, -0.175), (0.5, 0, 0),
                                      (0.325, 0, 0.175), (0.325, 0, 0.061), (0.061, 0, 0.061), (0.061, 0, 0.325), (0.175, 0, 0.325), (0, 0, 0.5), (-0.175, 0, 0.325),
                                      (-0.061, 0, 0.325), (-0.061, 0, 0.061), (-0.325, 0, 0.061), (-0.325, 0, 0.175), (-0.5, 0, 0), (-0.325, 0, -0.175), (-0.325, 0, -0.061),
                                      (-0.061, 0, -0.061), (-0.061, 0, -0.325), (-0.175, 0, -0.325), (0, 0, -0.5)],
                             "4方向矢印 + 円形":[(0, 0, -0.5), (0.175, 0, -0.325), (0.061, 0, -0.325), (0.061, 0, -0.234), (0.125, 0, -0.217), (0.217, 0, -0.125), (0.234, 0, -0.061),
                                           (0.325, 0, -0.061), (0.325, 0, -0.175), (0.5, 0, 0), (0.325, 0, 0.175), (0.325, 0, 0.061), (0.234, 0, 0.061), (0.217, 0, 0.125),
                                           (0.125, 0, 0.217), (0.061, 0, 0.234), (0.061, 0, 0.325), (0.175, 0, 0.325), (0, 0, 0.5), (-0.175, 0, 0.325), (-0.061, 0, 0.325),
                                           (-0.061, 0, 0.234), (-0.125, 0, 0.217), (-0.217, 0, 0.125), (-0.234, 0, 0.061), (-0.325, 0, 0.061), (-0.325, 0, 0.175), (-0.5, 0, 0),
                                           (-0.325, 0, -0.175), (-0.325, 0, -0.061), (-0.234, 0, -0.061), (-0.217, 0, -0.125), (-0.125, 0, -0.217), (-0.061, 0, -0.234),
                                           (-0.061, 0, -0.325), (-0.175, 0, -0.325), (0, 0, -0.5)],
                             "8方向矢印":[(0, 0, -0.5), (0.125, 0, -0.375), (0.044, 0, -0.375), (0.044, 0, -0.106), (0.234, 0, -0.296), (0.177, 0, -0.354), (0.354, 0, -0.354),
                                      (0.354, 0, -0.177), (0.296, 0, -0.234), (0.106, 0, -0.044), (0.375, 0, -0.044), (0.375, 0, -0.125), (0.5, 0, 0), (0.375, 0, 0.125),
                                      (0.375, 0, 0.044), (0.106, 0, 0.044), (0.296, 0, 0.234), (0.354, 0, 0.177), (0.354, 0, 0.354), (0.177, 0, 0.354), (0.234, 0, 0.296),
                                      (0.044, 0, 0.106), (0.044, 0, 0.375), (0.125, 0, 0.375), (0, 0, 0.5), (-0.125, 0, 0.375), (-0.044, 0, 0.375), (-0.044, 0, 0.106),
                                      (-0.234, 0, 0.296), (-0.177, 0, 0.354), (-0.354, 0, 0.354), (-0.354, 0, 0.177), (-0.296, 0, 0.234), (-0.106, 0, 0.044), (-0.375, 0, 0.044),
                                      (-0.375, 0, 0.125), (-0.5, 0, 0), (-0.375, 0, -0.125), (-0.375, 0, -0.044), (-0.106, 0, -0.044), (-0.296, 0, -0.234), (-0.354, 0, -0.177),
                                      (-0.354, 0, -0.354), (-0.177, 0, -0.354), (-0.234, 0, -0.296), (-0.044, 0, -0.106), (-0.044, 0, -0.375), (-0.125, 0, -0.375), (0, 0, -0.5)],
                             "8方向矢印 + 円形":[(0, 0, -0.5), (0.125, 0, -0.375), (0.044, 0, -0.375), (0.044, 0, -0.246), (0.143, 0, -0.205), (0.234, 0, -0.296), (0.177, 0, -0.354),
                                           (0.354, 0, -0.354), (0.354, 0, -0.177), (0.296, 0, -0.234), (0.205, 0, -0.143), (0.246, 0, -0.044), (0.375, 0, -0.044), (0.375, 0, -0.125),
                                           (0.5, 0, 0), (0.375, 0, 0.125), (0.375, 0, 0.044), (0.246, 0, 0.044), (0.205, 0, 0.143), (0.296, 0, 0.234), (0.354, 0, 0.177),
                                           (0.354, 0, 0.354), (0.177, 0, 0.354), (0.234, 0, 0.296), (0.143, 0, 0.205), (0.044, 0, 0.246), (0.044, 0, 0.375), (0.125, 0, 0.375),
                                           (0, 0, 0.5), (-0.125, 0, 0.375), (-0.044, 0, 0.375), (-0.044, 0, 0.246), (-0.143, 0, 0.205), (-0.234, 0, 0.296), (-0.177, 0, 0.354),
                                           (-0.354, 0, 0.354), (-0.354, 0, 0.177), (-0.296, 0, 0.234), (-0.205, 0, 0.143), (-0.246, 0, 0.044), (-0.375, 0, 0.044), (-0.375, 0, 0.125),
                                           (-0.5, 0, 0), (-0.375, 0, -0.125), (-0.375, 0, -0.044), (-0.246, 0, -0.044), (-0.205, 0, -0.143), (-0.296, 0, -0.234), (-0.354, 0, -0.177),
                                           (-0.354, 0, -0.354), (-0.177, 0, -0.354), (-0.234, 0, -0.296), (-0.143, 0, -0.205), (-0.044, 0, -0.246), (-0.044, 0, -0.375),
                                           (-0.125, 0, -0.375), (0, 0, -0.5)],
                             "平歯車":[(0.048, 0, -0.498), (0.061, 0, -0.395), (0.145, 0, -0.373), (0.207, 0, -0.455), (0.291, 0, -0.407), (0.25, 0, -0.312), (0.312, 0, -0.25),
                                    (0.407, 0, -0.291), (0.455, 0, -0.207), (0.373, 0, -0.145), (0.395, 0, -0.061), (0.498, 0, -0.048), (0.498, 0, 0.048), (0.395, 0, 0.061),
                                    (0.373, 0, 0.145), (0.455, 0, 0.207), (0.407, 0, 0.291), (0.312, 0, 0.25), (0.25, 0, 0.312), (0.291, 0, 0.407), (0.207, 0, 0.455), (0.145, 0, 0.373),
                                    (0.061, 0, 0.395), (0.048, 0, 0.498), (-0.048, 0, 0.498), (-0.061, 0, 0.395), (-0.145, 0, 0.373), (-0.207, 0, 0.455), (-0.291, 0, 0.407),
                                    (-0.25, 0, 0.312), (-0.312, 0, 0.25), (-0.407, 0, 0.291), (-0.455, 0, 0.207), (-0.373, 0, 0.145), (-0.395, 0, 0.061), (-0.498, 0, 0.048),
                                    (-0.498, 0, -0.048), (-0.395, 0, -0.061), (-0.373, 0, -0.145), (-0.455, 0, -0.207), (-0.407, 0, -0.291), (-0.312, 0, -0.25), (-0.25, 0, -0.312),
                                    (-0.291, 0, -0.407), (-0.207, 0, -0.455), (-0.145, 0, -0.373), (-0.061, 0, -0.395), (-0.048, 0, -0.498), (0.048, 0, -0.498)],
                             "星形":[(0, 0, -0.476), (0.118, 0, -0.112), (0.5, 0, -0.112), (0.191, 0, 0.112), (0.309, 0, 0.476), (0, 0, 0.251), (-0.309, 0, 0.476), (-0.191, 0, 0.112),
                                   (-0.5, 0, -0.112), (-0.118, 0, -0.112), (0, 0, -0.476)]} #一筆書きで作成できるカーブ
        presets_fromMesh = ["球体", "立方体", "三角錐", "四角錐", "正八面体"] #Meshから作成するカーブ
        
        if self.listArea_presets.currentItem() == None:
            cmds.confirmDialog(b = "OK", icn = 'critical', m = "何も選択されていません、作成に失敗しました。", t = "ERROR: Rig Controller Generator")
        
        elif selected_presetItem in presets_oneStroke.keys(): #一筆書きに含まれるもの
            curve_preset = cmds.curve(n = "PresetCurve_OneStroke", d = 1, p = presets_oneStroke[selected_presetItem])

        elif selected_presetItem in presets_fromMesh: #Meshから作成に含まれるもの
            if selected_presetItem == "球体":
                for one_num in range(3):
                    cmds.polyCylinder(n = f"PresetCurveFromMesh_Sphere{one_num}", h = 0, r = 0.5)
                    cmds.delete(f"PresetCurveFromMesh_Sphere{one_num}.f[0:20]")
                else:
                    cmds.rotate(90, "PresetCurveFromMesh_Sphere1", x = True)
                    cmds.rotate(90, "PresetCurveFromMesh_Sphere2", z = True)
                    object_reference = cmds.polyUnite("PresetCurveFromMesh_Sphere0", "PresetCurveFromMesh_Sphere1", "PresetCurveFromMesh_Sphere2")[0]
                    cmds.DeleteHistory()

            elif selected_presetItem == "立方体":
                object_reference = cmds.polyCube(n = "PresetCurveFromMesh_Cube", d = 1, h = 1, w = 1)
            
            elif selected_presetItem == "三角錐":
                object_reference = cmds.polyCone(n = "PresetCurveFromMesh_TriangularPyramid", h = 1, r = 0.7, sa = 3)
            
            elif selected_presetItem == "四角錐":
                object_reference = cmds.polyPyramid(n = "PresetCurveFromMesh_SquarePyramid", w = 1)
            
            elif selected_presetItem == "正八面体":
                object_reference = cmds.polyCube(n = "PresetCurveFromMesh_Octahedron", d = 1.5, h = 1.5, w = 1.5)
                cmds.polyBevel3(at = 180, d = 1, mvt = 0.001, mv = True, ma = 180, oaf = True, sg = 1, sa = 30, ws = True, f = 1, sn = True)
                cmds.polyMergeVertex(d = 0.001)
                cmds.select("PresetCurveFromMesh_Octahedron")

            self.convert_fromSelectedMesh()
            cmds.delete(object_reference)
            return
        
        elif selected_presetItem == "円形":
            curve_preset = cmds.circle(n = "PresetCurve_Circle")
            cmds.rotate(90, curve_preset, x = True)

        elif selected_presetItem == "正符号 (プラス記号): 線":
            curve_preset = cmds.curve(n = "PresetCurve_Cross", d = 1, p = [(0, 0, 0.5), (0, 0, -0.5)])
            curve_sub = cmds.curve(n = "PresetCurve_CrossSub", d = 1, p = [(0.5, 0, 0), (-0.5, 0, 0)])
            cmds.parent(cmds.listRelatives(curve_sub, s = True)[0], curve_preset, r = True, s = True)
            cmds.delete(curve_sub)

        elif selected_presetItem == "4方向矢印: 線":
            curve_preset = cmds.curve(n = "PresetCurve_CrossArrow", d = 1, p = [(-0.175, 0, -0.325), (0, 0, -0.5), (0.175, 0, -0.325),(0, 0, -0.5),
                                                                                (0, 0, 0.5), (-0.175, 0, 0.325), (0, 0, 0.5), (0.175, 0, 0.325)])
            curve_sub = cmds.curve(n = "PresetCurve_CrossArrowSub", d = 1, p = [(0.325, 0, -0.175), (0.5, 0, 0), (0.325, 0, 0.175), (0.5, 0, 0),
                                                                                (-0.5, 0, 0), (-0.325, 0, -0.175), (-0.5, 0, 0), (-0.325, 0, 0.175)])
            cmds.parent(cmds.listRelatives(curve_sub, s = True)[0], curve_preset, r = True, s = True)
            cmds.delete(curve_sub)

        elif selected_presetItem == "8方向矢印: 線":
            curve_preset = cmds.curve(n = "PresetCurve_EightArrow", d = 1, p = [(-0.125, 0, -0.375), (0, 0, -0.5), (0.125, 0, -0.375), (0, 0, -0.5),
                                                                                (0, 0, 0.5), (-0.125, 0, 0.375), (0, 0, 0.5), (0.125, 0, 0.375)])
            curve_sub = cmds.curve(n = "PresetCurve_EightArrowSub", d = 1, p = [(0.375, 0, -0.125), (0.5, 0, 0), (0.375, 0, 0.125), (0.5, 0, 0),
                                                                                (-0.5, 0, 0), (-0.375, 0, -0.125), (-0.5, 0, 0), (-0.375, 0, 0.125)])
            curve_sub2 = cmds.curve(n = "PresetCurve_EightArrowSub2", d = 1, p = [(0.177, 0, -0.354), (0.354, 0, -0.354), (0.354, 0, -0.177), (0.354, 0, -0.354),
                                                                                  (-0.354, 0, 0.354), (-0.354, 0, 0.177), (-0.354, 0, 0.354), (-0.177, 0, 0.354)])
            curve_sub3 = cmds.curve(n = "PresetCurve_EightArrowSub3", d = 1, p = [(-0.177, 0, -0.354), (-0.354, 0, -0.354), (-0.354, 0, -0.177), (-0.354, 0, -0.354),
                                                                                  (0.354, 0, 0.354), (0.354, 0, 0.177), (0.354, 0, 0.354), (0.177, 0, 0.354)])
            cmds.parent(cmds.listRelatives(curve_sub, s = True)[0], curve_preset, r = True, s = True)
            cmds.parent(cmds.listRelatives(curve_sub2, s = True)[0], curve_preset, r = True, s = True)
            cmds.parent(cmds.listRelatives(curve_sub3, s = True)[0], curve_preset, r = True, s = True)
            cmds.delete([curve_sub, curve_sub2, curve_sub3])

        elif selected_presetItem == "Avicii ロゴ":
            curve_preset = cmds.curve(n = "PresetCurve_AviciiLogo", d = 1, p = [(-0.11, 0, -0.5), (-0.11, 0, 0.5), (-1.11, 0, 0.5), (-0.11, 0, -0.5)])
            curve_sub = cmds.curve(n = "PresetCurve_AviciiLogoSub", d = 1, p = [(0.113, 0, -0.5), (0.113, 0, 0.5), (1.11, 0, -0.5), (0.113, 0, -0.5)])
            cmds.parent(cmds.listRelatives(curve_sub, s = True)[0], curve_preset, r = True, s = True)
            cmds.delete(curve_sub)

        shapeNodes_curve = cmds.listRelatives(curve_preset, s = True)

        for one_node in shapeNodes_curve:
            cmds.setAttr(one_node + ".overrideEnabled", 1) #描画オーバーライドを有効化
            cmds.setAttr(one_node + ".overrideRGBColors", 1) #RGB使用
            cmds.setAttr(one_node + ".overrideColorRGB", self.color_rigController[0], self.color_rigController[1], self.color_rigController[2]) #色を設定
        else:
            cmds.scale(self.scale_rigController, self.scale_rigController, self.scale_rigController, curve_preset)
            cmds.move(positionX_rigController, positionY_rigController, positionZ_rigController, curve_preset)
            cmds.select(curve_preset)
            cmds.rename(self.name_rigController)
    

    def convert_fromSelectedMesh(self):
        selected_mesh = cmds.ls(sl = True)

        if not selected_mesh:
            cmds.confirmDialog(b = "OK", icn = 'critical', m = "何も選択されていません、変換に失敗しました。", t = "ERROR: Rig Controller Generator")

        elif len(selected_mesh) != 1:
            print(selected_mesh)
            cmds.confirmDialog(b = "OK", icn = 'critical', m = "複数同時に変換することはできません、変換に失敗しました。", t = "ERROR: Rig Controller Generator")

        elif cmds.objectType(cmds.listRelatives(selected_mesh[0], f = True, s = True)) == 'mesh':
            num_edgeTotal = cmds.polyEvaluate(selected_mesh[0], e = True) #エッジ総数
            namesAll_edge = [f"{selected_mesh[0]}.e[{one_num}]" for one_num in range(num_edgeTotal)] #全エッジ名
            curve_generated = []
            shapeNodes_generated = []

            for one_edge in namesAll_edge:
                positions_vertex = cmds.xform(one_edge, q = True, t = True, ws = True) #エッジを構成する2頂点の座標
                curve_fromEdge = cmds.curve(n = "GeneratedCurve_FromMeshEdge", d = 1, p = [(positions_vertex[0], positions_vertex[1], positions_vertex[2]),
                                                                                           (positions_vertex[3], positions_vertex[4], positions_vertex[5])]) #頂点座標からカーブを作成
                shapeNode_curve = cmds.listRelatives(curve_fromEdge, s = True)[0] #curveのシェイプノード
                cmds.setAttr(shapeNode_curve + ".overrideEnabled", 1)
                cmds.setAttr(shapeNode_curve + ".overrideRGBColors", 1)
                cmds.setAttr(shapeNode_curve + ".overrideColorRGB", self.color_rigController[0], self.color_rigController[1], self.color_rigController[2])
                curve_generated.append(curve_fromEdge)
                shapeNodes_generated.append(shapeNode_curve)
            else:
                cmds.parent(shapeNodes_generated[1:], curve_generated[0], r = True, s = True) #1つにまとめる
                cmds.delete(curve_generated[1:]) #0番目(上記でまとめた先)を除く空のトランスフォームノードを削除
                curve_generated = str(curve_generated[0]) #要素が1つのリストから、文字列に変換
                cmds.scale(self.scale_rigController, self.scale_rigController, self.scale_rigController, curve_generated)
                cmds.select(curve_generated)
                cmds.rename("GeneratedCurve_FromMeshEdge", self.name_rigController)
        else:
            cmds.confirmDialog(b = "OK", icn = 'critical', m = "メッシュ以外変換することはできません、変換に失敗しました。", t = "ERROR: Rig Controller Generator")
    

    def open_colorEditor(self):
        cmds.colorEditor()

        if cmds.colorEditor(q = True, r = True):
            color_rgb = cmds.colorEditor(q = True, rgb = True) #正規化(0-1範囲)されたRGB値を取得
            self.button_controllerColor.setStyleSheet(f"background-color: rgb({color_rgb[0] * 255}, {color_rgb[1] * 255}, {color_rgb[2] * 255})") #0-255範囲に変換
            self.color_rigController = color_rgb
    

    def changed_methodSelect(self):
        if self.radioGroup_methodSelect.checkedId() == 1: #プリセット形状
            self.spinBox_controllerPositionX.setEnabled(True)
            self.spinBox_controllerPositionY.setEnabled(True)
            self.spinBox_controllerPositionZ.setEnabled(True)
        else: #選択中のメッシュを変換
            self.spinBox_controllerPositionX.setEnabled(False)
            self.spinBox_controllerPositionY.setEnabled(False)
            self.spinBox_controllerPositionZ.setEnabled(False)
    

    def valueUpdate_spinBox_controllerScale(self):
        value_now = self.spinBox_controllerScale.value()
        self.slider_controllerScale.setValue(value_now)
    

    def valueUpdate_slider_controllerScale(self):
        value_now = self.slider_controllerScale.value()
        self.spinBox_controllerScale.setValue(value_now)


toolWindow = RigControllerGenerator()
toolWindow.show()
