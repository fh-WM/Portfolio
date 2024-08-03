#For Autodesk Maya 2024, Encoding UTF-8
import maya.cmds as cmds

class ObjectVisibilityOptionsTool():
    def __init__(self):
        self.toolWindow_objectVisibilityOptionsTool()


    def toolWindow_objectVisibilityOptionsTool(self):
        winName = "Object Visibility Options Tool"
        toolWin = cmds.window(winName)

        if cmds.window(winName, ex = True):
            cmds.deleteUI(winName) #同一のウィンドウが存在する場合削除

        cmds.columnLayout(adj = True)
        cmds.frameLayout("設定 01")
        cmds.textFieldButtonGrp('setObjNm01', l = "非表示にしたいオブジェクト名", bl = "選択中のオブジェクトを指定", bc = self.selected_object01)
        cmds.checkBoxGrp('setViewCb01', l = "非表示にしたいビュー選択", ncb = 4, la4 = ['パースビュー', '前面ビュー', '左面ビュー', '右面ビュー'])
        cmds.checkBoxGrp('setViewCb02', l = "　　　　　　　　　　　　", ncb = 3, la3 = ['上面ビュー', '下面ビュー', '後面ビュー'])
        cmds.frameLayout("設定 02")
        cmds.textFieldButtonGrp('setObjNm02', l = "非表示にしたいオブジェクト名", bl = "選択中のオブジェクトを指定", bc = self.selected_object02)
        cmds.checkBoxGrp('setViewCb03', l = "非表示にしたいビュー選択", ncb = 4, la4 = ['パースビュー', '前面ビュー', '左面ビュー', '右面ビュー'])
        cmds.checkBoxGrp('setViewCb04', l = "　　　　　　　　　　　　", ncb = 3, la3 = ['上面ビュー', '下面ビュー', '後面ビュー'])
        cmds.frameLayout("設定 03")
        cmds.textFieldButtonGrp('setObjNm03', l = "非表示にしたいオブジェクト名", bl = "選択中のオブジェクトを指定", bc = self.selected_object03)
        cmds.checkBoxGrp('setViewCb05', l = "非表示にしたいビュー選択", ncb = 4, la4 = ['パースビュー', '前面ビュー', '左面ビュー', '右面ビュー'])
        cmds.checkBoxGrp('setViewCb06', l = "　　　　　　　　　　　　", ncb = 3, la3 = ['上面ビュー', '下面ビュー', '後面ビュー'])
        cmds.frameLayout(l = "インフォメーション")
        cmds.text(l = "Last Updated: 2024.07.22", al = 'left')
        cmds.text(l = "For: Maya 2024", al = 'left')
        cmds.text(l = "Fuma Hara", al = 'left')
        cmds.button(l = "非表示を適用", c = self.hidden_objectVisibility)
        cmds.button(l = "非表示を全て解除", c = self.visible_objectVisibility)

        cmds.showWindow(toolWin)
        cmds.scriptJob(uid = [toolWin, self.close_toolWin]) #ウィンドウを削除した際に実行


    def selected_object01(self):
        self.sltObj01 = cmds.ls(sl = True) #選択中のオブジェクト

        if len(self.sltObj01) == 0:
            cmds.error("何も選択されていません、指定に失敗しました")
        elif len(self.sltObj01) > 1:
            cmds.error("複数指定することはできません、指定に失敗しました")

        cmds.textFieldButtonGrp('setObjNm01', e = True, tx = self.sltObj01[0]) #オブジェクト名を自動入力、設定01


    def selected_object02(self):
        self.sltObj02 = cmds.ls(sl = True) #選択中のオブジェクト

        if len(self.sltObj02) == 0:
            cmds.error("何も選択されていません、指定に失敗しました")
        elif len(self.sltObj02) > 1:
            cmds.error("複数指定することはできません、指定に失敗しました")

        cmds.textFieldButtonGrp('setObjNm02', e = True, tx = self.sltObj02[0]) #オブジェクト名を自動入力、設定02


    def selected_object03(self):
        self.sltObj03 = cmds.ls(sl = True) #選択中のオブジェクト

        if len(self.sltObj03) == 0:
            cmds.error("何も選択されていません、指定に失敗しました")
        elif len(self.sltObj03) > 1:
            cmds.error("1つ以上選択することはできません、指定に失敗しました")

        cmds.textFieldButtonGrp('setObjNm03', e = True, tx = self.sltObj03[0]) #オブジェクト名を自動入力、設定03


    def hidden_objectVisibility(self, *args):
        prpChk01 = cmds.checkBoxGrp('setViewCb01', q = True, v1 = True) #(Chk01全て)非表示にするカメラのチェック状態、設定01
        frtChk01 = cmds.checkBoxGrp('setViewCb01', q = True, v2 = True)
        lftChk01 = cmds.checkBoxGrp('setViewCb01', q = True, v3 = True)
        rgtChk01 = cmds.checkBoxGrp('setViewCb01', q = True, v4 = True)
        topChk01 = cmds.checkBoxGrp('setViewCb02', q = True, v1 = True)
        btmChk01 = cmds.checkBoxGrp('setViewCb02', q = True, v2 = True)
        bckChk01 = cmds.checkBoxGrp('setViewCb02', q = True, v3 = True)

        prpChk02 = cmds.checkBoxGrp('setViewCb03', q = True, v1 = True) #(Chk02全て)非表示にするカメラのチェック状態、設定02
        frtChk02 = cmds.checkBoxGrp('setViewCb03', q = True, v2 = True)
        lftChk02 = cmds.checkBoxGrp('setViewCb03', q = True, v3 = True)
        rgtChk02 = cmds.checkBoxGrp('setViewCb03', q = True, v4 = True)
        topChk02 = cmds.checkBoxGrp('setViewCb04', q = True, v1 = True)
        btmChk02 = cmds.checkBoxGrp('setViewCb04', q = True, v2 = True)
        bckChk02 = cmds.checkBoxGrp('setViewCb04', q = True, v3 = True)

        prpChk03 = cmds.checkBoxGrp('setViewCb05', q = True, v1 = True) #(Chk03全て)非表示にするカメラのチェック状態、設定03
        frtChk03 = cmds.checkBoxGrp('setViewCb05', q = True, v2 = True)
        lftChk03 = cmds.checkBoxGrp('setViewCb05', q = True, v3 = True)
        rgtChk03 = cmds.checkBoxGrp('setViewCb05', q = True, v4 = True)
        topChk03 = cmds.checkBoxGrp('setViewCb06', q = True, v1 = True)
        btmChk03 = cmds.checkBoxGrp('setViewCb06', q = True, v2 = True)
        bckChk03 = cmds.checkBoxGrp('setViewCb06', q = True, v3 = True)

        chkList01 = (prpChk01, frtChk01, lftChk01, rgtChk01, topChk01, btmChk01, bckChk01) #(List01-03)上記のチェック状態をまとめる
        chkList02 = (prpChk02, frtChk02, lftChk02, rgtChk02, topChk02, btmChk02, bckChk02)
        chkList03 = (prpChk03, frtChk03, lftChk03, rgtChk03, topChk03, btmChk03, bckChk03)
        camList = ('persp', 'front', 'left', 'side', 'top', 'bottom', 'back') #非表示に設定できるカメラ一覧
        camNum = 0 #カメラ指定番号

        nowCams01 = cmds.ls(ca = True) #現在アウトライナに存在するカメラ一覧
        nowCams02 = cmds.listRelatives(nowCams01, p = True) #カメラ名のみに絞る

        cmds.perCameraVisibility(ra = True) #可視性をリセット

        for camChk01 in chkList01: #設定01
            if camChk01 == True:
                if camList[camNum] in nowCams02:
                    cmds.perCameraVisibility(self.sltObj01, c = camList[camNum], hi = True) #チェックが入っており、カメラがアウトライナに存在している場合、非表示に設定
            camNum += 1 #値を調整
        else:
            camNum = 0 #値をリセット

        for camChk02 in chkList02: #設定02
            if camChk02 == True:
                if camList[camNum] in nowCams02:
                    cmds.perCameraVisibility(self.sltObj02, c = camList[camNum], hi = True)
            camNum += 1
        else:
            camNum = 0

        for camChk03 in chkList03: #設定03
            if camChk03 == True:
                if camList[camNum] in nowCams02:
                    cmds.perCameraVisibility(self.sltObj03, c = camList[camNum], hi = True)
            camNum += 1
        else:
            camNum = 0


    def visible_objectVisibility(self, *args):
        cmds.perCameraVisibility(ra = True) #可視性をリセット


    def close_toolWin(self):
        cmds.perCameraVisibility(ra = True) #ウィンドウを削除した際に可視性をリセット


ObjectVisibilityOptionsTool()
