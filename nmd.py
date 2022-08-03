#!/bin/env python3
# coding:UTF-8

#
# Code by:moink14           Thanks: https://github.com/metowolf/Meting
# https://github.com/moink14/nmd    https://github.com/Beadd/MusicDownloader
#

import json
import os
import requests
import eyed3
import time
import sys
import argparse

musicdir = "musics"
logdir = "logs"
logfile = (
    logdir
    + "/"
    + str(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time())))
    + ".log"
)
width = os.get_terminal_size().columns
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14",
    "Cookies": "JSESSIONID-WYYY=CvT03ZFeNp885UcP64TeTdiWUSHtJkHXN9bC9Q%2FOPNPTO9zPEAncPij3bVmZNtQbEAH0Y%2B6eEcNs4Kc%2F9khDXGgMtGwVJ24o79mQ6sEHqMq5KwPaCMDIggYjD%2FWBh6qwlp%2Fcp5fOQma0t6nddSnI5eziWO6IrjCDTYUkVF5fgt4Rp1Rm%3A1659358235220; _iuqxldmzr_=33; _ntes_nnid=1e9255eee71648482dd16c3d87ba0339,1659356435452; _ntes_nuid=1e9255eee71648482dd16c3d87ba0339; WEVNSM=1.0.0; WNMCID=ltednd.1659356435851.01.0",
    "Referer": "http://music.163.com/",
}


def cls():
    if sys.platform == "linux":
        try:
            input("将清空屏幕，回车继续，Ctrl+C终止")
        except KeyboardInterrupt:
            print("已退出")
            exit()
        os.system("clear")
    elif sys.platform == "windows":
        try:
            input("将清空屏幕，回车继续，Ctrl+C终止")
        except KeyboardInterrupt:
            print("已退出")
            exit()
        os.system("cls")
    else:
        input("回车继续，Ctrl+C终止")


global num
global count
global size
num, count, size = 0, 0, 0


def plog(pinfo, loginfo):
    print(pinfo, end="")
    with open(logfile, "a", encoding="utf8") as f:
        f.write(loginfo + "\n")


def check(path):
    if not os.path.exists(path):
        os.makedirs(path)


check(logdir)


# 单曲下载函数
def dsong(sid, sdir):
    global num
    global count
    global size
    # 定义，初始化
    url = "http://music.163.com/api/song/detail/?ids=%5B" + str(sid) + "%5D"
    req = requests.get(url, headers)
    j = json.loads(req.text)
    try:
        name = j["songs"][0]["name"]
    except KeyError:
        print("\033[33m歌曲不存在\033[0m")
        return 255
    num += 1
    # 可能的合作歌曲
    c = 1
    for i in j["songs"][0]["artists"]:
        if c:
            artist = i["name"]
        else:
            artist += "/" + i["name"]
        c = 0
    plog("%-3s" % str(num) + " | " + name + " - " + artist, name + " - " + artist)
    # 可能的特殊字符
    for i in '\/:*?">|':
        if i in name:
            name = name.replace(i, " ")

    check(sdir)

    musicapi = json.loads(
        requests.get(
            "http://music.163.com/api/song/enhance/player/url?ids=["
            + str(sid)
            + "]&br=320000",
            headers,
        ).text
    )
    musicurl = musicapi["data"][0]["url"]
    # 保存音频文件
    path = sdir + "/" + name + "." + musicapi["data"][0]["type"]
    with open(path, "wb") as f:
        f.write(requests.get(musicurl, headers).content)
    if not os.path.getsize(path):
        plog("\n\033[33m音乐 " + name + " 下载失败\033[0m\n", "  音乐下载失败")
        os.remove(path)
        return 255
    plog(
        " (%.1f Mb)\n" % (os.path.getsize(path) / 1024 / 1024),
        "  已保存，大小" + str(os.path.getsize(path)),
    )

    # 加载音频文件，增加ID3数据
    af = eyed3.load(path)
    af.tag.name = name
    af.tag.artist = artist
    plog("      基本信息嵌入", "  基本信息嵌入")
    picdata = requests.get(j["songs"][0]["album"]["picUrl"]).content
    af.tag.images.set(3, picdata, "image/jpeg")
    plog("  封面嵌入", "  封面嵌入")
    album = j["songs"][0]["album"]["name"]
    af.tag.album = album
    plog("  专辑嵌入", "  专辑嵌入")
    lyric = json.loads(
        requests.get(
            "http://music.163.com/api/song/lyric?id="
            + str(sid)
            + "&os=linux&lv=-1&kv=-1&tv=-1",
            headers,
        ).text
    )
    af.tag.lyrics.set(lyric["lrc"]["lyric"])
    plog("  歌词嵌入", "  歌词嵌入")
    af.tag.save(encoding="utf-8")
    print("")
    count += 1
    size += os.path.getsize(path)


# 多首歌曲下载
def dmore(url, name, typename, coverurl, tracklist):
    print("-" * width)
    req = requests.get(url, headers)
    j = json.loads(req.text)
    name = eval(name)
    coverurl = eval(coverurl)
    tracklist = eval(tracklist)
    mdir = musicdir + "/" + typename + "/" + name
    check(mdir)
    plog(typename + " " + name + " 已创建", "")
    with open(mdir + "/cover.jpg", "wb") as f:
        coverimgdata = requests.get(coverurl, headers).content
        f.write(coverimgdata)
    plog("  封面已写入\n", "")

    for i in tracklist:
        print("-" * width)
        dsong(i["id"], mdir)

    print("-" * width)
    print("状态 [%s/%s] 大小：%.1f MB" % (str(count), str(num), size / 1024 / 1024))
    print("-" * width)


