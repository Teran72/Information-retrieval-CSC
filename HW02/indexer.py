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
    docnames = {}
    
    for filename in filenames:
        curfile = open(directory + filename, 'r')

        for line in curfile:
            preview = line.split()
            
            docnum = int(filter(str.isdigit, preview[0]))
            docnames[docnum] = preview[1]
            
            print 'computing:', docnum
            
            doc =  ' '.join(preview[2:])
            
            wordlist = filter(None, re.split("[/\\\ .,<>\t\n\[\]'\"!?:;(){}]+", doc))
            
            pos = 0
            for word in wordlist:
                utfword = word.decode('utf8')
                uword = unicode(utfword)
                parses = morph.parse(uword)
                for pars in parses:
                    key = pars.normal_form.encode('utf8')
                    d[key] = d.get(key, {})
                    if d[key].get(docnum, []) == []:
                        d[key][docnum] = [pos]
                    else:
                        if (d[key][docnum][-1] != pos):
                            d[key][docnum] += [pos]
                pos += 1
        curfile.close()
    return [d, docnames]

def print_index(d, docnames, foutname):
    fout = open(foutname, 'w')

    print >>fout, len(docnames)
    nums = docnames.keys()
    for num in nums:
        print >>fout, num, docnames[num]
    
    keys = d.keys()
    keys.sort()
    
    for key in keys:
        print >>fout, key,
        docs = d[key].keys()
        docs.sort()
        
        for docnum in docs:
            print >>fout, docnum,
            poss = d[key][docnum]
            poss.sort()
            print >>fout, len(poss),
            for pos in poss:
                print >>fout, pos,
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
        [d, docnames] = compute_files(directory, filenames, morph)
        print u'saving index:'
        print_index(d, docnames, indexfile)
        print u'Done'
