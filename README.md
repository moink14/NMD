
# NMD

Netease Music Downloader（网易云音乐下载器，简称NMD）

# 功能特性

|功能|介绍|
|:-----|:-----|
|单曲下载|下载单曲，选项包括：歌曲ID|
|歌单下载|下载歌单，选项包括：歌单ID|
|专辑下载|下载专辑，选项包括：专辑ID|
|歌手下载|下载歌手热门歌曲，选项包括：歌手ID，歌曲个数等|
|搜索|调用网易云官方API进行搜索操作，选项包括：搜索个数，关键词等|

|特性|介绍|
|:-----|:-----|
|官方|调用官方API，较安全|
|质量|320kb/s高质量音频|
|VIP|可试听即可下载，部分版权保护歌曲、灰色歌曲无法下载|
|完整|使用eyeD3模块对歌曲文件操作，实现歌曲封面，歌词等ID3数据存储，在播放器中效果更佳|
|自由|无保护，代码可进行fork，可自由修改|
|美观|界面多样，具有颜色显示，可切换使用tui或cli|

# 模块依赖

`requests`
`eyed3`

# 使用方法

```bash
pip install -r requirements.txt
python nmd.py
```

或

```bash
pip install -r requirements.txt
chmod +x nmd.py
./nmd.py
```

如需命令行执行，可

```bash
./nmd.py -h    查看帮助
./nmd.py -u0 -t 1 -i 歌曲ID                下载指定歌曲
./nmd.py -u0 -t 2 -i 歌单ID                下载指定歌单
./nmd.py -u0 -t 3 -i 专辑ID                下载指定歌单
./nmd.py -u0 -t 4 -n 下载个数 -i 歌单ID    下载指定歌手
./nmd.py -u0 -s 关键词 -n 搜索个数         搜索歌曲
```

# 屏幕截图

![单曲](https://user-images.githubusercontent.com/110345389/182302026-c6a5b1fc-8b78-45e1-9984-9d120ac71d86.jpg)
![歌单](https://user-images.githubusercontent.com/110345389/182302063-c69b5f55-7b8f-4a5b-9d91-e378bd6042a8.jpg)
![歌手](https://user-images.githubusercontent.com/110345389/182302166-3d1f4436-a41f-4a5f-800c-512943d1e9aa.jpg)
![专辑](https://user-images.githubusercontent.com/110345389/182302189-b4eb8929-d40d-471f-af01-d3d2108a9272.jpg)
![搜索](https://user-images.githubusercontent.com/110345389/182302177-07f8ea19-491d-4598-a4b4-4bdf1906a9e4.jpg)

# 感谢

- [metowolf/Meting](https://github.com/metowolf/Meting)
- [Beadd/MusicDownloader](https://github.com/Beadd/MusicDownloader)
