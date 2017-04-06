# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
import re
import json
import getMusicList as gml
import sys
import os
import shutil
import ast
word_stat = {}
reload(sys)
sys.setdefaultencoding( "utf-8" )

try:
    os.mkdir("lyric")
    os.mkdir("lyric/lyricac")
    os.mkdir("lyric/lyricpop")
    os.mkdir("lyric/lyricrock")
    os.mkdir("lyric/lyriccountry")
except OSError as err:
    print(format(err))
    pass

def getlyricfromurl(sid, c, counts, fails, flist):
    hm = 'http://music.163.com/api/song/lyric?os=pc&' + sid +'&lv=-1&kv=-1&tv=-1'
    data_json = gml.gethtml(hm)
    data = json.loads(data_json)
    data = json.dumps(data, ensure_ascii=False, encoding='utf8')
    data = json.loads(data)
    reg = r'[^0-9\[\]\.\:]'
    string = re.compile(reg)
    lyricname = ""
    ger = ["ac","rock","pop","country"]
    gtags = ["(1,0,0,0)\n\n", "(0,1,0,0)\n\n", "(0,0,1,0)\n\n", "(0,0,0,1)\n\n",]
    gna = ger[c]
    gtag = gtags[c]
    try:
        st = data["lrc"]["lyric"]
        # print st
        lyriclist = re.findall(string, st)
        # print 1
        if 'klyric' in data and "lyric" in data['klyric'] and not data['klyric']["lyric"] is None:
                lyricname = data['klyric']["lyric"]
                end = lyricname.index("]")
                lyricname = lyricname[4:end]
        # print 2
        str_lrc = ','.join(lyriclist)
        fn = 'lyric/lyric' + gna + '/' + sid[3:] + '.txt'
        flist.append(fn)
        # print 3
        with open(fn, 'w+') as file:
            file.write(gtag)
            file.write(lyricname + '\n')
            file.write(str_lrc.replace(',', ''))
            file.close()
        counts[c] += 1
    except:
        fails[c] += 1
        print hm
        pass
    print counts[c],fails[c]

if __name__ == '__main__':
    pl = [['490929456','19820015','109452668','508460812', '380725136', '465297820', '553775897'],['759331', '138911210','100524452', '3010292'],['78044620'],['378324005','131368017','112136328','49927225']]
    cset = set([])
    counts = [0,0,0,0]
    fails = [0,0,0,0]
    idlist = []
    for i in xrange(4):
        l = pl[i]
        for lid in l:
            html = gml.gethtml("http://music.163.com/playlist?id=" + lid)
            musiclist = gml.getmusic(html)
            for key in musiclist:
                if not key in cset:
                    cset.add(key)
                    getlyricfromurl(key, i, counts, fails, idlist)
                    if counts[i] == 500:
                        break
            if counts[i] == 500:
                    break
    file = open("pathlist.txt", "w+")
    json.dump([idlist], file)
    file.close()
    print counts
