#For Autodesk Maya 2024, Encoding UTF-8
import maya.cmds as cmds
from PySide2 import QtWidgets
from maya.app.general import mayaMixin

class ObjectRenamer(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    def __init__(self):
        super(ObjectRenamer, self).__init__()
        self.toolUI()


    def toolUI(self):
        self.setGeometry(500, 300, 500, 530)
        self.setWindowTitle("Object Renamer")
        self.statusBar().showMessage("Last Updated: 2024.09.22   |   For: Maya 2024   |   Fuma Hara")

        menu_tool = QtWidgets.QMenu("Sub Tools") #メニュー項目
        action_menuTool = QtWidgets.QAction("Name Blocks Sort Tool", self)
        action_menuTool.triggered.connect(self.open_nameBlocksSortTool)
        menu_tool.addAction(action_menuTool)
        self.menuBar().addMenu(menu_tool) #メニューバーに追加

        self.txtLine_search = QtWidgets.QLineEdit(placeholderText = "検索するオブジェクト名を入力") #(txtLine全て)各入力欄
        self.txtLine_prefix = QtWidgets.QLineEdit(placeholderText = "プレフィックス", fixedHeight = 25) #fixedHeightで縦のサイズを指定
        self.txtLine_nameMain = QtWidgets.QLineEdit(placeholderText = "オブジェクト名", fixedHeight = 25)
        self.txtLine_suffix = QtWidgets.QLineEdit(placeholderText = "サフィックス", fixedHeight = 25)
        self.txtLine_repBefore = QtWidgets.QLineEdit(placeholderText = "置き換える文字列", enabled = False)
        self.txtLine_repAfter = QtWidgets.QLineEdit(placeholderText = "置き換え後", enabled = False)
        self.txtLine_addPrefix = QtWidgets.QLineEdit(placeholderText = "プレフィックスの先頭に追加する文字列", fixedHeight = 22)
        self.txtLine_addSuffix = QtWidgets.QLineEdit(placeholderText = "サフィックスの末尾に追加する文字列", fixedHeight = 22)

        self.listArea_before = QtWidgets.QListWidget() #リネーム前表示
        self.listArea_after = QtWidgets.QListWidget() #リネーム後表示
        self.listArea_before.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection) #Shift/Ctrlキーを利用した複数選択を有効化
        self.listArea_before.setDragDropMode(QtWidgets.QListWidget.InternalMove) #ドラッグ&ドロップを有効化

        button_search = QtWidgets.QPushButton("検索") #(button全て)各機能用ボタン
        button_register = QtWidgets.QPushButton("登録")
        button_preview = QtWidgets.QPushButton("変更をプレビュー")
        button_clearBefore = QtWidgets.QPushButton("クリア")
        button_clearAfter = QtWidgets.QPushButton("クリア")
        button_rename = QtWidgets.QPushButton("リネーム")
        button_search.clicked.connect(self.search_objectNames)
        button_register.clicked.connect(self.register_objectNames)
        button_preview.clicked.connect(self.preview_objectNames)
        button_clearBefore.clicked.connect(self.clear_txtList_before)
        button_clearAfter.clicked.connect(self.clear_txtList_after)
        button_rename.clicked.connect(self.rename_objectNames)

        self.cmbBox_prefix = QtWidgets.QComboBox() #(cmbBox全て)各機能設定用コンボボックス
        self.cmbBox_nameMain = QtWidgets.QComboBox()
        self.cmbBox_suffix = QtWidgets.QComboBox()
        self.cmbBox_underscore = QtWidgets.QComboBox()
        self.cmbBox_prefix.addItems(["自由入力", "数字"])
        self.cmbBox_nameMain.addItems(["自由入力", "そのまま", "全て大文字に変換", "全て小文字に変換", "タイトルケースに変換", "指定の文字列を置き換える"])
        self.cmbBox_suffix.addItems(["自由入力", "数字"])
        self.cmbBox_underscore.addItems(["追加しない", "[プレフィックス] _ [オブジェクト名][サフィックス]", "[プレフィックス][オブジェクト名] _ [サフィックス]", 
                                     "[プレフィックス] _ [オブジェクト名] _ [サフィックス]"])
        self.cmbBox_prefix.currentIndexChanged.connect(self.change_prefixComboBox) #(currentIndexChanged.connect全て)項目が変更された際の処理
        self.cmbBox_nameMain.currentIndexChanged.connect(self.change_nameComboBox)
        self.cmbBox_suffix.currentIndexChanged.connect(self.change_suffixComboBox)

        label_digitPrefix = QtWidgets.QLabel("桁数") #(label全て)各ラベル
        label_firstPrefix = QtWidgets.QLabel("最初の値")
        label_digitSuffix = QtWidgets.QLabel("桁数")
        label_firstSuffix = QtWidgets.QLabel("最初の値")
        label_underscore = QtWidgets.QLabel("文字列の間にアンダーバーを追加")

        self.spnBox_digitPrefix = QtWidgets.QSpinBox(minimum = 1, maximum = 8, enabled = False) #桁数、プレフィックス用
        self.spnBox_firstPrefix = QtWidgets.QSpinBox(minimum = 0, maximum = 9999999, enabled = False) #最初の値、プレフィックス用
        self.spnBox_digitSuffix = QtWidgets.QSpinBox(minimum = 1, maximum = 8, enabled = False) #桁数、サフィックス用
        self.spnBox_firstSuffix = QtWidgets.QSpinBox(minimum = 0, maximum = 9999999, enabled = False) #最初の値、サフィックス用

        radioGrp_replace = QtWidgets.QButtonGroup(self) #文字列置き換え設定用ラジオボタン
        self.radioBtn01 = QtWidgets.QRadioButton("大/小文字を区別", enabled = False, checked = True)
        self.radioBtn02 = QtWidgets.QRadioButton("区別しない", enabled = False)
        radioGrp_replace.addButton(self.radioBtn01)
        radioGrp_replace.addButton(self.radioBtn02)

        lyt_hBox_search = QtWidgets.QHBoxLayout() #検索項目用レイアウト
        lyt_hBox_search.addWidget(self.txtLine_search)
        lyt_hBox_search.addWidget(button_search)

        lyt_hBox_listArea = QtWidgets.QHBoxLayout() #リネーム前後表示用レイアウト
        lyt_hBox_listArea.addWidget(self.listArea_before)
        lyt_hBox_listArea.addWidget(self.listArea_after)

        lyt_hBox_button = QtWidgets.QHBoxLayout() #リネーム前後表示操作ボタン用レイアウト
        lyt_hBox_button.addWidget(button_register, stretch = 3) #stretchでボタンの横サイズを比率で指定
        lyt_hBox_button.addWidget(button_clearBefore, stretch = 1)
        lyt_hBox_button.addWidget(button_preview, stretch = 3)
        lyt_hBox_button.addWidget(button_clearAfter, stretch = 1)

        lyt_grid_optionPrefix = QtWidgets.QGridLayout() #プレフィックス数字設定用レイアウト
        lyt_grid_optionPrefix.addWidget(label_digitPrefix, 0, 0)
        lyt_grid_optionPrefix.addWidget(self.spnBox_digitPrefix, 0, 1)
        lyt_grid_optionPrefix.addWidget(label_firstPrefix, 1, 0)
        lyt_grid_optionPrefix.addWidget(self.spnBox_firstPrefix, 1, 1)

        lyt_grid_optionNameMain = QtWidgets.QGridLayout() #オブジェクト名置き換え用レイアウト
        lyt_grid_optionNameMain.addWidget(self.txtLine_repBefore, 0, 0)
        lyt_grid_optionNameMain.addWidget(self.txtLine_repAfter, 0, 1)
        lyt_grid_optionNameMain.addWidget(self.radioBtn01, 1, 0)
        lyt_grid_optionNameMain.addWidget(self.radioBtn02, 1, 1)

        lyt_grid_optionSuffix = QtWidgets.QGridLayout() #サフィックス数字設定用レイアウト
        lyt_grid_optionSuffix.addWidget(label_digitSuffix, 0, 0)
        lyt_grid_optionSuffix.addWidget(self.spnBox_digitSuffix, 0, 1)
        lyt_grid_optionSuffix.addWidget(label_firstSuffix, 1, 0)
        lyt_grid_optionSuffix.addWidget(self.spnBox_firstSuffix, 1, 1)

        lyt_vBox_prefix = QtWidgets.QVBoxLayout() #プレフィックス設定用レイアウト
        lyt_vBox_prefix.addWidget(self.cmbBox_prefix)
        lyt_vBox_prefix.addWidget(self.txtLine_prefix)
        lyt_vBox_prefix.addLayout(lyt_grid_optionPrefix)

        lyt_vBox_nameMain = QtWidgets.QVBoxLayout() #オブジェクト名設定用レイアウト
        lyt_vBox_nameMain.addWidget(self.cmbBox_nameMain)
        lyt_vBox_nameMain.addWidget(self.txtLine_nameMain)
        lyt_vBox_nameMain.addLayout(lyt_grid_optionNameMain)

        lyt_vBox_suffix = QtWidgets.QVBoxLayout() #サフィックス設定用レイアウト
        lyt_vBox_suffix.addWidget(self.cmbBox_suffix)
        lyt_vBox_suffix.addWidget(self.txtLine_suffix)
        lyt_vBox_suffix.addLayout(lyt_grid_optionSuffix)

        lyt_hBox_nameSetting = QtWidgets.QHBoxLayout() #プレフィックス・オブジェクト名・サフィックス配置用レイアウト
        lyt_hBox_nameSetting.addLayout(lyt_vBox_prefix)
        lyt_hBox_nameSetting.addLayout(lyt_vBox_nameMain)
        lyt_hBox_nameSetting.addLayout(lyt_vBox_suffix)
        lyt_hBox_nameSetting.setStretch(0, 1)
        lyt_hBox_nameSetting.setStretch(1, 2)
        lyt_hBox_nameSetting.setStretch(2, 1)

        lyt_form_underscore = QtWidgets.QFormLayout() #アンダーバー設定用レイアウト
        lyt_form_underscore.addRow(label_underscore, self.cmbBox_underscore)
        lyt_form_underscore.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow) #ウィンドウの横幅に合わせる

        lyt_hBox_additional = QtWidgets.QHBoxLayout() #追加文字列設定用レイアウト
        lyt_hBox_additional.addWidget(self.txtLine_addPrefix)
        lyt_hBox_additional.addWidget(self.txtLine_addSuffix)

        lyt_vBox_main = QtWidgets.QVBoxLayout() #全てまとめたレイアウト
        lyt_vBox_main.addLayout(lyt_hBox_search)
        lyt_vBox_main.addLayout(lyt_hBox_listArea)
        lyt_vBox_main.addLayout(lyt_hBox_button)
        lyt_vBox_main.addLayout(lyt_hBox_nameSetting)
        lyt_vBox_main.addLayout(lyt_form_underscore)
        lyt_vBox_main.addLayout(lyt_hBox_additional)
        lyt_vBox_main.addWidget(button_rename)

        lyt_widget = QtWidgets.QWidget()
        lyt_widget.setLayout(lyt_vBox_main)
        self.setCentralWidget(lyt_widget) #CentralWidgetに配置

        self.names_before = [] #名前のリスト、リネーム前


    def search_objectNames(self):
        objects01_ls = cmds.ls(typ = ['mesh', 'nurbsSurface']) #アウトライナに存在する全てのメッシュ＆NURBSサーフェス
        objects02_lr = cmds.listRelatives(objects01_ls, p = True) #オブジェクト名に変換
        name_search = self.txtLine_search.text() #検索欄に入力した内容
        list_result = [] #検索結果を格納するリスト

        for one_result in objects02_lr:
            if name_search.lower() in one_result.lower(): #両者共に小文字に変換し比較
                list_result.append(one_result)
        else:
            cmds.select(list_result) #検索結果を選択する


    def register_objectNames(self):
        selected_objects = cmds.ls(sl = True) #選択中のオブジェクト

        for one_obj in selected_objects:
            if one_obj not in self.names_before:
                self.names_before.append(one_obj) #選択中のオブジェクトでリネーム前のリストに既に登録されていなければ追加
        else:
            self.listArea_before.clear()
            self.listArea_before.addItems(self.names_before) #一度クリアしてから再表示


    def preview_objectNames(self):
        self.names_after = [] #名前のリスト、リネーム後プレビュー
        txt_prefix = self.txtLine_prefix.text() #プレフィックス
        txt_nameMain = self.txtLine_nameMain.text() #オブジェクト名
        txt_suffix = self.txtLine_suffix.text() #サフィックス
        txt_repBefore = self.txtLine_repBefore.text() #置き換える文字列
        txt_repAfter = self.txtLine_repAfter.text() #置き換え後
        txt_addPrefix = self.txtLine_addPrefix.text() #プレフィックス先頭の追加語句
        txt_addSuffix = self.txtLine_addSuffix.text() #サフィックス末尾の追加語句
        digit_prefix = self.spnBox_digitPrefix.value() #桁数、プレフィックス
        first_prefix = self.spnBox_firstPrefix.value() #最初の値、プレフィックス
        digit_suffix = self.spnBox_digitSuffix.value() #桁数、サフィックス
        first_suffix = self.spnBox_firstSuffix.value() #最初の値、サフィックス
        select_indexNum01 = self.listArea_before.selectedIndexes() #リネーム前のリストで選択中のアイテムのインデックス番号
        select_indexNum02 = [] #検出できる形に変換したインデックス番号のリスト

        self.names_before.clear()
        self.names_after.clear()
        self.listArea_after.clear()

        for one_name in range(self.listArea_before.count()):
            dd_name = self.listArea_before.item(one_name)
            self.names_before.append(dd_name.text()) #ドラッグ&ドロップで並び順が変更されている事を考慮して再登録

        for idxNum in select_indexNum01:
            select_indexNum02.append(idxNum.row()) #検出できる形に変換しインデックス番号を移動
        
        for one_name in self.names_before:
            if self.names_before.index(one_name) in select_indexNum02: #リネーム前のリストで選択中のアイテムであるか
                if self.cmbBox_nameMain.currentText() == "そのまま": #以下オブジェクト名の設定
                    txt_nameMain = one_name

                elif self.cmbBox_nameMain.currentText() == "全て大文字に変換":
                    txt_nameMain = one_name.upper()

                elif self.cmbBox_nameMain.currentText() == "全て小文字に変換":
                    txt_nameMain = one_name.lower()      

                elif self.cmbBox_nameMain.currentText() == "タイトルケースに変換":
                    txt_nameMain = one_name.title()

                elif self.cmbBox_nameMain.currentText() == "指定の文字列を置き換える":
                    if self.radioBtn01.isChecked():
                        txt_nameMain = one_name.replace(txt_repBefore, txt_repAfter)

                    elif self.radioBtn02.isChecked():
                        mem_name = one_name #そのままのオブジェクト名を一時保存する
                        rep_name = one_name.lower().replace(txt_repBefore.lower(), txt_repAfter)

                        if mem_name.lower() == rep_name.lower(): #replace前後で変化があるか否か
                            txt_nameMain = mem_name
                        else:
                            txt_nameMain = rep_name

                if self.cmbBox_prefix.currentText() == "数字": #以下プレフィックスとサフィックスの数字の設定
                    txt_prefix = str(first_prefix).zfill(digit_prefix)
                    first_prefix += 1
                
                if self.cmbBox_suffix.currentText() == "数字":
                    txt_suffix = str(first_suffix).zfill(digit_suffix)
                    first_suffix += 1

                if self.cmbBox_underscore.currentText() == "追加しない": #以下アンダーバーの設定
                    name_convert = txt_prefix + txt_nameMain + txt_suffix

                elif self.cmbBox_underscore.currentText() == "[プレフィックス] _ [オブジェクト名][サフィックス]":
                    name_convert = txt_prefix + "_" + txt_nameMain + txt_suffix

                elif self.cmbBox_underscore.currentText() == "[プレフィックス][オブジェクト名] _ [サフィックス]":
                    name_convert = txt_prefix + txt_nameMain + "_" + txt_suffix

                elif self.cmbBox_underscore.currentText() == "[プレフィックス] _ [オブジェクト名] _ [サフィックス]":
                    name_convert = txt_prefix + "_" + txt_nameMain + "_" + txt_suffix

                name_convert = txt_addPrefix + name_convert + txt_addSuffix #プレフィックス先頭、サフィックス末尾の追加の文字列を追加
                self.names_after.append(name_convert)              
            else:
                self.names_after.append(one_name)
        else:
            self.listArea_after.addItems(self.names_after)


    def rename_objectNames(self):
        names_updated = [] #リネーム後にリネーム前のリストへ更新した名前を移動する前に一時保存するリスト

        for old_name, new_name in zip(self.names_before, self.names_after):
            cmds.select(old_name) #同一名称が存在しないように自動で番号が追加された際に、検出ミスが発生するのを防ぐため
            cmds.rename(old_name, new_name)
            object_renamed = cmds.ls(sl = True)
            names_updated.extend(object_renamed)
        else:
            cmds.select(cl = True)
            self.names_before = names_updated
            self.listArea_before.clear()
            self.listArea_after.clear()
            self.listArea_before.addItems(self.names_before)


    def clear_txtList_before(self):
        self.names_before.clear()
        self.listArea_before.clear() #表示も中のリストもクリア


    def clear_txtList_after(self):
        self.names_after.clear()
        self.listArea_after.clear()


    def open_nameBlocksSortTool(self):
        toolWindow_sub = NameBlocksSortTool()
        toolWindow_sub.show()


    def change_prefixComboBox(self):
        if self.cmbBox_prefix.currentText() == "自由入力":
            self.txtLine_prefix.setEnabled(True) #操作可
            self.spnBox_digitPrefix.setEnabled(False) #操作不可
            self.spnBox_firstPrefix.setEnabled(False)
        
        elif self.cmbBox_prefix.currentText() == "数字":
            self.txtLine_prefix.setEnabled(False)
            self.spnBox_digitPrefix.setEnabled(True)
            self.spnBox_firstPrefix.setEnabled(True)
    

    def change_nameComboBox(self):
        if self.cmbBox_nameMain.currentText() == "自由入力":
            self.txtLine_nameMain.setEnabled(True)
            self.txtLine_repBefore.setEnabled(False)
            self.txtLine_repAfter.setEnabled(False)
            self.radioBtn01.setEnabled(False)
            self.radioBtn02.setEnabled(False)

        elif self.cmbBox_nameMain.currentText() == "指定の文字列を置き換える":
            self.txtLine_nameMain.setEnabled(False)
            self.txtLine_repBefore.setEnabled(True)
            self.txtLine_repAfter.setEnabled(True)
            self.radioBtn01.setEnabled(True)
            self.radioBtn02.setEnabled(True)
        
        else:
            self.txtLine_nameMain.setEnabled(False)
            self.txtLine_repBefore.setEnabled(False)
            self.txtLine_repAfter.setEnabled(False)
            self.radioBtn01.setEnabled(False)
            self.radioBtn02.setEnabled(False)
    

    def change_suffixComboBox(self):
        if self.cmbBox_suffix.currentText() == "自由入力":
            self.txtLine_suffix.setEnabled(True)
            self.spnBox_digitSuffix.setEnabled(False)
            self.spnBox_firstSuffix.setEnabled(False)
        
        elif self.cmbBox_suffix.currentText() == "数字":
            self.txtLine_suffix.setEnabled(False)
            self.spnBox_digitSuffix.setEnabled(True)
            self.spnBox_firstSuffix.setEnabled(True)


