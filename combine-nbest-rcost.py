#!/usr/bin/env python

import sys

nbest_fh = open(sys.argv[1])
rcost_fh = open(sys.argv[2])

while True:
    nbest_line = nbest_fh.readline()
    if nbest_line == "":
        break
    rcost_line = rcost_fh.readline()
    print "%s ||| %s" % (nbest_line.strip(), rcost_line.strip())
