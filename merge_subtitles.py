import youtube_dl
from datetime import timedelta
import srt
import os
import shutil
from pytube import YouTube
import re

def edit_filecontent(count):
    for i in range (count-1):
        fname = str(i+1)+".srt"
        filein = open(fname,"r",encoding="utf-8")
        a = filein.readlines()
        fileout = open(fname,"w",encoding="utf-8")
        b = "".join(a[3:])
        fileout.write(b)

        filein.close()
        fileout.close()

        f = open(fname,encoding="utf-8")
        index = 1
        line = f.readline()
        with open("file"+str(i+1)+".srt",'a',encoding="utf-8") as new_file:
            while line:
                if "-->" in line:
                    new_file.write(f"{str(index)}\n{line}")
                    index += 1
                else:
                    new_file.write(line)
                line = f.readline()
        f.close()
        os.remove(fname)


def merge_subs(count):
    allsubs = list()
    for i in range (count-1):
        fname = "file"+str(i+1)+".srt"
        fileread = open(fname,"r",encoding="utf-8")
        sub = list(srt.parse(fileread, ignore_errors=False))
        for j in range (len(sub)):
            allsubs.append(sub[j])
        fileread.close()

    merge = list(srt.sort_and_reindex(allsubs))
    
    total_file = open("merge.srt","w",encoding="utf-8")
    total_file.writelines(srt.compose(merge))
    total_file.close()

def add_folder(url):
    yt = YouTube(url)
    path2 = "./" + re.sub(r'[\/:*"<>|]',"",yt.title)
    if os.path.isdir(path2) == False: 
        os.mkdir(path2)
    return path2

def files_move(Path,path2):
    all_file_list = os.listdir(Path)

    for fname in all_file_list:
        ftype = os.path.splitext(fname)[1]
        if ftype == r".srt" or ftype == r".mp4" or ftype == r".mkv" or ftype == r".ogg" or ftype == r".webm" or ftype == r".flv" or ftype == r".txt":
            shutil.move(fname,path2)

def convert_txt():
    f = open("merge.srt","r",encoding="utf-8")
    srtfile = list(srt.parse(f, ignore_errors=False))
    with open("lyrics.txt","a",encoding="utf-8") as txtfile:
        for i in range (len(srtfile)):
            txtfile.write(srtfile[i].content+"\n")
    f.close


def main():
    url = input()
    lang = input().split()

    for i in range (len(lang)):
        ydl_opts = {
            "writesubtitles": True,
            "subtitleslangs": [lang[i]]}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    Path = os.getcwd() 
    all_file_list = os.listdir(Path)
    count = 1

    for file_name in all_file_list:
        new_fname = str(count)
        ftype = os.path.splitext(file_name)[1]
        if ftype == r".vtt":
            os.rename(os.path.join(Path, file_name), os.path.join(Path, new_fname+r".srt"))
            count = count + 1

    edit_filecontent(count)
    if count >= 3:
        merge_subs(count)
        convert_txt()
    add_folder(url)
    path2 = add_folder(url)
    files_move(Path,path2)

if __name__ == "__main__": 
    main()
