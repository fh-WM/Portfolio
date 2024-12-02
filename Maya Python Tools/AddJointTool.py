#For Autodesk Maya 2024, Encoding UTF-8
import maya.cmds as cmds
from PySide2 import QtWidgets
from PySide2 import QtCore
from maya.app.general import mayaMixin

class AddJointTool(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    def __init__(self):
        super(AddJointTool, self).__init__()
        self.toolUI()

    
    def toolUI(self):
        self.setGeometry(500, 300, 470, 180)
        self.setWindowTitle("Add Joint Tool")
        self.statusBar().showMessage("Last Updated: 2024.11.25   |   For: Maya 2024   |   Fuma Hara")

        label_jointNum = QtWidgets.QLabel("追加するジョイント数")
        label_methodSelect = QtWidgets.QLabel("追加方法")
        label_jointName = QtWidgets.QLabel("ジョイント名")

        self.spinBox_jointNum = QtWidgets.QSpinBox(minimum = 1, maximum = 100, value = 1)
        self.spinBox_jointNameNum = QtWidgets.QSpinBox(minimum = 0, maximum = 999, value = 1)
        self.spinBox_jointNum.valueChanged.connect(self.valueUpdate_spinBox_addJoints)

        self.slider_jointNum = QtWidgets.QSlider(QtCore.Qt.Horizontal, minimum = 1, maximum = 100, value = 1)
        self.slider_jointNum.valueChanged.connect(self.valueUpdate_slider_addJoints)

        self.radioGroup_methodSelect = QtWidgets.QButtonGroup()
        radioButton_01 = QtWidgets.QRadioButton("親ジョイントと子ジョイントの間を分割する形でジョイントを追加する", self, checked = True)
        radioButton_02 = QtWidgets.QRadioButton("子ジョイントと同階層にジョイントを追加する", self)
        radioButton_03 = QtWidgets.QRadioButton("子ジョイントと同階層にジョイントを全て追加する", self)
        self.radioGroup_methodSelect.addButton(radioButton_01, 1)
        self.radioGroup_methodSelect.addButton(radioButton_02, 2)
        self.radioGroup_methodSelect.addButton(radioButton_03, 3)

        self.txtLine_jointName = QtWidgets.QLineEdit(placeholderText = "追加するジョイントの名前を入力")

        button_addJoints = QtWidgets.QPushButton("追加")
        button_addJoints.clicked.connect(self.add_joints)

        lyt_hBox_jointNum = QtWidgets.QHBoxLayout()
        lyt_hBox_jointNum.addWidget(self.spinBox_jointNum, 1)
        lyt_hBox_jointNum.addWidget(self.slider_jointNum, 4)

        lyt_hBox_jointName = QtWidgets.QHBoxLayout()
        lyt_hBox_jointName.addWidget(self.txtLine_jointName, 4)
        lyt_hBox_jointName.addWidget(self.spinBox_jointNameNum, 1)

        lyt_grid_main = QtWidgets.QGridLayout()
        lyt_grid_main.addWidget(label_jointNum, 0, 0)
        lyt_grid_main.addLayout(lyt_hBox_jointNum, 0, 1)
        lyt_grid_main.addWidget(label_methodSelect, 1, 0)
        lyt_grid_main.addWidget(radioButton_01, 1, 1)
        lyt_grid_main.addWidget(radioButton_02, 2, 1)
        lyt_grid_main.addWidget(radioButton_03, 3, 1)
        lyt_grid_main.addWidget(label_jointName, 4, 0)
        lyt_grid_main.addLayout(lyt_hBox_jointName, 4, 1)

        lyt_vBox_main = QtWidgets.QVBoxLayout()
        lyt_vBox_main.addLayout(lyt_grid_main)
        lyt_vBox_main.addWidget(button_addJoints)

        lyt_widget = QtWidgets.QWidget()
        lyt_widget.setLayout(lyt_vBox_main)
        self.setCentralWidget(lyt_widget)


    def add_joints(self):
        selected_joints = cmds.ls(sl = True)
        num_addJoints = self.spinBox_jointNum.value() #追加するジョイント数
        name_addJoints = self.txtLine_jointName.text() #追加するジョイント名
        nameNum_addJoints = self.spinBox_jointNameNum.value() #追加するジョイント名末尾の番号

        if not selected_joints:
            cmds.confirmDialog(b = "OK", icn = 'critical', m = "何も選択されていません、追加に失敗しました。", t = "ERROR: Add Joint Tool")

        elif len(selected_joints) != 2:
            cmds.confirmDialog(b = "OK", icn = 'critical', m = "必ず2つ選択してください、追加に失敗しました。", t = "ERROR: Add Joint Tool")

        else:
            detected_children0 = cmds.listRelatives(selected_joints[0], c = True) #子ジョイントの検出
            detected_children1 = cmds.listRelatives(selected_joints[1], c = True)

            if detected_children0 != None and selected_joints[1] in detected_children0: #子ジョイントが存在しており名前が一致する場合
                joint_parent = selected_joints[0]
                joint_child = selected_joints[1]

            elif detected_children1 != None and selected_joints[0] in detected_children1:
                joint_parent = selected_joints[1]
                joint_child = selected_joints[0]

            else:
                cmds.confirmDialog(b = "OK", icn = 'critical', m = "必ず直接の親子関係にあるジョイントを選択してください、追加に失敗しました。", t = "ERROR: Add Joint Tool")
                return

            jointPosition_parent = cmds.xform(joint_parent, q = True, t = True, ws = True)
            jointPosition_child = cmds.xform(joint_child, q = True, t = True, ws = True)
            positions_addJoints = [] #追加するジョイント全ての座標
            names_addJoints = [] #追加するジョイント全て

            ratio_p = 1 #親ジョイントと子ジョイントの間を直線で繋いだ際の親側の比、内分点計算より
            ratio_c = num_addJoints #子側の比

            while len(positions_addJoints) < num_addJoints:
                position_interiorPoint = [(ratio_c * jointPosition_parent[0] + ratio_p * jointPosition_child[0]) / (ratio_p + ratio_c),
                                        (ratio_c * jointPosition_parent[1] + ratio_p * jointPosition_child[1]) / (ratio_p + ratio_c),
                                        (ratio_c * jointPosition_parent[2] + ratio_p * jointPosition_child[2]) / (ratio_p + ratio_c)] #追加するジョイントの座標
                positions_addJoints.append(position_interiorPoint)
                ratio_p += 1
                ratio_c -= 1

            if self.txtLine_jointName.text() == "":
                name_addJoints = "additional_joint"

            cmds.select(joint_parent)

            for i in range(num_addJoints):
                joint_addition = cmds.joint(n = f"{name_addJoints}{nameNum_addJoints + i}")
                cmds.move(positions_addJoints[i][0], positions_addJoints[i][1], positions_addJoints[i][2], joint_addition)
                names_addJoints.append(cmds.ls(sl = True)[0])

            if self.radioGroup_methodSelect.checkedId() == 1: #親ジョイントと子ジョイントの間を分割する形でジョイントを追加する
                cmds.parent(joint_child, names_addJoints[-1])

            elif self.radioGroup_methodSelect.checkedId() == 3: #子ジョイントと同階層にジョイントを全て追加する
                del names_addJoints[0] #親子関係を改める必要がないため

                for one_joint in names_addJoints:
                    cmds.parent(one_joint, joint_parent)
    

    def valueUpdate_spinBox_addJoints(self):
        value_now = self.spinBox_jointNum.value() #現在の値を取得
        self.slider_jointNum.setValue(value_now) #値を上書き
    

    def valueUpdate_slider_addJoints(self):
        value_now = self.slider_jointNum.value()
        self.spinBox_jointNum.setValue(value_now)


toolWindow = AddJointTool()
toolWindow.show()
