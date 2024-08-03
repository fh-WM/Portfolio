#For Autodesk Maya 2024, For Windows OS Only, Encoding UTF-8
import maya.cmds as cmds
import os
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
        self.statusBar().showMessage("Last Updated: 2024.07.22   |   For: Maya 2024   |   Fuma Hara")

        fstMsgLbl = QtWidgets.QLabel("※まず始めに書き出したいオブジェクトをビューもしくはアウトライナから選択してください") #(Lbl全て)各テキストラベル
        fileNmLbl = QtWidgets.QLabel("ファイル名")
        filePhLbl = QtWidgets.QLabel("書き出し先(ファイルパス)")

        self.nmMode = QtWidgets.QComboBox() #ファイル名入力選択
        self.nmMode.addItems(["入力する", "そのまま"])
        self.nmMode.currentIndexChanged.connect(self.change_nmMode) #状態が変化した際の処理

        self.fileNmBox = QtWidgets.QLineEdit() #ファイル名入力欄
        self.filePhBox = QtWidgets.QLineEdit() #書き出し先(ファイルパス)入力欄
        self.fldrNmBox = QtWidgets.QLineEdit(ReadOnly = True) #新規フォルダ名入力欄、ツール起動時は編集不可
        self.fldrNmBox.setText("←をチェックした場合のみ入力が可能です")

        self.fldrNmChk = QtWidgets.QCheckBox("新規フォルダを作成 | 新規フォルダ名") #新規フォルダを作成するか否かのチェックボックス
        self.fldrNmChk.stateChanged.connect(self.change_fldrNmChk)

        self.logBox = QtWidgets.QTextEdit(ReadOnly = True) #ログを表示するためのテキストフィールド、ReadOnlyのため入力を受け付けない
        self.logBox.setPlainText("・「新規フォルダを作成」にチェックを入れた場合、書き出し先に新規フォルダが作成され、その中に書き出したFBXファイルが格納されます")

        expBtn = QtWidgets.QPushButton("書き出し") #(Btn全て)各機能用ボタン
        opdBtn = QtWidgets.QPushButton("ダイアログボックスを開く")
        opeBtn = QtWidgets.QPushButton("エクスプローラーを開く")
        clrBtn = QtWidgets.QPushButton("ログのクリア")
        expBtn.clicked.connect(self.export_fbxFile) #(Btn.clicked.connect全て)ボタンを押した際の処理
        opdBtn.clicked.connect(self.open_fileDialog)
        opeBtn.clicked.connect(self.open_explorer)
        clrBtn.clicked.connect(self.clear_logBox)

        lyt_formFileNm = QtWidgets.QFormLayout() #ファイル名左横、ラベルとコンボボックスを横に並べる
        lyt_formFileNm.addRow(fileNmLbl, self.nmMode)

        lyt_grid = QtWidgets.QGridLayout() #上のフォームレイアウト、ファイル名入力欄、ファイルパスラベル、ファイルパス入力欄をグリッド状に並べる
        lyt_grid.addLayout(lyt_formFileNm, 0, 0)
        lyt_grid.addWidget(self.fileNmBox, 0, 1)
        lyt_grid.addWidget(filePhLbl, 1, 0)
        lyt_grid.addWidget(self.filePhBox, 1, 1)

        lyt_formFldrNm = QtWidgets.QFormLayout() #チェックボックスと新規フォルダ名入力欄を横に並べる
        lyt_formFldrNm.addRow(self.fldrNmChk, self.fldrNmBox)

        lyt_hBoxBtn = QtWidgets.QHBoxLayout() #ボタンを横に並べる
        lyt_hBoxBtn.addWidget(opdBtn)
        lyt_hBoxBtn.addWidget(opeBtn)
        lyt_hBoxBtn.addWidget(clrBtn)

        lyt_vBox = QtWidgets.QVBoxLayout() #ウィジェットを縦に並べる
        lyt_vBox.addWidget(fstMsgLbl)
        lyt_vBox.addLayout(lyt_grid)
        lyt_vBox.addLayout(lyt_formFldrNm)
        lyt_vBox.addWidget(self.logBox)
        lyt_vBox.addWidget(expBtn)
        lyt_vBox.addLayout(lyt_hBoxBtn)

        lyt_wdgt = QtWidgets.QWidget()
        lyt_wdgt.setLayout(lyt_vBox)
        self.setCentralWidget(lyt_wdgt) #QMainWindow内のCentralWidgetに配置


    def change_nmMode(self):
        if self.nmMode.currentText() == "入力する":
            self.fileNmBox.setReadOnly(False) #編集可能にする
            self.fileNmBox.setText("")
        elif self.nmMode.currentText() == "そのまま":
            self.fileNmBox.setReadOnly(True) #編集不可にする
            self.fileNmBox.setText("選択中のオブジェクト名.fbxになります")


    def change_fldrNmChk(self):
        if self.fldrNmChk.isChecked():
            self.fldrNmBox.setReadOnly(False)
            self.fldrNmBox.setText("")
        else:
            self.fldrNmBox.setReadOnly(True)
            self.fldrNmBox.setText("←をチェックした場合のみ入力が可能です")

    
    def export_fbxFile(self, *args):
        fileNm = self.fileNmBox.text() #ファイル名
        filePh = self.filePhBox.text() #書き出し先(ファイルパス)
        fldrNm = self.fldrNmBox.text() #新規フォルダ名
        newFilePh = filePh + "/" + fldrNm + "/" #新規フォルダを含む書き出し先(ファイルパス)
        dfltNm = cmds.ls(sl = True) #選択中のオブジェクト
        joinNm = ('_'.join(dfltNm)) #選択中のオブジェクト名を_で全て繋げたもの(obj_obj_objになる)

        if self.nmMode.currentText() == "そのまま":
            fileNm = joinNm #選択中のオブジェクト名をそのまま使用する

        expFbxNm1 = filePh + "/" + fileNm + ".fbx" #新規フォルダを作成しない.fbx
        expFbxNm2 = newFilePh + "/" + fileNm + ".fbx" #新規フォルダを作成する.fbx

        if self.fldrNmChk.isChecked():
            if os.path.isdir(newFilePh) == True:
                self.logBox.append("\n##同一の名称のフォルダが既に存在しています、書き出しが中止されました##") #ログ表示
            elif os.path.isfile(expFbxNm2) == True:
                self.logBox.append("\n##同一の名称のFBXファイルが既に存在しています、書き出しが中止されました##")
            else:
                os.makedirs(newFilePh) #新規フォルダ作成
                cmds.file(expFbxNm2, f = True, op = "v=0;", typ = "FBX Export", pr = True, es = True, ch = False, chn = False, exp = False, con = False) #FBX書き出し
                self.logBox.append(f"\n書き出しが完了しました\n・FBXファイル名: {fileNm + '.fbx'}\n・書き出したオブジェクト名: {', '.join(dfltNm)}\n・書き出し先: {newFilePh}")
                self.fldrNmChk.setChecked(False) #新規フォルダ作成のチェックを外す
                self.filePhBox.setText(newFilePh) #入力欄を新規フォルダを含むファイルパスに更新
                os.startfile(newFilePh) #エクスプローラーを開く
        elif os.path.isfile(expFbxNm1) == True:
            self.logBox.append("\n##同一の名称のFBXファイルが既に存在しています、書き出しが中止されました##")
        else:
            cmds.file(expFbxNm1, f = True, op = "v=0;", typ = "FBX Export", pr = True, es = True, ch = False, chn = False, exp = False, con = False)
            self.logBox.append(f"\n書き出しが完了しました\n・FBXファイル名: {fileNm + '.fbx'}\n・書き出したオブジェクト名: {', '.join(dfltNm)}\n・書き出し先: {filePh}")
            os.startfile(filePh)

    
    def open_fileDialog(self):
        cmds.fileDialog2() #ダイアログボックスを開く

    
    def open_explorer(self):
        subprocess.Popen(['explorer']) #エクスプローラーを開く


    def clear_logBox(self):
        self.logBox.setPlainText("・「新規フォルダを作成」にチェックを入れた場合、書き出し先に新規フォルダが作成され\n"\
                                 "その中に書き出したFBXファイルが格納されます")


toolWindow = FBXExportTool()
toolWindow.show()
