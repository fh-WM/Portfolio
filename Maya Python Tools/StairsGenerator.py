#For Autodesk Maya 2024, Encoding UTF-8
import maya.cmds as cmds
import math

class StairsGenerator():
    def __init__(self):
        self.toolUI()


    def toolUI(self):
        windowName = "Stairs Generator"
        toolWindow = cmds.window(windowName)

        if cmds.window(windowName, ex = True):
            cmds.deleteUI(windowName) #同一のウィンドウが存在する場合削除

        lyt_tabs = cmds.tabLayout(imh = 5, imw = 5)

        tab01_stairsGenerator = cmds.columnLayout(adj = True)
        cmds.frameLayout(l = "直線階段の設定")
        cmds.optionMenu('setSt_genType_stairs', l = "生成方法の選択", cc = self.change_st_genTypeStairs_genTypeStep)
        cmds.floatSliderGrp('setSt_length_stairs', l = "長さ", f = True, min = 0.1, max = 100, v = 25)
        cmds.floatSliderGrp('setSt_height_stairs', l = "高さ", f = True, min = 0.1, max = 100, v = 20)
        cmds.floatSliderGrp('setSt_angle_stairs', l = "角度", f = True, min = 0.1, max = 90, v = 30, en = False)
        cmds.radioButtonGrp('setSt_genType_step', l = "段の生成方法の選択", nrb = 3, la3 = ("1段あたりの高さ", "1段あたりの奥行", "段数"), sl = 1, cc = self.change_st_genTypeStairs_genTypeStep)
        cmds.floatSliderGrp('setSt_height_step', l = "1段あたりの高さ", f = True, min = 0.1, max = 50, v = 0.5)
        cmds.floatSliderGrp('setSt_depth_step', l = "1段あたりの奥行", f = True, min = 0.1, max = 50, v = 0.5, en = False)
        cmds.intSliderGrp('setSt_num_steps', l = "段数", f = True, min = 1, max = 500, v = 20, en = False)
        cmds.radioButtonGrp('setSt_type_stairs', l = "階段の種類の選択", nrb = 2, la2 = ("スケルトン階段", "ボックス階段"), sl = 1, cc = self.change_st_typeStairs_deleteFaces)
        cmds.menuItem(l = "長さ & 高さ", p = 'setSt_genType_stairs')
        cmds.menuItem(l = "長さ & 角度", p = 'setSt_genType_stairs')
        cmds.menuItem(l = "高さ & 角度", p = 'setSt_genType_stairs')
        cmds.menuItem(l = "1段あたりの高さ & 1段あたりの奥行 & 段数", p = 'setSt_genType_stairs')
        cmds.setParent(u = True) #"直線階段の設定"を親に指定

        cmds.frameLayout(l = "踏板の設定")
        cmds.floatSliderGrp('setSt_width_tread', l = "横幅", f = True, min = 0.1, max = 100, v = 3)
        cmds.floatSliderGrp('setSt_height_tread', l = "高さ", f = True, min = 0.1, max = 50, v = 0.3)
        cmds.floatSliderGrp('setSt_depth_tread', l = "奥行", f = True, min = 0.1, max = 50, v = 0.5)
        cmds.checkBox('setSt_delete_faces', l = "階段の表面以外のフェースを削除", cc = self.change_st_typeStairs_deleteFaces)
        cmds.checkBox('setSt_merge_vertex', l = "踏板同士の重なった頂点をマージ", en = False)
        cmds.button(l = "生成", c = self.generate_straightStairs)
        cmds.setParent(u = True) #"踏板の設定"を親に指定
        cmds.setParent(top = True) #tab01_StairsGeneratorを親に指定

        tab02_spiralStairsGenerator = cmds.columnLayout(adj = True)
        cmds.frameLayout(l = "らせん階段の設定")
        cmds.optionMenu('setSp_genType_stairs', l = "生成方法の選択", cc = self.change_sp_genTypeStairs_genTypeStep)
        cmds.floatSliderGrp('setSp_height_stairs', l = "高さ", f = True, min = 0.1, max = 100, v = 20)
        cmds.floatSliderGrp('setSp_angle_stairs', l = "角度", f = True, min = 0.1, max = 80, v = 20, en = False)
        cmds.radioButtonGrp('setSp_genType_step', l = "段の生成方法の選択", nrb = 2, la2 = ("1段あたりの高さ", "1周あたりの段数"), sl = 1, cc = self.change_sp_genTypeStairs_genTypeStep)
        cmds.floatSliderGrp('setSp_height_step', l = "1段あたりの高さ", f = True, min = 0.1, max = 50, v = 0.5)
        cmds.intSliderGrp('setSp_num_steps', l = "1周あたりの段数", f = True, min = 4, max = 500, v = 20, en = False)
        cmds.radioButtonGrp('setSp_type_stairs', l = "階段の種類の選択", nrb = 2, la2 = ("スケルトン階段", "ボックス階段"), sl = 1, cc = self.change_sp_typeStairs_deleteFaces)
        cmds.intSliderGrp('setSp_num_rounds', l = "周数", f = True, min = 1, max = 10, v = 1)
        cmds.floatSliderGrp('setSp_radius_hole', l = "中央支柱用の穴の半径", f = True, min = 0.1, max = 100, v = 2)
        cmds.menuItem(l = "高さ", p = 'setSp_genType_stairs')
        cmds.menuItem(l = "角度", p = 'setSp_genType_stairs')
        cmds.menuItem(l = "1段あたりの高さ & 1周あたりの段数", p = 'setSp_genType_stairs')
        cmds.setParent(u = True) #"らせん階段の設定"を親に指定

        cmds.frameLayout(l = "踏板の設定")
        cmds.floatSliderGrp('setSp_width_tread', l = "横幅", f = True, min = 0.1, max = 100, v = 3)
        cmds.floatSliderGrp('setSp_height_tread', l = "高さ", f = True, min = 0.1, max = 50, v = 0.3)
        cmds.checkBox('setSp_create_pillar', l = "支柱を作成")
        cmds.checkBox('setSp_delete_faces', l = "階段の表面以外のフェースを削除", cc = self.change_sp_typeStairs_deleteFaces)
        cmds.checkBox('setSp_merge_vertex', l = "踏板同士の重なった頂点をマージ", en = False)
        cmds.button(l = "生成", c = self.generate_spiralStairs)
        cmds.setParent(u = True) #"踏板の設定"を親に指定
        cmds.setParent(top = True) #tab02_SpiralStairsGeneratorを親に指定

        tab03_infomation = cmds.columnLayout(adj = True)
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
        cmds.text(l = "Last Updated: 2024.12.24", al = 'left')
        cmds.text(l = "For: Maya 2024", al = 'left')
        cmds.text(l = "Fuma Hara", al = 'left')
        cmds.setParent(u = True) #"インフォメーション"を親に指定
        cmds.setParent(top = True) #tab03_Infomationを親に指定

        cmds.tabLayout(lyt_tabs, e = True, tl = ((tab01_stairsGenerator, "直線階段   "),
                                                (tab02_spiralStairsGenerator, "らせん階段   "),
                                                (tab03_infomation, "インフォメーション   ")))
        cmds.showWindow(toolWindow)


    def generate_straightStairs(self, *args):
        st_genType_stairs = cmds.optionMenu('setSt_genType_stairs', q = True, v = True) #階段の生成方法の選択
        st_genType_step = cmds.radioButtonGrp('setSt_genType_step', q = True, sl = True) #段の生成方法の選択
        st_type_stairs = cmds.radioButtonGrp('setSt_type_stairs', q = True, sl = True) #階段の種類の選択

        st_length_stairs = cmds.floatSliderGrp('setSt_length_stairs', q = True, v = True) #階段の長さ
        st_height_stairs = cmds.floatSliderGrp('setSt_height_stairs', q = True, v = True) #階段の高さ
        st_angle_stairs = cmds.floatSliderGrp('setSt_angle_stairs', q = True, v = True) #階段の角度

        st_height_step = cmds.floatSliderGrp('setSt_height_step', q = True, v = True) #1段あたりの高さ
        st_depth_step = cmds.floatSliderGrp('setSt_depth_step', q = True, v = True) #1段あたりの奥行
        st_num_steps = cmds.intSliderGrp('setSt_num_steps', q = True, v = True) #段数

        st_width_tread = cmds.floatSliderGrp('setSt_width_tread', q = True, v = True) #踏板1つあたりの横幅
        st_height_tread = cmds.floatSliderGrp('setSt_height_tread', q = True, v = True) #踏板1つあたりの高さ
        st_depth_tread = cmds.floatSliderGrp('setSt_depth_tread', q = True, v = True) #踏板1つあたりの奥行

        st_delete_faces = cmds.checkBox('setSt_delete_faces', q = True, v = True) #階段の表面以外のフェースを削除
        st_merge_vertex = cmds.checkBox('setSt_merge_vertex', q = True, v = True) #踏板同士の重なった頂点をマージ

        tan_angle_stairs = math.tan(math.radians(st_angle_stairs))

        if st_genType_stairs == '長さ & 高さ' and st_genType_step == 1: #階段の長さ, 階段の高さ, 1段あたりの高さ
            st_num_steps = st_height_stairs / st_height_step

            if st_num_steps == round(st_num_steps): #段数の値が整数で割り切れているか否か
                st_depth_step = round(st_length_stairs / st_num_steps, 3)
            else:
                cmds.confirmDialog(b = "OK", icn = 'critical', m = "現在指定している値では階段を生成できません", t = "ERROR: Stairs Generator")
                cmds.error("生成が中止されました")

        elif st_genType_stairs == '長さ & 高さ' and st_genType_step == 2: #階段の長さ, 階段の高さ, 1段あたりの奥行
            st_num_steps = st_length_stairs / st_depth_step
            
            if st_num_steps == round(st_num_steps):
                st_height_step = round(st_height_stairs / st_num_steps, 3)
            else:
                cmds.confirmDialog(b = "OK", icn = 'critical', m = "現在指定している値では階段を生成できません", t = "ERROR: Stairs Generator")
                cmds.error("生成が中止されました")

        elif st_genType_stairs == '長さ & 高さ' and st_genType_step == 3: #階段の長さ, 階段の高さ, 段数
            st_height_step = round(st_height_stairs / st_num_steps, 3)
            st_depth_step = round(st_length_stairs / st_num_steps, 3)

        elif st_genType_stairs == '長さ & 角度' and st_genType_step == 1: #階段の長さ, 階段の角度, 1段あたりの高さ
            st_depth_step = round(st_height_step / tan_angle_stairs, 3)
            st_num_steps = round(st_length_stairs / st_depth_step)

        elif st_genType_stairs == '長さ & 角度' and st_genType_step == 2: #階段の長さ, 階段の角度, 1段あたりの奥行
            st_num_steps = round(st_length_stairs / st_depth_step)
            st_height_step = round(st_depth_step * tan_angle_stairs, 3)

        elif st_genType_stairs == '長さ & 角度' and st_genType_step == 3: #階段の長さ, 階段の角度, 段数
            st_depth_step = round(st_length_stairs / st_num_steps, 3)
            st_height_step = round(st_depth_step * tan_angle_stairs, 3)

        elif st_genType_stairs == '高さ & 角度' and st_genType_step == 1: #階段の高さ, 階段の角度, 1段あたりの高さ
            st_num_steps = round(st_height_stairs / st_height_step)
            st_depth_step = round(st_height_step / tan_angle_stairs, 3)

        elif st_genType_stairs == '高さ & 角度' and st_genType_step == 2: #階段の高さ, 階段の角度, 1段あたりの奥行
            st_height_step = round(st_depth_step * tan_angle_stairs, 3)
            st_num_steps = round(st_height_stairs / st_height_step)

        elif st_genType_stairs == '高さ & 角度' and st_genType_step == 3: #階段の高さ, 階段の角度, 段数
            st_height_step = round(st_height_stairs / st_num_steps, 3)
            st_depth_step = round(st_height_step / tan_angle_stairs, 3)

        elif st_genType_stairs == '1段あたりの高さ & 1段あたりの奥行 & 段数':
            pass #指定された値をそのまま使用し計算不要なため

        st_now_locationX = st_depth_step #現在の配置座標X、配置の度に変化する
        st_now_locationY = st_height_step #現在の配置座標Y、配置の度に変化する

        if st_type_stairs == 2: #ボックス階段
            st_depth_tread = st_depth_step #踏板の奥行を1段あたりの奥行で上書き
            st_height_tread = st_height_step #踏板の高さを1段あたりの高さで上書き

        cmds.polyCube(n = "StraightStairsTread_BaseShape", d = st_width_tread, h = st_height_tread, w = st_depth_tread) #踏板を作成

        if st_delete_faces == True: #階段の表面以外のフェース削除
            cmds.delete('StraightStairsTread_BaseShape.f[0]', 'StraightStairsTread_BaseShape.f[2:4]') #底面、側面、後面のフェースを削除

        cmds.select('StraightStairsTread_BaseShape') #フェース選択の状態からオブジェクト選択に変更
        cmds.move(-st_depth_tread / 2, st_height_tread / 2, st_width_tread / 2, 'StraightStairsTread_BaseShape.scalePivot', 'StraightStairsTread_BaseShape.rotatePivot', rpr = True) #踏板のピボット位置を変更
        cmds.move(-st_height_tread / 2, 'StraightStairsTread_BaseShape', y = True) #踏板のピボットY座標をワールドのY座標0に合わせる
        cmds.makeIdentity(a = True, pn = True, r = True, s = True, t = True) #座標の値を全て0にする
        cmds.move(st_now_locationY, 'StraightStairsTread_BaseShape', y = True) #1段目の位置に移動
        st_now_locationY += st_height_step #2段目配置のために値を調整

        for i in range(int(st_num_steps - 1)):
            st_duplicated_object = cmds.duplicate('StraightStairsTread_BaseShape', n = "dup_StraightStairsTreadBaseShape") #複製し仮名称に変更
            cmds.move(st_now_locationX, st_now_locationY, 0, st_duplicated_object) #踏板を配置
            cmds.rename("dup_StraightStairsTreadBaseShape", "renamed_StraightStairsTreadBaseShape") #仮名称から変更
            st_now_locationX += st_depth_step #(mvLoc全て)次の段のために値を調整
            st_now_locationY += st_height_step

        st_objects01_ls = cmds.ls('StraightStairsTread_BaseShape*', 'renamed_StraightStairsTreadBaseShape*', g = True) #結合するオブジェクトを検索
        st_objects02_lr = cmds.listRelatives(st_objects01_ls, p = True) #検索結果からオブジェクト名のみに絞る
        cmds.select(st_objects02_lr)
        cmds.polyUnite()

        if st_type_stairs == 2 and st_delete_faces == True and st_merge_vertex == True: #ボックス階段、表面以外フェース削除、頂点マージの3つ全て選択した場合
            cmds.polyMergeVertex() #重なっている頂点をマージ、上記の条件以外で仮に実行した場合エラーポリゴンになる可能性があるため

        cmds.rename("StraightStairs")
        cmds.DeleteHistory()


    def change_st_genTypeStairs_genTypeStep(self, *args):
        if cmds.optionMenu('setSt_genType_stairs', q = True, v = True) == '1段あたりの高さ & 1段あたりの奥行 & 段数':
            cmds.floatSliderGrp('setSt_length_stairs', e = True, en = False) #en = Falseは操作不可
            cmds.floatSliderGrp('setSt_height_stairs', e = True, en = False)
            cmds.floatSliderGrp('setSt_angle_stairs', e = True, en = False)
            cmds.floatSliderGrp('setSt_height_step', e = True, en = True) #en = Trueは操作可
            cmds.floatSliderGrp('setSt_depth_step', e = True, en = True)
            cmds.intSliderGrp('setSt_num_steps', e = True, en = True)
            cmds.radioButtonGrp('setSt_genType_step', e = True, en = False)
        else:
            cmds.radioButtonGrp('setSt_genType_step', e = True, en = True)

            if cmds.optionMenu('setSt_genType_stairs', q = True, v = True) == '長さ & 高さ':
                cmds.floatSliderGrp('setSt_length_stairs', e = True, en = True)
                cmds.floatSliderGrp('setSt_height_stairs', e = True, en = True)
                cmds.floatSliderGrp('setSt_angle_stairs', e = True, en = False)

            elif cmds.optionMenu('setSt_genType_stairs', q = True, v = True) == '長さ & 角度':
                cmds.floatSliderGrp('setSt_length_stairs', e = True, en = True)
                cmds.floatSliderGrp('setSt_height_stairs', e = True, en = False)
                cmds.floatSliderGrp('setSt_angle_stairs', e = True, en = True)

            elif cmds.optionMenu('setSt_genType_stairs', q = True, v = True) == '高さ & 角度':
                cmds.floatSliderGrp('setSt_length_stairs', e = True, en = False)
                cmds.floatSliderGrp('setSt_height_stairs', e = True, en = True)
                cmds.floatSliderGrp('setSt_angle_stairs', e = True, en = True)

            if cmds.radioButtonGrp('setSt_genType_step', q = True, sl = True) == 1:
                cmds.floatSliderGrp('setSt_height_step', e = True, en = True)
                cmds.floatSliderGrp('setSt_depth_step', e = True, en = False)
                cmds.intSliderGrp('setSt_num_steps', e = True, en = False)

            elif cmds.radioButtonGrp('setSt_genType_step', q = True, sl = True) == 2:
                cmds.floatSliderGrp('setSt_height_step', e = True, en = False)
                cmds.floatSliderGrp('setSt_depth_step', e = True, en = True)
                cmds.intSliderGrp('setSt_num_steps', e = True, en = False)

            elif cmds.radioButtonGrp('setSt_genType_step', q = True, sl = True) == 3:
                cmds.floatSliderGrp('setSt_height_step', e = True, en = False)
                cmds.floatSliderGrp('setSt_depth_step', e = True, en = False)
                cmds.intSliderGrp('setSt_num_steps', e = True, en = True)
    

    def change_st_typeStairs_deleteFaces(self, *args):
        if cmds.radioButtonGrp('setSt_type_stairs', q = True, sl = True) == 1: #スケルトン階段
            cmds.floatSliderGrp('setSt_height_tread', e = True, en = True)
            cmds.floatSliderGrp('setSt_depth_tread', e = True, en = True)
        else: #ボックス階段
            cmds.floatSliderGrp('setSt_height_tread', e = True, en = False)
            cmds.floatSliderGrp('setSt_depth_tread', e = True, en = False)

        if cmds.radioButtonGrp('setSt_type_stairs', q = True, sl = True) == 2 and cmds.checkBox('setSt_delete_faces', q = True, v = True):
            cmds.checkBox('setSt_merge_vertex', e = True, en = True) #ボックス階段、表面以外のフェース削除を選択した場合
        else:
            cmds.checkBox('setSt_merge_vertex', e = True, en = False)


    def generate_spiralStairs(self, *args):
        sp_genType_stairs = cmds.optionMenu('setSp_genType_stairs', q = True, v = True) #階段の生成方法の選択
        sp_genType_step = cmds.radioButtonGrp('setSp_genType_step', q = True, sl = True) #段の生成方法の選択
        sp_type_stairs = cmds.radioButtonGrp('setSp_type_stairs', q = True, sl = True) #階段の種類の選択

        sp_height_stairs = cmds.floatSliderGrp('setSp_height_stairs', q = True, v = True) #階段の高さ
        sp_angle_stairs = cmds.floatSliderGrp('setSp_angle_stairs', q = True, v = True) #階段の角度
        sp_height_step = cmds.floatSliderGrp('setSp_height_step', q = True, v = True) #1段あたりの高さ
        sp_num_steps = cmds.intSliderGrp('setSp_num_steps', q = True, v = True) #1周あたりの段数

        sp_num_rounds = cmds.intSliderGrp('setSp_num_rounds', q = True, v = True) #螺旋の周数
        sp_radius_hole = cmds.floatSliderGrp('setSp_radius_hole', q = True, v = True) #中央支柱用の穴の半径

        sp_width_tread = cmds.floatSliderGrp('setSp_width_tread', q = True, v = True) #踏板の横幅
        sp_height_tread = cmds.floatSliderGrp('setSp_height_tread', q = True, v = True) #踏板の高さ

        sp_create_pillar = cmds.checkBox('setSp_create_pillar', q = True, v = True) #支柱を作成
        sp_delete_faces = cmds.checkBox('setSp_delete_faces', q = True, v = True) #階段の表面以外のフェースを削除
        sp_merge_vertex = cmds.checkBox('setSp_merge_vertex', q = True, v = True) #踏板同士の重なった頂点をマージ

        sp_radius_pPipe = sp_width_tread + sp_radius_hole #polyPipeの半径
        sp_height_tread = sp_height_tread * 2 #polyPipeのheightは何故か指定した値/2になってしまうため、Maya2024現在、理由は不明
        sp_height_stairs_1R = sp_height_stairs / sp_num_rounds #1周あたりの高さ
        
        if sp_genType_stairs == '高さ' and sp_genType_step == 1: #階段の高さ & 1段あたりの高さ
            sp_num_steps = round(sp_height_stairs_1R / sp_height_step)
        
        elif sp_genType_stairs == '高さ' and sp_genType_step == 2: #階段の高さ & 1周あたりの段数
            sp_height_step = round(sp_height_stairs_1R / sp_num_steps, 3)
        
        elif sp_genType_stairs == '角度' and sp_genType_step == 2: #階段の角度 & 1周あたりの段数
            sp_stpDph = round(math.sin(math.pi / sp_num_steps) * 2 * sp_radius_pPipe, 3) #1段あたりの奥行
            sp_height_step = round(math.tan(math.radians(sp_angle_stairs)) * sp_stpDph, 3)
            sp_height_stairs = sp_height_step * sp_num_steps * sp_num_rounds
        
        elif sp_genType_stairs == '1段あたりの高さ & 1周あたりの段数':
            sp_height_stairs = sp_height_step * sp_num_steps * sp_num_rounds

        sp_placeAngle_tread = round(360 / sp_num_steps, 3) #踏板の配置角度
        sp_now_angle = sp_placeAngle_tread #現在の配置角度、配置の度に変化する
        sp_now_locationY = sp_height_step #現在の配置高さ、配置の度に変化する

        if sp_num_steps < 4:
            cmds.confirmDialog(b = "OK", icn = 'critical', m = "現在指定している値では階段を生成できません", t = "ERROR: Stairs Generator")
            cmds.error("生成が中止されました")

        if sp_type_stairs == 2: #ボックス階段
            sp_height_tread = sp_height_step * 2 #踏板の高さを1段あたりの高さで上書き

        cmds.polyPipe(n = "SpiralStairsTread_BaseShape", h = sp_height_tread, t = sp_width_tread, r = sp_radius_pPipe, sa = sp_num_steps) #踏板のベースとなるパイプ作成
        cmds.delete(f"SpiralStairsTread_BaseShape.f[1:{sp_num_steps - 1}]", f"SpiralStairsTread_BaseShape.f[{sp_num_steps + 1}:{sp_num_steps * 2 - 1}]",
                    f"SpiralStairsTread_BaseShape.f[{sp_num_steps * 2 + 1}:{sp_num_steps * 3 - 1}]",
                    f"SpiralStairsTread_BaseShape.f[{sp_num_steps * 3 + 1}:{sp_num_steps * 4 - 1}]") #不要なフェースを削除
        cmds.select('SpiralStairsTread_BaseShape.e[4]', 'SpiralStairsTread_BaseShape.e[6]',
                    'SpiralStairsTread_BaseShape.e[8]', 'SpiralStairsTread_BaseShape.e[10]') #穴を構成するエッジを選択、1/2
        cmds.polyCloseBorder() #穴を埋める、1/2
        cmds.select('SpiralStairsTread_BaseShape.e[5]', 'SpiralStairsTread_BaseShape.e[7]',
                    'SpiralStairsTread_BaseShape.e[9]', 'SpiralStairsTread_BaseShape.e[11]') #穴を構成するエッジを選択、2/2
        cmds.polyCloseBorder() #穴を埋める、2/2

        if sp_delete_faces == True: #階段の表面以外のフェース削除
            cmds.delete('SpiralStairsTread_BaseShape.f[0]', 'SpiralStairsTread_BaseShape.f[2:3]','SpiralStairsTread_BaseShape.f[5]') #底面、側面、後面のフェースを削除
        else:
            if sp_create_pillar == True: #支柱を作成
                cmds.delete('SpiralStairsTread_BaseShape.f[0]') #支柱と接するフェースを削除

        cmds.select('SpiralStairsTread_BaseShape') #フェース選択の状態からオブジェクト選択に変更
        cmds.move(-sp_height_tread / 4, 'SpiralStairsTread_BaseShape', y = True) #Y座標0に踏板の天面をそろえる
        location_vertex = cmds.xform('SpiralStairsTread_BaseShape.vtx[4]', q = True, t = True, ws = True) #踏板の設置基準となる頂点4の座標を取得
        cmds.move(location_vertex[1], 'SpiralStairsTread_BaseShape.scalePivot', 'SpiralStairsTread_BaseShape.rotatePivot', rpr = True, y = True) #踏板のピボットY座標を頂点4のY座標に合わせる
        cmds.makeIdentity(a = True, pn = True, r = True, s = True, t = True) #座標の値を全て0にする
        cmds.move(sp_height_step, 'SpiralStairsTread_BaseShape', y = True) #1段目の位置に移動
        sp_now_locationY += sp_height_step #2段目のために変数調整

        for a in range(sp_num_rounds): #螺旋の周数
            for b in range(sp_num_steps - 1): #1周あたりの段数
                sp_duplicated_object = cmds.duplicate('SpiralStairsTread_BaseShape', n = "dup_SpiralStairsTreadBaseShape") #踏板を複製
                cmds.rotate(sp_now_angle, sp_duplicated_object, y = True, r = True, os = True, fo = True) #複製した踏板を回転
                cmds.move(sp_now_locationY, sp_duplicated_object, y = True) #複製した踏板を配置
                sp_renamed_object = cmds.rename("dup_SpiralStairsTreadBaseShape", "renamed_SpiralStairsTreadBaseShape") #処理重複を防ぐために名称変更
                sp_now_angle += sp_placeAngle_tread #(sp_now全て)次の段のために値を調整
                sp_now_locationY += sp_height_step
        else:
            sp_location_lastObject = cmds.xform(sp_renamed_object, q = True, t = True, ws = True) #最後に複製したオブジェクトの座標を取得
            sp_num_difference = sp_height_stairs - sp_location_lastObject[1] #指定した階段の高さと実際の高さの差

            if sp_location_lastObject[1] < sp_height_stairs and sp_num_difference >= sp_height_step: #現在の階段の高さが指定した値に到達しておらず、かつ差の値が1段あたりの高さ以上であるか
                sp_num_extraSteps = round(sp_num_difference / sp_height_step) #差に追加できる段数

                for c in range(sp_num_extraSteps):
                    sp_duplicated_object = cmds.duplicate('SpiralStairsTread_BaseShape', n = "dup_SpiralStairsTreadBaseShape")
                    cmds.rotate(sp_now_angle, sp_duplicated_object, y = True, r = True, os = True, fo = True)
                    cmds.move(sp_now_locationY, sp_duplicated_object, y = True)
                    sp_renamed_object = cmds.rename("dup_SpiralStairsTreadBaseShape", "renamed_SpiralStairsTreadBaseShape")
                    sp_now_angle += sp_placeAngle_tread
                    sp_now_locationY += sp_height_step

        sp_objects01_ls = cmds.ls('SpiralStairsTread_BaseShape*', 'renamed_SpiralStairsTreadBaseShape*', g = True) #結合するオブジェクトを検索
        sp_objects02_lr = cmds.listRelatives(sp_objects01_ls, p = True) #検索結果からオブジェクト名のみに絞る
        cmds.select(sp_objects02_lr)
        cmds.polyUnite()

        if sp_type_stairs == 2 and sp_delete_faces == True and sp_merge_vertex == True: #ボックス階段、表面以外フェース削除、頂点マージの3つ全て選択した場合
            cmds.polyMergeVertex() #重なっている頂点をマージ、上記の条件以外で仮に実行した場合エラーポリゴンになる可能性があるため

        cmds.rename("united_SpiralStairs")

        if sp_create_pillar == True: #支柱を作成
            cmds.polyCylinder(n = "SpiralStairsPillar_BaseShape", h = sp_height_stairs, r = sp_radius_hole, sa = sp_num_steps, sc = 1) #支柱を作成
            cmds.move(sp_height_stairs / 2, y = True) #螺旋階段の座標Yに合わせる
            sp_objects01_ls = cmds.ls('united_SpiralStairs*', 'SpiralStairsPillar_BaseShape*', g = True) #結合する螺旋階段と支柱を検索
            sp_objects02_lr = cmds.listRelatives(sp_objects01_ls, p = True)
            cmds.select(sp_objects02_lr)
            cmds.polyUnite()
            cmds.rename("SpiralStairs_withPillar")
        else:
            cmds.rename("united_SpiralStairs", "SpiralStairs")
        
        cmds.DeleteHistory()


    def change_sp_genTypeStairs_genTypeStep(self, *args):
        if cmds.optionMenu('setSp_genType_stairs', q = True, v = True) == '1段あたりの高さ & 1周あたりの段数':
            cmds.floatSliderGrp('setSp_height_stairs', e = True, en = False)
            cmds.floatSliderGrp('setSp_angle_stairs', e = True, en = False)
            cmds.floatSliderGrp('setSp_height_step', e = True, en = True)
            cmds.intSliderGrp('setSp_num_steps', e = True, en = True)
            cmds.radioButtonGrp('setSp_genType_step', e = True, en = False)
        else:
            if cmds.optionMenu('setSp_genType_stairs', q = True, v = True) == '高さ':
                cmds.floatSliderGrp('setSp_height_stairs', e = True, en = True)
                cmds.floatSliderGrp('setSp_angle_stairs', e = True, en = False)
                cmds.radioButtonGrp('setSp_genType_step', e = True, en = True)

            elif cmds.optionMenu('setSp_genType_stairs', q = True, v = True) == '角度':
                cmds.floatSliderGrp('setSp_height_stairs', e = True, en = False)
                cmds.floatSliderGrp('setSp_angle_stairs', e = True, en = True)
                cmds.radioButtonGrp('setSp_genType_step', e = True, en = True, sl = 2) #段の生成方法の選択を強制的に「1周あたりの段数」にする
            
            if cmds.radioButtonGrp('setSp_genType_step', q = True, sl = True) == 1: #1段あたりの高さ
                cmds.floatSliderGrp('setSp_height_step', e = True, en = True)
                cmds.intSliderGrp('setSp_num_steps', e = True, en = False)
            else: #1周あたりの段数
                cmds.floatSliderGrp('setSp_height_step', e = True, en = False)
                cmds.intSliderGrp('setSp_num_steps', e = True, en = True)

    
    def change_sp_typeStairs_deleteFaces(self, *args):
        if cmds.radioButtonGrp('setSp_type_stairs', q = True, sl = True) == 1: #スケルトン階段
                cmds.floatSliderGrp('setSp_height_tread', e = True, en = True)
        else: #ボックス階段
            cmds.floatSliderGrp('setSp_height_tread', e = True, en = False)

        if cmds.radioButtonGrp('setSp_type_stairs', q = True, sl = True) == 2 and cmds.checkBox('setSp_delete_faces', q = True, v = True):
            cmds.checkBox('setSp_merge_vertex', e = True, en = True) #ボックス階段、表面以外のフェース削除を選択した場合
        else:
            cmds.checkBox('setSp_merge_vertex', e = True, en = False)


StairsGenerator()
