# Maya Python Tools
## 共通概要
### 使用言語
- Python 3.10.8
### 使用ライブラリ
- **メイン**：maya.cmds, PySide2
- **その他**：Python 標準ライブラリ、Maya 2024にデフォルトで搭載されているライブラリ
### 実行環境
- Autodesk Maya 2024 - Windows, Mac
### 実行方法
- **方法01**：
    1. Windowsの場合は`C:/Users/ユーザー名/Documents/maya/2024/ja-JP/scripts`、  
        Macの場合は`/Users/ユーザー名/Library/Preferences/Autodesk/maya/2024/ja-JP/scripts`にPythonファイルを入れ、Maya 2024を再起動
    2. Maya 2024エディタ下方にあるコマンドラインをPythonに切り替え、左側のInputに`.py`を省いたPythonファイル名を入力し実行、お好みでシェルフに登録
- **方法02**：
    - スクリプトを直接、Maya 2024のスクリプトエディタのPythonタブ内にペーストし実行
### ライセンス
- 常識の範囲内でご自由にご利用ください、また利用の際に生じたトラブルや損害等の責任は一切負いません。

## 各ツール概要
### Add Joint Tool
- **ツール概要**：親子関係にある2つのジョイントの間に、長さを均等に分割してジョイントを追加するツール
- **制作理由**：既にあるジョイントの間に追加でジョイントが欲しいとのことから

<details>
<summary>使用方法</summary>

1. **間にジョイントを追加したい直接の親子関係にあるジョイント2つを選択**
2. **「追加するジョイント数」を指定**
3. **「追加方法」から選択**
4. **「ジョイント名」を指定**
   - 未入力の場合、ジョイント名が`additional_joint`になります
   - 右横のスピンボックスからジョイント名末尾につける番号の最初の値を指定できます
5. **「追加」をクリック**
   - 2ジョイント間の長さを均等に分割する形でジョイントが追加されます
</details>

### Cube To Sphere Generator
- **ツール概要**：立方体をベースにポリゴンが均等に配分される球を生成するツール
- **制作理由**：Mayaのデフォルトで作成できるSphereではポリゴンの配分が上下に偏っており、そうでない均等に配分された球が必要な際に一手間かかるとのことから

<details>
<summary>使用方法</summary>

1. **「生成方法の選択」から選択**
2. **各値を指定**
   - 「球のセグメント数/分割数」は、「生成方法の選択」でベベルを選択した場合はセグメント数、スムースを選択した場合は分割数として扱われます
3. **その他項目を指定**
   - 「球全体をハードエッジ」：ハードエッジの球が生成されます、デフォルトではソフトエッジです
   - 「ヒストリを維持する」：生成する球のヒストリ情報が維持されたままになります、デフォルトでは削除されます
4. **「生成」をクリック**
</details>

### FBX Export Tool
- **ツール概要**：任意のファイルパス先に、新規フォルダの作成とFBX形式での書き出しを一緒に行えるツール
- **制作理由**：新規フォルダを事前に用意する手間を省き、かつ手軽に書き出しを行いたかったことから

<details>
<summary>使用方法</summary>

1. **FBX形式で書き出すオブジェクトを選択、複数選択可**
2. **「ファイル名」を指定**
   - 「入力する」：`入力した名前.fbx`になります
   - 「そのまま」：`選択中のオブジェクト名.fbx`になります、また複数のオブジェクトを選択し書き出す場合、選択中の全オブジェクト名がアンダーバーで接続された名前になります   
      (例: `pCube1_pCylinder1_pSphere1.fbx`)
3. **「書き出し先(ファイルパス)」を指定**
4. **新規フォルダの作成有無を指定**
   - 新規フォルダを作成する場合、「新規フォルダを作成」にチェックし新規フォルダ名を入力   
      「書き出し先(ファイルパス)」で指定した場所に新規フォルダが作成され、その中にFBXファイルの書き出しが行われます
5. **「書き出し」をクリック**
   - 書き出しが実行され、書き出したFBXファイルをエクスプローラーもしくはFinderで開きます
   - ツール上に今回の書き出しの諸情報がログとして記載されます
- **「ダイアログボックスを開く」**：Mayaのダイアログボックスが開きます
- **「エクスプローラー/Finderを開く」**：使用中のOSに合わせてどちらかが開きます
- **「ログをクリア」**：ログをクリアし、初期状態にリセットします
</details>

