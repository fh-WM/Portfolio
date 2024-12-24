#For Autodesk Maya 2024, Encoding UTF-8
import maya.cmds as cmds
import math
import random
from PySide2 import QtWidgets
from PySide2 import QtCore
from maya.app.general import mayaMixin

class PlacementTool(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    def __init__(self):
        super(PlacementTool, self).__init__()
        self.toolUI()
        self.initialize_settings()


    def toolUI(self):
        self.setGeometry(500, 300, 400, 500)
        self.setWindowTitle("Placement Tool")
        self.statusBar().showMessage("Last Updated: 2024.12.24   |   For: Maya 2024   |   Fuma Hara")

        label_referenceName = QtWidgets.QLabel("配置基準")
        label_percentage = QtWidgets.QLabel("配置割合")
        label_componentsSelect = QtWidgets.QLabel("配置場所")
        self.label_listTotal = QtWidgets.QLabel("配置場所数:\n0")

        self.txtLine_referenceName = QtWidgets.QLineEdit(readOnly = True, placeholderText = "オブジェクト名", fixedHeight = 25)
        self.txtLine_referenceInfo = QtWidgets.QLineEdit(readOnly = True, placeholderText = "↑の、頂点数 / エッジ数 / フェース数 (登録時)")

        self.spinBox_percentage = QtWidgets.QSpinBox(minimum = 0, maximum = 100, value = 100, suffix = "%") #配置割合％設定
        self.spinBox_percentage.valueChanged.connect(self.valueUpdate_spinBox_percentage)

        self.slider_percentage = QtWidgets.QSlider(QtCore.Qt.Horizontal, minimum = 0, maximum = 100, value = 100) #配置割合％設定
        self.slider_percentage.valueChanged.connect(self.valueUpdate_slider_percentage)

        self.radioGroup_componentsSelect = QtWidgets.QButtonGroup()
        radioButton_vertex = QtWidgets.QRadioButton("頂点位置", self, checked = True)
        radioButton_edge = QtWidgets.QRadioButton("エッジ位置", self)
        radioButton_face = QtWidgets.QRadioButton("フェース位置", self)
        self.radioGroup_componentsSelect.addButton(radioButton_vertex, 1)
        self.radioGroup_componentsSelect.addButton(radioButton_edge, 2)
        self.radioGroup_componentsSelect.addButton(radioButton_face, 3)
        self.radioGroup_componentsSelect.buttonClicked.connect(self.reset_componentNames_and_changed_radioGroup)

        self.checkBox_normal = QtWidgets.QCheckBox("配置角度を配置場所の法線に合わせる", checked = True)
        self.checkBox_duplicate = QtWidgets.QCheckBox("配置するオブジェクトを配置場所数に合わせて複製し補完する", checked = True)
        self.checkBox_group = QtWidgets.QCheckBox("配置後グループにまとめる", checked = True)
        self.checkBox_highlight = QtWidgets.QCheckBox("ハイライト")
        self.checkBox_highlight.stateChanged.connect(self.changed_checkBox_highlight)

        self.listArea_componentNames = QtWidgets.QListWidget(selectionMode = QtWidgets.QAbstractItemView.ExtendedSelection) #コンポーネント名一覧用リスト、Shift/Ctrlによる複数選択を有効化
        self.listArea_componentNames.itemSelectionChanged.connect(self.selected_listArea_componentNames)

        button_register = QtWidgets.QPushButton("登録")
        button_exclusion = QtWidgets.QPushButton("除外")
        button_reset = QtWidgets.QPushButton("リセット")
        button_clear = QtWidgets.QPushButton("クリア")
        button_placement = QtWidgets.QPushButton("選択中のオブジェクトを配置")
        button_register.clicked.connect(self.register_referenceObject)
        button_exclusion.clicked.connect(self.exclusion_componentNames)
        button_reset.clicked.connect(self.reset_componentNames_and_changed_radioGroup)
        button_clear.clicked.connect(self.clear_componentNames)
        button_placement.clicked.connect(self.placement_objects)

        spacer_buttonLayout = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding) #ウィンドウサイズに合わせて自動伸縮するスペーサー

        lyt_hBox_referenceName = QtWidgets.QHBoxLayout() #配置基準用レイアウト
        lyt_hBox_referenceName.addWidget(self.txtLine_referenceName, 3)
        lyt_hBox_referenceName.addWidget(button_register, 1)

        lyt_hBox_percentage = QtWidgets.QHBoxLayout() #配置割合用レイアウト
        lyt_hBox_percentage.addWidget(self.spinBox_percentage, 1)
        lyt_hBox_percentage.addWidget(self.slider_percentage, 3)

        lyt_hBox_radioButton = QtWidgets.QHBoxLayout() #配置場所用レイアウト
        lyt_hBox_radioButton.addWidget(radioButton_vertex)
        lyt_hBox_radioButton.addWidget(radioButton_edge)
        lyt_hBox_radioButton.addWidget(radioButton_face)

        lyt_grid_main = QtWidgets.QGridLayout()
        lyt_grid_main.addWidget(label_referenceName, 0, 0)
        lyt_grid_main.addLayout(lyt_hBox_referenceName, 0, 1)
        lyt_grid_main.addWidget(self.txtLine_referenceInfo, 1, 1)
        lyt_grid_main.addWidget(label_percentage, 2, 0)
        lyt_grid_main.addLayout(lyt_hBox_percentage, 2, 1)
        lyt_grid_main.addWidget(label_componentsSelect, 3, 0)
        lyt_grid_main.addLayout(lyt_hBox_radioButton, 3, 1)

        lyt_vBox_button = QtWidgets.QVBoxLayout() #リスト横ボタン用レイアウト
        lyt_vBox_button.addWidget(button_exclusion)
        lyt_vBox_button.addWidget(button_reset)
        lyt_vBox_button.addWidget(button_clear)
        lyt_vBox_button.addWidget(self.label_listTotal)
        lyt_vBox_button.addItem(spacer_buttonLayout)
        lyt_vBox_button.addWidget(self.checkBox_highlight)

        lyt_hBox_componentsList = QtWidgets.QHBoxLayout()
        lyt_hBox_componentsList.addWidget(self.listArea_componentNames, 4)
        lyt_hBox_componentsList.addLayout(lyt_vBox_button, 1)

        lyt_vBox_main = QtWidgets.QVBoxLayout()
        lyt_vBox_main.addLayout(lyt_grid_main)
        lyt_vBox_main.addWidget(self.checkBox_normal)
        lyt_vBox_main.addWidget(self.checkBox_duplicate)
        lyt_vBox_main.addWidget(self.checkBox_group)
        lyt_vBox_main.addLayout(lyt_hBox_componentsList)
        lyt_vBox_main.addWidget(button_placement)

        lyt_widget = QtWidgets.QWidget()
        lyt_widget.setLayout(lyt_vBox_main)
        self.setCentralWidget(lyt_widget)


    def initialize_settings(self):
        self.vertex_namesAll = [] #頂点名全て
        self.edge_namesAll = [] #エッジ名全て
        self.face_namesAll = [] #フェース名全て
        self.vertex_positionsAll = [] #頂点位置全て
        self.edge_positionsAll = [] #エッジ位置全て
        self.face_positionsAll = [] #フェース位置全て
        self.vertex_anglesAll = [] #頂点角度全て
        self.face_anglesAll = [] #フェース角度全て


    def register_referenceObject(self):
        selected_object = cmds.ls(sl = True)
        self.initialize_settings()

        if not selected_object:
            cmds.confirmDialog(b = "OK", icn = 'critical', m = "何も選択されていません、登録に失敗しました。", t = "ERROR: Placement Tool")

        elif len(selected_object) != 1:
            cmds.confirmDialog(b = "OK", icn = 'critical', m = "複数登録することはできません、登録に失敗しました。", t = "ERROR: Placement Tool")

        elif cmds.objectType(cmds.listRelatives(selected_object[0], f = True, s = True)) == 'mesh':
            totalNum_vertex = cmds.polyEvaluate(selected_object[0], v = True) #頂点総数
            totalNum_edge = cmds.polyEvaluate(selected_object[0], e = True) #エッジ総数
            totalNum_face = cmds.polyEvaluate(selected_object[0], f = True) #フェース総数

            self.txtLine_referenceName.setText(selected_object[0])
            self.txtLine_referenceInfo.setText(f"頂点数: {totalNum_vertex} / エッジ数: {totalNum_edge} / フェース数: {totalNum_face}")

            for one_vertexNum in range(totalNum_vertex):
                self.vertex_namesAll.append(f"{selected_object[0]}.vtx[{one_vertexNum}]") #頂点総数から頂点名に変換
            else:
                for one_vertex in self.vertex_namesAll:
                    self.vertex_positionsAll.append(cmds.xform(one_vertex, q = True, t = True, ws = True)) #全頂点のWorld位置を特定
                    normal_vertex = cmds.polyNormalPerVertex(one_vertex, q = True, xyz = True) #頂点の法線を取得
                    num_connectedEdges = len(normal_vertex) / 3 #頂点に接続しているエッジの本数
                    normalX_vertex = sum(normal_vertex[::3]) / num_connectedEdges #xyzそれぞれの平均を求める、接続しているエッジの本数分値が検出される&ハードエッジの場合値が全て異なるため
                    normalY_vertex = sum(normal_vertex[1::3]) / num_connectedEdges
                    normalZ_vertex = sum(normal_vertex[2::3]) / num_connectedEdges
                    angleX_vertex = 90 - math.degrees(math.atan2(normalY_vertex, math.sqrt(normalX_vertex ** 2 + normalZ_vertex ** 2))) #角度を求める
                    angleY_vertex = math.degrees(math.atan2(normalX_vertex, normalZ_vertex))
                    self.vertex_anglesAll.append([angleX_vertex, angleY_vertex, 0]) #Z軸回転は行わないのでゼロ

            for one_edgeNum in range(totalNum_edge):
                self.edge_namesAll.append(f"{selected_object[0]}.e[{one_edgeNum}]") #エッジ総数からエッジ名に変換
            else:
                for one_edge in self.edge_namesAll:
                    result_edge = cmds.xform(one_edge, q = True, t = True, ws = True) #1エッジあたり2頂点分のWorld位置が特定される(x1, y1, z1, x2, y2, z2)
                    self.edge_positionsAll.append([sum(result_edge[::3]) / 2, sum(result_edge[1::3]) / 2, sum(result_edge[2::3]) / 2]) #xyz別に分けて全エッジ位置を計算

            for one_faceNum in range(totalNum_face):
                self.face_namesAll.append(f"{selected_object[0]}.f[{one_faceNum}]") #フェース総数からフェース名に変換
            else:
                for one_face in self.face_namesAll:
                    result_face = cmds.xform(one_face, q = True, t = True, ws = True) #1フェースあたりn角形x3(1頂点のxyz)のWorld位置が特定される
                    nGon_face = len(result_face) / 3 #フェースが何角形であるか
                    self.face_positionsAll.append([sum(result_face[::3]) / nGon_face, sum(result_face[1::3]) / nGon_face, sum(result_face[2::3]) / nGon_face]) #xyz別に分けて全フェース位置を計算
                    normal_face = (cmds.polyInfo(one_face, fn = True))[0].split() #フェースの法線を取得
                    del normal_face[:2] #不要な項目を削除
                    normal_face = list(map(float, normal_face)) #項目をstrからfloatに変換
                    normalX_face = normal_face[0]
                    normalY_face = normal_face[1]
                    normalZ_face = normal_face[2]
                    angleX_face = 90 - math.degrees(math.atan2(normalY_face, math.sqrt(normalX_face ** 2 + normalZ_face ** 2)))
                    angleY_face = math.degrees(math.atan2(normalX_face, normalZ_face))
                    self.face_anglesAll.append([angleX_face, angleY_face, 0])

            if self.radioGroup_componentsSelect.checkedId() == 1: #頂点
                self.listArea_componentNames.clear() #項目をリセット
                self.listArea_componentNames.addItems(self.vertex_namesAll) #項目を追加し表示
            
            elif self.radioGroup_componentsSelect.checkedId() == 2: #エッジ
                self.listArea_componentNames.clear()
                self.listArea_componentNames.addItems(self.edge_namesAll)
            
            elif self.radioGroup_componentsSelect.checkedId() == 3: #フェース
                self.listArea_componentNames.clear()
                self.listArea_componentNames.addItems(self.face_namesAll)

            self.label_listTotal.setText(f"配置場所数:\n{self.listArea_componentNames.count()}") #項目数表記を更新

            self.vertex_namesPositionsAll = dict(zip(self.vertex_namesAll, self.vertex_positionsAll)) #名称と位置を合わせて辞書化
            self.edge_namesPositionsAll = dict(zip(self.edge_namesAll, self.edge_positionsAll))
            self.face_namesPositionAll = dict(zip(self.face_namesAll, self.face_positionsAll))
            self.vertex_namesAnglesAll = dict(zip(self.vertex_namesAll, self.vertex_anglesAll)) #名称と角度を合わせて辞書化
            self.face_namesAnglesAll = dict(zip(self.face_namesAll, self.face_anglesAll))
        else:
            cmds.confirmDialog(b = "OK", icn = 'critical', m = "メッシュ以外登録することはできません、登録に失敗しました。", t = "ERROR: Placement Tool")


    def placement_objects(self):
        selected_objects = cmds.ls(sl = True, fl = True)
        toBePlaced_objects = list(selected_objects) #配置予定のオブジェクト群
        now_componentNames = [] #現在のコンポーネント名リストの中身

        for one_name in range(self.listArea_componentNames.count()):
            now_componentNames.append(self.listArea_componentNames.item(one_name).text()) #現在のコンポーネント名リストの中身を取得し変換

        if not selected_objects:
            cmds.confirmDialog(b = "OK", icn = 'critical', m = "何も選択されていません、配置に失敗しました。", t = "ERROR: Placement Tool")
        else:
            if len(selected_objects) <= self.listArea_componentNames.count():
                if len(selected_objects) < self.listArea_componentNames.count() and self.checkBox_duplicate.isChecked(): #選択中のオブジェクト数が配置場所の総数を下回っており、かつ複製補完を行う場合
                    for i in range(self.listArea_componentNames.count() - len(selected_objects)):
                        num_random = int(random.uniform(0, len(selected_objects))) #選択中のオブジェクトの総数の範囲内でランダムな値
                        duplicated_object = cmds.duplicate(selected_objects[num_random]) #配置場所の総数に満たない分を選択中のオブジェクトからランダムに複製
                        toBePlaced_objects.append(duplicated_object[0])

                if self.radioGroup_componentsSelect.checkedId() == 1: #頂点
                    for one_object, one_name in zip(toBePlaced_objects, now_componentNames):
                        cmds.move(self.vertex_namesPositionsAll[one_name][0], self.vertex_namesPositionsAll[one_name][1], self.vertex_namesPositionsAll[one_name][2], one_object) #配置

                        if self.checkBox_normal.isChecked() == True:
                            cmds.rotate(self.vertex_namesAnglesAll[one_name][0], self.vertex_namesAnglesAll[one_name][1], self.vertex_namesAnglesAll[one_name][2], one_object) #回転
                
                elif self.radioGroup_componentsSelect.checkedId() == 2: #エッジ
                    for one_object, one_name in zip(toBePlaced_objects, now_componentNames):
                        cmds.move(self.edge_namesPositionsAll[one_name][0], self.edge_namesPositionsAll[one_name][1], self.edge_namesPositionsAll[one_name][2], one_object)
                
                elif self.radioGroup_componentsSelect.checkedId() == 3: #フェース
                    for one_object, one_name in zip(toBePlaced_objects, now_componentNames):
                        cmds.move(self.face_namesPositionAll[one_name][0], self.face_namesPositionAll[one_name][1], self.face_namesPositionAll[one_name][2], one_object)

                        if self.checkBox_normal.isChecked() == True:
                            cmds.rotate(self.face_namesAnglesAll[one_name][0], self.face_namesAnglesAll[one_name][1], self.face_namesAnglesAll[one_name][2], one_object)

                if self.checkBox_group.isChecked() == True:
                    group_placedObjects = cmds.group(toBePlaced_objects, n = "placedObjects") #グループ化
                    cmds.select(group_placedObjects)
                else:
                    cmds.select(toBePlaced_objects) #全選択
            
            elif len(selected_objects) > self.listArea_componentNames.count():
                cmds.confirmDialog(b = "OK", icn = 'warning', m = "選択中のオブジェクト数が、配置場所の総数を上回っています", t = "WARNING: Placement Tool")


    def exclusion_componentNames(self):
        selected_items = self.listArea_componentNames.selectedItems() #リストで選択中の項目

        for one_item in selected_items:
            self.listArea_componentNames.takeItem(self.listArea_componentNames.row(one_item)) #項目を削除
        else:
            self.label_listTotal.setText(f"配置場所数:\n{self.listArea_componentNames.count()}")


    def clear_componentNames(self):
        self.spinBox_percentage.setValue(100)
        self.slider_percentage.setValue(100)
        self.txtLine_referenceName.setText("")
        self.txtLine_referenceInfo.setText("")
        self.listArea_componentNames.clear()
        self.checkBox_highlight.setChecked(False)
        self.vertex_namesAll.clear()
        self.edge_namesAll.clear()
        self.face_namesAll.clear()
        self.vertex_positionsAll.clear()
        self.edge_positionsAll.clear()
        self.face_positionsAll.clear()
        self.label_listTotal.setText(f"配置場所数:\n{self.listArea_componentNames.count()}")


    def reset_componentNames_and_changed_radioGroup(self):
        self.spinBox_percentage.setValue(100) #配置割合をリセット
        self.slider_percentage.setValue(100)

        if self.radioGroup_componentsSelect.checkedId() == 1: #頂点
            self.checkBox_normal.setEnabled(True) #操作可
            self.listArea_componentNames.clear()
            self.listArea_componentNames.addItems(self.vertex_namesAll)
        
        elif self.radioGroup_componentsSelect.checkedId() == 2: #エッジ
            self.checkBox_normal.setEnabled(False) #操作不可
            self.listArea_componentNames.clear()
            self.listArea_componentNames.addItems(self.edge_namesAll)
        
        elif self.radioGroup_componentsSelect.checkedId() == 3: #フェース
            self.checkBox_normal.setEnabled(True)
            self.listArea_componentNames.clear()
            self.listArea_componentNames.addItems(self.face_namesAll)

        self.label_listTotal.setText(f"配置場所数:\n{self.listArea_componentNames.count()}")


    def valueUpdate_spinBox_percentage(self):
        value_now = self.spinBox_percentage.value() #spinBoxの現在の値を取得
        self.slider_percentage.setValue(value_now) #sliderの値を上書き
        self.update_componentNames()
    

    def valueUpdate_slider_percentage(self):
        value_now = self.slider_percentage.value() #sliderの現在の値を取得
        self.spinBox_percentage.setValue(value_now) #spinBoxの値を上書き
        self.update_componentNames()

    
    def update_componentNames(self):
        if self.radioGroup_componentsSelect.checkedId() == 1: #頂点
            sampled_items = random.sample(self.vertex_namesAll, int(len(self.vertex_namesAll) * (self.spinBox_percentage.value() / 100))) #配置割合分、要素をサンプリング
            self.listArea_componentNames.clear()
            self.listArea_componentNames.addItems(sampled_items)
                
        elif self.radioGroup_componentsSelect.checkedId() == 2: #エッジ
            sampled_items = random.sample(self.edge_namesAll, int(len(self.edge_namesAll) * (self.spinBox_percentage.value() / 100)))
            self.listArea_componentNames.clear()
            self.listArea_componentNames.addItems(sampled_items)
                
        elif self.radioGroup_componentsSelect.checkedId() == 3: #フェース
            sampled_items = random.sample(self.face_namesAll, int(len(self.face_namesAll) * (self.spinBox_percentage.value() / 100)))
            self.listArea_componentNames.clear()
            self.listArea_componentNames.addItems(sampled_items)

        self.label_listTotal.setText(f"配置場所数:\n{self.listArea_componentNames.count()}")


    def selected_listArea_componentNames(self):
        if self.checkBox_highlight.isChecked() == True:
            selected_componentNames = [one_item.text() for one_item in self.listArea_componentNames.selectedItems()] #コンポーネント名リストで選択中の項目名

            if self.radioGroup_componentsSelect.checkedId() == 1: #頂点
                cmds.selectMode(co = True)
                cmds.selectType(v = True) #頂点選択モードに切り替え

            elif self.radioGroup_componentsSelect.checkedId() == 2: #エッジ
                cmds.selectMode(co = True)
                cmds.selectType(eg = True) #エッジ選択モード
                
            elif self.radioGroup_componentsSelect.checkedId() == 3: #フェース
                cmds.selectMode(co = True)
                cmds.selectType(fc = True) #フェース選択モード

            cmds.select(selected_componentNames)


    def changed_checkBox_highlight(self):
        if self.checkBox_highlight.isChecked() == True:
            job_event = 'SelectionChanged' #選択が行われた際に実行
            job_action = self.jobAction_highlight
            self.scriptJob_highlight = cmds.scriptJob(e = [job_event, job_action], pro = True)
        else:
            cmds.scriptJob(k = self.scriptJob_highlight, f = True) #scriptJobの終了
    

    def jobAction_highlight(self):
        selected_component = cmds.ls(sl = True, fl = True)
        now_componentNames = []

        for one_name in range(self.listArea_componentNames.count()):
            now_componentNames.append(self.listArea_componentNames.item(one_name).text())

        self.listArea_componentNames.clearSelection() #コンポーネント名リスト上での選択をクリア
        self.listArea_componentNames.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection) #通常の複数選択を有効化

        for one_component in selected_component:
            if one_component in now_componentNames:
                index = now_componentNames.index(one_component) #ビューポート上で選択したコンポーネントがリスト上にも存在する場合インデックス番号を取得
                self.listArea_componentNames.setCurrentRow(index, QtCore.QItemSelectionModel.Select) #コンポーネント名リスト上で選択
        else:
            self.listArea_componentNames.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection) #Shift/Ctrlによる複数選択に戻す
    

    def closeEvent(self, event): #ウィンドウを閉じた際に実行
        if self.checkBox_highlight.isChecked() == True:
            cmds.scriptJob(k = self.scriptJob_highlight, f = True)


toolWindow = PlacementTool()
toolWindow.show()
