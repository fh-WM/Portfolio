#For Autodesk Maya 2024, Encoding UTF-8
import maya.cmds as cmds
from PySide2 import QtWidgets
from maya.app.general import mayaMixin

class WhatIsTheWorkingUnitsTool(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QMainWindow): #mayaMixin.MayaQWidgetBaseMixinでツールウィンドウがMayaウィンドウの裏側に移動するのを防ぐ
    def __init__(self):
        super(WhatIsTheWorkingUnitsTool, self).__init__()
        self.toolUI()


    def toolUI(self, *args):
        self.setGeometry(500, 300, 400, 400)
        self.setWindowTitle("What Is The Working Units Tool")
        self.statusBar().showMessage("Last Updated: 2024.07.22   |   For: Maya 2024   |   Fuma Hara")

        lnrLbl = QtWidgets.QLabel("長さ") #(Lbl全て)コンボボックス左横に表示するラベルテキスト
        aglLbl = QtWidgets.QLabel("角度")
        tmeLbl = QtWidgets.QLabel("時間")

        self.lnrCmb = QtWidgets.QComboBox() #長さのコンボボックス
        self.aglCmb = QtWidgets.QComboBox() #角度のコンボボックス
        self.tmeCmb = QtWidgets.QComboBox() #時間のコンボボックス
        self.lnrCmb.addItems(["mm(ミリメートル)", "cm(センチメートル)", "m(メートル)", "inch(インチ)", "feet(フィート)", "yard(ヤード)"]) #(addItems全て)コンボボックスの中身
        self.aglCmb.addItems(["°(度)", "rad(ラジアン)"])
        self.tmeCmb.addItems(["2fps", "3fps", "4fps", "5fps", "6fps", "8fps", "10fps", "12fps", "15fps", "16fps", "20fps",  "23.976fps", "24fps", "25fps(PAL方式)",
                              "29.97fps", "29.97df", "30fps(NTSC方式)", "40fps", "47.952fps", "48fps", "50fps(PAL方式)", "59.94fps", "60fps(NTSC方式)", "75fps",
                              "80fps", "90fps", "100fps", "120fps", "125fps", "150fps", "200fps", "240fps", "250fps", "300fps", "375fps", "400fps", "500fps",
                              "600fps", "750fps", "1200fps", "1500fps", "2000fps", "3000fps", "6000fps", "44100fps", "48000fps"])

        self.logFld = QtWidgets.QTextEdit(ReadOnly = True) #ログを表示する為のテキストフィールド、ReadOnlyのため入力を受け付けない
        self.logFld.setPlainText("・作業単位を確認する場合、下の「作業単位の確認」をクリックしてください、確認結果がここに表示されます\n\n"\
                                 "・作業単位を変更する場合、上の各項目から選択し「作業単位を変更」をクリックしてください") #メッセージ表示

        nowBtn = QtWidgets.QPushButton("作業単位の確認") #(Btn全て)各機能用ボタン
        chgBtn = QtWidgets.QPushButton("作業単位を変更")
        oppBtn = QtWidgets.QPushButton("プリファレンスを開く")
        nowBtn.clicked.connect(self.now_workingUnits) #(Btn.clicked.connect全て)ボタンを押した際の処理
        chgBtn.clicked.connect(self.change_workingUnits)
        oppBtn.clicked.connect(self.open_preferencesWindow)

        lyt_formLnr = QtWidgets.QFormLayout() #文字とウィジェットを横に並べるレイアウト
        lyt_formLnr.addRow(lnrLbl, self.lnrCmb) #ラベルとコンボボックスを横に配置、長さ
        lyt_formLnr.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow) #ウィンドウのサイズに合わせる

        lyt_formAgl = QtWidgets.QFormLayout()
        lyt_formAgl.addRow(aglLbl, self.aglCmb) #角度
        lyt_formAgl.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)

        lyt_formTme = QtWidgets.QFormLayout()
        lyt_formTme.addRow(tmeLbl, self.tmeCmb) #時間
        lyt_formTme.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)

        lyt_hBoxBtn = QtWidgets.QHBoxLayout() #ウィジェットを横に並べる
        lyt_hBoxBtn.addWidget(nowBtn) #レイアウトに追加
        lyt_hBoxBtn.addWidget(chgBtn)

        lyt_vBox = QtWidgets.QVBoxLayout() #ウィジェットを縦に並べる
        lyt_vBox.addLayout(lyt_formLnr)
        lyt_vBox.addLayout(lyt_formAgl)
        lyt_vBox.addLayout(lyt_formTme)
        lyt_vBox.addWidget(self.logFld)
        lyt_vBox.addLayout(lyt_hBoxBtn)
        lyt_vBox.addWidget(oppBtn) #レイアウトを追加する場合はaddLayout、ウィジェットを追加する場合はaddWidget

        lyt_wdgt = QtWidgets.QWidget()
        lyt_wdgt.setLayout(lyt_vBox)
        self.setCentralWidget(lyt_wdgt) #QMainWindowのCentralWidgetに配置


    def now_workingUnits(self):
        nowLnrVal = cmds.currentUnit(q = True, l = True) #現在の長さの作業単位を取得
        nowAglVal = cmds.currentUnit(q = True, a = True) #現在の角度の作業単位を取得
        nowTmeVal = cmds.currentUnit(q = True, t = True) #現在の時間の作業単位を取得

        lnrUnits = {'mm':'mm(ミリメートル)', 'cm':'cm(センチメートル)', 'm':'m(メートル)', 'in':'inch(インチ)', 'ft':'feet(フィート)', 'yd':'yard(ヤード)'} #長さの作業単位一覧
        aglUnits = {'deg':'°(度)', 'rad':'rad(ラジアン)'} #角度の作業単位一覧
        tmeUnits = {'game':'15fps', 'film':'24fps', 'pal':'25fps(PAL方式)', 'ntsc':'30fps(NTSC方式)', 'show':'48fps', 'palf':'50fps(PAL方式)', 'ntscf':'60fps(NTSC方式)', 
                    '23.976fps':'23.976fps', '29.97fps':'29.97fps', '29.97df':'29.97df', '47.952fps':'47.952fps', '59.94fps':'59.94fps', '44100fps':'44100fps', 
                    '48000fps':'48000fps', '2fps':'2fps', '3fps':'3fps', '4fps':'4fps', '5fps':'5fps', '6fps':'6fps', '8fps':'8fps', '10fps':'10fps', '12fps':'12fps', 
                    '16fps':'16fps', '20fps':'20fps', '40fps':'40fps', '75fps':'75fps', '80fps':'80fps', '90fps':'90fps', '100fps':'100fps', '120fps':'120fps', 
                    '125fps':'125fps', '150fps':'150fps', '200fps':'200fps', '240fps':'240fps', '250fps':'250fps', '300fps':'300fps', '375fps':'375fps', '400fps':'400fps', 
                    '500fps':'500fps', '600fps':'600fps', '750fps':'750fps', '1200fps':'1200fps', '1500fps':'1500fps', '2000fps':'2000fps', '3000fps':'3000fps', 
                    '6000fps':'6000fps'} #時間の作業単位一覧
        
        self.logFld.append(f"\n現在の作業単位は\n・長さ: {lnrUnits[nowLnrVal]}\n・角度: {aglUnits[nowAglVal]}\n・時間: {tmeUnits[nowTmeVal]}\nです") #ログ表示


    def change_workingUnits(self, *args):
        lnrUnits2 = {'mm(ミリメートル)':'mm', 'cm(センチメートル)':'cm', 'm(メートル)':'m', 'inch(インチ)':'in', 'feat(フィート)':'ft', 'yard(ヤード)':'yd'} #長さの作業単位一覧
        aglUnits2 = {'°(度)':'deg', 'rad(ラジアン)':'rad'} #角度の作業単位一覧
        tmeUnits2 = {'15fps':'game', '24fps':'film', '25fps(PAL方式)':'pal', '30fps(NTSC方式)':'ntsc', '48fps':'show', '50fps(PAL方式)':'palf', '60fps(NTSC方式)':'ntscf', 
                     '23.976fps':'23.976fps', '29.97fps':'29.97fps', '29.97df':'29.97df', '47.952fps':'47.952fps', '59.94fps':'59.94fps', '44100fps':'44100fps', 
                     '48000fps':'48000fps', '2fps':'2fps', '3fps':'3fps', '4fps':'4fps', '5fps':'5fps', '6fps':'6fps', '8fps':'8fps', '10fps':'10fps', '12fps':'12fps', 
                     '16fps':'16fps', '20fps':'20fps', '40fps':'40fps', '75fps':'75fps', '80fps':'80fps', '90fps':'90fps', '100fps':'100fps', '120fps':'120fps', 
                     '125fps':'125fps', '150fps':'150fps', '200fps':'200fps', '240fps':'240fps', '250fps':'250fps', '300fps':'300fps', '375fps':'375fps', '400fps':'400fps', 
                     '500fps':'500fps', '600fps':'600fps', '750fps':'750fps', '1200fps':'1200fps', '1500fps':'1500fps', '2000fps':'2000fps', '3000fps':'3000fps', 
                     '6000fps':'6000fps'} #時間の作業単位一覧
        
        cmds.currentUnit(l = f"{lnrUnits2[self.lnrCmb.currentText()]}", a = f"{aglUnits2[self.aglCmb.currentText()]}", t = f"{tmeUnits2[self.tmeCmb.currentText()]}") #作業単位を変更
        self.logFld.append(f"\n作業単位が変更されました")


    def open_preferencesWindow(self):
        cmds.PreferencesWindow() #プリファレンスを開く


toolWindow = WhatIsTheWorkingUnitsTool()
toolWindow.show()
