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
        directory = "\\Source\\"
        indexfile = "index.inv"
        morph = pymorphy2.MorphAnalyzer()

        directory = os.getcwd() + '\\Source\\'
        filenames = os.listdir(directory)
        [d, docnames] = compute_files(directory, filenames, morph)
        print u'saving index:'
        print_index(d, docnames, indexfile)
        print u'Done'
