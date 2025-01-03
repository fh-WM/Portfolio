#For Autodesk Maya 2024, Encoding UTF-8
import maya.cmds as cmds
from PySide2 import QtWidgets
from PySide2 import QtCore
from maya.app.general import mayaMixin

class JointChainStraightener(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    def __init__(self):
        super(JointChainStraightener, self).__init__()
        self.toolUI()
        self.initialize_settings()


    def toolUI(self):
        self.setGeometry(500, 300, 400, 350)
        self.setWindowTitle("JointChain Straightener")
        self.statusBar().showMessage("Last Updated: 2024.12.28   |   For: Maya 2024   |   Fuma Hara")

        label_JointsToBeStraight = QtWidgets.QLabel("矯正するジョイント", alignment = QtCore.Qt.AlignBottom)
        label_axisSelect = QtWidgets.QLabel("矯正する軸")
        label_order = QtWidgets.QLabel("- 親\n-\n-\n-\n-\n- 子")

        self.listArea_jointsToBeStraight = QtWidgets.QListWidget(selectionMode = QtWidgets.QAbstractItemView.ExtendedSelection) #Shift/Ctrlによる複数選択可

        self.checkBox_axisX = QtWidgets.QCheckBox("X軸", checked = True)
        self.checkBox_axisY = QtWidgets.QCheckBox("Y軸", checked = True)
        self.checkBox_axisZ = QtWidgets.QCheckBox("Z軸", checked = True)

        spacer_buttonLayout = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        button_register = QtWidgets.QPushButton("登録", fixedWidth = 80)
        button_exclusion = QtWidgets.QPushButton("除外", fixedWidth = 80)
        button_reset = QtWidgets.QPushButton("リセット", fixedWidth = 80)
        button_clear = QtWidgets.QPushButton("クリア", fixedWidth = 80)
        button_straightening = QtWidgets.QPushButton("矯正 / 直線化")
        button_return = QtWidgets.QPushButton("元の位置に戻す")
        button_register.clicked.connect(self.register_joints)
        button_exclusion.clicked.connect(self.exclusion_joints)
        button_reset.clicked.connect(self.reset_joints)
        button_clear.clicked.connect(self.clear_joints)
        button_straightening.clicked.connect(self.straightening_joints)
        button_return.clicked.connect(self.return_jointsPosition)

        lyt_vBox_button = QtWidgets.QVBoxLayout() #リスト横ボタン用
        lyt_vBox_button.addWidget(button_exclusion)
        lyt_vBox_button.addWidget(button_reset)
        lyt_vBox_button.addWidget(button_clear)
        lyt_vBox_button.addWidget(label_order)
        lyt_vBox_button.addItem(spacer_buttonLayout)

        lyt_hBox_axisSelect = QtWidgets.QHBoxLayout() #軸設定用
        lyt_hBox_axisSelect.addWidget(label_axisSelect)
        lyt_hBox_axisSelect.addWidget(self.checkBox_axisX)
        lyt_hBox_axisSelect.addWidget(self.checkBox_axisY)
        lyt_hBox_axisSelect.addWidget(self.checkBox_axisZ)

        lyt_grid_main = QtWidgets.QGridLayout()
        lyt_grid_main.addWidget(label_JointsToBeStraight, 0, 0)
        lyt_grid_main.addWidget(button_register, 0, 1)
        lyt_grid_main.addWidget(self.listArea_jointsToBeStraight, 1, 0)
        lyt_grid_main.addLayout(lyt_vBox_button, 1, 1)

        lyt_hBox_button = QtWidgets.QHBoxLayout() #ツール下ボタン用
        lyt_hBox_button.addWidget(button_straightening, 3)
        lyt_hBox_button.addWidget(button_return, 1)

        lyt_vBox_main = QtWidgets.QVBoxLayout()
        lyt_vBox_main.addLayout(lyt_grid_main)
        lyt_vBox_main.addLayout(lyt_hBox_axisSelect)
        lyt_vBox_main.addLayout(lyt_hBox_button)

        lyt_widget = QtWidgets.QWidget()
        lyt_widget.setLayout(lyt_vBox_main)
        self.setCentralWidget(lyt_widget)


    def initialize_settings(self):
        self.joints_registered = []
        self.jointsPosition_registered = []


    def register_joints(self):
        selected_joints = cmds.ls(sl = True, l = True) #フルパス名で取得
        joint_parents = [] #親ジョイント(最上層)のリスト
        joint_children = [] #子ジョイント(最下層)のリスト
        self.initialize_settings()

        if not selected_joints:
            cmds.confirmDialog(b = "OK", icn = 'critical', m = "何も選択されていません、登録に失敗しました。", t = "ERROR: JointChain Straightener")

        elif len(selected_joints) > 2:
            for one_joint in selected_joints:
                detected_parent = cmds.listRelatives(one_joint, p = True, f = True) #フルパス名で取得
                detected_child = cmds.listRelatives(one_joint, c = True, f = True)

                if detected_parent is not None:
                    for one_parent in detected_parent:
                        if one_parent not in selected_joints: #検出結果がNoneではなく、かつ選択中のジョイントに含まれていなかった場合
                            joint_parents.append(one_joint)
                else:
                    joint_parents.append(one_joint) #検出結果がNoneであった場合は確定

                if detected_child is not None:
                    for one_child in detected_child:
                        if one_child not in selected_joints:
                            joint_children.append(one_joint)
                else:
                    joint_children.append(one_joint)
            else:
                if len(joint_parents) == 1 and len(joint_children) == 1: #検出した親子が共に単一であった場合
                    joints_allChild = list(reversed(cmds.listRelatives(joint_parents[0], ad = True, f = True))) #親ジョイント(最上層)の子全てを検出
                    joints_toBeRegister = [one_joint for one_joint in joints_allChild if one_joint in selected_joints and one_joint != joint_children[0]] #検出結果から選択中のジョイントに含まれるものと、子ジョイント(最下層)以外
                    joints_toBeRegister = joint_parents + joints_toBeRegister + joint_children
                    self.jointsPosition_registered = [cmds.xform(one_joint, q = True, t = True, ws = True) for one_joint in joints_toBeRegister] #全てのジョイントの現在位置
                    joints_nameOnly = [(one_joint.split("|"))[-1] for one_joint in joints_toBeRegister] #フルパス名ではなく通常の名称表示のリスト
                    self.joints_registered = [f"{one_name}  /  {one_path}" for one_name, one_path in zip(joints_nameOnly, joints_toBeRegister)] #通常の名称とフルパス名をセットにしたリスト
                    self.listArea_jointsToBeStraight.clear()
                    self.listArea_jointsToBeStraight.addItems(self.joints_registered)
                else:
                    cmds.confirmDialog(b = "OK", icn = 'critical', m = "選択状態が不適切もしくは\n連続した親子関係でない可能性があります、登録に失敗しました。", t = "ERROR: JointChain Straightener")
        else:
            cmds.confirmDialog(b = "OK", icn = 'critical', m = "最低3つから登録が可能です、登録に失敗しました。", t = "ERROR: JointChain Straightener")


    def straightening_joints(self):
        axisX = self.checkBox_axisX.isChecked()
        axisY = self.checkBox_axisY.isChecked()
        axisZ = self.checkBox_axisZ.isChecked()
        joints_nowRegistered = [self.listArea_jointsToBeStraight.item(one_name).text() for one_name in range(self.listArea_jointsToBeStraight.count())] #リストに表示中の項目

        if len(joints_nowRegistered) < 3:
            cmds.confirmDialog(b = "OK", icn = 'critical', m = "実行には登録数が3つ以上である必要があります、矯正/直線化に失敗しました。", t = "ERROR: JointChain Straightener")

        elif axisX == False and axisY == False and axisZ == False:
            cmds.confirmDialog(b = "OK", icn = 'critical', m = "「矯正する軸」が指定されていません、矯正/直線化に失敗しました。", t = "ERROR: JointChain Straightener")

        else:
            joints_registeredFullPath = [(one_joint.split("  /  "))[-1] for one_joint in self.joints_registered] #登録済みのジョイント
            joints_toBeStraightening = [(one_joint.split("  /  "))[-1] for one_joint in joints_nowRegistered] #登録済みかつ除外が済んだ後のジョイントのリスト
            jointPosition_parent = cmds.xform(joints_toBeStraightening[0], q = True, t = True, ws = True) #矯正の基準となる親ジョイント
            jointPosition_child = cmds.xform(joints_toBeStraightening[-1], q = True, t = True, ws = True) #矯正の基準となる子ジョイント

            for one_joint in joints_registeredFullPath:
                if one_joint == joints_toBeStraightening[0] or one_joint == joints_toBeStraightening[-1] or one_joint not in joints_toBeStraightening:
                    position_joint = self.jointsPosition_registered[joints_registeredFullPath.index(one_joint)] #親ジョイントではなく子ジョイントでもなく登録からも除外されている場合に、元の位置に再配置
                    cmds.move(position_joint[0], position_joint[1], position_joint[2], one_joint, ws = True)
                else:
                    jointPosition_straightening = cmds.xform(one_joint, q = True, t = True, ws = True)
                    vector_pr_ch = [ch_num - pr_num for ch_num, pr_num in zip(jointPosition_child, jointPosition_parent)] #親子間のベクトル
                    vector_pr_st = [st_num - pr_num for st_num, pr_num in zip(jointPosition_straightening, jointPosition_parent)] #親と移動するジョイント間のベクトル
                    product_prCh_prSt = sum(prSt_num * prCh_num for prSt_num, prCh_num in zip(vector_pr_st, vector_pr_ch)) #上記2つのベクトルの内積
                    squared_prCh = sum(one_num ** 2 for one_num in vector_pr_ch) #親子間のベクトルの二乗
                    scalar = product_prCh_prSt / squared_prCh
                    position_newX = jointPosition_parent[0] + scalar * vector_pr_ch[0]
                    position_newY = jointPosition_parent[1] + scalar * vector_pr_ch[1]
                    position_newZ = jointPosition_parent[2] + scalar * vector_pr_ch[2]
                    
                    if axisX == True:
                        cmds.move(position_newX, one_joint, x = True, ws = True)

                    if axisY == True:
                        cmds.move(position_newY, one_joint, y = True, ws = True)

                    if axisZ == True:
                        cmds.move(position_newZ, one_joint, z = True, ws = True)


    def return_jointsPosition(self):
        if not self.joints_registered:
            cmds.confirmDialog(b = "OK", icn = 'critical', m = "何も登録されていません、元の位置に戻す事に失敗しました。", t = "ERROR: JointChain Straightener")
        else:
            joints_registeredFullPath = [(one_joint.split("  /  "))[-1] for one_joint in self.joints_registered]

            for one_joint, one_position in zip(joints_registeredFullPath, self.jointsPosition_registered):
                cmds.move(one_position[0], one_position[1], one_position[2], one_joint, ws = True)


    def exclusion_joints(self):
        selected_items = self.listArea_jointsToBeStraight.selectedItems()

        for one_item in selected_items:
            self.listArea_jointsToBeStraight.takeItem(self.listArea_jointsToBeStraight.row(one_item))


    def reset_joints(self):
        self.listArea_jointsToBeStraight.clear()
        self.listArea_jointsToBeStraight.addItems(self.joints_registered)


    def clear_joints(self):
        self.listArea_jointsToBeStraight.clear()
        self.initialize_settings()


toolWindow = JointChainStraightener()
toolWindow.show()
