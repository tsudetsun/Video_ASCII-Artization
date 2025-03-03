# 動画をアスキーアート化
Video ASCII-Artizationは動画をアスキーアート化するアプリです。

![変換前](example_before.gif)
![変換後](example_after.gif)

なんと、このソースコードのプログラムはすべて**AIによって作成**されています。
具体的には、Microsoft 360 Copilotを使用し、制作者が日本語でプロンプトを入力、Copilotにプログラムを生成してもらうといった形です。私は一切プログラムには手を付けておらず、欲しい機能があれば随時プロンプトに入力し、エラーが発生した場合はプロンプトにそれを貼り付けて修正させることを繰り返しました。

## 使用方法
### 引数
#### 位置引数:

  `video_path`  動画ファイルのファイスパス
  
#### オプション:

  `-h, --help`  ヘルプメッセージを表示 
  
  `--font_path FONT_PATH`  fontファイルへのパス

  `--font_size FONT_SIZE`  アスキーアートに使うフォントの大きさ
                        
  `--char_width CHAR_WIDTH`  アスキーアート1文字あたりのピクセル数(大きいほど粗く)
                       
  `--output_width OUTPUT_WIDTH`  出力動画の横幅
                        
  `--output_height OUTPUT_HEIGHT`  出力動画の縦幅
                        
  `--frame_skip FRAME_SKIP`  スキップするフレーム数(これを2にするとフレームレートが元動画の1/2になる)
                        
  `--max_workers MAX_WORKERS`  並列プロセス数(大きくすると高速化するが、CPUやメモリーの使用率が上昇する)
                        
  `--ascii_set {default,simple,complex}`  使用するASCII文字セット(default,simple,complex)

### exeファイルを使用する場合
1. コマンドプロンプトを起動し、exeファイルのパスを指定
2. その後ろに変換したい動画ファイルのパスを指定
3. 任意でオプションを追加
4. 実行すると`ユーザー\ビデオ\ASCII-artized_videos`にファイルが生成される
   
例 `C:\Users\user> Desctop\Video_ASCII_Artization.exe Videos\original.mp4 --ascii_set simple`
