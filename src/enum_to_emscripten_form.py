#!/usr/bin/env python
import argparse


def process_arguments():
    parser = argparse.ArgumentParser(description="Convert libCellML enums to emscripten form.")
    parser.add_argument('--file',
                        help='Specify the file that contains the text of the enum, one per line.')
    parser.add_argument('--className',
                        help='Name of the class the enum belongs to.')
    parser.add_argument('--enum',
                        help='Name of the enum in the class.')

    return parser


def main():
    parser = process_arguments()
    args = parser.parse_args()

    print('enum_<libcellml::{0}::{1}>("{0}_{1}")'.format(args.className, args.enum))
    with open(args.file) as f:
        for line in f:
            line = line.strip()
            if line.endswith(','):
                line = line.replace(',', '')
            print('.value("{0}", libcellml::{1}::{2}::{0})'.format(line.strip(), args.className, args.enum))
    print(";")


if __name__ == "__main__":
    main()
