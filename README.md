# 動画をアスキーアート化
Video ASCII-Artizationは動画をアスキーアート化するアプリです。
|  ![変換前](example_before.gif)  |  ![変換後](example_after.gif)   |
| :----: | :----: |
| 変換前 | 変換後 |

なんと、このソースコードのプログラムはすべて**AIによって作成**されています。
具体的には、Microsoft 360 Copilotを使用し、制作者が日本語でプロンプトを入力、Copilotにプログラムを生成してもらうといった形です。私は一切プログラムには手を付けておらず、欲しい機能があれば随時プロンプトに入力し、エラーが発生した場合はプロンプトにそれを貼り付けて修正させることを繰り返しました。一部、AIには難しい問題が発生した部分ではExcelなども使用しました。

## 使用方法
### 引数
#### 位置引数:

  `video_path`  
  動画ファイルのファイスパス
  
#### オプション:

  `-h, --help`  
  ヘルプメッセージを表示 
  
  `--font_path FONT_PATH`  default: `C:/Windows/Fonts/msgothic.ttc`  
  fontファイルへのパス

  `--font_size FONT_SIZE`  default: `10`  
  アスキーアートに使うフォントの大きさ(大きくすると文字の解像度が大きくなる)
                        
  `--char_width CHAR_WIDTH`  default: `4`  
  アスキーアート1文字あたりのピクセル数(大きいほど粗くなる)
                       
  `--output_width OUTPUT_WIDTH`  default: `1280`  
  出力動画の横幅
                        
  `--output_height OUTPUT_HEIGHT`  default: `720`  
  出力動画の縦幅
                        
  `--frame_skip FRAME_SKIP`  default: `1`  
  スキップするフレーム数(これを2にするとフレームレートが元動画の1/2になる)
                        
  `--max_workers MAX_WORKERS`  default: `4`  
  並列プロセス数(大きくすると高速化するが、CPUやメモリーの使用率が上昇する)
                        
  `--ascii_set {default,simple,complex}`  default: `default`  
  使用するASCII文字セット(default,simple,complex)

### exeファイルを使用する場合
1. コマンドプロンプトを起動し、exeファイルのパスを指定
2. その後ろに変換したい動画ファイルのパスを指定
3. 任意でオプションを追加
4. 実行すると`ユーザー\ビデオ\ASCII-artized_videos`にファイルが生成される
   
例 `C:\Users\user> Desctop\Video_ASCII_Artization.exe Videos\original.mp4 --ascii_set simple`
