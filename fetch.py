#!/usr/bin/env python
import json
from sys import argv, stdout, exit
from urllib2 import urlopen
from getopt import getopt

CHUNK = 16 * 1024

def read_args(argv):
    filename = None
    uuid = None

    try:
        opts, args = getopt(argv[1:], 'u:o:h')
    except getopt.GetoptError:
        usage()
        exit(1)

    for opt, arg in opts:
        if opt == '-h':
            usage()
            exit(0)
        elif opt == '-o':
            filename = arg
        elif opt == '-u':
            uuid = arg
        else:
            usage()
            exit(1)

    if not filename or not uuid:
        usage()
        exit(1)
    return filename, uuid

def usage():
    print 'Usage: %s -u uuid -o file' % argv[0]

def fetch_video_url(uuid):
    url =\
      'http://scs.hosted.panopto.com/Panopto/PublicAPI/4.1/TabletDeliveryInfo'\
      + '?DeliveryId=%s&forDownload=true' % uuid
    req = urlopen(url)
    res = json.loads(req.read())
    return res['PhoneDownloadUrl']

def download_video(video_url, filename):
    video_req = urlopen(video_url)
    chunk_count = 0
    total_length = float(video_req.headers.get('content-length'))
    with open(filename, 'wb') as fp:
        while True:
            percent = 100.0 * chunk_count * CHUNK / total_length
            percent = min(percent, 100.0)
            stdout.write("\r%.2f%%" % percent)
            stdout.flush()
            chunk = video_req.read(CHUNK)
            if not chunk:
                break
            fp.write(chunk)
            chunk_count += 1

def fetch_video(filename, uuid):
    print 'Fetching video %s' % filename
    print 'Fetching video url...'
    video_url = fetch_video_url(uuid)
    print 'video url: %s' % video_url

    print 'Downloading %s' % filename
    download_video(video_url, filename)

    print ''
    print 'Done!'

if __name__ == '__main__':
    filename, uuid = read_args(argv)
    fetch_video(filename, uuid)
