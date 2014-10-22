# -*- coding: utf-8 -*-
"""
Created on Wed Oct 08 00:03:40 2014

@author: ASUS
"""

import pymorphy2
import sys

def get_index_doc_positions(j, words):
    docnum = int(words[j])
    df = int(words[j + 1])
    poss = []
    for strpos in words[(j + 2):(j + 2 + df)]:
        poss = poss + [int(strpos)]
    return [j + df + 2, docnum, poss]

def read_index(indexname):
    d = {}
    docnames = {}
    fin = open(indexname, 'r')
    i = 0
    docnum = 0
    for line in fin:
        if (i == 0):
            docnum = int(filter(str.isdigit, line))
            i += 1
            continue
        if (i < docnum + 1):
            [dnum, dname] = line.split()
            docnames[int(dnum)] = dname
            i += 1
            continue
        words = line.split()
        key = unicode(words[0].decode('utf8')).encode('utf8')
        d[key] = {}
        
        j = 1
        wlen = len(words)
        while (j < wlen):
            [j, dnum, poss] = get_index_doc_positions(j, words)
            d[key][dnum] = poss
        i += 1
    
    fin.close()
    return [d, docnames]

def wrong_query():
    print u'Wrong query'
    print u'Use one of the formats:'
    print u'корабль /1 билеты /+1 спб'
    print u'корабль /-5 билеты /3 спб'
    exit(0)

def print_set(s, docnames):
    if len(s) == 0:
        print u'no documents found'
        return
    print u'found in',
    it = 0
    for elem in s:
        if it != 0:
            print '\b,',
        print docnames[elem],
            
        it += 1
        if it == 2:
            print u'and', len(s) - 2, u'more',
            break
    print
    return

def parse_param(word):
    if (word[0] != '/'):
        return ['!', 0]
    if (word[1] == '+' or word[1] == '-'):
        if (not word[2:].isdigit()):
            return ['!', 0]
        else:
            return [word[1], int(word[2:])]
    else:
        if (not word[1:].isdigit()):
            return ['!', 0]
        else:
            return ['*', int(word[1:])]
    
def merge_left(l1, l2, dist, mask):
    ans = set([])
    common = set(l1.keys()) & set(l2.keys()) & mask
    for ndoc in common:
        a1 = l1[ndoc]
        a2 = l2[ndoc]
        flag = False
        p2 = 0
        for p1 in range(len(a1)):
            while (p2 < len(a2) and a2[p2] <= a1[p1] + dist):
                if (a1[p1] <= a2[p2]):
                    flag = True
                    break
                else:
                    p2 += 1
            if (flag):
                break
        if (flag):
            ans.add(ndoc)
    return ans

def merge(l1, l2, t, dist, mask):
    if (t == '+'):
        return merge_left(l1, l2, dist, mask)
    if (t == '-'):
        return merge_left(l2, l1, dist, mask)
    if (t == '*'):
        return merge_left(l1, l2, dist, mask) | merge_left(l2, l1, dist, mask)
    return set([])

def compute_query(d, query):
    if (query.__len__() % 2 != 1):
        wrong_query()
    
    it = 0
    key0 = unicode(query[0].decode('cp1251')).encode('utf8')
    l = d.get(key0, {})
    ans = set(l.keys())
    
    dist = 0
    t = '!'
    for word in query[1:]:
        if (it % 2 == 0):
            [t, dist] = parse_param(word)
            if (t == '!'):
                wrong_query()
        else:
            key = unicode(word.decode('cp1251')).encode('utf8')
            nl = d.get(key, {})
            ans = merge(l, nl, t, dist, ans)
            l = nl
        it += 1
    return ans

if __name__ == "__main__":
    if sys.argv.__len__() < 2:
        print u'Wrong number of parameters'
        print u'Execute as \"searcher.py index.inv это\"'
        exit(0)
    indexfile = sys.argv[1]

    [d, docnames] = read_index(indexfile)
    #print_index(d, docnames, 'index1.inv')
    
    ans = compute_query(d, sys.argv[2:])
    print_set(ans, docnames)
