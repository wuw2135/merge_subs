import youtube_dl
from datetime import timedelta
import srt
import os
import shutil
from pytube import YouTube
import re

def edit_filecontent():
    Path = os.getcwd() 
    all_file_list = os.listdir(Path)

    for file_name in all_file_list:
        fname = os.path.splitext(file_name)[0].split(".")[-1]
        ftype = os.path.splitext(file_name)[1]
        new_filename = fname+r".srt"
        if ftype == r".vtt":
            os.rename(os.path.join(Path, file_name), os.path.join(Path, new_filename))
            filein = open(new_filename,"r",encoding="utf-8")
            a = filein.readlines()
            fileout = open(new_filename,"w",encoding="utf-8")
            b = "".join(a[4:])
            fileout.write(b)

            filein.close()
            fileout.close()

            f = open(new_filename,encoding="utf-8")
            index = 1
            line = f.readline()
            with open("_"+new_filename,"a",encoding="utf-8") as new_file:
                while line:
                    if "-->" in line:
                        new_file.write(f"{str(index)}\n{line}")
                        index += 1
                    else:
                        new_file.write(line)
                    line = f.readline()
                f.close()
                os.remove(new_filename)
                            
    return Path,all_file_list

def merge_subs(all_file_list):
    mergesub = list()
    for file_name in all_file_list:
        ftype = os.path.splitext(file_name)[1]
        if ftype == r".srt":
            fileread = open(file_name,"r",encoding="utf-8")
            mergesub_list = list(srt.parse(fileread,ignore_errors=False))
            for i in range (len(mergesub_list)):
                mergesub.append(mergesub_list[i])
            fileread.close()

    merge = list(srt.sort_and_reindex(mergesub))
    
    total_file = open("merge.srt","w",encoding="utf-8")
    total_file.writelines(srt.compose(merge))
    total_file.close()

def add_folder(url):
    yt = YouTube(url)
    path2 = "./" + re.sub(r'[\/:*"<>|]',"_",yt.title)
    if os.path.isdir(path2) == False: 
        os.mkdir(path2)
    return path2

def files_move(Path,path2):
    all_file_list = os.listdir(Path)

    for file_name in all_file_list:
        ftype = os.path.splitext(file_name)[1]
        if ftype == r".srt" or ftype == r".mp4" or ftype == r".mkv" or ftype == r".ogg" or ftype == r".webm" or ftype == r".flv" or ftype == r".txt":
            shutil.move(file_name,path2)

def convert_txt():
    f = open("merge.srt","r",encoding="utf-8")
    srtfile = list(srt.parse(f, ignore_errors=False))
    timedetect = srtfile[0].start
    with open("lyrics.txt","a",encoding="utf-8") as txtfile:
        for i in range (len(srtfile)):
            if i+1 < len(srtfile):
                if srtfile[i+1].start - timedetect >= timedelta(seconds=1):
                    txtfile.write(srtfile[i].content+"\n\n")
                    timedetect = srtfile[i+1].start
                else:
                    txtfile.write(srtfile[i].content+"\n")
            else:
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

    edit_filecontent()
    Path = edit_filecontent()[0]
    all_file_list = edit_filecontent()[1]

    count = 1
    for file_name in all_file_list:
        ftype = os.path.splitext(file_name)[1]
        if ftype == r".srt":
            count = count +1

    if count >= 3:
        merge_subs(all_file_list)
        convert_txt()
    
    add_folder(url)
    path2 = add_folder(url)

    files_move(Path,path2)

if __name__ == "__main__": 
    main()
