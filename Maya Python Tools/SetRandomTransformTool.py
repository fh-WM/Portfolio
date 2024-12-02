#For Autodesk Maya 2024, Encoding UTF-8
import maya.cmds as cmds
import random

class SetRandomTransformTool():
    def __init__(self):
        self.toolUI()


    def toolUI(self):
        windowName = "Set Random Transform Tool"
        toolWindow = cmds.window(windowName)

        if cmds.window(windowName, ex = True):
            cmds.deleteUI(windowName) #同一のウィンドウが存在する場合削除

        cmds.columnLayout(adj = True)
        cmds.frameLayout(l = "ランダム配置の設定")
        cmds.text(l = "※始めにランダムに配置したいオブジェクトを選択してください", al = 'left')
        cmds.radioButtonGrp('set_type_location', l = "配置座標基準の選択", nrb = 2, la2 = ("完全にランダム", "現在の座標から"), sl = 1)
        cmds.floatSliderGrp('set_randomMin_location', l = "座標の範囲：最小値", f = True, min = -100, max = 100, v = -10)
        cmds.floatSliderGrp('set_randomMax_location', l = "最大値", f = True, min = -100, max = 100, v = 10)
        cmds.checkBoxGrp('setRLZero', l = "座標の値をゼロに設定", ncb = 3, la3 = ["X (左右)", "Y (高さ)", "Z (前後)"])
        cmds.floatSliderGrp('set_randomMin_rotation', l = "回転の範囲：最小値", f = True, min = -180, max = 180, v = -90)
        cmds.floatSliderGrp('set_randomMax_rotation', l = "最大値", f = True, min = -180, max = 180, v = 90)
        cmds.checkBoxGrp('setRRZero', l = "回転の値をゼロに設定", ncb = 3, la3 = ["X軸", "Y軸", "Z軸"])
        cmds.floatSliderGrp('set_randomMin_scale', l = "スケールの範囲：最小値", f = True, min = 0.1, max = 10, v = 0.5)
        cmds.floatSliderGrp('set_randomMax_scale', l = "最大値", f = True, min = 0.1, max = 10, v = 2)
        cmds.frameLayout(l = "複製の設定")
        cmds.text(l = "※始めに複製したいオブジェクトを選択してください", al = 'left')
        cmds.intSliderGrp('set_num_duplication', l = "複製回数", f = True, min = 1, max = 100, v = 10)
        cmds.frameLayout(l = "インフォメーション")
        cmds.text(l = "Last Updated: 2024.09.15", al = 'left')
        cmds.text(l = "For: Maya 2024", al = 'left')
        cmds.text(l = "Fuma Hara", al = 'left')
        cmds.button(l = "ランダム配置", c = self.setRandomTransform_objects)
        cmds.button(l = "複製", c = self.duplicate_objects)

        cmds.showWindow(toolWindow)


    def setRandomTransform_objects(self, *args):
        type_location = cmds.radioButtonGrp('set_type_location', q = True, sl = True) #配置座標基準の選択
        randomMin_location = cmds.floatSliderGrp('set_randomMin_location', q = True, v = True) #座標の範囲の最小値
        randomMax_location = cmds.floatSliderGrp('set_randomMax_location', q = True, v = True) #座標の範囲の最大値
        randomMin_rotation = cmds.floatSliderGrp('set_randomMin_rotation', q = True, v = True) #回転の範囲の最小値
        randomMax_rotation = cmds.floatSliderGrp('set_randomMax_rotation', q = True, v = True) #回転の範囲の最大値
        randomMin_scale = cmds.floatSliderGrp('set_randomMin_scale', q = True, v = True) #スケールの範囲の最小値
        randomMax_scale = cmds.floatSliderGrp('set_randomMax_scale', q = True, v = True) #スケールの範囲の最大値
        selected_objects = cmds.ls(sl = True, fl = True) #選択中のオブジェクト

        if type_location == 1:
            if cmds.checkBoxGrp('setRLZero', q = True, v1 = True): #座標：Xの値 World
                for oneObjL1 in selected_objects:
                    cmds.move(0, oneObjL1, x = True) #X軸方向に移動しない
            else:
                for oneObjL1 in selected_objects:
                    rndNum1 = round(random.uniform(randomMin_location, randomMax_location), 3) #範囲内でランダムな値を出し丸める
                    cmds.move(rndNum1, oneObjL1, x = True) #X軸方向に移動

            if cmds.checkBoxGrp('setRLZero', q = True, v2 = True): #座標：Yの値 World
                for oneObjL2 in selected_objects:
                    cmds.move(0, oneObjL2, y = True) #Y軸方向に移動しない
            else:
                for oneObjL2 in selected_objects:
                    rndNum2 = round(random.uniform(randomMin_location, randomMax_location), 3)
                    cmds.move(rndNum2, oneObjL2, y = True) #Y軸方向に移動

            if cmds.checkBoxGrp('setRLZero', q = True, v3 = True): #座標：Zの値 World
                for oneObjL3 in selected_objects:
                    cmds.move(0, oneObjL3, z = True) #Z軸方向に移動しない
            else:
                for oneObjL3 in selected_objects:
                    rndNum3 = round(random.uniform(randomMin_location, randomMax_location), 3)
                    cmds.move(rndNum3, oneObjL3, z = True) #Z軸方向に移動

        if type_location == 2:
            if cmds.checkBoxGrp('setRLZero', q = True, v1 = True): #座標：Xの値 Relative
                pass
            else:
                for oneObjL4 in selected_objects:
                    rndNum4 = round(random.uniform(randomMin_location, randomMax_location), 3)
                    cmds.move(rndNum4, oneObjL4, r = True, x = True) #X軸方向に移動、現在位置から

            if cmds.checkBoxGrp('setRLZero', q = True, v2 = True): #座標：Yの値 Relative
                pass
            else:
                for oneObjL5 in selected_objects:
                    rndNum5 = round(random.uniform(randomMin_location, randomMax_location), 3)
                    cmds.move(rndNum5, oneObjL5, r = True, y = True) #Y軸方向に移動、現在位置から

            if cmds.checkBoxGrp('setRLZero', q = True, v3 = True): #座標：Zの値 Relative
                pass
            else:
                for oneObjL6 in selected_objects:
                    rndNum6 = round(random.uniform(randomMin_location, randomMax_location), 3)
                    cmds.move(rndNum6, oneObjL6, r = True, z = True) #Z軸方向に移動、現在位置から

        if cmds.checkBoxGrp('setRRZero', q = True, v1 = True): #回転：Xの値
            for oneObjR1 in selected_objects:
                cmds.rotate(0, oneObjR1, x = True) #X軸で回転しない
        else:
            for oneObjR1 in selected_objects:
                rndNum7 = round(random.uniform(randomMin_rotation, randomMax_rotation), 3)
                cmds.rotate(rndNum7, oneObjR1, x = True) #X軸で回転

        if cmds.checkBoxGrp('setRRZero', q = True, v2 = True): #回転：Yの値
            for oneObjR2 in selected_objects:
                cmds.rotate(0, oneObjR2, y = True) #Y軸で回転しない
        else:
            for oneObjR2 in selected_objects:
                rndNum8 = round(random.uniform(randomMin_rotation, randomMax_rotation), 3)
                cmds.rotate(rndNum8, oneObjR2, y = True) #Y軸で回転

        if cmds.checkBoxGrp('setRRZero', q = True, v3 = True): #回転：Zの値
            for oneObjR3 in selected_objects:
                cmds.rotate(0, oneObjR3, z = True) #Z軸で回転しない
        else:
            for oneObjR3 in selected_objects:
                rndNum9 = round(random.uniform(randomMin_rotation, randomMax_rotation), 3)
                cmds.rotate(rndNum9, oneObjR3, z = True) #Z軸で回転

        for oneObj in selected_objects:
            rndNum = round(random.uniform(randomMin_scale, randomMax_scale), 3)
            cmds.scale(rndNum, rndNum, rndNum, oneObj) #大きさを変更

        cmds.select(selected_objects) #再度全て選択


    def duplicate_objects(self, *args):
        num_duplicate = cmds.intSliderGrp('set_num_duplication', q = True, v = True) #複製回数
        selected_objects = cmds.ls(sl = True, fl = True) #選択中のオブジェクト

        for i in range(num_duplicate):
            cmds.duplicate(selected_objects)


SetRandomTransformTool()
