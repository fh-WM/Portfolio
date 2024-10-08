# Maya Python Tools
## 実行環境
- Autodesk Maya 2024 - Windows, Mac

## 使用言語
- Python 3.10.8

## 使用モジュール
- Maya 2024にデフォルトで含まれているモジュールを使用しているため、追加インストールはありません

## 実行方法
- **Windows**: `C:/Users/ユーザー名/Documents/maya/2024/ja-JP/scripts`に`.py`ファイルを入れ、実行
- **Mac**: `/Users/ユーザー名/Library/Preferences/Autodesk/maya/2024/ja-JP/scripts`に`.py`ファイルを入れ、実行
- スクリプトエディタのPythonタブ内に直接ペーストし実行することでもご利用いただけます

## ライセンス
- 常識の範囲内でご自由にご利用ください、また利用において生じたトラブルや損害等の責任は一切負いません

## キャプチャ動画 - YouTube
- [Maya Python Tools - YouTube](https://youtu.be/Mw3HSoIUSNw)

## 各ツール概要
### Object Renamer
- **作品概要**：オブジェクトのリネームを行うツール
- **制作理由**：以前より多機能なリネームツールを制作したかったことから
- **スクリプト**：[ObjectRenamer.py](https://github.com/fh-WM/Portfolio/blob/main/Maya%20Python%20Tools/ObjectRenamer.py)

<details>
<summary>使用方法</summary>

1. **リネームするオブジェクトを選択、複数選択可**
2. **「登録」をクリック**
   - 「登録」ボタン直上の「変更前リスト」に選択したオブジェクトが登録されます
3. **「変更前リスト」からリネームする対象を選択、複数選択可**
   - リストで選択した対象のみリネームされます
   - Shift/Ctrlによる複数選択、ドラッグ&ドロップによる並べ替えが可能です
4. **新規名称を指定**
   - 「オブジェクト名」
     - 「自由入力」：入力欄に自由に入力を行うことができます
     - 「そのまま」：選択中のオブジェクト名をそのまま使用します
     - 「全て大文字に変換」：選択中のオブジェクト名を全て大文字に変換します  
       (例: `pSphere1` > `PSPHERE1`)
     - 「全て小文字に変換」：選択中のオブジェクト名を全て小文字に変換します  
       (例: `pSphere1` > `psphere1`)
     - 「タイトルケースに変換」：選択中のオブジェクト名を全てタイトルケースに変換します  
       (例: `pSphere1` > `Psphere1`)
     - 「指定の文字列を置き換える」：選択中のオブジェクト名の指定部分の文字列を置き換えることができます  
       置き換える際に、大文字/小文字を区別するか否かを選択できます
   - 「プレフィックス」「サフィックス」
     - 「自由入力」：入力欄に自由に入力を行うことができます
     - 「数字」：「桁数」と「最初の値」を指定して数字を入れることができます、複数選択の場合連番となります
5. **オプションを指定**
   - 「文字列の間にアンダーバーを追加」：プレフィックス/オブジェクト名/サフィックス間のどこにアンダーバーを入れるか指定できます
   - 「プレフィックスの先頭に追加する文字列」：プレフィックスよりも前に文字列を追加することができます
   - 「サフィックスの末尾に追加する文字列」：サフィックスよりも後ろに文字列を追加することができます
6. **「変更をプレビュー」をクリック**
   - 「変更前リスト」の右側にある「変更後リスト」にリネーム後の名称をプレビューします、この段階ではまだリネームは行われていません
7. **「リネーム」をクリック**
   - リネームが行われ、リネーム後のオブジェクト名が「変更前リスト」に自動入力されます
- **「クリア」**：それぞれ「変更前リスト」「変更後リスト」をクリアできます
- **「検索」**：左横の入力欄に入力した内容からオブジェクト名を検索できます
  - 検索結果が自動選択されます
  - メッシュとNURBSサーフェスのみ検索できます
</details>

---

### Name Blocks Sort Tool (Built-In: Object Renamer)
本ツールはObject Renamerにサブツールとして実装されています
- **作品概要**：アンダーバーで区切られた名前の各文字列を入れ替えるツール
- **制作理由**：長い名前かつ部分的に入れ替えたいだけの場合に、1から入力し直すのは大変な手間がかかることから
- **スクリプト**：[ObjectRenamer.py](https://github.com/fh-WM/Portfolio/blob/main/Maya%20Python%20Tools/ObjectRenamer.py)

<details>
<summary>使用方法</summary>
  
1. **リネームするオブジェクトを1つ選択**
2. **「登録」をクリック**
   - 「並べ替え前」にオブジェクト名が自動入力されます
3. **文字列をドラッグ&ドロップで並べ替え**
   - アンダーバーで区切られた各文字列を並べ替えることができます  
    並べ替えの際に、アンダーバーは表示されません
4. **「変更をプレビュー」をクリック**
   - 「並べ替え後(プレビュー)」に並べ替えたオブジェクト名が自動入力されます
5. **「リネーム」をクリック**
- **「クリア」**：全ての項目がクリアされ、初期状態の戻ります
</details>

---

### Stairs Generator
- **作品概要**：直線階段・らせん階段を生成するツール
- **制作理由**：階段を1からモデリングするのは大変な手間と時間がかかることから
- **スクリプト**：[StairsGenerator.py](https://github.com/fh-WM/Portfolio/blob/main/Maya%20Python%20Tools/StairsGenerator.py)

<details>
<summary>使用方法：直線階段</summary>
  
1. **「生成方法の選択」から選択**
   - 選択した内容によって指定不要になる項目は一時的に操作不可となります
2. **「段の生成方法の選択」から選択**
   - 選択した内容によって指定不要となる項目は一時的に操作不可となります
3. **「階段の種類の選択」から選択**
   - 「スケルトン階段」を選択した場合、各値の指定次第では踏板同士が離れた状態になります
   - 「ボックス階段」を選択した場合、踏板同士がぴったりとくっついた状態になります  
    また「踏板の設定」の「高さ」「奥行」が指定不可となります
4. **各値を指定**
5. **オプションを指定**
   - 「階段の表面以外のフェースを削除」：一般的に階段表面の人の足と触れる部分以外のフェースが削除されます
   - 「踏板同士の重なった頂点をマージ」：踏板同士の重なった頂点がマージされます  
    本項目は、エラーポリゴンを防ぐため「階段の種類の選択」より「ボックス階段」を選択しており、「階段の表面以外のフェースを削除」にチェックが入っている場合にのみ利用できます
5. **「生成」をクリック**
</details>

<details>
<summary>使用方法：らせん階段</summary>
  
1. **「生成方法の選択」から選択**
   - 選択した内容によって指定不要になる項目は一時的に操作不可となります
2. **「段の生成方法の選択」から選択**
   - 選択した内容によって指定不要となる項目は一時的に操作不可となります
3. **「階段の種類の選択」から選択**
   - 「スケルトン階段」を選択した場合、各値の指定次第では踏板同士が離れた状態になります
   - 「ボックス階段」を選択した場合、踏板同士がぴったりとくっついた状態になります  
    また「踏板の設定」の「高さ」が指定不可となります
4. **各値を指定**
5. **オプションを指定**
   - 「支柱を作成」：「中央支柱用の穴の半径」に合わせて支柱が作成されます  
    また支柱と接する踏板のフェースが自動的に削除されます
   - 「階段の表面以外のフェースを削除」：一般的に階段表面の人の足と触れる部分以外のフェースが削除されます
   - 「踏板同士の重なった頂点をマージ」：踏板同士の重なった頂点がマージされます  
    本項目は、エラーポリゴンを防ぐため「階段の種類の選択」より「ボックス階段」を選択しており、「階段の表面以外のフェースを削除」にチェックが入っている場合にのみ利用できます
6. **「生成」をクリック**
</details>

---

### FBX Export Tool
- **作品概要**：任意のファイルパス先に、新規フォルダの作成とFBX形式での書き出しを同時に行えるツール
- **制作理由**：新規フォルダを事前に用意する手間を省き、かつ手軽に書き出しを行いたかったことから
- **スクリプト**：[FBXExportTool.py](https://github.com/fh-WM/Portfolio/blob/main/Maya%20Python%20Tools/FBXExportTool.py)

<details>
<summary>使用方法</summary>
  
1. **書き出すオブジェクトを選択、複数選択可**
2. **「ファイル名」を指定**
   - 「入力する」を選択した場合、`入力した名前.fbx`になります
   - 「そのまま」を選択した場合、`選択中のオブジェクト名.fbx`になります  
     また複数のオブジェクトを選択し書き出す場合、各オブジェクト名がアンダーバーで接続されます  
     (例: `obj_obj_obj.fbx`)
3. **「書き出し先(ファイルパス)」を指定**
4. **新規フォルダの作成有無を指定**
   - 新規フォルダを作成する場合、「新規フォルダを作成」にチェックし「新規フォルダ名」を指定  
    「書き出し先(ファイルパス)」で指定した場所に新規フォルダが作成され、その中に書き出したFBXファイルが格納されます
5. **「書き出し」をクリック**
   - 書き出しが実行されエクスプローラーもしくはFinderが自動で開き、書き出したFBXファイルを即座に確認することができます
   - また、ツール上に今回の書き出しの諸情報がログとして表示されます
- **「ダイアログボックスを開く」**：Mayaのダイアログボックスが開きます
- **「エクスプローラー/Finderを開く」**：Windowsの場合エクスプローラー、Macの場合Finderが開きます
- **「ログをクリア」**：ログがクリアされ、初期状態に戻ります
</details>

---

### Object Visibility Controller
- **作品概要**：オブジェクトを任意のビューでは非表示で、別の任意のビューでは表示できるように設定するツール
- **制作理由**：Mayaのイメージプレーンにあるオプション「カメラ越しの視点」をオブジェクトに対しても使用したいとのことから
- **スクリプト**：[ObjectVisibilityController.py](https://github.com/fh-WM/Portfolio/blob/main/Maya%20Python%20Tools/ObjectVisibilityController.py)

<details>
<summary>使用方法</summary>
  
1. **非表示にするオブジェクトを1つ選択**
   - 「設定」毎に指定することが可能なため、最大で3つのオブジェクトを同時に非表示にできます
2. **「選択中のオブジェクトを指定」をクリック**
   - オブジェクト名がボタン左横の欄に表示されます
3. **「非表示にするビュー選択」より指定、複数指定可**
4. **「非表示を適用」をクリック**
   - 指定したビューでオブジェクトが非表示になります、また複数のビューを利用している場合でも使用可能です
- **「非表示を全て解除」**：全てのビューで非表示が解除され、オブジェクトが再び表示されます
- 非表示を適用したまま誤ってツールを削除した場合でも、自動的に非表示を全て解除します
</details>

---

### What Is The Working Units Tool
- **作品概要**：現在の作業単位の確認や変更を行えるツール
- **制作理由**：チーム制作の際に、作業単位の確認を見落としサイズの異なるモデルを提出される事が度々あり、きちんと確認を行なってほしいと感じたことや、より簡単に作業単位の変更が行えるようにと思ったことから
- **スクリプト**：[WhatIsTheWorkingUnitsTool.py](https://github.com/fh-WM/Portfolio/blob/main/Maya%20Python%20Tools/WhatIsTheWorkingUnitsTool.py)

<details>
<summary>使用方法</summary>
  
1. **作業単位を変更する場合、「長さ」「角度」「時間」からそれぞれ選択**
2. **「作業単位を変更」をクリック**
   - 一括で作業単位が変更されます
- **「作業単位の確認」**：現在の作業単位がツール上にログとして表示されます
- **「ログをクリア」**：ログがクリアされ、初期状態に戻ります
- **「プリファレンスを開く」**：Mayaのプリファレンスが開きます
</details>

---

### Set Random Transform Tool
- **作品概要**：オブジェクトを指定した範囲でランダムに配置、回転、スケールを行うツール
- **制作理由**：オブジェクトを乱数的に人の手で配置するのは大変な手間がかかる上、どうしても偏りが出てしまうことから
- **スクリプト**：[SetRandomTransformTool.py](https://github.com/fh-WM/Portfolio/blob/main/Maya%20Python%20Tools/SetRandomTransformTool.py)

<details>
<summary>使用方法：ランダム配置</summary>
  
1. **ランダムに配置したいオブジェクトを選択、複数選択可**
2. **「配置座標基準の選択」から選択**
   - 「完全にランダム」を選択した場合、World座標基準で配置が行われます
   - 「現在の座標から」を選択した場合、Relative座標基準で配置が行われます
3. **各値を指定**
   - 「最小値」「最大値」でランダムに算出される値の範囲を指定できます
4. **値のゼロ設定有無を指定**
   - 「〜の値をゼロに設定」で指定した値にランダムを適用させることなくゼロに設定できます
5. **「ランダム配置」をクリック**
   - 選択状態を維持したままオブジェクトがランダムに配置されます
</details>

<details>
<summary>使用方法：複製</summary>
  
1. **複製したいオブジェクトを選択、複数選択可**
2. **「複製回数」を指定**
3. **「複製」をクリック**
</details>

---

### Spur Gear Generator
- **作品概要**：平歯車を生成するツール
- **制作理由**：平歯車を1からモデリングするのは大変な手間と時間がかかることから
- **スクリプト**：[SpurGearGenerator.py](https://github.com/fh-WM/Portfolio/blob/main/Maya%20Python%20Tools/SpurGearGenerator.py)

<details>
<summary>使用方法</summary>
  
1. **各値を指定**
   - 「軸穴の半径」と「高さ(全歯たけ)」の和が「半径(歯先円半径)」の値を超えないように指定してください
2. **「生成」をクリック**
</details>

---

### Cube To Sphere Generator
- **作品概要**：立方体をベースにポリゴンが均等に配分される球を生成するツール
- **制作理由**：Mayaのデフォルトで作成できるSphereではポリゴンの配分が上下に偏っており、そうでない均等に配分された球が必要な際に一手間かかるとのことから
- **スクリプト**：[CubeToSphereGenetator.py](https://github.com/fh-WM/Portfolio/blob/main/Maya%20Python%20Tools/CubeToSphereGenerator.py)

<details>
<summary>使用方法</summary>
  
1. **「生成方法の選択」から選択**
2. **各値を指定**
   - 「球のセグメント数/分割数」は、ベベルの場合はセグメント数、スムースの場合は分割数として扱われます
3. **オプションを指定**
   - 「球全体をハードエッジ」：球全体がハードエッジの状態で生成されます、デフォルトではソフトエッジです
   - 「ヒストリを維持する」：生成した球のヒストリ情報が維持されたままになります、デフォルトでは削除されます
4. **「生成」をクリック**
</details>
