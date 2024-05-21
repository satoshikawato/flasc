#!/usr/bin/env python
# coding: utf-8

import argparse
import sys
import os
import toml
from contextlib import redirect_stdout
from Bio import AlignIO
from importlib import resources
from importlib.abc import Traversable

def load_toml(file_name=None, absolute_file_path=None) -> dict:
    toml_dict = {}  # Initialize to empty dict to handle cases where loading fails.
    if absolute_file_path and file_name:
        raise ValueError("Cannot specify both file name and absolute file path for load_toml()")

    elif absolute_file_path:  # Initialize outside of try for scope in exception block
        try:
            # To check if the file exists, do this:
            os.path.isfile(absolute_file_path)
            #logger.info(f"INFO: Found TOML file: {absolute_file_path}")
            file_path = absolute_file_path
        except FileNotFoundError as e:
            #logger.error(f"TOML file {absolute_file_path} does not exist: {e}")
            sys.exit(1)
    else:
        try:
            pass
            # Generate the path object for the 'config.toml' file
            #file_path_traversable: Traversable = resources.files(
            #    'rasc.data').joinpath(file_name)
            # Convert the path to an absolute path
            #file_path = file_path_traversable.resolve()  # type: ignore
            #file_path = absolute_file_path
        except FileNotFoundError as e:
            #logger.error(f"Config file {file_name} does not exist: {e}")
            sys.exit(1)
    try:
        with open(file_path, 'r') as toml_file:
            toml_dict: dict = toml.load(toml_file)
            #logger.info(f"INFO: Loaded TOML file: {file_path}")
    except FileNotFoundError as e:
        #logger.error(f"Failed to load TOML file {file_path}: {e}")
        sys.exit(1)
    return toml_dict    

def _get_args():
    parser = argparse.ArgumentParser(
        description='Scan for mutations in a multiple sequence alignment')
    parser.add_argument(
        "--input",
        "-i",
        "--in",
        required = True,
        metavar="FILE",
        help="Input FASTA file")
    parser.add_argument(
        "--output",
        "-o",
        "--out",
        "--output",
        metavar="FILE",
        help="output txt file")
    parser.add_argument(
        "-g",
        "--gap",
        type=str,
        help='gap character (default: "-")',
        default="-")
    parser.add_argument("-d", "--db", type=str, help="reference file for mutations (required)")
    parser.add_argument(
        '-q',
        '--query',
        type=str,
        required=True,
        help='query sequence')
    parser.add_argument("--all", action="store_true", help="print all scanned sites regardless of mutations")
    parser.add_argument("-t", "--target", type=str, help="target gene")
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()
    return args

def get_ref_record(records, ref_name):
    if ref_name is not None:
        record_dict = dict()
        for record in records:
            record_dict[record.id] = record
        ref_record = record_dict[ref_name]
    else:
        ref_record = records[0]
    return ref_record


def determine_residue_coordinate(record, gap_character):
    gap_character = gap_character
    coordinate_dict = {}
    residue_count = 1
    residue_count_dict = dict()
    seq_length = len(record.seq)
    for i in range(seq_length):
        if record.seq[i] == gap_character:
            pass
        else:
            coordinate_dict[residue_count] = i
            residue_count += 1
    return coordinate_dict


def print_residue_coordinate(ref_record, records, coordinate_dict, gap_character, mutations_of_concern, query_list, all=False):
    for query in query_list:
        for key in mutations_of_concern.keys():
            mutation_name =  mutations_of_concern[key]['name']
            gene_id = mutations_of_concern[key]['gene_id']
            note = mutations_of_concern[key]['note']
            target = int(mutations_of_concern[key]['coordinate'])
            wildtype = "/".join(mutations_of_concern[key]['wildtype'])
            for record in records:
                if record.id == query:
                    record_coordinate = len(record.seq[:coordinate_dict[target]].replace(gap_character, "")) + 1
                    if all:
                        print(f"{record.id}\t{gene_id}\t{record_coordinate}\t{mutation_name}\t{wildtype}\t{record.seq[coordinate_dict[target]]}\t{note}")
                    else:
                        if record.seq[coordinate_dict[target]] == mutations_of_concern[key]['mutant']:
                            print(f"{record.id}\t{gene_id}\t{record_coordinate}\t{mutation_name}\t{wildtype}\t{record.seq[coordinate_dict[target]]}\t{note}")

def main():
    args = _get_args()
    in_fa = args.input
    out_file = args.output
    all = args.all
    queries = args.query
    gap_character = args.gap
    mutation_db = args.db
    target = args.target
    records = AlignIO.read(in_fa, "fasta")
    mutation_toml = load_toml(absolute_file_path=mutation_db)
    mutations_of_concern = mutation_toml[target]
    mutations_of_concern = mutation_toml[target]

    reference_ids = set()
    for key in mutations_of_concern.keys():
        reference_ids.add(mutations_of_concern[key]['protein_id'])
    ref_records = []
    for reference_id in reference_ids:
        for record in records:
            if record.id == reference_id:
                ref_records.append(record)

    coordinate_dicts = dict()
    for ref_record in ref_records:
        coordinate_dict = determine_residue_coordinate(ref_record, gap_character)
        coordinate_dicts[ref_record.id] = coordinate_dict

    
    query_list = queries.split(",")
    if out_file is not None:
        with open(out_file, 'w') as f:
            with redirect_stdout(f):
                print(f"query\tgene\tcoordinate\tvariant\treference\tresidue\tnote")
                print_residue_coordinate(ref_record, records, coordinate_dict, gap_character, mutations_of_concern, query_list, all)
    else:
        print(f"query\tgene\tcoordinate\tvariant\treference\tresidue\tnote")
        print_residue_coordinate(ref_record, records, coordinate_dict, gap_character, mutations_of_concern, query_list, all)


if __name__ == "__main__":
    main()