class NameBlocksSortTool(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    def __init__(self):
        super(NameBlocksSortTool, self).__init__()
        self.toolUI()


    def toolUI(self):
        self.setGeometry(500, 300, 440, 250)
        self.setWindowTitle("Name Blocks Sort Tool - Object Renamer")
        self.statusBar().showMessage("Last Updated: 2024.09.22   |   For: Maya 2024   |   Fuma Hara")

        label_message = QtWidgets.QLabel("※本ツールはアンダーバーで区切られた名前の各ブロックを並べ替えることができます")

        self.txtLine_before = QtWidgets.QLineEdit(placeholderText = "並べ替え前", readOnly = True, fixedHeight = 25) #(txtLine全て)オブジェクト名の前後表示
        self.txtLine_after = QtWidgets.QLineEdit(placeholderText = "並べ替え後(プレビュー)", readOnly = True, fixedHeight = 25)

        self.listArea_nameBlocks = QtWidgets.QListWidget() #名前のブロックを入れ替えるためのリスト
        self.listArea_nameBlocks.setFlow(QtWidgets.QListView.LeftToRight) #リストを横向きの左から右に並ぶ形式に変更
        self.listArea_nameBlocks.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection) #Shift/Ctrlキーを利用した複数選択を有効化
        self.listArea_nameBlocks.setDragDropMode(QtWidgets.QListWidget.InternalMove) #ドラッグ&ドロップを有効化

        button_register = QtWidgets.QPushButton("登録") #(button全て)各機能用ボタン
        button_preview = QtWidgets.QPushButton("変更をプレビュー")
        button_clear = QtWidgets.QPushButton("クリア")
        button_rename = QtWidgets.QPushButton("リネーム")
        button_register.clicked.connect(self.register_nameBlocks)
        button_preview.clicked.connect(self.preview_nameBlocks)
        button_clear.clicked.connect(self.clear_nameBlocks)
        button_rename.clicked.connect(self.rename_nameBlocks)

        lyt_hBox_button = QtWidgets.QHBoxLayout() #ボタン用レイアウト
        lyt_hBox_button.addWidget(button_register)
        lyt_hBox_button.addWidget(button_preview)
        lyt_hBox_button.addWidget(button_clear)

        lyt_vBox_main = QtWidgets.QVBoxLayout() #全てまとめたレイアウト
        lyt_vBox_main.addWidget(label_message)
        lyt_vBox_main.addWidget(self.txtLine_before)
        lyt_vBox_main.addWidget(self.listArea_nameBlocks)
        lyt_vBox_main.addWidget(self.txtLine_after)
        lyt_vBox_main.addLayout(lyt_hBox_button)
        lyt_vBox_main.addWidget(button_rename)

        lyt_widget = QtWidgets.QWidget()
        lyt_widget.setLayout(lyt_vBox_main)
        self.setCentralWidget(lyt_widget) #CentralWidgetに配置

        self.nameBlocks_before = [] #並べ替え前の名前
        self.nameBlocks_after = [] #並べ替え後の名前


    def register_nameBlocks(self):
        selected_object = cmds.ls(sl = True) #選択中のオブジェクト
        
        if len(selected_object) == 0:
            cmds.confirmDialog(b = "OK", icn = 'critical', m = "何も選択されていません、登録に失敗しました", t = "ERROR: Name Blocks Sort Tool")
        
        elif len(selected_object) > 1:
            cmds.confirmDialog(b = "OK", icn = 'critical', m = "複数登録することはできません、登録に失敗しました", t = "ERROR: Name Blocks Sort Tool")

        else:
            self.nameBlocks_before.clear()
            self.nameBlocks_after.clear()
            self.listArea_nameBlocks.clear()
            self.txtLine_after.setText("")
            self.nameBlocks_before = selected_object[0].split("_") #アンダーバーで区切り、並べ替え前のリストに格納
            self.listArea_nameBlocks.addItems(self.nameBlocks_before) #並べ替えられるようにListWidgetに登録
            self.txtLine_before.setText(selected_object[0]) #変更前の名前を表示
    

    def preview_nameBlocks(self):
        self.nameBlocks_after.clear()

        for one_block in range(self.listArea_nameBlocks.count()):
            block = self.listArea_nameBlocks.item(one_block)
            self.nameBlocks_after.append(block.text()) #並べ替えた名前を並べ替え後のリストに格納
        else:
            name_joined = ("_".join(self.nameBlocks_after)) #アンダーバーを挟んで繋げる
            self.txtLine_after.setText(name_joined) #変更後の名前を表示
    

    def clear_nameBlocks(self):
        self.nameBlocks_before.clear() #全項目をクリア
        self.nameBlocks_after.clear()
        self.txtLine_before.setText("")
        self.txtLine_after.setText("")
        self.listArea_nameBlocks.clear()
    

    def rename_nameBlocks(self):
        name_old = self.txtLine_before.text() #変更前の名前

        self.nameBlocks_after.clear()

        for one_block in range(self.listArea_nameBlocks.count()):
            block = self.listArea_nameBlocks.item(one_block)
            self.nameBlocks_after.append(block.text())
        else:
            name_new = ("_".join(self.nameBlocks_after))

        cmds.rename(name_old, name_new)
        self.txtLine_before.setText("")
        self.txtLine_after.setText("")
        self.listArea_nameBlocks.clear()


toolWindow = ObjectRenamer()
toolWindow.show()
