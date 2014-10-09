# -*- coding: utf-8 -*-
"""
Created on Wed Oct 08 00:03:40 2014

@author: ASUS
"""

import pymorphy2
import sys

def read_index(indexname):
    d = {}
    fin = open(indexname, 'r')    
    for line in fin:
        words = line.split()
        key = unicode(words[0].decode('utf8')).encode('utf8')
        d[key] = []
        for word in words[1:]:
            d[key] = d[key] + [int(word)]
    
    fin.close()
    return d

def wrong_query():
    print u'Wrong query'
    print u'Use one of the formats:'
    print u'корабль AND билеты AND спб'
    print u'корабль OR билеты OR спб'
    exit(0)

def print_set(s):
    if s.__len__() == 0:
        print u'no documents found'
        return
    print u'found in',
    it = 0
    for elem in s:
        if it != 0:
            print '\b,',
        print elem,
            
        it += 1
        if it == 2:
            print u'and', s.__len__() - 2, u'more',
            break
    print
    return

def compute_query(d, morph, query):
    if (query.__len__() % 2 != 1):
        wrong_query()
    
    it = 0
    l = set()
    and_flag = True
    for word in query:
        if (it % 2 == 0):
            key = unicode(word.decode('cp1251')).encode('utf8')
            if (it == 0):
                l = set(d.get(key, []))
            else:
                if and_flag:
                    l = l & set(d.get(key, []))
                else:
                    l = l | set(d.get(key, []))
        else:
            if (it == 1):
                if (word == 'AND'):
                    and_flag = True
                else:
                    if (word == 'OR'):
                        and_flag = False
                    else:
                        wrong_query()
            else:
                if (not(word == 'AND' and and_flag or word == 'OR' and (not and_flag))):
                    wrong_query()
        it += 1
    print_set(l)

if __name__ == "__main__":
    if sys.argv.__len__() < 2:
        print u'Wrong number of parameters'
        print u'Execute as \"searcher.py index.inv это\"'
        exit(0)
    indexfile = sys.argv[1]
    morph = pymorphy2.MorphAnalyzer()

    d = read_index(indexfile)
    compute_query(d, morph, sys.argv[2:])