### JointChain Straightener
- **ツール概要**：ジョイントチェーンを直線化するツール
- **制作理由**：手軽に直線化や矯正を行えるようにしたかったことから

<details>
<summary>使用方法</summary>

1. **連続した親子関係にあるジョイントチェーンを3つ以上選択**
   - 矯正する座標基準に2つ、矯正対象に最低でも1つのジョイントが必要になるためです
2. **「登録」をクリック**
   - ジョイント名がボタン左横のリストに、上から親→子の順番で表示されます
   - オブジェクト名 / フルパス名で表示されます
3. **「矯正する軸」を1つ以上指定**
   - XYZ全て指定した場合は直線化になります
4. **「矯正 / 直線化」をクリック**
   - リストの一番上と一番下の2ジョイントを座標基準にし、矯正を行います
   - リストから「除外」を行なったジョイントは矯正されません
- **「除外」**：リストで選択している項目を除外します、リストはShift/Ctrlによる複数選択が利用できます
- **「リセット」**：リストを登録直後の状態にリセットします
- **「クリア」**：リストをクリアし、初期状態に戻します
- **「元の位置に戻す」**：ジョイントチェーンを登録時の位置に戻します
</details>

### Object Renamer
- **ツール概要**：オブジェクトのリネームを行うツール
- **制作理由**：多機能なリネームツールを制作したかったことから

<details>
<summary>使用方法</summary>

**リネーム**
1. **リネームするオブジェクトを選択、複数選択可**
2. **「登録」をクリック**
   - 「リネーム前」リストにオブジェクト名が登録されます   
3. **「リネーム前」リストからリネームするオブジェクト名を選択、複数選択可**
   - リストで選択したオブジェクト名のみリネームされます
   - Shift/Ctrlによる複数選択、ドラッグ＆ドロップによる並べ替えが利用できます
4. **リネーム後の名称を指定**
   - 「オブジェクト名」
      - 「自由入力」：入力欄に入力した名称を使用します
      - 「そのまま」：現在の名称を引き続き使用します
      - 「全て大文字に変換」：現在の名称を全て大文字に変換します
      - 「全て小文字に変換」：現在の名称を全て小文字に変換します
      - 「タイトルケースに変換」：現在の名称をタイトルケースに変換します   
         (例: `pSphere1` → `Psphere1`)
      - 「指定の文字列を置き換える」：現在の名称の指定部分の文字列を置き換えることができます   
         置き換えを行う際に大文字/小文字を区別しない場合、「大文字/小文字を区別する」のチェックを外す
   - 「プレフィックス」「サフィックス」
     - 「自由入力」：入力欄に入力した名称を使用します
     - 「数字」：「桁数」と「最初の値」を指定して数字を入れることができます、複数選択の場合、連番となります
1. **その他項目を指定**
   - 「文字列の間にアンダーバーを追加」：プレフィックス・オブジェクト名・サフィックスの各間にアンダーバーを追加するか指定できます
   - 「プレフィックスの前に追加する文字列」：プレフィックスよりも前に文字列を追加することができます
   - 「サフィックスの後に追加する文字列」：サフィックスよりも後ろに文字列を追加することができます
2. **「変更をプレビュー」をクリック**
   - 「リネーム後(プレビュー)」リストにリネーム後の名称をプレビューします、この段階ではまだリネームは行われていません
3. **「リネーム」をクリック**
   - リネームが行われ、「リネーム前」リストが更新されます
- **「ハイライト」**：ビューポート上で選択したオブジェクトが「リネーム前」リストに登録されていた場合、自動でリスト側も選択状態になります、またリスト上で選択したオブジェクトをビューポート上でも自動で選択します
- **「除外」**：「リネーム前」リストで選択している項目を除外します
- **「クリア」**：「リネーム前」「リネーム後(プレビュー)」のそれぞれをクリアします

**検索**
1. **検索するオブジェクト名を入力**
2. **検索するオブジェクトの種類を選択**
   - 選択した種類の中で検索が行われます
3. **「検索」をクリック**
   - 該当したオブジェクトが選択状態になります

**リセット**
1. メニューバーの「Reset」をクリック
2. リセットしたい項目を選択しクリック
</details>

### Name Blocks Sort Tool (Built-In: Object Renamer)
- **ツール概要**：アンダーバーで区切られた名前の各文字列を入れ替えるツール
- **制作理由**：名前が長く、部分的に入れ替えたいだけの場合に入力し直すのは一手間かかることから

