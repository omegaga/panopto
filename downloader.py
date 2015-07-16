#!/usr/bin/env python
from fetch import fetch_video
from urllib2 import urlopen, HTTPError
import json
from sys import argv, exit, stderr
from getopt import getopt


# folder id of 15-213 Introduction to Computer Systems, change if necessary
CSAPP_FOLDER_ID = '2be55024-d2d3-4a3c-ac9c-9b348ddce5c4'

def read_args(argv):
    try:
        opts, args = getopt(argv[1:], 'ah')
    except getopt.GetoptError:
        usage()
        exit(1)

    all_flag = False

    for opt, arg in opts:
        if opt == '-h':
            usage()
            exit(0)
        elif opt == '-a':
            all_flag = True

    return all_flag

def usage():
    print 'Usage: %s [-a]' % argv[0]

def get_sessions(folder_id):
    url = 'https://scs.hosted.panopto.com/Panopto/PublicAPI/4.1/ListSessions'\
        + '?FolderId=%s' % folder_id
    print "Fetching video list, please wait..."
    req = urlopen(url)
    res = json.loads(req.read())
    video_list = [(e['Id'], '%s.mp4' % e['Name']) for e in res['Results']]
    return video_list

if __name__ == '__main__':
    all_flag = read_args(argv)
    video_list = get_sessions(CSAPP_FOLDER_ID)
    idx = 0
    if all_flag:
        for video in video_list:
            try:
                fetch_video(video[1], video[0])
            except HTTPError:
                stderr.write('Error: fail to download %s\n' % video[1])
        exit(0)

    for idx in xrange(len(video_list)):
        print '%d) %s' % (idx, video_list[idx][1])

    idx = input('Please input the index of the video to download: ')
    video = video_list[idx]
    fetch_video(video[1], video[0])
