#For Autodesk Maya 2024, Encoding UTF-8
import maya.cmds as cmds
import math

class StairsGenerator():
    def __init__(self):
        self.toolWindow_stairsGenerator()


    def toolWindow_stairsGenerator(self):
        winName = "Stairs Generator"
        toolWin = cmds.window(winName)

        if cmds.window(winName, ex = True):
            cmds.deleteUI(winName) #同一のウィンドウが存在する場合削除

        lyt_tabs = cmds.tabLayout(imh = 5, imw = 5)

        tab01_StairsGenerator = cmds.columnLayout(adj = True)
        cmds.frameLayout(l = "直線階段の設定")
        cmds.optionMenu('setSt_strGenType', l = "生成方法の選択", cc = self.change_stStrGenType_stStpGenType)
        cmds.floatSliderGrp('setSt_strLgh', l = "長さ", f = True, min = 0.1, max = 100, v = 25)
        cmds.floatSliderGrp('setSt_strHgt', l = "高さ", f = True, min = 0.1, max = 100, v = 20)
        cmds.floatSliderGrp('setSt_strAgl', l = "角度", f = True, min = 0.1, max = 90, v = 30, en = False)
        cmds.radioButtonGrp('setSt_stpGenType', l = "段の生成方法の選択", nrb = 3, la3 = ("1段あたりの高さ", "1段あたりの奥行", "段数"), sl = 1, cc = self.change_stStrGenType_stStpGenType)
        cmds.floatSliderGrp('setSt_stpHgt', l = "1段あたりの高さ", f = True, min = 0.1, max = 50, v = 0.5)
        cmds.floatSliderGrp('setSt_stpDph', l = "1段あたりの奥行", f = True, min = 0.1, max = 50, v = 0.5, en = False)
        cmds.intSliderGrp('setSt_stpNum', l = "段数", f = True, min = 1, max = 500, v = 20, en = False)
        cmds.radioButtonGrp('setSt_strType', l = "階段の種類の選択", nrb = 2, la2 = ("スケルトン階段", "ボックス階段"), sl = 1, cc = self.change_stStrType_stDltFcs)
        cmds.menuItem(l = "長さ & 高さ", p = 'setSt_strGenType')
        cmds.menuItem(l = "長さ & 角度", p = 'setSt_strGenType')
        cmds.menuItem(l = "高さ & 角度", p = 'setSt_strGenType')
        cmds.menuItem(l = "1段あたりの高さ & 1段あたりの奥行 & 段数", p = 'setSt_strGenType')
        cmds.setParent(u = True) #"直線階段の設定"を親に指定

        cmds.frameLayout(l = "踏板の設定")
        cmds.floatSliderGrp('setSt_trdWdh', l = "横幅", f = True, min = 0.1, max = 100, v = 3)
        cmds.floatSliderGrp('setSt_trdHgt', l = "高さ", f = True, min = 0.1, max = 50, v = 0.3)
        cmds.floatSliderGrp('setSt_trdDph', l = "奥行", f = True, min = 0.1, max = 50, v = 0.5)
        cmds.checkBox('setSt_dltFcs', l = "階段の表面以外のフェースを削除", cc = self.change_stStrType_stDltFcs)
        cmds.checkBox('setSt_mrgVtx', l = "踏板同士の重なった頂点をマージ", en = False)
        cmds.button(l = "生成", c = self.generate_straightStairs)
        cmds.setParent(u = True) #"踏板の設定"を親に指定
        cmds.setParent(top = True) #tab01_StairsGeneratorを親に指定

        tab02_SpiralStairsGenerator = cmds.columnLayout(adj = True)
        cmds.frameLayout(l = "らせん階段の設定")
        cmds.optionMenu('setSp_strGenType', l = "生成方法の選択", cc = self.change_spStrGenType_spStpGenType)
        cmds.floatSliderGrp('setSp_strHgt', l = "高さ", f = True, min = 0.1, max = 100, v = 20)
        cmds.floatSliderGrp('setSp_strAgl', l = "角度", f = True, min = 0.1, max = 80, v = 20, en = False)
        cmds.radioButtonGrp('setSp_stpGenType', l = "段の生成方法の選択", nrb = 2, la2 = ("1段あたりの高さ", "1周あたりの段数"), sl = 1, cc = self.change_spStrGenType_spStpGenType)
        cmds.floatSliderGrp('setSp_stpHgt', l = "1段あたりの高さ", f = True, min = 0.1, max = 50, v = 0.5)
        cmds.intSliderGrp('setSp_stpNum', l = "1周あたりの段数", f = True, min = 4, max = 500, v = 20, en = False)
        cmds.radioButtonGrp('setSp_strType', l = "階段の種類の選択", nrb = 2, la2 = ("スケルトン階段", "ボックス階段"), sl = 1, cc = self.change_spStrType_spDltFcs)
        cmds.intSliderGrp('setSp_rndNum', l = "周数", f = True, min = 1, max = 10, v = 1)
        cmds.floatSliderGrp('setSp_hleRds', l = "中央支柱用の穴の半径", f = True, min = 0.1, max = 100, v = 2)
        cmds.menuItem(l = "高さ", p = 'setSp_strGenType')
        cmds.menuItem(l = "角度", p = 'setSp_strGenType')
        cmds.menuItem(l = "1段あたりの高さ & 1周あたりの段数", p = 'setSp_strGenType')
        cmds.setParent(u = True) #"らせん階段の設定"を親に指定

        cmds.frameLayout(l = "踏板の設定")
        cmds.floatSliderGrp('setSp_trdWdh', l = "横幅", f = True, min = 0.1, max = 100, v = 3)
        cmds.floatSliderGrp('setSp_trdHgt', l = "高さ", f = True, min = 0.1, max = 50, v = 0.3)
        cmds.checkBox('setSp_crtPlr', l = "支柱を作成")
        cmds.checkBox('setSp_dltFcs', l = "階段の表面以外のフェースを削除", cc = self.change_spStrType_spDltFcs)
        cmds.checkBox('setSp_mrgVtx', l = "踏板同士の重なった頂点をマージ", en = False)
        cmds.button(l = "生成", c = self.generate_spiralStairs)
        cmds.setParent(u = True) #"踏板の設定"を親に指定
        cmds.setParent(top = True) #tab02_SpiralStairsGeneratorを親に指定

        tab03_Infomation = cmds.columnLayout(adj = True)
        cmds.frameLayout(l = "注意事項")
        cmds.text(l = "")
        cmds.text(l = "「踏板同士の重なった頂点をマージ」を利用したい場合、", al = 'left')
        cmds.text(l = "・「階段の種類の選択」から「ボックス階段」を選択", al = 'left')
        cmds.text(l = "・「階段の表面以外のフェースを削除」にチェック", al = 'left')
        cmds.text(l = "以上が必要になります。", al = 'left')
        cmds.text(l = "")
        cmds.text(l = "らせん階段を生成する際に", al = 'left')
        cmds.text(l = "「生成方法の選択」で「角度」を選んだ場合、", al = 'left')
        cmds.text(l = "「1段あたりの高さ」を利用することはできません、ご了承ください。", al = 'left')
        cmds.text(l = "")
        cmds.setParent(u = True) #"注意事項"を親に指定

        cmds.frameLayout(l = "インフォメーション")
        cmds.text(l = "Last Updated: 2024.07.22", al = 'left')
        cmds.text(l = "For: Maya 2024", al = 'left')
        cmds.text(l = "Fuma Hara", al = 'left')
        cmds.setParent(u = True) #"インフォメーション"を親に指定
        cmds.setParent(top = True) #tab03_Infomationを親に指定

        cmds.tabLayout(lyt_tabs, e = True, tl = ((tab01_StairsGenerator, "直線階段   "),
                                                (tab02_SpiralStairsGenerator, "らせん階段   "),
                                                (tab03_Infomation, "インフォメーション   ")))
        cmds.showWindow(toolWin)


    def generate_straightStairs(self, *args):
        st_strGenType = cmds.optionMenu('setSt_strGenType', q = True, v = True) #階段の生成方法の選択
        st_stpGenType = cmds.radioButtonGrp('setSt_stpGenType', q = True, sl = True) #段の生成方法の選択
        st_strType = cmds.radioButtonGrp('setSt_strType', q = True, sl = True) #階段の種類の選択

        st_strLgh = cmds.floatSliderGrp('setSt_strLgh', q = True, v = True) #階段の長さ
        st_strHgt = cmds.floatSliderGrp('setSt_strHgt', q = True, v = True) #階段の高さ
        st_strAgl = cmds.floatSliderGrp('setSt_strAgl', q = True, v = True) #階段の角度

        st_stpHgt = cmds.floatSliderGrp('setSt_stpHgt', q = True, v = True) #1段あたりの高さ
        st_stpDph = cmds.floatSliderGrp('setSt_stpDph', q = True, v = True) #1段あたりの奥行
        st_stpNum = cmds.intSliderGrp('setSt_stpNum', q = True, v = True) #段数

        st_trdWdh = cmds.floatSliderGrp('setSt_trdWdh', q = True, v = True) #踏板1つあたりの横幅
        st_trdHgt = cmds.floatSliderGrp('setSt_trdHgt', q = True, v = True) #踏板1つあたりの高さ
        st_trdDph = cmds.floatSliderGrp('setSt_trdDph', q = True, v = True) #踏板1つあたりの奥行

        st_dltFcs = cmds.checkBox('setSt_dltFcs', q = True, v = True) #階段の表面以外のフェースを削除
        st_mrgVtx = cmds.checkBox('setSt_mrgVtx', q = True, v = True) #踏板同士の重なった頂点をマージ

        tan_strAgl = math.tan(math.radians(st_strAgl))

        if st_strGenType == '長さ & 高さ' and st_stpGenType == 1: #階段の長さ, 階段の高さ, 1段あたりの高さ
            st_stpNum = st_strHgt / st_stpHgt

            if st_stpNum == round(st_stpNum): #段数の値が整数で割り切れているか否か
                st_stpDph = round(st_strLgh / st_stpNum, 3)
            else:
                cmds.confirmDialog(b = "OK", icn = 'critical', m = "現在指定している値では階段を生成できません", t = "ERROR: Stairs Generator")
                cmds.error("生成が中止されました")

        if st_strGenType == '長さ & 高さ' and st_stpGenType == 2: #階段の長さ, 階段の高さ, 1段あたりの奥行
            st_stpNum = st_strLgh / st_stpDph
            
            if st_stpNum == round(st_stpNum):
                st_stpHgt = round(st_strHgt / st_stpNum, 3)
            else:
                cmds.confirmDialog(b = "OK", icn = 'critical', m = "現在指定している値では階段を生成できません", t = "ERROR: Stairs Generator")
                cmds.error("生成が中止されました")

        if st_strGenType == '長さ & 高さ' and st_stpGenType == 3: #階段の長さ, 階段の高さ, 段数
            st_stpHgt = round(st_strHgt / st_stpNum, 3)
            st_stpDph = round(st_strLgh / st_stpNum, 3)

        if st_strGenType == '長さ & 角度' and st_stpGenType == 1: #階段の長さ, 階段の角度, 1段あたりの高さ
            st_stpDph = round(st_stpHgt / tan_strAgl, 3)
            st_stpNum = round(st_strLgh / st_stpDph)

        if st_strGenType == '長さ & 角度' and st_stpGenType == 2: #階段の長さ, 階段の角度, 1段あたりの奥行
            st_stpNum = round(st_strLgh / st_stpDph)
            st_stpHgt = round(st_stpDph * tan_strAgl, 3)

        if st_strGenType == '長さ & 角度' and st_stpGenType == 3: #階段の長さ, 階段の角度, 段数
            st_stpDph = round(st_strLgh / st_stpNum, 3)
            st_stpHgt = round(st_stpDph * tan_strAgl, 3)

        if st_strGenType == '高さ & 角度' and st_stpGenType == 1: #階段の高さ, 階段の角度, 1段あたりの高さ
            st_stpNum = round(st_strHgt / st_stpHgt)
            st_stpDph = round(st_stpHgt / tan_strAgl, 3)

        if st_strGenType == '高さ & 角度' and st_stpGenType == 2: #階段の高さ, 階段の角度, 1段あたりの奥行
            st_stpHgt = round(st_stpDph * tan_strAgl, 3)
            st_stpNum = round(st_strHgt / st_stpHgt)

        if st_strGenType == '高さ & 角度' and st_stpGenType == 3: #階段の高さ, 階段の角度, 段数
            st_stpHgt = round(st_strHgt / st_stpNum, 3)
            st_stpDph = round(st_stpHgt / tan_strAgl, 3)

        if st_strGenType == '1段あたりの高さ & 1段あたりの奥行 & 段数':
            pass #指定された値をそのまま使用し計算不要なため

        st_nowLoX = st_stpDph #現在の配置座標X、配置の度に変化する
        st_nowLoY = st_stpHgt #現在の配置座標Y、配置の度に変化する

        if st_strType == 2: #ボックス階段
            st_trdDph = st_stpDph #踏板の奥行を1段あたりの奥行で上書き
            st_trdHgt = st_stpHgt #踏板の高さを1段あたりの高さで上書き

        cmds.polyCube(n = "StraightStairsTread_BaseShape", d = st_trdWdh, h = st_trdHgt, w = st_trdDph) #踏板を作成

        if st_dltFcs == True: #階段の表面以外のフェース削除
            cmds.delete('StraightStairsTread_BaseShape.f[0]', 'StraightStairsTread_BaseShape.f[2:4]') #底面、側面、後面のフェースを削除

        cmds.select('StraightStairsTread_BaseShape') #フェース選択の状態からオブジェクト選択に変更
        cmds.move(-st_trdDph / 2, st_trdHgt / 2, st_trdWdh / 2, 'StraightStairsTread_BaseShape.scalePivot', 'StraightStairsTread_BaseShape.rotatePivot', rpr = True) #踏板のピボット位置を変更
        cmds.move(-st_trdHgt / 2, 'StraightStairsTread_BaseShape', y = True) #踏板のピボットY座標をワールドのY座標0に合わせる
        cmds.makeIdentity(a = True, pn = True, r = True, s = True, t = True) #座標の値を全て0にする
        cmds.move(st_nowLoY, 'StraightStairsTread_BaseShape', y = True) #1段目の位置に移動
        st_nowLoY += st_stpHgt #2段目配置のために値を調整

        for i in range(int(st_stpNum - 1)):
            st_dupObj = cmds.duplicate('StraightStairsTread_BaseShape', n = "dup_StraightStairsTreadBaseShape") #複製し仮名称に変更
            cmds.move(st_nowLoX, st_nowLoY, 0, st_dupObj) #踏板を配置
            cmds.rename("dup_StraightStairsTreadBaseShape", "renamed_StraightStairsTreadBaseShape") #仮名称から変更
            st_nowLoX += st_stpDph #(mvLoc全て)次の段のために値を調整
            st_nowLoY += st_stpHgt

        st_objNms = cmds.ls('StraightStairsTread_BaseShape*', 'renamed_StraightStairsTreadBaseShape*', g = True) #結合するオブジェクトを検索
        st_objLRs = cmds.listRelatives(st_objNms, p = True) #検索結果からオブジェクト名のみに絞る
        cmds.select(st_objLRs)
        cmds.polyUnite()

        if st_strType == 2 and st_dltFcs == True and st_mrgVtx == True: #ボックス階段、表面以外フェース削除、頂点マージの3つ全て選択した場合
            cmds.polyMergeVertex() #重なっている頂点をマージ、上記の条件以外で仮に実行した場合エラーポリゴンになる可能性があるため

        cmds.rename("StraightStairs")
        cmds.DeleteHistory()


    def change_stStrGenType_stStpGenType(self, *args):
        if cmds.optionMenu('setSt_strGenType', q = True, v = True) == '1段あたりの高さ & 1段あたりの奥行 & 段数':
            cmds.floatSliderGrp('setSt_strLgh', e = True, en = False) #en = Falseは操作不可
            cmds.floatSliderGrp('setSt_strHgt', e = True, en = False)
            cmds.floatSliderGrp('setSt_strAgl', e = True, en = False)
            cmds.floatSliderGrp('setSt_stpHgt', e = True, en = True) #en = Trueは操作可
            cmds.floatSliderGrp('setSt_stpDph', e = True, en = True)
            cmds.intSliderGrp('setSt_stpNum', e = True, en = True)
            cmds.radioButtonGrp('setSt_stpGenType', e = True, en = False)
        else:
            cmds.radioButtonGrp('setSt_stpGenType', e = True, en = True)

            if cmds.optionMenu('setSt_strGenType', q = True, v = True) == '長さ & 高さ':
                cmds.floatSliderGrp('setSt_strLgh', e = True, en = True)
                cmds.floatSliderGrp('setSt_strHgt', e = True, en = True)
                cmds.floatSliderGrp('setSt_strAgl', e = True, en = False)
            elif cmds.optionMenu('setSt_strGenType', q = True, v = True) == '長さ & 角度':
                cmds.floatSliderGrp('setSt_strLgh', e = True, en = True)
                cmds.floatSliderGrp('setSt_strHgt', e = True, en = False)
                cmds.floatSliderGrp('setSt_strAgl', e = True, en = True)
            elif cmds.optionMenu('setSt_strGenType', q = True, v = True) == '高さ & 角度':
                cmds.floatSliderGrp('setSt_strLgh', e = True, en = False)
                cmds.floatSliderGrp('setSt_strHgt', e = True, en = True)
                cmds.floatSliderGrp('setSt_strAgl', e = True, en = True)

            if cmds.radioButtonGrp('setSt_stpGenType', q = True, sl = True) == 1:
                cmds.floatSliderGrp('setSt_stpHgt', e = True, en = True)
                cmds.floatSliderGrp('setSt_stpDph', e = True, en = False)
                cmds.intSliderGrp('setSt_stpNum', e = True, en = False)
            elif cmds.radioButtonGrp('setSt_stpGenType', q = True, sl = True) == 2:
                cmds.floatSliderGrp('setSt_stpHgt', e = True, en = False)
                cmds.floatSliderGrp('setSt_stpDph', e = True, en = True)
                cmds.intSliderGrp('setSt_stpNum', e = True, en = False)
            elif cmds.radioButtonGrp('setSt_stpGenType', q = True, sl = True) == 3:
                cmds.floatSliderGrp('setSt_stpHgt', e = True, en = False)
                cmds.floatSliderGrp('setSt_stpDph', e = True, en = False)
                cmds.intSliderGrp('setSt_stpNum', e = True, en = True)
    

    def change_stStrType_stDltFcs(self, *args):
        if cmds.radioButtonGrp('setSt_strType', q = True, sl = True) == 1: #スケルトン階段
            cmds.floatSliderGrp('setSt_trdHgt', e = True, en = True)
            cmds.floatSliderGrp('setSt_trdDph', e = True, en = True)
        else: #ボックス階段
            cmds.floatSliderGrp('setSt_trdHgt', e = True, en = False)
            cmds.floatSliderGrp('setSt_trdDph', e = True, en = False)

        if cmds.radioButtonGrp('setSt_strType', q = True, sl = True) == 2 and cmds.checkBox('setSt_dltFcs', q = True, v = True):
            cmds.checkBox('setSt_mrgVtx', e = True, en = True) #ボックス階段、表面以外のフェース削除を選択した場合
        else:
            cmds.checkBox('setSt_mrgVtx', e = True, en = False)


    def generate_spiralStairs(self, *args):
        sp_strGenType = cmds.optionMenu('setSp_strGenType', q = True, v = True) #階段の生成方法の選択
        sp_stpGenType = cmds.radioButtonGrp('setSp_stpGenType', q = True, sl = True) #段の生成方法の選択
        sp_strType = cmds.radioButtonGrp('setSp_strType', q = True, sl = True) #階段の種類の選択

        sp_strHgt = cmds.floatSliderGrp('setSp_strHgt', q = True, v = True) #階段の高さ
        sp_strAgl = cmds.floatSliderGrp('setSp_strAgl', q = True, v = True) #階段の角度
        sp_stpHgt = cmds.floatSliderGrp('setSp_stpHgt', q = True, v = True) #1段あたりの高さ
        sp_stpNum = cmds.intSliderGrp('setSp_stpNum', q = True, v = True) #1周あたりの段数

        sp_rodNum = cmds.intSliderGrp('setSp_rndNum', q = True, v = True) #螺旋の周数
        sp_hleRds = cmds.floatSliderGrp('setSp_hleRds', q = True, v = True) #中央支柱用の穴の半径

        sp_trdWdh = cmds.floatSliderGrp('setSp_trdWdh', q = True, v = True) #踏板の横幅
        sp_trdHgt = cmds.floatSliderGrp('setSp_trdHgt', q = True, v = True) #踏板の高さ

        sp_crtPlr = cmds.checkBox('setSp_crtPlr', q = True, v = True) #支柱を作成
        sp_dltFcs = cmds.checkBox('setSp_dltFcs', q = True, v = True) #階段の表面以外のフェースを削除
        sp_mrgVtx = cmds.checkBox('setSp_mrgVtx', q = True, v = True) #踏板同士の重なった頂点をマージ

        sp_pipRds = sp_trdWdh + sp_hleRds #polyPipeの半径
        sp_trdHgt = sp_trdHgt * 2 #polyPipeのheightは何故か指定した値/2になってしまうため、おそらく仕様に問題あり
        sp_strHgt_1R = sp_strHgt / sp_rodNum #1周あたりの高さ
        
        if sp_strGenType == '高さ' and sp_stpGenType == 1: #階段の高さ & 1段あたりの高さ
            sp_stpNum = round(sp_strHgt_1R / sp_stpHgt)
        
        if sp_strGenType == '高さ' and sp_stpGenType == 2: #階段の高さ & 1周あたりの段数
            sp_stpHgt = round(sp_strHgt_1R / sp_stpNum, 3)
        
        if sp_strGenType == '角度' and sp_stpGenType == 2: #階段の角度 & 1周あたりの段数
            sp_stpDph = round(math.sin(math.pi / sp_stpNum) * 2 * sp_pipRds, 3) #1段あたりの奥行
            sp_stpHgt = round(math.tan(math.radians(sp_strAgl)) * sp_stpDph, 3)
            sp_strHgt = sp_stpHgt * sp_stpNum * sp_rodNum
        
        if sp_strGenType == '1段あたりの高さ & 1周あたりの段数':
            sp_strHgt = sp_stpHgt * sp_stpNum * sp_rodNum

        sp_plcAgl = round(360 / sp_stpNum, 3) #踏板の配置角度
        sp_nowAgl = sp_plcAgl #現在の配置角度、配置の度に変化する
        sp_nowLoY = sp_stpHgt #現在の配置高さ、配置の度に変化する

        if sp_stpNum < 4:
            cmds.confirmDialog(b = "OK", icn = 'critical', m = "現在指定している値では階段を生成できません", t = "ERROR: Stairs Generator")
            cmds.error("生成が中止されました")

        if sp_strType == 2: #ボックス階段
            sp_trdHgt = sp_stpHgt * 2 #踏板の高さを1段あたりの高さで上書き

        cmds.polyPipe(n = "SpiralStairsTread_BaseShape", h = sp_trdHgt, t = sp_trdWdh, r = sp_pipRds, sa = sp_stpNum) #踏板のベースとなるパイプ作成
        cmds.delete('SpiralStairsTread_BaseShape.f[1:' + str(sp_stpNum - 1) + ']',
                    'SpiralStairsTread_BaseShape.f[' + str(sp_stpNum + 1) + ':' + str(sp_stpNum * 2 - 1) + ']',
                    'SpiralStairsTread_BaseShape.f[' + str(sp_stpNum * 2 + 1) + ':' + str(sp_stpNum * 3 - 1) + ']',
                    'SpiralStairsTread_BaseShape.f[' + str(sp_stpNum * 3 + 1) + ':' + str(sp_stpNum * 4 - 1) + ']') #不要なフェースを削除
        cmds.select('SpiralStairsTread_BaseShape.e[4]', 'SpiralStairsTread_BaseShape.e[6]',
                    'SpiralStairsTread_BaseShape.e[8]', 'SpiralStairsTread_BaseShape.e[10]') #穴を構成するエッジを選択、1/2
        cmds.polyCloseBorder() #穴を埋める、1/2
        cmds.select('SpiralStairsTread_BaseShape.e[5]', 'SpiralStairsTread_BaseShape.e[7]',
                    'SpiralStairsTread_BaseShape.e[9]', 'SpiralStairsTread_BaseShape.e[11]') #穴を構成するエッジを選択、2/2
        cmds.polyCloseBorder() #穴を埋める、2/2

        if sp_dltFcs == True: #階段の表面以外のフェース削除
            cmds.delete('SpiralStairsTread_BaseShape.f[0]', 'SpiralStairsTread_BaseShape.f[2:3]', 'SpiralStairsTread_BaseShape.f[5]') #底面、側面、後面のフェースを削除
        else:
            if sp_crtPlr == True: #支柱を作成
                cmds.delete('SpiralStairsTread_BaseShape.f[0]') #支柱と接するフェースを削除

        cmds.select('SpiralStairsTread_BaseShape') #フェース選択の状態からオブジェクト選択に変更
        cmds.move(-sp_trdHgt / 4, 'SpiralStairsTread_BaseShape', y = True) #Y座標0に踏板の天面をそろえる
        vtxLoc = cmds.xform('SpiralStairsTread_BaseShape.vtx[4]', q = True, t = True, ws = True) #踏板の設置基準となる頂点4の座標を取得
        cmds.move(vtxLoc[1], 'SpiralStairsTread_BaseShape.scalePivot', 'SpiralStairsTread_BaseShape.rotatePivot', rpr = True, y = True) #踏板のピボットY座標を頂点4のY座標に合わせる
        cmds.makeIdentity(a = True, pn = True, r = True, s = True, t = True) #座標の値を全て0にする
        cmds.move(sp_stpHgt, 'SpiralStairsTread_BaseShape', y = True) #1段目の位置に移動
        sp_nowLoY += sp_stpHgt #2段目のために変数調整

        for a in range(sp_rodNum): #螺旋の周数
            for b in range(sp_stpNum - 1): #1周あたりの段数
                sp_dupObj = cmds.duplicate('SpiralStairsTread_BaseShape', n = "dup_SpiralStairsTreadBaseShape") #踏板を複製
                cmds.rotate(sp_nowAgl, sp_dupObj, y = True, r = True, os = True, fo = True) #複製した踏板を回転
                cmds.move(sp_nowLoY, sp_dupObj, y = True) #複製した踏板を配置
                sp_rnmObj = cmds.rename("dup_SpiralStairsTreadBaseShape", "renamed_SpiralStairsTreadBaseShape") #処理重複を防ぐために名称変更
                sp_nowAgl += sp_plcAgl #(sp_now全て)次の段のために値を調整
                sp_nowLoY += sp_stpHgt
        else:
            sp_objPos = cmds.xform(sp_rnmObj, q = True, t = True, ws = True) #最後に複製したオブジェクトの座標を取得
            sp_remNum = sp_strHgt - sp_objPos[1] #指定した階段の高さと実際の高さの差
            if sp_objPos[1] < sp_strHgt and sp_remNum >= sp_stpHgt: #現在の階段の高さが指定した値に到達しておらず、かつ差の値が1段あたりの高さ以上であるか
                sp_extStp = round(sp_remNum / sp_stpHgt) #差に追加できる段数
                for c in range(sp_extStp):
                    sp_dupObj = cmds.duplicate('SpiralStairsTread_BaseShape', n = "dup_SpiralStairsTreadBaseShape")
                    cmds.rotate(sp_nowAgl, sp_dupObj, y = True, r = True, os = True, fo = True)
                    cmds.move(sp_nowLoY, sp_dupObj, y = True)
                    sp_rnmObj = cmds.rename("dup_SpiralStairsTreadBaseShape", "renamed_SpiralStairsTreadBaseShape")
                    sp_nowAgl += sp_plcAgl
                    sp_nowLoY += sp_stpHgt

        sp_objNms = cmds.ls('SpiralStairsTread_BaseShape*', 'renamed_SpiralStairsTreadBaseShape*', g = True) #結合するオブジェクトを検索
        sp_objLRs = cmds.listRelatives(sp_objNms, p = True) #検索結果からオブジェクト名のみに絞る
        cmds.select(sp_objLRs)
        cmds.polyUnite()

        if sp_strType == 2 and sp_dltFcs == True and sp_mrgVtx == True: #ボックス階段、表面以外フェース削除、頂点マージの3つ全て選択した場合
            cmds.polyMergeVertex() #重なっている頂点をマージ、上記の条件以外で仮に実行した場合エラーポリゴンになる可能性があるため

        cmds.rename("united_SpiralStairs")

        if sp_crtPlr == True: #支柱を作成
            cmds.polyCylinder(n = "SpiralStairsPillar_BaseShape", h = sp_strHgt, r = sp_hleRds, sa = sp_stpNum, sc = 1) #支柱を作成
            cmds.move(sp_strHgt / 2, y = True) #螺旋階段の座標Yに合わせる
            sp_objNms = cmds.ls('united_SpiralStairs*', 'SpiralStairsPillar_BaseShape*', g = True) #結合する螺旋階段と支柱を検索
            sp_objLRs = cmds.listRelatives(sp_objNms, p = True)
            cmds.select(sp_objLRs)
            cmds.polyUnite()
            cmds.rename("SpiralStairs_withPillar")
        else:
            cmds.rename("united_SpiralStairs", "SpiralStairs")
        
        cmds.DeleteHistory()


    def change_spStrGenType_spStpGenType(self, *args):
        if cmds.optionMenu('setSp_strGenType', q = True, v = True) == '1段あたりの高さ & 1周あたりの段数':
            cmds.floatSliderGrp('setSp_strHgt', e = True, en = False)
            cmds.floatSliderGrp('setSp_strAgl', e = True, en = False)
            cmds.floatSliderGrp('setSp_stpHgt', e = True, en = True)
            cmds.intSliderGrp('setSp_stpNum', e = True, en = True)
            cmds.radioButtonGrp('setSp_stpGenType', e = True, en = False)
        else:
            if cmds.optionMenu('setSp_strGenType', q = True, v = True) == '高さ':
                cmds.floatSliderGrp('setSp_strHgt', e = True, en = True)
                cmds.floatSliderGrp('setSp_strAgl', e = True, en = False)
                cmds.radioButtonGrp('setSp_stpGenType', e = True, en = True)
            elif cmds.optionMenu('setSp_strGenType', q = True, v = True) == '角度':
                cmds.floatSliderGrp('setSp_strHgt', e = True, en = False)
                cmds.floatSliderGrp('setSp_strAgl', e = True, en = True)
                cmds.radioButtonGrp('setSp_stpGenType', e = True, en = True, sl = 2) #段の生成方法の選択を強制的に「1周あたりの段数」にする
            
            if cmds.radioButtonGrp('setSp_stpGenType', q = True, sl = True) == 1: #1段あたりの高さ
                cmds.floatSliderGrp('setSp_stpHgt', e = True, en = True)
                cmds.intSliderGrp('setSp_stpNum', e = True, en = False)
            else: #1周あたりの段数
                cmds.floatSliderGrp('setSp_stpHgt', e = True, en = False)
                cmds.intSliderGrp('setSp_stpNum', e = True, en = True)

    
    def change_spStrType_spDltFcs(self, *args):
        if cmds.radioButtonGrp('setSp_strType', q = True, sl = True) == 1: #スケルトン階段
                cmds.floatSliderGrp('setSp_trdHgt', e = True, en = True)
        else: #ボックス階段
            cmds.floatSliderGrp('setSp_trdHgt', e = True, en = False)

        if cmds.radioButtonGrp('setSp_strType', q = True, sl = True) == 2 and cmds.checkBox('setSp_dltFcs', q = True, v = True):
            cmds.checkBox('setSp_mrgVtx', e = True, en = True) #ボックス階段、表面以外のフェース削除を選択した場合
        else:
            cmds.checkBox('setSp_mrgVtx', e = True, en = False)


StairsGenerator()
