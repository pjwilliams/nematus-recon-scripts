#!/usr/bin/env python3

import argparse
import sys


def parse_cmd():
    parser = argparse.ArgumentParser()
    parser.add_argument("one_best_translations", help="path to 1-best translations")
    parser.add_argument("nbest_alignments", help="path to n-best alignments")

    args = parser.parse_args()

    return args

def parse_nbest_alignment_header_line(line):
    cols = line.split("|||")
    if len(cols) != 5:
        error("unsupported n-best alignments format")
    sent_num = cols[0].strip()
    translation = cols[1].strip()
    cost = cols[2].strip()
    input_sentence = cols[3].strip()
    lengths = [int(c.strip()) for c in cols[4].split(" ")]
    return sent_num, translation, cost, input_sentence, lengths


def error(msg):
    sys.stderr.write("%s: error: %s\n" % (sys.argv[0], msg.strip()))
    sys.exit(1)


def main():

    args = parse_cmd()

    with open(args.one_best_translations, "r") as one_best_handle:
        with open(args.nbest_alignments, "r") as alignments_handle:
            for one_best_line in one_best_handle:
                one_best = one_best_line.strip()

                found_in_alignments_header = False
                while not found_in_alignments_header:
                    alignments_line = alignments_handle.readline()
                    alignments_line = alignments_line.strip()

                    if alignments_line == "":
                        continue
                    try:
                        sent_num, translation, cost, input_sentence, lengths = \
                            parse_nbest_alignment_header_line(alignments_line)
                    except:
                        continue

                    if translation == one_best:
                        found_in_alignments_header = True
                        break

                if not found_in_alignments_header:
                    error("1best translation '%s' not found in any alignment header" % one_best)

                sys.stdout.write(alignments_line + "\n")
                for i in range(lengths[1]):
                    alignments_line = alignments_handle.readline()
                    sys.stdout.write(alignments_line)


if __name__ == "__main__":
    main()