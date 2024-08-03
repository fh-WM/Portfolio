#For Autodesk Maya 2024, Encoding UTF-8
import maya.cmds as cmds
import math

class SpurGearGenerator():
    def __init__(self):
        self.toolWindow_spurGearGenerator()
    

    def toolWindow_spurGearGenerator(self):
        winName = "Spur Gear Generator"
        toolWin = cmds.window(winName)

        if cmds.window(winName, ex = True):
            cmds.deleteUI(winName) #同一のウィンドウが存在する場合削除

        cmds.columnLayout(adj = True)
        cmds.frameLayout(l = "歯車の設定")
        cmds.floatSliderGrp('setSpGrRds', l = "半径(歯先円半径)", f = True, min = 0.1, max = 100, v = 3)
        cmds.floatSliderGrp('setSpGrHgt', l = "厚み(歯幅)", f = True, min = 0.1, max = 100, v = 0.6)
        cmds.floatSliderGrp('setSftHRds', l = "軸穴の半径", f = True, min = 0.1, max = 100, v = 0.3)
        cmds.intSliderGrp('setGrNum', l = "歯数", f = True, min = 8, max = 200, v = 12)
        cmds.frameLayout(l = "歯1つあたりの設定")
        cmds.floatSliderGrp('setGrHgt', l = "高さ(全歯たけ)", f = True, min = 0.1, max = 100, v = 0.5)
        cmds.floatSliderGrp('setGrAgl', l = "角度(圧力角)", f = True, min = 0.1, max = 180, v = 20)
        cmds.frameLayout(l = "インフォメーション")
        cmds.text(l = "Last Updated: 2024.07.22", al = 'left')
        cmds.text(l = "For: Maya 2024", al = 'left')
        cmds.text(l = "Fuma Hara", al = 'left')
        cmds.button(l = "生成", c = self.generate_spurGear)

        cmds.showWindow(toolWin)


    def generate_spurGear(self, *args):
        spGrRds = cmds.floatSliderGrp('setSpGrRds', q = True, v = True) #歯車の半径
        spGrHgt = cmds.floatSliderGrp('setSpGrHgt', q = True, v = True) #歯車の厚み
        sftHRds = cmds.floatSliderGrp('setSftHRds', q = True, v = True) #軸穴の半径
        grNum = cmds.intSliderGrp('setGrNum', q = True, v = True) #歯数
        grHgt = cmds.floatSliderGrp('setGrHgt', q = True, v = True) #歯1つあたりの高さ
        grAgl = cmds.floatSliderGrp('setGrAgl', q = True, v = True) #歯1つあたりの角度(圧力角)
        
        grNumX2 = grNum * 2 #歯数x2、歯車の凹凸両方を含めた数
        fcNum1 = grNumX2 * 2     #フェース選択用変数、凸部(歯)
        fcNum2 = grNumX2 * 2 + 1 #フェース選択用変数、凹部(歯と歯の間)

        tan_grAgl = math.tan(math.radians(grAgl)) #grAglにおけるtanθの値
        triHgt = tan_grAgl * grHgt #grHgtを直角三角形における底辺とした場合の高さ
        sclVal = 1 - round(triHgt, 5) #triHgtを小数点第五位で四捨五入、scaleが1を基準とした値のため引き算

        if sftHRds >= spGrRds - grHgt:
            cmds.error("軸穴の半径の値が大きすぎます、生成が中止されました")

        if grHgt >= spGrRds:
            cmds.error("歯1つあたりの高さの値が大きすぎます、生成が中止されました")

        if sclVal <= 0:
            cmds.error("歯1つあたりの角度の値が大きすぎます、生成が中止されました")

        cmds.polyPipe(n = "SpurGearBaseShape", h = spGrHgt * 2, r = spGrRds - grHgt, sa = grNumX2, t = spGrRds - grHgt - sftHRds) #歯車のベースとなるパイプ作成

        while fcNum1 < grNumX2 * 3 - 1:
            cmds.polyExtrudeFacet('SpurGearBaseShape.f[' + str(fcNum1) + ']', kft = True, ltz = grHgt) #歯となる部分を押し出し
            cmds.select('SpurGearBaseShape.f[' + str(fcNum1) + ']') #押し出したフェースを改めて選択
            cmds.scale(sclVal, sclVal, 1, cs = True) #歯に角度をつけるため大きさを調整
            fcNum1 += 2 #次の歯のために値を調整

        while fcNum2 < grNumX2 * 3:
            cmds.select('SpurGearBaseShape.f[' + str(fcNum2) + ']') #凹部のフェースを選択
            cmds.scale(sclVal, sclVal, 1, cs = True) #歯に角度をつけるため大きさを調整
            fcNum2 += 2

        cmds.select('SpurGearBaseShape')
        cmds.rename("SpurGearBaseShape", "SpurGear")
        cmds.DeleteHistory()


SpurGearGenerator()
