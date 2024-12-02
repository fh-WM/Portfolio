#For Autodesk Maya 2024, Encoding UTF-8
import maya.cmds as cmds

class CubeToSphereGenerator():
    def __init__(self):
        self.toolUI()


    def toolUI(self):
        windowName = "Cube To Sphere Generator"
        toolWindow = cmds.window(windowName)

        if cmds.window(windowName, ex = True):
            cmds.deleteUI(windowName) #同一のウィンドウが存在する場合削除

        cmds.columnLayout(adj = True)
        cmds.frameLayout(l = "設定")
        cmds.radioButtonGrp('set_genType_ctSphere', l = "生成方法の選択", nrb = 2, la2 = ("ベベル", "スムース"), sl = 1)
        cmds.floatSliderGrp('set_diameter_ctSphere', l = "球の直径", f = True, min = 0.1, max = 100, v = 1)
        cmds.intSliderGrp('set_num_ctSphere', l = "球のセグメント数/分割数", f = True, min = 1, max = 20, v = 4)
        cmds.checkBox('set_type_edge', l = "球全体をハードエッジ")
        cmds.checkBox('set_delete_history', l = "ヒストリを維持する")
        cmds.frameLayout(l = "インフォメーション")
        cmds.text(l = "Last Updated: 2024.09.22", al = 'left')
        cmds.text(l = "For: Maya 2024", al = 'left')
        cmds.text(l = "Fuma Hara", al = 'left')
        cmds.button(l = "生成", c = self.generate_cubeToSphere)

        cmds.showWindow(toolWindow) #ウィンドウ表示


    def generate_cubeToSphere(self, *args):
        genType_ctSphere = cmds.radioButtonGrp('set_genType_ctSphere', q = True, sl = True) #球の生成方法選択
        diameter_ctSphere = cmds.floatSliderGrp('set_diameter_ctSphere', q = True, v = True) #球の直径
        num_ctSphere = cmds.intSliderGrp('set_num_ctSphere', q = True, v = True) #球のセグメント数(ベベル)/分割数(スムース)

        type_edge = cmds.checkBox('set_type_edge', q = True, v = True) #球全体をハードエッジ
        delete_history = cmds.checkBox('set_delete_history', q = True, v = True) #ヒストリを残さず生成

        cmds.polyCube(n = "CubeToSphere_BaseShape", sx = 1, sy = 1, sz = 1, w = diameter_ctSphere, d = diameter_ctSphere, h = diameter_ctSphere) #球のベースとなる立方体作成

        if genType_ctSphere == 1:
            cmds.polyBevel3(at = 180, d = 1, mvt = 0.001, mv = True, ma = 180, oaf = True, sg = num_ctSphere, sa = 30, ws = True, f = 1, sn = True) #立方体全体をベベル処理
            cmds.polyMergeVertex(d = 0.001) #頂点のマージ処理

        elif genType_ctSphere == 2:
            cmds.polySmooth(sdt = 2, ovb = 1, ofb = 3, dv = num_ctSphere, c = 1, ksb = True, kt = True, kmb = 1, suv = True, sl = 1, dpe = 1, ps = 0.1, ro = 1, ch = True) #立方体全体をスムース処理
            position_vtx24 = cmds.xform("CubeToSphere_BaseShape.vtx[24]", q = True, t = True, ws = True)
            position_vtx25 = cmds.xform("CubeToSphere_BaseShape.vtx[25]", q = True, t = True, ws = True) #対称の位置にある2頂点のワールド座標を取得、スムースはサイズが小さくなってしまうため
            distance_vtxs = abs(position_vtx24[0]) + abs(position_vtx25[0]) #現在の直径、2頂点の絶対値の和
            value_scale = diameter_ctSphere / distance_vtxs #元の指定した直径へスケールするのに必要な値
            cmds.scale(value_scale, value_scale, value_scale, "CubeToSphere_BaseShape")
            cmds.makeIdentity(a = True, s = True) #スケールの値を1にする

        if type_edge == True:
            cmds.polySoftEdge(a = 0) #ハードエッジ処理
        else:
            cmds.polySoftEdge(a = 180) #ソフトエッジ処理

        cmds.rename("CubeToSphere_BaseShape", "CubeToSphere") #処理重複を防ぐために名称変更

        if delete_history == False:
            cmds.DeleteHistory() #ヒストリ削除


CubeToSphereGenerator()
