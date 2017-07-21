#!/usr/bin/env python

import argparse
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("nbest_file", metavar="NBEST-FILE",
        help="path to n-best file")
    parser.add_argument("rcost_file", metavar="RCOST-FILE",
        help="path to reconstruction cost file")
    parser.add_argument("--pick-tcosts", type=int, nargs='+', metavar="INDEX",
        help="indices of translation costs to pick (zero-based)")
    parser.add_argument("--pick-rcosts", type=int, nargs='+', metavar="INDEX",
        help="indices of reconstruction costs to pick (zero-based)")
    args = parser.parse_args()

    nbest_fh = open(args.nbest_file)
    rcost_fh = open(args.rcost_file)

    while True:
        nbest_line = nbest_fh.readline()
        rcost_line = rcost_fh.readline()
        if nbest_line == "" and rcost_line == "":
            break
        if nbest_line == "" or rcost_line == "":
            error("nbest and rcost files must be of same length")
        sent_num, translation, tcosts = parse_nbest_line(nbest_line)
        rcosts = rcost_line.split()
        if args.pick_tcosts != None:
            tcosts = [tcosts[i] for i in args.pick_tcosts]
        if args.pick_rcosts != None:
            rcosts = [rcosts[i] for i in args.pick_rcosts]
        print "%s ||| %s ||| %s ||| %s" % (sent_num, translation,
                                           " ".join(tcosts), " ".join(rcosts))

def parse_nbest_line(line):
    cols = line.split("|||")
    if len(cols) != 3:
        error("unsupported n-best format")
    sent_num = cols[0].strip()
    translation = cols[1].strip()
    tcosts = cols[2].split()
    return sent_num, translation, tcosts


def error(msg):
    sys.stderr.write("%s: error: %s\n" % (sys.argv[0], msg.strip()))
    sys.exit(1)


if __name__ == "__main__":
    main()
