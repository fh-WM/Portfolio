#For Autodesk Maya 2024, Encoding UTF-8
import maya.cmds as cmds

class CubeToSphereGenerator():
    def __init__(self):
        self.toolWindow_cubeToSphereGenerator()


    def toolWindow_cubeToSphereGenerator(self):
        winName = "Cube To Sphere Generator"
        toolWin = cmds.window(winName)

        if cmds.window(winName, ex = True):
            cmds.deleteUI(winName) #同一のウィンドウが存在する場合削除

        cmds.columnLayout(adj = True)
        cmds.frameLayout(l = "設定")
        cmds.radioButtonGrp('setGenType', l = "生成方法の選択", nrb = 2, la2 = ("ベベル", "スムース"), sl = 1)
        cmds.floatSliderGrp('setCbSpDmr', l = "球の直径", f = True, min = 0.1, max = 100, v = 1)
        cmds.intSliderGrp('setCbSpVal', l = "球のセグメント数/分割数", f = True, min = 1, max = 20, v = 4)
        cmds.checkBox('setEdgType', l = "球全体をハードエッジ")
        cmds.checkBox('setDltHist', l = "ヒストリを残さず生成", v = True) #起動時はチェック
        cmds.frameLayout(l = "インフォメーション")
        cmds.text(l = "Last Updated: 2024.07.22", al = 'left')
        cmds.text(l = "For: Maya 2024", al = 'left')
        cmds.text(l = "Fuma Hara", al = 'left')
        cmds.button(l = "生成", c = self.generate_cubeToSphere)

        cmds.showWindow(toolWin) #ウィンドウ表示


    def generate_cubeToSphere(self, *args):
        genType = cmds.radioButtonGrp('setGenType', q = True, sl = True) #球の生成方法選択
        cbSpDmr = cmds.floatSliderGrp('setCbSpDmr', q = True, v = True) #球の直径
        cbSpVal = cmds.intSliderGrp('setCbSpVal', q = True, v = True) #球のセグメント数(ベベル)/分割数(スムース)

        edgType = cmds.checkBox('setEdgType', q = True, v = True) #球全体をハードエッジ
        dltHist = cmds.checkBox('setDltHist', q = True, v = True) #ヒストリを残さず生成

        cmds.polyCube(n = "CubeToSphere_BaseShape", sx = 1, sy = 1, sz = 1, w = cbSpDmr, d = cbSpDmr, h = cbSpDmr) #球のベースとなる立方体作成

        if genType == 1:
            cmds.polyBevel3(at = 180, d = 1, mvt = 0.001, mv = True, ma = 180, oaf = True, sg = cbSpVal, sa = 30, ws = True, f = 1, sn = True) #立方体全体をベベル処理
            cmds.polyMergeVertex(d = 0.001) #頂点のマージ処理
        elif genType == 2:
            cmds.polySmooth(sdt = 2, ovb = 1, ofb = 3, dv = cbSpVal, c = 1, ksb = True, kt = True, kmb = 1, suv = True, sl = 1, dpe = 1, ps = 0.1, ro = 1, ch = True) #立方体全体をスムース処理

        if edgType == True:
            cmds.polySoftEdge(a = 0) #ハードエッジ処理
        else:
            cmds.polySoftEdge(a = 180) #ソフトエッジ処理

        cmds.rename("CubeToSphere_BaseShape", "CubeToSphere") #処理重複を防ぐために名称変更

        if dltHist == True:
            cmds.DeleteHistory() #ヒストリ削除


CubeToSphereGenerator()
