#!/usr/bin/env python3

import argparse
import sys


def parse_cmd():
    parser = argparse.ArgumentParser()
    parser.add_argument("--one-best-translations", help="path to 1-best translations", required=True)
    parser.add_argument("--nbest-alignments", help="path to n-best alignments", required=True)

    args = parser.parse_args()

    return args

def parse_nbest_alignment_header_line(line):
    cols = line.split("|||")
    if len(cols) != 5:
        raise Exception("unsupported n-best alignments format")
    cols = [col.strip() for col in cols]
    sent_num = cols[0]
    translation = cols[1]
    cost = cols[2]
    input_sentence = cols[3]
    lengths = [int(c.strip()) for c in cols[4].split(" ")]
    return sent_num, translation, cost, input_sentence, lengths


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

                    sent_num, translation, cost, input_sentence, lengths = parse_nbest_alignment_header_line(alignments_line)

                    if translation == one_best:
                        found_in_alignments_header = True
                        break
                    else:
                        # skip weights of this hypothesis
                        for i in range(lengths[1]):
                            alignments_handle.readline()

                if not found_in_alignments_header:
                    raise Exception("1best translation '%s' not found in any alignment header" % one_best)

                sys.stdout.write(alignments_line + "\n")
                for i in range(lengths[1]):
                    alignments_line = alignments_handle.readline()
                    sys.stdout.write(alignments_line)


if __name__ == "__main__":
    main()