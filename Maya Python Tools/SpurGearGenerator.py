#For Autodesk Maya 2024, Encoding UTF-8
import maya.cmds as cmds
import math

class SpurGearGenerator():
    def __init__(self):
        self.toolUI()
    

    def toolUI(self):
        windowName = "Spur Gear Generator"
        toolWindow = cmds.window(windowName)

        if cmds.window(windowName, ex = True):
            cmds.deleteUI(windowName) #同一のウィンドウが存在する場合削除

        cmds.columnLayout(adj = True)
        cmds.frameLayout(l = "歯車の設定")
        cmds.floatSliderGrp('set_radius_spurGear', l = "半径(歯先円半径)", f = True, min = 0.1, max = 100, v = 3)
        cmds.floatSliderGrp('set_height_spurGear', l = "厚み(歯幅)", f = True, min = 0.1, max = 100, v = 0.6)
        cmds.floatSliderGrp('set_radius_shaftHole', l = "軸穴の半径", f = True, min = 0.1, max = 100, v = 0.3)
        cmds.intSliderGrp('set_num_gears', l = "歯数", f = True, min = 8, max = 200, v = 12)
        cmds.frameLayout(l = "歯1つあたりの設定")
        cmds.floatSliderGrp('set_height_gear', l = "高さ(全歯たけ)", f = True, min = 0.1, max = 100, v = 0.5)
        cmds.floatSliderGrp('set_angle_gear', l = "角度(圧力角)", f = True, min = 0.1, max = 180, v = 20)
        cmds.frameLayout(l = "インフォメーション")
        cmds.text(l = "Last Updated: 2024.09.15", al = 'left')
        cmds.text(l = "For: Maya 2024", al = 'left')
        cmds.text(l = "Fuma Hara", al = 'left')
        cmds.button(l = "生成", c = self.generate_spurGear)

        cmds.showWindow(toolWindow)


    def generate_spurGear(self, *args):
        radius_spurGear = cmds.floatSliderGrp('set_radius_spurGear', q = True, v = True) #歯車の半径
        height_spurGear = cmds.floatSliderGrp('set_height_spurGear', q = True, v = True) #歯車の厚み
        radius_shaftHole = cmds.floatSliderGrp('set_radius_shaftHole', q = True, v = True) #軸穴の半径
        num_gears = cmds.intSliderGrp('set_num_gears', q = True, v = True) #歯数
        height_gear = cmds.floatSliderGrp('set_height_gear', q = True, v = True) #歯1つあたりの高さ
        angle_gear = cmds.floatSliderGrp('set_angle_gear', q = True, v = True) #歯1つあたりの角度(圧力角)
        
        num_gearsX2 = num_gears * 2 #歯数x2、歯車の凹凸両方を含めた数
        num_face01 = num_gearsX2 * 2     #フェース選択用変数、凸部(歯)
        num_face02 = num_gearsX2 * 2 + 1 #フェース選択用変数、凹部(歯と歯の間)

        tan_angle_gear = math.tan(math.radians(angle_gear)) #grAglにおけるtanθの値
        height_triangle = tan_angle_gear * height_gear #grHgtを直角三角形における底辺とした場合の高さ
        val_scale = 1 - round(height_triangle, 5) #triHgtを小数点第五位で四捨五入、scaleが1を基準とした値のため引き算

        if radius_shaftHole >= radius_spurGear - height_gear:
            cmds.error("軸穴の半径の値が大きすぎます、生成が中止されました")

        if height_gear >= radius_spurGear:
            cmds.error("歯1つあたりの高さの値が大きすぎます、生成が中止されました")

        if val_scale <= 0:
            cmds.error("歯1つあたりの角度の値が大きすぎます、生成が中止されました")

        cmds.polyPipe(n = "SpurGearBaseShape", h = height_spurGear * 2, r = radius_spurGear - height_gear, sa = num_gearsX2, t = radius_spurGear - height_gear - radius_shaftHole) #歯車のベースとなるパイプ作成

        while num_face01 < num_gearsX2 * 3 - 1:
            cmds.polyExtrudeFacet('SpurGearBaseShape.f[' + str(num_face01) + ']', kft = True, ltz = height_gear) #歯となる部分を押し出し
            cmds.select('SpurGearBaseShape.f[' + str(num_face01) + ']') #押し出したフェースを改めて選択
            cmds.scale(val_scale, val_scale, 1, cs = True) #歯に角度をつけるため大きさを調整
            num_face01 += 2 #次の歯のために値を調整

        while num_face02 < num_gearsX2 * 3:
            cmds.select('SpurGearBaseShape.f[' + str(num_face02) + ']') #凹部のフェースを選択
            cmds.scale(val_scale, val_scale, 1, cs = True) #歯に角度をつけるため大きさを調整
            num_face02 += 2

        cmds.select('SpurGearBaseShape')
        cmds.rename("SpurGearBaseShape", "SpurGear")
        cmds.DeleteHistory()


SpurGearGenerator()