<details>
<summary>起動方法</summary>

1. Object Renamerのメニューバーの「Sub Tool」をクリック
2. 「Name Blocks Sort Tool」を選択しクリック
</details>

<details>
<summary>使用方法</summary>

1. **リネームするオブジェクトを1つ選択**
2. **「登録」をクリック**
   - 「並べ替え前」にオブジェクト名が表示されます
3. **文字列のブロックをドラッグ＆ドロップで並べ替え**
   - アンダーバーで区切られた各文字列のブロックを並べ替えることができます
   - 並べ替えのエリアにアンダーバーは表示されません
4. **「変更をプレビュー」をクリック**
   - 「並べ替え後(プレビュー)」に並べ替え後のアンダーバーで接続されたオブジェクト名が表示されます
5. **「リネーム」をクリック**
- **「クリア」**：全ての項目がクリアされ、初期状態にリセットされます
</details>

### Object Visibility Controller
- **ツール概要**：オブジェクトを任意のビューでは非表示、別の任意のビューでは表示するように設定するツール
- **制作理由**：Mayaのイメージプレーンにあるオプション「カメラ越しの視点」をオブジェクトに対しても使用したいとのことから

<details>
<summary>使用方法</summary>

1. **非表示に設定するオブジェクトを選択、複数選択可**
2. **「登録」をクリック**
   - 「設定」項目別に3種類の非表示設定を管理できます
   - オブジェクト名が、クリックしたボタン左横のリストに表示されます
3. **非表示に設定するビューのチェックボックスにチェック、複数指定可**
4. **「非表示」をクリック**
   - マルチビューを利用している場合でも適用されます
- **「除外」**：クリックしたボタン左横のリストで選択している項目を除外します、リストはShift/Ctrlによる複数選択が利用できます
- **「クリア」**：クリックしたボタン左横のリストをクリアします
- **「非表示を全て解除」**：全てのビューで非表示が解除され、再び表示されます
- 非表示を適用したままツールを閉じた場合、自動的に非表示が全て解除されます
</details>

### Open Windows Detector
- **ツール概要**：Maya上で開いているウィンドウを検出し、管理や手前に移動を行うツール
- **制作理由**：WindowsのタスクビューではMacのMission Controlと異なり、子ウィンドウを表示してくれないためウィンドウを探す際に一手間かかることから

<details>
<summary>使用方法</summary>

1. **「検出/更新」をクリック**
   - Maya上で開いているウィンドウを検出し、リストに表示します
2. **リストより操作を行いたい項目を選択、複数選択可**
3. **ウィンドウを手前に移動させたい場合、「選択中の項目を手前に移動」をクリック**   
   **ウィンドウを閉じたい場合、「選択中の項目を閉じる」をクリック**
</details>

### Placement Tool
- **ツール概要**：配置基準に設定したメッシュのコンポーネント位置にオブジェクトを配置するツール
- **制作理由**：オブジェクトを人の手で大量に配置するのは大変な手間と時間がかかることから

<details>
<summary>使用方法</summary>

1. **配置基準とするメッシュを1つ選択**
2. **「登録」をクリック**
   - メッシュ名と頂点数/エッジ数/フェース数が表示されます
3. **「配置場所」「配置割合」を指定**
   - 「配置場所」
      - 「頂点位置」を選択した場合、そのまま頂点位置に配置されます
      - 「エッジ位置」を選択した場合、エッジの中央に配置されます
      - 「フェース位置」を選択した場合、フェースの中心に配置されます
   - 「配置割合」は指定した割合に合わせてランダムに配置場所が選ばれます
4. **その他項目を指定**
   - 「配置角度を配置場所の法線に合わせる」：法線に合わせて角度を調整します、「エッジ位置」を選択した場合は利用できません
   - 「配置するオブジェクトを配置場所数に合わせて複製し補完する」：配置場所数にあわせてオブジェクトを自動で補充します、チェックを外した場合、選択したオブジェクトのみが配置されます
   - 「配置後グループにまとめる」：配置したオブジェクトをグループにまとめます
