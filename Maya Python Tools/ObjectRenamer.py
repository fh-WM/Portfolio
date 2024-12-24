#For Autodesk Maya 2024, Encoding UTF-8
import maya.cmds as cmds
from PySide2 import QtWidgets
from PySide2 import QtCore
from maya.app.general import mayaMixin

class ObjectRenamer(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    def __init__(self):
        super(ObjectRenamer, self).__init__()
        self.toolUI()
        self.initialize_settings()


    def toolUI(self):
        self.setGeometry(500, 300, 500, 550)
        self.setWindowTitle("Object Renamer")
        self.statusBar().showMessage("Last Updated: 2024.12.24   |   For: Maya 2024   |   Fuma Hara")

        menu_subTool = QtWidgets.QMenu("Sub Tool") #メニューバー項目
        action_subTool = QtWidgets.QAction("Name Blocks Sort Tool", self)
        action_subTool.triggered.connect(self.open_nameBlocksSortTool)
        menu_subTool.addAction(action_subTool)
        self.menuBar().addMenu(menu_subTool) #メニューバーに追加

        menu_reset = QtWidgets.QMenu("Reset")
        action_reset_prefix = QtWidgets.QAction("プレフィックス項目をリセット", self)
        action_reset_mainName = QtWidgets.QAction("オブジェクト名項目をリセット", self)
        action_reset_suffix = QtWidgets.QAction("サフィックス項目をリセット", self)
        action_reset_options = QtWidgets.QAction("その他項目をリセット", self)
        action_reset_search = QtWidgets.QAction("検索項目をリセット", self)
        action_reset_all = QtWidgets.QAction("全てリセット", self)
        action_reset_prefix.triggered.connect(self.reset_prefix)
        action_reset_mainName.triggered.connect(self.reset_mainName)
        action_reset_suffix.triggered.connect(self.reset_suffix)
        action_reset_options.triggered.connect(self.reset_options)
        action_reset_search.triggered.connect(self.reset_search)
        action_reset_all.triggered.connect(self.reset_all)
        menu_reset.addActions([action_reset_prefix, action_reset_mainName, action_reset_suffix, action_reset_options, action_reset_search, action_reset_all])
        self.menuBar().addMenu(menu_reset)

        label_namesBefore = QtWidgets.QLabel("リネーム前")
        label_namesAfter = QtWidgets.QLabel("リネーム後(プレビュー)")
        label_prefixDigits = QtWidgets.QLabel("桁数")
        label_prefixFirst = QtWidgets.QLabel("最初の値")
        label_suffixDigits = QtWidgets.QLabel("桁数")
        label_suffixFirst = QtWidgets.QLabel("最初の値")
        label_underscore = QtWidgets.QLabel("文字列の間にアンダーバーを追加")

        self.txtLine_search = QtWidgets.QLineEdit(placeholderText = "検索するオブジェクト名を入力")
        self.txtLine_prefix = QtWidgets.QLineEdit(placeholderText = "プレフィックス", fixedHeight = 25) #fixedHeightで縦幅を指定
        self.txtLine_mainName = QtWidgets.QLineEdit(placeholderText = "オブジェクト名", fixedHeight = 25)
        self.txtLine_suffix = QtWidgets.QLineEdit(placeholderText = "サフィックス", fixedHeight = 25)
        self.txtLine_replaceBefore = QtWidgets.QLineEdit(placeholderText = "置き換える文字列", enabled = False)
        self.txtLine_replaceAfter = QtWidgets.QLineEdit(placeholderText = "置き換え後", enabled = False)
        self.txtLine_addBeforePrefix = QtWidgets.QLineEdit(placeholderText = "プレフィックスの前に追加する文字列", fixedHeight = 22)
        self.txtLine_addAfterSuffix = QtWidgets.QLineEdit(placeholderText = "サフィックスの後に追加する文字列", fixedHeight = 22)

        self.listArea_namesBefore = QtWidgets.QListWidget(selectionMode = QtWidgets.QAbstractItemView.ExtendedSelection) #リネーム前用リスト表示、Shift/Ctrlによる複数選択を有効化
        self.listArea_namesAfter = QtWidgets.QListWidget() #リネーム後(プレビュー)用リスト表示
        self.listArea_namesBefore.setDragDropMode(QtWidgets.QListWidget.InternalMove) #ドラッグ&ドロップによる並べ替えを有効化
        self.listArea_namesBefore.itemSelectionChanged.connect(self.selected_listArea_namesBefore)

        self.comboBox_search = QtWidgets.QComboBox(fixedWidth = 120) #fixedWidthで横幅を指定
        self.comboBox_prefix = QtWidgets.QComboBox()
        self.comboBox_mainName = QtWidgets.QComboBox()
        self.comboBox_suffix = QtWidgets.QComboBox()
        self.comboBox_underscore = QtWidgets.QComboBox()
        self.comboBox_search.addItems(["メッシュ", "NURBSサーフェス", "NURBSカーブ", "ジョイント", "ライト", "カメラ", "トランスフォーム"])
        self.comboBox_prefix.addItems(["自由入力", "数字"])
        self.comboBox_mainName.addItems(["自由入力", "そのまま", "全て大文字に変換", "全て小文字に変換", "タイトルケースに変換", "指定の文字列を置き換える"])
        self.comboBox_suffix.addItems(["自由入力", "数字"])
        self.comboBox_underscore.addItems(["追加しない", "[プレフィックス] _ [オブジェクト名][サフィックス]",
                                           "[プレフィックス][オブジェクト名] _ [サフィックス]", "[プレフィックス] _ [オブジェクト名] _ [サフィックス]"])
        self.comboBox_prefix.currentIndexChanged.connect(self.change_comboBox_prefix)
        self.comboBox_mainName.currentIndexChanged.connect(self.change_comboBox_mainName)
        self.comboBox_suffix.currentIndexChanged.connect(self.change_comboBox_suffix)

        self.spinBox_prefixDigits = QtWidgets.QSpinBox(minimum = 1, maximum = 8, enabled = False) #桁数、プレフィックス用
        self.spinBox_prefixFirst = QtWidgets.QSpinBox(minimum = 0, maximum = 9999999, enabled = False) #最初の値、プレフィックス用
        self.spinBox_suffixDigits = QtWidgets.QSpinBox(minimum = 1, maximum = 8, enabled = False) #桁数、サフィックス用
        self.spinBox_suffixFirst = QtWidgets.QSpinBox(minimum = 0, maximum = 9999999, enabled = False) #最初の値、サフィックス用

        self.checkBox_highlight = QtWidgets.QCheckBox("ハイライト")
        self.checkBox_replace = QtWidgets.QCheckBox("大文字/小文字を区別する", checked = True, enabled = False)
        self.checkBox_highlight.stateChanged.connect(self.change_checkBox_highlight)

        button_search = QtWidgets.QPushButton("検索", fixedWidth = 40)
        button_register = QtWidgets.QPushButton("登録")
        button_preview = QtWidgets.QPushButton("変更をプレビュー")
        button_exclusion = QtWidgets.QPushButton("除外")
        button_clearNamesBefore = QtWidgets.QPushButton("クリア", objectName = "Clear_Before")
        button_clearNamesAfter = QtWidgets.QPushButton("クリア", objectName = "Clear_After")
        button_rename = QtWidgets.QPushButton("リネーム")
        button_search.clicked.connect(self.search_objectNames)
        button_register.clicked.connect(self.register_objectNames)
        button_preview.clicked.connect(self.preview_objectNames)
        button_exclusion.clicked.connect(self.exclusion_namesBefore)
        button_clearNamesBefore.clicked.connect(self.clear_namesBeforeAfter)
        button_clearNamesAfter.clicked.connect(self.clear_namesBeforeAfter)
        button_rename.clicked.connect(self.rename_objectNames)

        lyt_hBox_search = QtWidgets.QHBoxLayout() #検索用レイアウト
        lyt_hBox_search.addWidget(self.txtLine_search)
        lyt_hBox_search.addWidget(self.comboBox_search)
        lyt_hBox_search.addWidget(button_search)

        lyt_hBox_namesBeforeLabel = QtWidgets.QHBoxLayout() #リネーム前ラベル用レイアウト
        lyt_hBox_namesBeforeLabel.addWidget(label_namesBefore, 1)
        lyt_hBox_namesBeforeLabel.addWidget(self.checkBox_highlight, 3)

        lyt_hBox_namesBeforeButton = QtWidgets.QHBoxLayout() #リネーム前表示下ボタン用レイアウト
        lyt_hBox_namesBeforeButton.addWidget(button_register, 3)
        lyt_hBox_namesBeforeButton.addWidget(button_exclusion, 1)
        lyt_hBox_namesBeforeButton.addWidget(button_clearNamesBefore, 1)

        lyt_hBox_namesAfterButton = QtWidgets.QHBoxLayout() #リネーム後表示下ボタン用レイアウト
        lyt_hBox_namesAfterButton.addWidget(button_preview, 4)
        lyt_hBox_namesAfterButton.addWidget(button_clearNamesAfter, 1)

        lyt_grid_namesBeforeAfter = QtWidgets.QGridLayout() #リネーム前後表示用レイアウト
        lyt_grid_namesBeforeAfter.addLayout(lyt_hBox_namesBeforeLabel, 0, 0)
        lyt_grid_namesBeforeAfter.addWidget(label_namesAfter, 0, 1)
        lyt_grid_namesBeforeAfter.addWidget(self.listArea_namesBefore, 1, 0)
        lyt_grid_namesBeforeAfter.addWidget(self.listArea_namesAfter, 1, 1)
        lyt_grid_namesBeforeAfter.addLayout(lyt_hBox_namesBeforeButton, 2, 0)
        lyt_grid_namesBeforeAfter.addLayout(lyt_hBox_namesAfterButton, 2, 1)

        lyt_grid_prefix = QtWidgets.QGridLayout() #プレフィックス用レイアウト
        lyt_grid_prefix.addWidget(self.comboBox_prefix, 0, 0, 1, 2) #グリッド位置＆縦横幾つグリッドを使用するか
        lyt_grid_prefix.addWidget(self.txtLine_prefix, 1, 0, 1, 2)
        lyt_grid_prefix.addWidget(label_prefixDigits, 2, 0)
        lyt_grid_prefix.addWidget(self.spinBox_prefixDigits, 2, 1)
        lyt_grid_prefix.addWidget(label_prefixFirst, 3, 0)
        lyt_grid_prefix.addWidget(self.spinBox_prefixFirst, 3, 1)

        lyt_grid_suffix = QtWidgets.QGridLayout() #サフィックス用レイアウト
        lyt_grid_suffix.addWidget(self.comboBox_suffix, 0, 0, 1, 2)
        lyt_grid_suffix.addWidget(self.txtLine_suffix, 1, 0, 1, 2)
        lyt_grid_suffix.addWidget(label_suffixDigits, 2, 0)
        lyt_grid_suffix.addWidget(self.spinBox_suffixDigits, 2, 1)
        lyt_grid_suffix.addWidget(label_suffixFirst, 3, 0)
        lyt_grid_suffix.addWidget(self.spinBox_suffixFirst, 3, 1)

        lyt_grid_mainName = QtWidgets.QGridLayout() #オブジェクト名用レイアウト
        lyt_grid_mainName.addWidget(self.comboBox_mainName, 0, 0, 1, 2)
        lyt_grid_mainName.addWidget(self.txtLine_mainName, 1, 0, 1, 2)
        lyt_grid_mainName.addWidget(self.txtLine_replaceBefore, 2, 0)
        lyt_grid_mainName.addWidget(self.txtLine_replaceAfter, 2, 1)
        lyt_grid_mainName.addWidget(self.checkBox_replace, 3, 0, 1, 2)

        lyt_hBox_nameSettings = QtWidgets.QHBoxLayout() #プレフィックス・オブジェクト名・サフィックス設定用レイアウト
        lyt_hBox_nameSettings.addLayout(lyt_grid_prefix, 1)
        lyt_hBox_nameSettings.addLayout(lyt_grid_mainName, 2)
        lyt_hBox_nameSettings.addLayout(lyt_grid_suffix, 1)

        lyt_form_underscore = QtWidgets.QFormLayout() #アンダーバー設定用レイアウト
        lyt_form_underscore.addRow(label_underscore, self.comboBox_underscore)
        lyt_form_underscore.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow) #ウィンドウの横幅に合わせる

        lyt_hBox_addBeforeAfter = QtWidgets.QHBoxLayout() #追加文字列設定用レイアウト
        lyt_hBox_addBeforeAfter.addWidget(self.txtLine_addBeforePrefix)
        lyt_hBox_addBeforeAfter.addWidget(self.txtLine_addAfterSuffix)

        lyt_vBox_main = QtWidgets.QVBoxLayout()
        lyt_vBox_main.addLayout(lyt_hBox_search)
        lyt_vBox_main.addLayout(lyt_grid_namesBeforeAfter)
        lyt_vBox_main.addLayout(lyt_hBox_nameSettings)
        lyt_vBox_main.addLayout(lyt_form_underscore)
        lyt_vBox_main.addLayout(lyt_hBox_addBeforeAfter)
        lyt_vBox_main.addWidget(button_rename)

        lyt_widget = QtWidgets.QWidget()
        lyt_widget.setLayout(lyt_vBox_main)
        self.setCentralWidget(lyt_widget)


    def initialize_settings(self):
        self.names_before = [] #リネーム前オブジェクト名リスト
        self.names_after = [] #リネーム後(プレビュー)オブジェクト名リスト


    def search_objectNames(self):
        object_types = ['mesh', 'nurbsSurface', 'nurbsCurve', 'joint', 'light', 'camera', 'transform'] #オブジェクトのタイプ
        text_search = self.txtLine_search.text() #検索欄に入力した内容
        search_results = cmds.listRelatives(cmds.ls(typ = object_types[self.comboBox_search.currentIndex()]), p = True) #検索結果
        results_toSelect = [] #検索結果から検索欄に入力した内容と合致したもの

        if not text_search:
            cmds.confirmDialog(b = "OK", icn = 'critical', m = "何も入力されていません、検索に失敗しました。", t = "ERROR: Object Renamer")

        elif search_results:
            for one_result in search_results:
                if text_search.lower() in one_result.lower(): #両者小文字に変換し比較し、リストに含まれていなかった場合追加登録
                    results_toSelect.append(one_result)
            else:
                cmds.select(results_toSelect)


    def register_objectNames(self):
        selected_objects = cmds.ls(sl = True)

        if not selected_objects:
            cmds.confirmDialog(b = "OK", icn = 'critical', m = "何も選択されていません、登録に失敗しました。", t = "ERROR: Object Renamer")
        else:
            for one_object in selected_objects:
                if one_object not in self.names_before:
                    self.names_before.append(one_object)
            else:
                self.listArea_namesBefore.clear()
                self.listArea_namesBefore.addItems(self.names_before)


    def preview_objectNames(self):
        text_prefix = self.txtLine_prefix.text() #プレフィックス
        text_mainName = self.txtLine_mainName.text() #オブジェクト名
        text_suffix = self.txtLine_suffix.text() #サフィックス
        text_replaceBefore = self.txtLine_replaceBefore.text() #置き換える文字列
        text_replaceAfter = self.txtLine_replaceAfter.text() #置き換え後
        text_addBeforePrefix = self.txtLine_addBeforePrefix.text() #プレフィックス前に追加する文字列
        text_addAfterSuffix = self.txtLine_addAfterSuffix.text() #サフィックス後に追加する文字列
        num_prefixDigits = self.spinBox_prefixDigits.value() #桁数、プレフィックス
        num_prefixFirst = self.spinBox_prefixFirst.value() #最初の値、プレフィックス
        num_suffixDigits = self.spinBox_suffixDigits.value() #桁数、サフィックス
        num_suffixFirst = self.spinBox_suffixFirst.value() #最初の値、サフィックス
        selected_namesBefore = [one_item.text() for one_item in self.listArea_namesBefore.selectedItems()] #リネーム前リストで選択中の項目
        
        self.initialize_settings()
        self.listArea_namesAfter.clear()

        for one_name in range(self.listArea_namesBefore.count()):
            self.names_before.append(self.listArea_namesBefore.item(one_name).text()) #除外や並べ替えを加味してリストから再登録

        for one_name in self.names_before:
            if one_name in selected_namesBefore: #リネーム前リストで選択中の項目であるか否か
                if self.comboBox_mainName.currentText() == "そのまま": #以下オブジェクト名設定
                    text_mainName = one_name
                
                elif self.comboBox_mainName.currentText() == "全て大文字に変換":
                    text_mainName = one_name.upper()

                elif self.comboBox_mainName.currentText() == "全て小文字に変換":
                    text_mainName = one_name.lower()

                elif self.comboBox_mainName.currentText() == "タイトルケースに変換":
                    text_mainName = one_name.title()

                elif self.comboBox_mainName.currentText() == "指定の文字列を置き換える":
                    if self.checkBox_replace.isChecked() == True: #大文字/小文字を区別するか否か
                        text_mainName = one_name.replace(text_replaceBefore, text_replaceAfter)
                    else:
                        if one_name.lower() == one_name.lower().replace(text_replaceBefore.lower(), text_replaceAfter): #replace前後で変化しているか否か
                            text_mainName = one_name
                        else:
                            text_mainName = one_name.lower().replace(text_replaceBefore.lower(), text_replaceAfter)

                if self.comboBox_prefix.currentText() == "数字": #プレフィックス
                    text_prefix = str(num_prefixFirst).zfill(num_prefixDigits)
                    num_prefixFirst += 1

                if self.comboBox_suffix.currentText() == "数字": #サフィックス
                    text_suffix = str(num_suffixFirst).zfill(num_suffixDigits)
                    num_suffixFirst += 1

                if self.comboBox_underscore.currentIndex() == 0: #以下アンダーバー設定
                    name_preview = text_prefix + text_mainName + text_suffix

                elif self.comboBox_underscore.currentIndex() == 1:
                    name_preview = text_prefix + "_" + text_mainName + text_suffix

                elif self.comboBox_underscore.currentIndex() == 2:
                    name_preview = text_prefix + text_mainName + "_" + text_suffix

                elif self.comboBox_underscore.currentIndex() == 3:
                    name_preview = text_prefix + "_" + text_mainName + "_" + text_suffix

                name_preview = text_addBeforePrefix + name_preview + text_addAfterSuffix #プレフィックス前、サフィックス後文字列を追加
                self.names_after.append(name_preview)
            else:
                self.names_after.append(one_name)
        else:
            self.listArea_namesAfter.addItems(self.names_after)
        

    def rename_objectNames(self):
        names_renamed = [] #リネーム後オブジェクト名リスト

        if not self.names_after:
            cmds.confirmDialog(b = "OK", icn = 'warning', m = "先に「変更をプレビュー」を行ってください、リネームに失敗しました。", t = "ERROR: Object Renamer")
        else:
            for one_beforeName, one_afterName in zip(self.names_before, self.names_after):
                cmds.select(one_beforeName) #同一名称が存在しないようにMaya側で自動的に番号など追加された際に、検出ミスを防ぐため一時的に選択
                try:
                    cmds.rename(one_beforeName, one_afterName)
                except:
                    continue #リネーム不可オブジェクトなどが含まれていた場合に
                names_renamed.append(cmds.ls(sl = True)[0])
            else:
                cmds.select(cl = True)
                self.listArea_namesBefore.clear()
                self.listArea_namesAfter.clear()
                self.names_before = names_renamed #リネーム前オブジェクト名リストに移動
                self.names_after.clear()
                self.listArea_namesBefore.addItems(self.names_before)


    def exclusion_namesBefore(self):
        selected_items = self.listArea_namesBefore.selectedItems() #リストで選択中の項目

        for one_item in selected_items:
            self.listArea_namesBefore.takeItem(self.listArea_namesBefore.row(one_item)) #項目を削除


    def clear_namesBeforeAfter(self):
        name_clickedButton = self.sender().objectName() #クリックしたボタン名

        if name_clickedButton == "Clear_Before":
            self.names_before.clear()
            self.listArea_namesBefore.clear()
        else:
            self.names_after.clear()
            self.listArea_namesAfter.clear()


    def open_nameBlocksSortTool(self):
        toolWindow_sub = NameBlocksSortTool()
        toolWindow_sub.show()


    def reset_prefix(self):
        self.comboBox_prefix.setCurrentIndex(0)
        self.txtLine_prefix.setText("")
        self.spinBox_prefixDigits.setValue(1)
        self.spinBox_prefixFirst.setValue(0)
    

    def reset_mainName(self):
        self.comboBox_mainName.setCurrentIndex(0)
        self.txtLine_mainName.setText("")
        self.txtLine_replaceBefore.setText("")
        self.txtLine_replaceAfter.setText("")
        self.checkBox_replace.setChecked(True)
    

    def reset_suffix(self):
        self.comboBox_suffix.setCurrentIndex(0)
        self.txtLine_suffix.setText("")
        self.spinBox_suffixDigits.setValue(1)
        self.spinBox_suffixFirst.setValue(0)
    

    def reset_options(self):
        self.comboBox_underscore.setCurrentIndex(0)
        self.txtLine_addBeforePrefix.setText("")
        self.txtLine_addAfterSuffix.setText("")


    def reset_search(self):
        self.txtLine_search.setText("")
        self.comboBox_search.setCurrentIndex(0)
    

    def reset_all(self):
        self.reset_prefix()
        self.reset_mainName()
        self.reset_suffix()
        self.reset_options()
        self.reset_search()
        self.clear_namesBefore()
        self.clear_namesAfter()
        self.checkBox_highlight.setChecked(False)


    def change_comboBox_prefix(self):
        if self.comboBox_prefix.currentIndex() == 1: #数字
            self.txtLine_prefix.setEnabled(False) #操作不可
            self.spinBox_prefixDigits.setEnabled(True) #操作可
            self.spinBox_prefixFirst.setEnabled(True)
        else:
            self.txtLine_prefix.setEnabled(True)
            self.txtLine_prefix.setFocus()
            self.spinBox_prefixDigits.setEnabled(False)
            self.spinBox_prefixFirst.setEnabled(False)


    def change_comboBox_mainName(self):
        if self.comboBox_mainName.currentText() == "自由入力":
            self.txtLine_mainName.setEnabled(True)
            self.txtLine_mainName.setFocus()
            self.txtLine_replaceBefore.setEnabled(False)
            self.txtLine_replaceAfter.setEnabled(False)
            self.checkBox_replace.setEnabled(False)
        
        elif self.comboBox_mainName.currentText() == "指定の文字列を置き換える":
            self.txtLine_mainName.setEnabled(False)
            self.txtLine_replaceBefore.setEnabled(True)
            self.txtLine_replaceAfter.setEnabled(True)
            self.checkBox_replace.setEnabled(True)
        else:
            self.txtLine_mainName.setEnabled(False)
            self.txtLine_replaceBefore.setEnabled(False)
            self.txtLine_replaceAfter.setEnabled(False)
            self.checkBox_replace.setEnabled(False)


    def change_comboBox_suffix(self):
        if self.comboBox_suffix.currentIndex() == 1: #数字
            self.txtLine_suffix.setEnabled(False)
            self.spinBox_suffixDigits.setEnabled(True)
            self.spinBox_suffixFirst.setEnabled(True)
        else:
            self.txtLine_suffix.setEnabled(True)
            self.txtLine_suffix.setFocus()
            self.spinBox_suffixDigits.setEnabled(False)
            self.spinBox_suffixFirst.setEnabled(False)


    def selected_listArea_namesBefore(self):
        if self.checkBox_highlight.isChecked() == True:
            selected_namesBefore = [one_item.text() for one_item in self.listArea_namesBefore.selectedItems()]
            cmds.selectMode(o = True) #オブジェクト選択モードに切り替える
            cmds.select(selected_namesBefore)


    def change_checkBox_highlight(self):
        if self.checkBox_highlight.isChecked() == True:
            job_event = 'SelectionChanged' #選択が行われた際に実行
            job_action = self.jobAction_highlight
            self.scriptJob_highlight = cmds.scriptJob(e = [job_event, job_action], pro = True)
        else:
            cmds.scriptJob(k = self.scriptJob_highlight, f = True) #scriptJobを終了


    def jobAction_highlight(self):
        selected_objects = cmds.ls(sl = True)
        now_objectNames = []

        for one_name in range(self.listArea_namesBefore.count()):
            now_objectNames.append(self.listArea_namesBefore.item(one_name).text())

        self.listArea_namesBefore.clearSelection() #リネーム前オブジェクト名リストでの選択をクリア
        self.listArea_namesBefore.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection) #通常の複数選択を有効化

        for one_object in selected_objects:
            if one_object in now_objectNames:
                index = now_objectNames.index(one_object) #ビューポート上で選択したオブジェクトがリスト上にも存在する場合インデックス番号を取得
                self.listArea_namesBefore.setCurrentRow(index, QtCore.QItemSelectionModel.Select) #リネーム前オブジェクト名リスト上で選択
        else:
            self.listArea_namesBefore.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection) #Shift/Ctrlによる複数選択に戻す


    def closeEvent(self, event): #ウィンドウを閉じた際に実行
        if self.checkBox_highlight.isChecked() == True:
            cmds.scriptJob(k = self.scriptJob_highlight, f = True)


