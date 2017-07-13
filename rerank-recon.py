#!/usr/bin/python
# -*- coding: utf-8 -*-
# Original Author: Rico Sennrich
# Adapted for reconstruction by Phil Williams
# Distributed under MIT license

import sys
from collections import defaultdict

if __name__ == '__main__':

    if len(sys.argv) != 3:
        sys.stderr.write("usage: %s K ALPHA\n" % sys.argv[0])
        sys.exit(1)
    k = float(sys.argv[1])
    lam = float(sys.argv[2])

    cur = 0
    best_score = float('inf')
    best_sent = ''
    idx = 0
    for line in sys.stdin:
        num, sent, tcosts, rcosts = line.split(' ||| ')

        # new input sentence: print best translation of previous sentence, and reset stats
        if int(num) > cur:
            print best_sent
            cur = int(num)
            best_score = float('inf')
            best_sent = ''
            idx = 0

        #only consider k-best hypotheses
        if idx >= k:
            continue

        mean_tcost = sum(map(float, tcosts.split())) / len(tcosts.split())
        mean_rcost = sum(map(float, rcosts.split())) / len(rcosts.split())
        score = mean_tcost + lam * mean_rcost
        if score < best_score:
            best_score = score
            best_sent = sent.strip()

        idx += 1

    # end of file; print best translation of last sentence
    print best_sent
