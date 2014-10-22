# -*- coding: utf-8 -*-
"""
Created on Wed Oct 08 00:03:40 2014

@author: ASUS
"""

import pymorphy2
import os
import re
import sys

def compute_files(directory, filenames, morph):
    d = {}
    for filename in filenames:
        curfile = open(directory + filename, 'r')
        firstline = True    
        
        for line in curfile:
            #wordlist = line.split()
            wordlist = filter(None, re.split("[/\\\ .,<>\t\n\[\]'\"!?:;(){}]+", line))
            docnum = 0
            
            # Удаление служебного символа файла в utf-8
            if firstline:
                docnum = int(wordlist[0][3:])
            else:
                docnum = int(wordlist[0])
                
            print 'computing:', docnum
            firstline = False
            
            for word in wordlist[1:]:
                utfword = word.decode('utf8')
                uword = unicode(utfword)
                parses = morph.parse(uword)
                for pars in parses:
                    key = pars.normal_form.encode('utf8')
                    if d.get(key, []) == []:
                        d[key] = [docnum]
                    else:
                        if (d[key][-1] != docnum):
                            d[key] += [docnum]
        curfile.close()
    return d

def print_index(d, foutname):
    fout = open(foutname, 'w')    
    keys = d.keys()
    keys.sort()
    
    for key in keys:
        print >>fout, key,
        valset = d[key]
        for ndoc in valset:
            print >>fout, ndoc,
        print >>fout

    fout.close()
    return

if __name__ == "__main__":
    if sys.argv.__len__() != 3:
        print u'Wrong number of parameters'
        print u'Execute as \"indexer.py \\Source\\ index.inv\"'
    else:
        directory = sys.argv[1]
        indexfile = sys.argv[2]
        morph = pymorphy2.MorphAnalyzer()

        filenames = os.listdir(directory)
        d = compute_files(directory, filenames, morph)
        print u'saving index:'
        print_index(d, indexfile)
        print u'Done'
