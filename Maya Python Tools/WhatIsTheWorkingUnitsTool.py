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
        self.statusBar().showMessage("Last Updated: 2024.09.22   |   For: Maya 2024   |   Fuma Hara")

        label_linear = QtWidgets.QLabel("長さ") #(Label全て)コンボボックス左横に表示するラベルテキスト
        label_angle = QtWidgets.QLabel("角度")
        label_time = QtWidgets.QLabel("時間")

        self.cmbBox_linear = QtWidgets.QComboBox() #長さのコンボボックス
        self.cmbBox_angle = QtWidgets.QComboBox() #角度のコンボボックス
        self.cmbBox_time = QtWidgets.QComboBox() #時間のコンボボックス
        self.cmbBox_linear.addItems(["mm(ミリメートル)", "cm(センチメートル)", "m(メートル)", "inch(インチ)", "feet(フィート)", "yard(ヤード)"]) #(addItems全て)コンボボックスの中身
        self.cmbBox_angle.addItems(["°(度)", "rad(ラジアン)"])
        self.cmbBox_time.addItems(["2fps", "3fps", "4fps", "5fps", "6fps", "8fps", "10fps", "12fps", "15fps", "16fps", "20fps",  "23.976fps", "24fps", "25fps(PAL方式)",
                              "29.97fps", "29.97df", "30fps(NTSC方式)", "40fps", "47.952fps", "48fps", "50fps(PAL方式)", "59.94fps", "60fps(NTSC方式)", "75fps",
                              "80fps", "90fps", "100fps", "120fps", "125fps", "150fps", "200fps", "240fps", "250fps", "300fps", "375fps", "400fps", "500fps",
                              "600fps", "750fps", "1200fps", "1500fps", "2000fps", "3000fps", "6000fps", "44100fps", "48000fps"])
        
        self.txtArea_log = QtWidgets.QTextEdit(readOnly = True) #ログを表示する為のテキストフィールド、readOnly = Trueのため入力を受け付けない
        self.txtArea_log.setPlainText("・作業単位を確認する場合、下の「作業単位の確認」をクリックしてください、確認結果がここに表示されます\n\n"\
                                 "・作業単位を変更する場合、上の各項目から選択し「作業単位を変更」をクリックしてください") #メッセージ表示
        
        button_checkUnits = QtWidgets.QPushButton("作業単位の確認") #(button全て)各機能用ボタン
        button_changeUnits = QtWidgets.QPushButton("作業単位を変更")
        button_clearLogs = QtWidgets.QPushButton("ログをクリア")
        button_openPrefs = QtWidgets.QPushButton("プリファレンスを開く")
        button_checkUnits.clicked.connect(self.check_workingUnits) #(clicked.connect全て)ボタンを押した際の処理
        button_changeUnits.clicked.connect(self.change_workingUnits)
        button_clearLogs.clicked.connect(self.clear_logs)
        button_openPrefs.clicked.connect(self.open_preferencesWindow)

        lyt_vBox_label = QtWidgets.QVBoxLayout() #ラベル用レイアウト
        lyt_vBox_label.addWidget(label_linear) #レイアウトに追加
        lyt_vBox_label.addWidget(label_angle)
        lyt_vBox_label.addWidget(label_time)

        lyt_vBox_cmbBox = QtWidgets.QVBoxLayout() #コンボボックス用レイアウト
        lyt_vBox_cmbBox.addWidget(self.cmbBox_linear)
        lyt_vBox_cmbBox.addWidget(self.cmbBox_angle)
        lyt_vBox_cmbBox.addWidget(self.cmbBox_time)

        lyt_hBox_setting = QtWidgets.QHBoxLayout() #ラベル&コンボボックス用レイアウト
        lyt_hBox_setting.addLayout(lyt_vBox_label, stretch = 1) #stretchで横サイズを比率で指定
        lyt_hBox_setting.addLayout(lyt_vBox_cmbBox, stretch = 11)

        lyt_hBox_button = QtWidgets.QHBoxLayout() #ボタン用レイアウト
        lyt_hBox_button.addWidget(button_checkUnits)
        lyt_hBox_button.addWidget(button_clearLogs)

        lyt_vBox_main = QtWidgets.QVBoxLayout() #全てまとめたレイアウト
        lyt_vBox_main.addLayout(lyt_hBox_setting)
        lyt_vBox_main.addWidget(self.txtArea_log)
        lyt_vBox_main.addLayout(lyt_hBox_button)
        lyt_vBox_main.addWidget(button_changeUnits)
        lyt_vBox_main.addWidget(button_openPrefs)

        lyt_widget = QtWidgets.QWidget()
        lyt_widget.setLayout(lyt_vBox_main)
        self.setCentralWidget(lyt_widget) #QMainWindowのCentralWidgetに配置


    def check_workingUnits(self):
        now_linearUnit = cmds.currentUnit(q = True, l = True) #現在の長さの作業単位を取得
        now_angleUnit = cmds.currentUnit(q = True, a = True) #現在の角度の作業単位を取得
        now_timeUnit = cmds.currentUnit(q = True, t = True) #現在の時間の作業単位を取得

        units01_linear = {'mm':'mm(ミリメートル)', 'cm':'cm(センチメートル)', 'm':'m(メートル)', 'in':'inch(インチ)', 'ft':'feet(フィート)', 'yd':'yard(ヤード)'} #長さの作業単位一覧
        units01_angle = {'deg':'°(度)', 'rad':'rad(ラジアン)'} #角度の作業単位一覧
        units01_time = {'game':'15fps', 'film':'24fps', 'pal':'25fps(PAL方式)', 'ntsc':'30fps(NTSC方式)', 'show':'48fps', 'palf':'50fps(PAL方式)', 'ntscf':'60fps(NTSC方式)', 
                        '23.976fps':'23.976fps', '29.97fps':'29.97fps', '29.97df':'29.97df', '47.952fps':'47.952fps', '59.94fps':'59.94fps', '44100fps':'44100fps', 
                        '48000fps':'48000fps', '2fps':'2fps', '3fps':'3fps', '4fps':'4fps', '5fps':'5fps', '6fps':'6fps', '8fps':'8fps', '10fps':'10fps', '12fps':'12fps', 
                        '16fps':'16fps', '20fps':'20fps', '40fps':'40fps', '75fps':'75fps', '80fps':'80fps', '90fps':'90fps', '100fps':'100fps', '120fps':'120fps', 
                        '125fps':'125fps', '150fps':'150fps', '200fps':'200fps', '240fps':'240fps', '250fps':'250fps', '300fps':'300fps', '375fps':'375fps', '400fps':'400fps', 
                        '500fps':'500fps', '600fps':'600fps', '750fps':'750fps', '1200fps':'1200fps', '1500fps':'1500fps', '2000fps':'2000fps', '3000fps':'3000fps', 
                        '6000fps':'6000fps'} #時間の作業単位一覧
        
        self.txtArea_log.append(f"\n現在の作業単位は\n・長さ: {units01_linear[now_linearUnit]}\n・角度: {units01_angle[now_angleUnit]}\n・時間: {units01_time[now_timeUnit]}\nです") #ログ表示
    

    def change_workingUnits(self, *args):
        units02_linear = {'mm(ミリメートル)':'mm', 'cm(センチメートル)':'cm', 'm(メートル)':'m', 'inch(インチ)':'in', 'feat(フィート)':'ft', 'yard(ヤード)':'yd'} #長さの作業単位一覧
        units02_angle = {'°(度)':'deg', 'rad(ラジアン)':'rad'} #角度の作業単位一覧
        units02_time = {'15fps':'game', '24fps':'film', '25fps(PAL方式)':'pal', '30fps(NTSC方式)':'ntsc', '48fps':'show', '50fps(PAL方式)':'palf', '60fps(NTSC方式)':'ntscf', 
                        '23.976fps':'23.976fps', '29.97fps':'29.97fps', '29.97df':'29.97df', '47.952fps':'47.952fps', '59.94fps':'59.94fps', '44100fps':'44100fps', 
                        '48000fps':'48000fps', '2fps':'2fps', '3fps':'3fps', '4fps':'4fps', '5fps':'5fps', '6fps':'6fps', '8fps':'8fps', '10fps':'10fps', '12fps':'12fps', 
                        '16fps':'16fps', '20fps':'20fps', '40fps':'40fps', '75fps':'75fps', '80fps':'80fps', '90fps':'90fps', '100fps':'100fps', '120fps':'120fps', 
                        '125fps':'125fps', '150fps':'150fps', '200fps':'200fps', '240fps':'240fps', '250fps':'250fps', '300fps':'300fps', '375fps':'375fps', '400fps':'400fps', 
                        '500fps':'500fps', '600fps':'600fps', '750fps':'750fps', '1200fps':'1200fps', '1500fps':'1500fps', '2000fps':'2000fps', '3000fps':'3000fps', 
                        '6000fps':'6000fps'} #時間の作業単位一覧
        
        cmds.currentUnit(l = f"{units02_linear[self.cmbBox_linear.currentText()]}", a = f"{units02_angle[self.cmbBox_angle.currentText()]}", t = f"{units02_time[self.cmbBox_time.currentText()]}") #作業単位を変更
        self.txtArea_log.append(f"\n作業単位が変更されました")
    

    def clear_logs(self):
        self.txtArea_log.setPlainText("・作業単位を確認する場合、下の「作業単位の確認」をクリックしてください、確認結果がここに表示されます\n\n"\
                                 "・作業単位を変更する場合、上の各項目から選択し「作業単位を変更」をクリックしてください") #ログを上書き
    

    def open_preferencesWindow(self):
        cmds.PreferencesWindow() #プリファレンスを開く
    

toolWindow = WhatIsTheWorkingUnitsTool()
toolWindow.show()
