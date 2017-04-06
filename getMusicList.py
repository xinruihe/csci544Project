# -*-coding:utf-8-*-
from __future__ import unicode_literals
import urllib
import sys
import re
sys_type = sys.getfilesystemencoding()


def gethtml(url):
    page = urllib.urlopen(url)
    html= page.read()
    html.decode('utf-8').encode(sys_type)
    return html


def getmusic(html):
    reg = r'href="/song\?id=[0-9]{0,9}"'

    musicre = re.compile(reg)
    musiclist_temp = re.findall(musicre, html)
    musiclist = []
    for item in musiclist_temp:
        musiclist.append(item[12:-1])
    return musiclist
