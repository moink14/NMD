# NMD
Netease Music Downloader（简称NMD）

# 功能特性
|功能|介绍|
|:-----|:-----|
|单曲下载|下载单曲，选项包括：歌曲ID|
|歌单下载|下载歌单，选项包括：歌单ID|
|专辑下载|下载专辑，选项包括：专辑ID|
|歌手下载|下载歌手热门歌曲，选项包括：歌手ID，歌曲个数等|
|搜索|调用网易云官方API进行搜索操作，选项包括：搜索个数，关键词等|

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

# 屏幕截图

![单曲](https://user-images.githubusercontent.com/110345389/182302026-c6a5b1fc-8b78-45e1-9984-9d120ac71d86.jpg)
![歌单](https://user-images.githubusercontent.com/110345389/182302063-c69b5f55-7b8f-4a5b-9d91-e378bd6042a8.jpg)
![歌手](https://user-images.githubusercontent.com/110345389/182302166-3d1f4436-a41f-4a5f-800c-512943d1e9aa.jpg)
![专辑](https://user-images.githubusercontent.com/110345389/182302189-b4eb8929-d40d-471f-af01-d3d2108a9272.jpg)
![搜索](https://user-images.githubusercontent.com/110345389/182302177-07f8ea19-491d-4598-a4b4-4bdf1906a9e4.jpg)


# 感谢
- [metowolf/Meting](https://github.com/metowolf/Meting)
- [Beadd/MusicDownloader](https://github.com/Beadd/MusicDownloader)
