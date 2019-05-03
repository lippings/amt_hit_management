# -*- coding: utf-8 -*-
"""
Created on Thu May 17 10:13:39 2018

@author: samue

Creates links for html <audio> element from Dropbox folder and uploads results
in csv format. Overwrites previous file and writes file on disc as well. 

NB: Depends on dropbox library
"""

from __future__ import print_function
import dropbox
from time import time
import numpy as np


def printProgressBar (iteration, total, prefix='Progress:', additional=[], suffix='Completed', decimals=1, length=50,
                      fill='█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    string = '\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix)
    string = "\t".join([string]+additional)
    print(string, end = '')
    # Print New Line on Complete
    if iteration == total: 
        print()


def main():
    colDelim = ","
    rowDelim = "\n"
	
	client_id = "<Your client id here>"
    audio_folder = "<Location folder of the audio files on Dropbox>"
	csv_destination = "<Destination folder of the csv file on Dropbox>"
	
    
    dbx = dropbox.Dropbox(client_id)
    data = [["audioUrl", "audioType"]]
    contents = dbx.files_list_folder(audio_folder).entries
    N = len(contents)
    cnt = 0
    start_time = time()
    times = []
    for entry in contents:
        lap_start = time()
        name = entry.name
        # Continue, if entry has an extension, i.e. it is a file not a folder
        if name.split(".")[0] != name:
            path = entry.path_display
            url = dbx.sharing_create_shared_link(path).url
            # Replacing "www" with "dl" and removing "?dl=0" creates a usable link for <audio>
            www_ind = url.find("www")
            dl_ind = url.find("?dl=")
            url = url[0:www_ind]+"dl"+url[www_ind+3:dl_ind]
            audio_format = url.split(".")[len(url.split("."))-1]
            audio_type = "audio/"
            
            if audio_format == "mp3":
                audio_type = audio_type + "mpeg"
            else:
                audio_type = audio_type + audio_format
            
            data.append([url, audio_type])

            times.append(time()-lap_start) 
            cnt += 1
            printProgressBar(cnt, N, suffix="Links created", additional=["Creating link for %s" % (name)])
            # print(f"Time for one file: {time()-lap_start}\tProgress: {cnt}/{N}")
            
    print("Total time elapsed for share links: {}, mean for one: {}".format(
        time()-start_time,
        np.mean(times)
    ))
    for i in range(len(data)):
        data[i] = colDelim.join(data[i])
        
    result = rowDelim.join(data)
    with open(csv_destination.split("/").pop(), "w") as f:f.write(result)
    
    dbx.files_upload(result.encode("utf-8"), csv_destination, mode=dropbox.files.WriteMode("overwrite"))

main()