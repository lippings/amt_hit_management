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
from tqdm import tqdm


def main():
    colDelim = ","
    rowDelim = "\n"

    client_id = "<Your client id here>"
    audio_folder = "<Location folder of the audio files on Dropbox>"
    csv_destination = "<Destination folder of the csv file on Dropbox>"

    dbx = dropbox.Dropbox(client_id)
    data = [["audioUrl", "audioType"]]
    contents = dbx.files_list_folder(audio_folder).entries
    start_time = time()
    times = []
    for entry in tqdm(contents):
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