class NameBlocksSortTool(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    def __init__(self):
        super(NameBlocksSortTool, self).__init__()
        self.toolUI()
        self.initialize_settings()


    def toolUI(self):
        self.setGeometry(500, 300, 440, 250)
        self.setWindowTitle("Name Blocks Sort Tool - Object Renamer")
        self.statusBar().showMessage("Last Updated: 2024.12.24   |   For: Maya 2024   |   Fuma Hara")

        label_message = QtWidgets.QLabel("※本ツールはアンダーバーで区切られた文字列のブロックを並べ替えることができます")

        self.txtLine_nameBefore = QtWidgets.QLineEdit(placeholderText = "並べ替え前", readOnly = True, fixedHeight = 25)
        self.txtLine_nameAfter = QtWidgets.QLineEdit(placeholderText = "並べ替え後(プレビュー)", readOnly = True, fixedHeight = 25)

        self.listArea_nameBlocks = QtWidgets.QListWidget(flow = QtWidgets.QListView.LeftToRight, selectionMode = QtWidgets.QAbstractItemView.ExtendedSelection) #flowでリストを横向きに設定、Shift/Ctrlによる複数選択を有効化
        self.listArea_nameBlocks.setDragDropMode(QtWidgets.QListWidget.InternalMove) #ドラッグ&ドロップによる並べ替えを有効化

        button_register = QtWidgets.QPushButton("登録")
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

        lyt_vBox_main = QtWidgets.QVBoxLayout()
        lyt_vBox_main.addWidget(label_message)
        lyt_vBox_main.addWidget(self.txtLine_nameBefore)
        lyt_vBox_main.addWidget(self.listArea_nameBlocks)
        lyt_vBox_main.addWidget(self.txtLine_nameAfter)
        lyt_vBox_main.addLayout(lyt_hBox_button)
        lyt_vBox_main.addWidget(button_rename)

        lyt_widget = QtWidgets.QWidget()
        lyt_widget.setLayout(lyt_vBox_main)
        self.setCentralWidget(lyt_widget)


    def initialize_settings(self):
        self.nameBlocks_before = [] #並べ替え前の名称
        self.nameBlocks_after = [] #並べ替え後の名称


    def register_nameBlocks(self):
        selected_object = cmds.ls(sl = True)

        if not selected_object:
            cmds.confirmDialog(b = "OK", icn = 'critical', m = "何も選択されていません、登録に失敗しました", t = "ERROR: Name Blocks Sort Tool")

        elif len(selected_object) != 1:
            cmds.confirmDialog(b = "OK", icn = 'critical', m = "複数登録することはできません、登録に失敗しました", t = "ERROR: Name Blocks Sort Tool")
        else:
            self.initialize_settings()
            self.listArea_nameBlocks.clear()
            self.txtLine_nameBefore.setText(selected_object[0])
            self.txtLine_nameAfter.setText("")
            self.nameBlocks_before = selected_object[0].split("_") #アンダーバーで区切り登録
            self.listArea_nameBlocks.addItems(self.nameBlocks_before)


    def preview_nameBlocks(self):
        self.nameBlocks_after.clear()

        for one_block in range(self.listArea_nameBlocks.count()):
            self.nameBlocks_after.append(self.listArea_nameBlocks.item(one_block).text())
        else:
            self.txtLine_nameAfter.setText("_".join(self.nameBlocks_after)) #アンダーバーを間に挟んで繋げる


    def rename_nameBlocks(self):
        name_before = self.txtLine_nameBefore.text() #リネーム前
        self.nameBlocks_after.clear()

        for one_block in range(self.listArea_nameBlocks.count()):
            self.nameBlocks_after.append(self.listArea_nameBlocks.item(one_block).text())
        else:
            name_after = "_".join(self.nameBlocks_after)
            try:
                cmds.rename(name_before, name_after)
            except:
                None
            self.nameBlocks_before.clear()
            self.nameBlocks_after.clear()
            self.txtLine_nameBefore.setText("")
            self.txtLine_nameAfter.setText("")
            self.listArea_nameBlocks.clear()


    def clear_nameBlocks(self):
        self.nameBlocks_before.clear()
        self.nameBlocks_after.clear()
        self.txtLine_nameBefore.setText("")
        self.txtLine_nameAfter.setText("")
        self.listArea_nameBlocks.clear()


toolWindow = ObjectRenamer()
toolWindow.show()