5. **配置するオブジェクトを選択、複数選択可**
6. **「選択中のオブジェクトを配置」をクリック**
- **「除外」**：リストで選択している項目を除外します、リストはShift/Ctrlによる複数選択が利用できます
- **「リセット」**：リストを登録直後の状態にリセットし、「配置割合」を100%に戻します
- **「クリア」**：全ての項目をクリアし、初期状態にリセットします
- **「ハイライト」**：ビューポート上で選択したコンポーネントがリストに登録されていた場合、自動でリスト側も選択状態になります、またリスト上で選択したコンポーネントをビューポート上でも自動で選択します
</details>

### Quick Capture Tool
- **ツール概要**：手軽に複数枚ビューポートのキャプチャを行うツール
- **制作理由**：都度スクリーンショットやSnipping Toolを利用するのは手間がかかるとのことから

<details>
<summary>使用方法</summary>

1. **「ファイル名」を指定**
   - 「自動」：`maya_年月日_時分秒_カメラ名`になります
   - 「入力指定」：`入力した名称_カメラ名`になります
   - 「入力 & 連番」：`入力した名称_番号`になります、番号はゼロから開始されます
2. **「保存先」を指定**
3. **「ファイル形式」から選択**
   - 全て静止画となります
   - PNG, TIFF, WebP, HEIF, GIFを選択した場合、背景が透過されます
4. **「表示モード設定」から選択**
   - 選択した設定でキャプチャ画像に写ります
5. **「ライト設定」から選択**
   - 選択した設定でキャプチャ画像に写ります
6. **「キャプチャを行うカメラ」を指定**
   - ツール起動時に、既に存在しているカメラが自動的に登録されます
   - キャプチャを行うカメラを登録する場合、登録したいカメラを選択して「登録」をクリック
   - 「除外」：リストで選択している項目を除外します、リストはShift/Ctrlによる複数選択が利用できます
   - 「クリア」：リストをクリアします
   - 「再検出」：エディタ上に存在している全てのカメラを検出して自動登録します、「デフォルトのカメラを含める」のチェックを外した場合、ビューの視点用に使用されるカメラ全てを検出結果から除外します
7. **「キャプチャに含める要素」を指定**
   - キャプチャ画像にこれらの要素を写すか否かを選択できます
8. **キャプチャ終了後に保存先を自動で開くか否かを指定**
9. **「キャプチャ」をクリック**
- **「ダイアログボックスを開く」**：Mayaのダイアログボックスが開きます
- **「エクスプローラー/Finderを開く」**：使用中のOSに合わせてどちらかが開きます
</details>

### Rig Controller Generator
- **ツール概要**：リギング用のコントローラーを作成するツール
- **制作理由**：メッシュからカーブを作成する際に非常に手間がかかることから

<details>
<summary>使用方法</summary>

**プリセット形状から作成**
1. **「作成方法」から「プリセット形状」を選択**
2. **「プリセット形状」のリストから作成する形状を選択**
3. **「色」を指定**
   - 起動時点で赤色のボタンをクリックするとMayaのカラーエディタが開きます
   - 色を選択し、カラーエディタ最下部の「終了」をクリックすると指定されます
4. **「スケール」を指定**
5. **「コントローラー名」を指定**
   - 未入力の場合、コントローラー名が`Controller`になります
6. **「配置座標(XYZ)」を指定**
7. **「作成 / 変換」をクリック**

**メッシュから変換**
1. **変換するメッシュを1つ選択**
2. **「作成方法」から「選択中のメッシュを変換」を選択**
3. **「色」を指定**
   - 起動時点で赤色のボタンをクリックするとMayaのカラーエディタが開きます
   - 色を選択し、カラーエディタ最下部の「終了」をクリックすると指定されます
3. **「スケール」を指定**
4. **「コントローラー名」を指定**
   - 未入力の場合、コントローラー名が`Controller`になります
5. **「作成 / 変換」をクリック**
   - 変換元のメッシュに被る形で作成されます
</details>

### Spur Gear Generator
- **ツール概要**：平歯車を生成するツール
- **制作理由**：平歯車を1からモデリングするのは大変な手間がかかることから

<details>
<summary>使用方法</summary>

1. **各値を指定**
   - 「軸穴の半径」と「高さ(全歯たけ)」の和が「半径(歯先円半径)」の値を超えることがないように注意してください
2. **「生成」をクリック**
</details>

### Stairs Generator
- **ツール概要**：直線階段・らせん階段を生成するツール
- **制作理由**：階段を1からモデリングするのは大変な手間と時間がかかることから

<details>
<summary>使用方法</summary>