def dplaylist(sid):
    try:
        dmore(
            "http://music.163.com/api/v6/playlist/detail?id=" + str(sid),
            'j["playlist"]["name"]',
            "歌单",
            'j["playlist"]["coverImgUrl"]',
            'j["playlist"]["trackIds"]',
        )
    except KeyError:
        print("\033[33m指定歌单不存在\033[0m")


def dalbum(sid):
    try:
        dmore(
            "http://music.163.com/api/v1/album/"
            + str(sid)
            + "?id="
            + str(sid)
            + "&ext=true&offset=0&total=true&limit=999",
            'j["album"]["name"]',
            "专辑",
            'j["album"]["picUrl"]',
            'j["songs"]',
        )
    except KeyError:
        print("\033[33m指定专辑不存在\033[0m")


def dartist(sid, num):
    try:
        dmore(
            "http://music.163.com/api/v1/artist/"
            + str(sid)
            + "?id="
            + str(sid)
            + "&ext=true&top="
            + str(num),
            'j["artist"]["name"]',
            "歌手",
            'j["artist"]["picUrl"]',
            'j["hotSongs"]',
        )
    except KeyError:
        print("\033[33m指定歌手不存在\033[0m")


def dsearch(keyword, num):
    url = (
        "http://music.163.com/api/cloudsearch/pc?s="
        + keyword
        + "&type=1&limit="
        + str(num)
        + "&total=true&offset=0"
    )
    req = requests.get(url, headers)
    j = json.loads(req.text)
    n = 1
    songs = {}
    for i in j["result"]["songs"]:
        print("%-2s %s" % (str(n), i["name"]))
        songs[n] = i["id"]
        n += 1
    sel = int(input("请输入结果序号："))
    print("-" * width)
    dsong(songs[sel], musicdir)
    print("-" * width)
    print("\033[36m下载完成\033[0m")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Netease Music Downloader(网易云音乐下载器)  推荐使用参数：-u进入交互界面"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-t",
        "--type",
        type=int,
        choices=[1, 2, 3, 4],
        help="下载类型，可选类型：1(单曲下载) 2（歌单下载） 3（专辑下载） 4（歌手下载）",
    )
    group.add_argument("-d", "--dir", type=str, help="音乐保存目录，参数：文件夹路径")
    group.add_argument("-s", "--search", type=str, help="搜索，参数：关键词")
    parser.add_argument(
        "-u",
        "--ui",
        type=int,
        choices=[0, 1],
        default=1,
        help="界面，可选类型：0（普通命令行） 1（终端交互）",
    )
    parser.add_argument("-i", "--id", type=int, help="网易云ID(单曲/歌单/专辑/歌手)")
    parser.add_argument("-n", "--num", type=int, help="获取数量（歌手及搜索需要）")
    args = parser.parse_args()
    if args.dir:
        musicdir = args.dir
    if args.ui == 1:
        cls()
        while True:
            print("-" * width)
            print("保存文件夹：\033[34m%s\033[0m\n日志：\033[34m%s\033[0m" % (musicdir, logfile))
            print("-" * width)
            print(
                """
            ID    介绍
            1     单曲下载
            2     歌单下载
            3     专辑下载
            4     歌手下载
            5     搜索
            """
            )
            print("-" * width)
            num = 0
            count = 0
            try:
                o = int(input("请输入选择："))
            except (TypeError, ValueError):
                print("\033[33m输入格式错误\033[0m")
                cls()
                continue
            if o == 1:
                i = int(input("请输入音乐ID："))
                dsong(i, musicdir)
                cls()
                continue
            if o == 2:
                i = int(input("请输入歌单ID："))
                dplaylist(i)
                cls()
                continue
            if o == 3:
                i = int(input("请输入专辑ID："))
                dalbum(i)
                cls()
                continue
            if o == 4:
                i = int(input("请输入歌手ID："))
                n = int(input("请输入获取个数："))
                dartist(i, n)
                cls()
                continue
            if o == 5:
                i = input("请输入搜索关键词：")
                n = int(input("请输入获取个数："))
                dsearch(i, n)
                cls()
                continue
            print("ID不存在")
            cls()
    if not args.id:
        if args.search:
            if args.num:
                dsearch(args.search, args.num)
            else:
                print("\033[33m请输入个数 --num\033[0m")
                parser.print_help()
        elif args.type:
            print("\033[33m请输入ID --id\033[0m")
            parser.print_help()
        else:
            print("\033[33m请输入合法参数\033[0m")
            parser.print_help()
    else:
        if args.type:
            if args.type == 4:
                if args.num:
                    dartist(args.id, args.num)
                else:
                    print("\033[33m请输入个数 --num\033[0m")
            else:
                if args.type == 1:
                    dsong(args.id, musicdir)
                elif args.type == 2:
                    dplaylist(args.id)
                else:
                    dalbum(args.id)
        else:
            print("\033[33m请输入类型 --type\033[0m")
