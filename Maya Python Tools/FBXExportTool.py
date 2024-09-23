#For Autodesk Maya 2024, Encoding UTF-8
import maya.cmds as cmds
import os
import platform
import subprocess
from PySide2 import QtWidgets
from maya.app.general import mayaMixin

class FBXExportTool(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    def __init__(self):
        super(FBXExportTool, self).__init__()
        self.toolUI()


    def toolUI(self):
        self.setGeometry(500, 300, 450, 350)
        self.setWindowTitle("FBX Export Tool")
        self.statusBar().showMessage("Last Updated: 2024.09.22   |   For: Maya 2024   |   Fuma Hara")

        label_message = QtWidgets.QLabel("※まず始めに書き出したいオブジェクトをビューもしくはアウトライナから選択してください") #(label全て)各ラベル
        label_fileName = QtWidgets.QLabel("ファイル名")
        label_filePath = QtWidgets.QLabel("書き出し先(ファイルパス)")

        self.cmbBox_fileName = QtWidgets.QComboBox() #ファイル名規則選択用コンボボックス
        self.cmbBox_fileName.addItems(["入力する", "そのまま"])
        self.cmbBox_fileName.currentIndexChanged.connect(self.change_fileNameComboBox) #項目が変更された際の処理

        self.txtLine_fileName = QtWidgets.QLineEdit() #(txtLine全て)各入力欄
        self.txtLine_filePath = QtWidgets.QLineEdit()
        self.txtLine_folderName = QtWidgets.QLineEdit(readOnly = True)
        self.txtLine_folderName.setText("←をチェックした場合のみ入力が可能です")

        self.chkBox_folderName = QtWidgets.QCheckBox("新規フォルダを作成 | 新規フォルダ名") #新規フォルダ作成有無用チェックボックス
        self.chkBox_folderName.stateChanged.connect(self.change_folderNameCheckBox)

        self.txtArea_log = QtWidgets.QTextEdit(readOnly = True)
        self.txtArea_log.setPlainText("・「新規フォルダを作成」にチェックを入れた場合、書き出し先に新規フォルダが作成され、その中に書き出したFBXファイルが格納されます")

        button_export = QtWidgets.QPushButton("書き出し") #(button全て)各機能用ボタン
        button_openDi = QtWidgets.QPushButton("ダイアログボックスを開く")
        button_openEx = QtWidgets.QPushButton("エクスプローラー/Finderを開く")
        button_clear = QtWidgets.QPushButton("ログをクリア")
        button_export.clicked.connect(self.export_fbxFile)
        button_openDi.clicked.connect(self.open_fileDialog)
        button_openEx.clicked.connect(self.open_explorerFinder)
        button_clear.clicked.connect(self.clear_logs)

        lyt_form_fileName = QtWidgets.QFormLayout() #ファイル名規則設定用レイアウト
        lyt_form_fileName.addRow(label_fileName, self.cmbBox_fileName)

        lyt_grid_setting = QtWidgets.QGridLayout() #ファイル名・ファイルパス用レイアウト
        lyt_grid_setting.addLayout(lyt_form_fileName, 0, 0)
        lyt_grid_setting.addWidget(self.txtLine_fileName, 0, 1)
        lyt_grid_setting.addWidget(label_filePath, 1, 0)
        lyt_grid_setting.addWidget(self.txtLine_filePath, 1, 1)

        lyt_form_folderName = QtWidgets.QFormLayout() #フォルダ名用レイアウト
        lyt_form_folderName.addRow(self.chkBox_folderName, self.txtLine_folderName)

        lyt_hBox_button = QtWidgets.QHBoxLayout() #ボタン用レイアウト
        lyt_hBox_button.addWidget(button_openDi)
        lyt_hBox_button.addWidget(button_openEx)
        lyt_hBox_button.addWidget(button_clear)

        lyt_vBox_main = QtWidgets.QVBoxLayout() #全てまとめたレイアウト
        lyt_vBox_main.addWidget(label_message)
        lyt_vBox_main.addLayout(lyt_grid_setting)
        lyt_vBox_main.addLayout(lyt_form_folderName)
        lyt_vBox_main.addWidget(self.txtArea_log)
        lyt_vBox_main.addWidget(button_export)
        lyt_vBox_main.addLayout(lyt_hBox_button)

        lyt_widget = QtWidgets.QWidget()
        lyt_widget.setLayout(lyt_vBox_main)
        self.setCentralWidget(lyt_widget) #CentralWidgetに配置

        self.name_os = platform.system() #使用中のOS


    def export_fbxFile(self):
        txt_fileName = self.txtLine_fileName.text() #ファイル名
        txt_filePath = self.txtLine_filePath.text() #書き出し先(ファイルパス)
        txt_folderName = self.txtLine_folderName.text() #フォルダ名
        filePath_folderName = txt_filePath + "/" + txt_folderName + "/" #新規フォルダを含む書き出し先(ファイルパス)
        selected_objects = cmds.ls(sl = True) #選択中のオブジェクト
        name_joined = ('_'.join(selected_objects)) #選択中のオブジェクトをアンダーバーで全て繋げたもの(obj01_obj02_obj03となる)

        if self.cmbBox_fileName.currentText() == "そのまま":
            txt_fileName = name_joined

        export_fbx01 = txt_filePath + "/" + txt_fileName + ".fbx" #新規フォルダを作成しない
        export_fbx02 = filePath_folderName + "/" + txt_fileName + ".fbx" #新規フォルダを作成

        if self.chkBox_folderName.isChecked():
            if os.path.isdir(filePath_folderName) == True:
                self.txtArea_log.append("\n##同一名称のフォルダが既に存在しています、書き出しが中止されました##")

            elif os.path.isfile(export_fbx02) == True:
                self.txtArea_log.append("\n##同一名称のFBXファイルが既に存在しています、書き出しが中止されました##")

            else:
                os.makedirs(filePath_folderName) #新規フォルダ作成
                cmds.file(export_fbx02, f = True, op = "v=0;", typ = "FBX Export", pr = True, es = True, ch = False, chn = False, exp = False, con = False) #書き出し
                self.txtArea_log.append(f"\n書き出しが完了しました\n・FBXファイル名: {txt_fileName + '.fbx'}\n・書き出したオブジェクト名: {', '.join(selected_objects)}\n・書き出し先: {filePath_folderName}") #ログ表示
                self.chkBox_folderName.setChecked(False) #新規フォルダ作成のチェックを外す
                self.txtLine_filePath.setText(filePath_folderName) #書き出し先(ファイルパス)入力欄を新規フォルダを含むファイルパスに更新
                filePath_open = filePath_folderName

        elif os.path.isfile(export_fbx01) == True:
            self.txtArea_log.append("\n##同一名称のFBXファイルが既に存在しています、書き出しが中止されました##")

        else:
            cmds.file(export_fbx01, f = True, op = "v=0;", typ = "FBX Export", pr = True, es = True, ch = False, chn = False, exp = False, con = False)
            self.txtArea_log.append(f"\n書き出しが完了しました\n・FBXファイル名: {txt_fileName + '.fbx'}\n・書き出したオブジェクト名: {', '.join(selected_objects)}\n・書き出し先: {txt_filePath}")
            filePath_open = txt_filePath

        if self.name_os == "Windows":
            os.startfile(filePath_open) #Windowsの場合、エクスプローラーを開く
                
        elif self.name_os == "Darwin":
            subprocess.Popen(['open', filePath_open]) #Macの場合、Finderを開く


    def open_fileDialog(self):
        cmds.fileDialog2() #ダイアログボックスを開く
    

    def open_explorerFinder(self):
        if self.name_os == "Windows":
            subprocess.Popen('explorer')
        
        elif self.name_os == "Darwin":
            subprocess.Popen(['open', '.'])
    

    def clear_logs(self):
        self.txtArea_log.setPlainText("・「新規フォルダを作成」にチェックを入れた場合、書き出し先に新規フォルダが作成され、その中に書き出したFBXファイルが格納されます")
    

    def change_fileNameComboBox(self):
        if self.cmbBox_fileName.currentText() == "入力する":
            self.txtLine_fileName.setReadOnly(False)
            self.txtLine_fileName.setText("")

        elif self.cmbBox_fileName.currentText() == "そのまま":
            self.txtLine_fileName.setReadOnly(True)
            self.txtLine_fileName.setText("選択中のオブジェクト名.fbxになります")
    

    def change_folderNameCheckBox(self):
        if self.chkBox_folderName.isChecked():
            self.txtLine_folderName.setReadOnly(False)
            self.txtLine_folderName.setText("")

        else:
            self.txtLine_folderName.setReadOnly(True)
            self.txtLine_folderName.setText("←をチェックした場合のみ入力が可能です")
    

toolWindow = FBXExportTool()
toolWindow.show()
