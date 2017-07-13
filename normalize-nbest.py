#!/usr/bin/env python

# Normalizes the translation and reconstruction costs in a combined n-best file

import sys

if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.stderr.write("usage: %s SRC ALPHA\n" % sys.argv[0])
        sys.exit(1)
    src, alpha = sys.argv[1], float(sys.argv[2])
    src_fh = open(src)

    prev_num = -1
    len_src = None
    for line in sys.stdin:
        num, sent, tcosts, rcosts = line.split(' ||| ')
        if int(num) > prev_num:
            src_line = src_fh.readline()
            len_src = len(src_line.split())
            prev_num = int(num)
        len_tgt = len(sent.split())
        adj_tcosts, adj_rcosts = [], []
        for cost in map(float, tcosts.split()):
            adj_tcosts.append(cost / (len_tgt+1)**alpha)
        for cost in map(float, rcosts.split()):
            adj_rcosts.append(cost / (len_src+1)**alpha)
        tcosts = " ".join(map(str, adj_tcosts))
        rcosts = " ".join(map(str, adj_rcosts))
        print " ||| ".join([num, sent, tcosts, rcosts])