**直線階段**
1. **「生成方法の選択」から選択**
2. **「段の生成方法の選択」から選択**
3. **「階段の種類の選択」から選択**
   - 「スケルトン階段」：踏板同士が離れた状態になります
   - 「ボックス階段」：踏板同士がくっついた状態になります
4. **各値を指定**
5. **その他項目を指定**
   - 「階段の表面以外のフェースを削除」：人の足と触れる階段表面部分以外のフェースが削除されます
   - 「踏板同士の重なった頂点をマージ」：踏板同士の重なった頂点がマージされます   
      本項目はエラーポリゴンを防ぐため、「ボックス階段」を選択しており「階段の表面以外のフェースを削除」にチェックを入れている場合にのみ利用できます
6. **「生成」をクリック**

**らせん階段**
1. **「生成方法の選択」から選択**
2. **「段の生成方法の選択」から選択**
3. **「階段の種類の選択」から選択**
   - 「スケルトン階段」：踏板同士が離れた状態になります
   - 「ボックス階段」：踏板同士がくっついた状態になります
4. **各値を指定**
5. **その他項目を指定**
   - 「支柱を作成」：「中央支柱用の穴の半径」の値をもとに支柱が作成されます、また踏板の支柱と接する部分のフェースが自動的に削除されます
   - 「階段の表面以外のフェースを削除」：人の足と触れる階段表面部分以外のフェースが削除されます
   - 「踏板同士の重なった頂点をマージ」：踏板同士の重なった頂点がマージされます   
      本項目はエラーポリゴンを防ぐため、「ボックス階段」を選択しており「階段の表面以外のフェースを削除」にチェックを入れている場合にのみ利用できます
6. **「生成」をクリック**
</details>

### Surround Camera Setup Tool
- **ツール概要**：対象をぐるりと取り囲むカメラを作成・配置するツール
- **制作理由**：キャラクターモデルなどのサークルショットを行う際に、手軽にカメラを用意できるようにと思ったことから

<details>
<summary>使用方法</summary>

1. **「配置するカメラ」から選択**
   - 「選択中のカメラを複製」を選択した場合、複製するカメラを選択してください
2. **各値を指定**
3. **「カメラの向き」から選択**
4. **「カメラ名」を指定**
   - 未入力の場合、カメラ名が`SurroundCamera`になります
   - 右横のスピンボックスからカメラ名末尾につける番号の最初の値を指定できます
5. **「中心座標(XYZ)」を指定**
6. **配置後グループにまとめるか否かを指定**
7. **「配置」をクリック**
</details>

### Transform Randomizer
- **ツール概要**：オブジェクトを指定した範囲でランダムに移動、回転、スケールを行うツール
- **制作理由**：オブジェクトに対して手軽に乱数を適用させたいと思ったことから

<details>
<summary>使用方法</summary>

1. **ランダムを適用したいオブジェクトを選択、複数選択可**
2. **「値の基準空間」から選択**
3. **「ランダムの範囲」を指定**
   - 各軸ごとに指定した「最小値」から「最大値」の間でランダムに値が算出されます
   - 「ゼロ」：指定した軸の値を0にし、「最小値」「最大値」の指定を無視します
   - 「イチ」：指定した軸の値を1にし、「最小値」「最大値」の指定を無視します
   - 「XYZまとめて変更」：指定したトランスフォームの項目において、Y, Zの値をXに指定した「最小値」「最大値」と同じ範囲から算出します
     またXをゼロに指定している場合はY, Zもゼロになります
   - 「XYZ同じ値を適用」：指定したトランスフォームの項目において、Y, Zの値をXと同一の値に指定します
5. **「適用」をクリック**
   - 「移動」「回転」「スケール」全てまとめて適用されます
</details>

### What Is The Working Units Tool
- **ツール概要**：現在の作業単位の確認や変更を行えるツール
- **制作理由**：チーム制作の際に、作業単位の確認を見落としたままサイズが適切でないモデルを提出されることが度々あったため、手軽に確認や変更を行えるようにと思ったことから

<details>
<summary>使用方法</summary>

1. **「長さ」「角度」「時間」からそれぞれ選択**
2. **「作業単位を変更」をクリック**
   - 作業単位がまとめて一括で変更されます
- **「作業単位の確認」**：現在の作業単位がツール上にログとして記載されます
- **「ログをクリア」**：ログをクリアし、初期状態にリセットします
- **「プリファレンスを開く」**：Mayaのプリファレンスが開きます
</details>
