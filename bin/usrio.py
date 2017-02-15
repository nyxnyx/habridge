#!/usr/bin/python
#coding=utf8

import sys, getopt
import urllib2
from urlparse import urlparse

IP="10.1.2.100"
URL="http://"+IP+"/httpapi.json?sndtime=0.2123&CMD=UART_WRITE&UWHEXVAL="

BASE=1792

def make_request(url):
    authinfo = urllib2.HTTPPasswordMgrWithDefaultRealm()
    urlParser = urlparse(url)
    uri = urlParser.scheme+"://"+urlParser.netloc+"/"
    authinfo.add_password(None, uri, 'admin', 'admin')

    urllib2.install_opener(urllib2.build_opener(urllib2.HTTPBasicAuthHandler(authinfo)))
    req = urllib2.Request(url)
    f = urllib2.urlopen(req)
    return f.read()

def get_bit(byteval,idx):
    return ((byteval&(1<<idx))!=0);

def get_status(bit):
    number=int(make_request(URL+"0")) - BASE
    return get_bit(number, bit-1)

def set_on(bit):
    status=get_status(bit)
    if not status:
        make_request(URL+`bit`)
    return get_status(bit)

def set_off(bit):
    status=get_status(bit)
    if status:
        make_request(URL+`bit`)
    return get_status(bit)

def get_gear():
    status1 = get_status(1)
    status2 = get_status(2)
    status3 = get_status(3)
    if status1 and status2 and status3:
        return 3
    elif status1 and status2:
        return 2
    elif status1:
        return 1
    else:
        return 0

def set_gear(gear):
    current_gear = get_gear()
    if current_gear == gear:
        return
    elif current_gear == 3:
        if gear == 2:
            set_off(3)
        elif gear == 1:
            set_off(3)
            set_off(2)
        elif gear == 0:
            set_off(3)
            set_off(2)
            set_off(1)
    elif current_gear == 2:
        if gear == 1:
            set_off(2)
        elif gear == 3:
            set_on(3)
        elif gear == 0:
            set_off(2)
            set_off(1)
    elif current_gear == 1:
        if gear == 0:
            set_off(1)
        elif gear == 2:
            set_on(2)
        elif gear == 3:
            set_on(2)
            set_on(3)
    elif current_gear == 0:
        if gear == 1:
            set_on(1)
        elif gear == 2:
            set_on(1)
            set_on(2)
        elif gear == 3:
            set_on(1)
            set_on(2)
            set_on(3)
        

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "i:n:f:eg:", ["info=", "on=", "off="])
    except getopt.GetoptError:
        print "Użyj parametru: -i <n> -n <n> -f <n> -e -g <gear>"
        sys.exit(2)

    for opt, arg in opts:
        try:
            if opt == '-i':
                print get_status(int(arg))
            elif opt == '-n':
                print set_on(int(arg))
            elif opt == '-f':
                print set_off(int(arg))
            elif opt == '-e':
                print get_gear()
            elif opt == '-g':
                set_gear(int(arg))
                print get_gear()
        except:
            print -1


if __name__ == "__main__":
       main(sys.argv[1:])
