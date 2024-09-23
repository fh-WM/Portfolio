#For Autodesk Maya 2024, Encoding UTF-8
import maya.cmds as cmds

class ObjectVisibilityController():
    def __init__(self):
        self.toolUI()


    def toolUI(self):
        windowName = "Object Visibility Controller"
        toolWindow = cmds.window(windowName)

        if cmds.window(windowName, ex = True):
            cmds.deleteUI(windowName) #同一のウィンドウが存在する場合削除

        cmds.columnLayout(adj = True)
        cmds.frameLayout("設定 01")
        cmds.textFieldButtonGrp('set_objectName01', l = "非表示にするオブジェクト名", bl = "選択中のオブジェクトを指定", ed = False, bc = self.specify_object01)
        cmds.checkBoxGrp('set_cameraVisibility01', l = "非表示にするビュー選択", ncb = 4, la4 = ['パースビュー', '前面ビュー', '左面ビュー', '右面ビュー'])
        cmds.checkBoxGrp('set_cameraVisibility02', l = "　　　　　　　　　　　　", ncb = 3, la3 = ['上面ビュー', '下面ビュー', '後面ビュー'])
        cmds.frameLayout("設定 02")
        cmds.textFieldButtonGrp('set_objectName02', l = "非表示にするオブジェクト名", bl = "選択中のオブジェクトを指定", ed = False, bc = self.specify_object02)
        cmds.checkBoxGrp('set_cameraVisibility03', l = "非表示にするビュー選択", ncb = 4, la4 = ['パースビュー', '前面ビュー', '左面ビュー', '右面ビュー'])
        cmds.checkBoxGrp('set_cameraVisibility04', l = "　　　　　　　　　　　　", ncb = 3, la3 = ['上面ビュー', '下面ビュー', '後面ビュー'])
        cmds.frameLayout("設定 03")
        cmds.textFieldButtonGrp('set_objectName03', l = "非表示にするオブジェクト名", bl = "選択中のオブジェクトを指定", ed = False, bc = self.specify_object03)
        cmds.checkBoxGrp('set_cameraVisibility05', l = "非表示にするビュー選択", ncb = 4, la4 = ['パースビュー', '前面ビュー', '左面ビュー', '右面ビュー'])
        cmds.checkBoxGrp('set_cameraVisibility06', l = "　　　　　　　　　　　　", ncb = 3, la3 = ['上面ビュー', '下面ビュー', '後面ビュー'])
        cmds.frameLayout("インフォメーション")
        cmds.text(l = "Last Updated: 2024.09.22", al = 'left')
        cmds.text(l = "For: Maya 2024", al = 'left')
        cmds.text(l = "Fuma Hara", al = 'left')
        cmds.button(l = "非表示を適用", c = self.hidden_objectVisibility)
        cmds.button(l = "非表示を全て解除", c = self.visible_objectVisibility)

        cmds.showWindow(toolWindow)
        cmds.scriptJob(uid = [toolWindow, self.close_toolWindow]) #ウィンドウを削除した際に実行


    def specify_object01(self):
        self.selected_object01 = cmds.ls(sl = True) #選択中のオブジェクト

        if len(self.selected_object01) == 0:
            cmds.confirmDialog(b = "OK", icn = 'critical', m = "何も選択されていません、指定に失敗しました", t = "ERROR: Object Visibility Controller")
        elif len(self.selected_object01) > 1:
            cmds.confirmDialog(b = "OK", icn = 'critical', m = "複数指定することはできません、指定に失敗しました", t = "ERROR: Object Visibility Controller")
        
        cmds.textFieldButtonGrp('set_objectName01', e = True, tx = self.selected_object01[0]) #指定したオブジェクト名を表示
    

    def specify_object02(self):
        self.selected_object02 = cmds.ls(sl = True)

        if len(self.selected_object02) == 0:
            cmds.confirmDialog(b = "OK", icn = 'critical', m = "何も選択されていません、指定に失敗しました", t = "ERROR: Object Visibility Controller")
        elif len(self.selected_object02) > 1:
            cmds.confirmDialog(b = "OK", icn = 'critical', m = "複数指定することはできません、指定に失敗しました", t = "ERROR: Object Visibility Controller")
        
        cmds.textFieldButtonGrp('set_objectName02', e = True, tx = self.selected_object02[0])
    

    def specify_object03(self):
        self.selected_object03 = cmds.ls(sl = True)

        if len(self.selected_object03) == 0:
            cmds.confirmDialog(b = "OK", icn = 'critical', m = "何も選択されていません、指定に失敗しました", t = "ERROR: Object Visibility Controller")
        elif len(self.selected_object03) > 1:
            cmds.confirmDialog(b = "OK", icn = 'critical', m = "複数指定することはできません、指定に失敗しました", t = "ERROR: Object Visibility Controller")
        
        cmds.textFieldButtonGrp('set_objectName03', e = True, tx = self.selected_object03[0])


    def hidden_objectVisibility(self, *args):
        chkBox_persp01 = cmds.checkBoxGrp('set_cameraVisibility01', q = True, v1 = True) #(01全て)非表示にするビューのチェック状態
        chkBox_front01 = cmds.checkBoxGrp('set_cameraVisibility01', q = True, v2 = True)
        chkBox_left01 = cmds.checkBoxGrp('set_cameraVisibility01', q = True, v3 = True)
        chkBox_right01 = cmds.checkBoxGrp('set_cameraVisibility01', q = True, v4 = True)
        chkBox_top01 = cmds.checkBoxGrp('set_cameraVisibility02', q = True, v1 = True)
        chkBox_bottom01 = cmds.checkBoxGrp('set_cameraVisibility02', q = True, v2 = True)
        chkBox_back01 = cmds.checkBoxGrp('set_cameraVisibility02', q = True, v3 = True)

        chkBox_persp02 = cmds.checkBoxGrp('set_cameraVisibility03', q = True, v1 = True) #(02全て)非表示にするビューのチェック状態
        chkBox_front02 = cmds.checkBoxGrp('set_cameraVisibility03', q = True, v2 = True)
        chkBox_left02 = cmds.checkBoxGrp('set_cameraVisibility03', q = True, v3 = True)
        chkBox_right02 = cmds.checkBoxGrp('set_cameraVisibility03', q = True, v4 = True)
        chkBox_top02 = cmds.checkBoxGrp('set_cameraVisibility04', q = True, v1 = True)
        chkBox_bottom02 = cmds.checkBoxGrp('set_cameraVisibility04', q = True, v2 = True)
        chkBox_back02 = cmds.checkBoxGrp('set_cameraVisibility04', q = True, v3 = True)

        chkBox_persp03 = cmds.checkBoxGrp('set_cameraVisibility05', q = True, v1 = True) #(03全て)非表示にするビューのチェック状態
        chkBox_front03 = cmds.checkBoxGrp('set_cameraVisibility05', q = True, v2 = True)
        chkBox_left03 = cmds.checkBoxGrp('set_cameraVisibility05', q = True, v3 = True)
        chkBox_right03 = cmds.checkBoxGrp('set_cameraVisibility05', q = True, v4 = True)
        chkBox_top03 = cmds.checkBoxGrp('set_cameraVisibility06', q = True, v1 = True)
        chkBox_bottom03 = cmds.checkBoxGrp('set_cameraVisibility06', q = True, v2 = True)
        chkBox_back03 = cmds.checkBoxGrp('set_cameraVisibility06', q = True, v3 = True)

        list_chkBox01 = (chkBox_persp01, chkBox_front01, chkBox_left01, chkBox_right01, chkBox_top01, chkBox_bottom01, chkBox_back01) #(list_chkBox全て)上記のチェック状態をまとめる
        list_chkBox02 = (chkBox_persp02, chkBox_front02, chkBox_left02, chkBox_right02, chkBox_top02, chkBox_bottom02, chkBox_back02)
        list_chkBox03 = (chkBox_persp03, chkBox_front03, chkBox_left03, chkBox_right03, chkBox_top03, chkBox_bottom03, chkBox_back03)
        list_camera = ('persp', 'front', 'left', 'side', 'top', 'bottom', 'back') #カメラ一覧
        num_camera = 0 #カメラ番号指定用変数
        nowCameras01_ls = cmds.ls(ca = True) #現在アウトライナ上に存在するカメラ一覧
        nowCameras02_lr = cmds.listRelatives(nowCameras01_ls, p = True) #カメラ名のみに絞る

        cmds.perCameraVisibility(ra = True) #可視性をリセット

        for one_check01 in list_chkBox01:
            if one_check01 == True:
                if list_camera[num_camera] in nowCameras02_lr:
                    cmds.perCameraVisibility(self.selected_object01, c = list_camera[num_camera], hi = True) #チェックが入っており、カメラがアウトライナ上に存在している場合に非表示
            num_camera += 1
        else:
            num_camera = 0

        for one_check02 in list_chkBox02:
            if one_check02 == True:
                if list_camera[num_camera] in nowCameras02_lr:
                    cmds.perCameraVisibility(self.selected_object02, c = list_camera[num_camera], hi = True)
            num_camera += 1
        else:
            num_camera = 0

        for one_check03 in list_chkBox03:
            if one_check03 == True:
                if list_camera[num_camera] in nowCameras02_lr:
                    cmds.perCameraVisibility(self.selected_object03, c = list_camera[num_camera], hi = True)
            num_camera += 1
        else:
            num_camera = 0


    def visible_objectVisibility(self, *args):
        cmds.perCameraVisibility(ra = True)


    def close_toolWindow(self):
        cmds.perCameraVisibility(ra = True) #ウィンドウを削除した際に念の為可視性をリセット


ObjectVisibilityController()
