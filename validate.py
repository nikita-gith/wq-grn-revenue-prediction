#!/usr/bin/env python

from __future__ import print_function, with_statement
import csv
import os.path as path

# Script to validate a user solution for either of the problems


def load_csv(filename):
    rows = []
    with open(filename, "r") as infile:
        reader = csv.reader(infile)
        for row in reader:
            rows.append(row)
    return rows


def check_name(filename, expected_name):
    """Checks filename is correct for the problem"""
    filebasename = path.split(filename)[-1]
    if filebasename != expected_name:
        raise Exception("Candidate solution file is named '%s', expecting '%s'"
                        % (filename, expected_name))

    
def compare(cand_rows, samp_rows):
    """Checks num rows, num columns and that inputs match"""
    # check length
    cand_rows_len = len(cand_rows)
    samp_rows_len = len(samp_rows)
    if cand_rows_len != samp_rows_len:
        raise Exception("Candidate solution contains %d lines, expecting %d lines" % (cand_rows_len, samp_rows_len))
    # check inputs
    line_counter = 0
    for cand_row, samp_row in zip(cand_rows, samp_rows):
        line_counter = line_counter + 1
        # number of columns check
        cand_row_len = len(cand_row)
        samp_row_len = len(samp_row)
        if cand_row_len != samp_row_len:
            raise Exception("line %d: candidate solution contains %d columns, expecting %d columns"
                            % (line_counter, cand_row_len, samp_row_len))
        # input checks
        cand_row_inputs = cand_row[:-1]
        samp_row_inputs = samp_row[:-1]
        if cand_row_inputs != samp_row_inputs:
            raise Exception("line %d: candidate solution inputs '%s' does not match expected inputs '%s'"
                            % (line_counter, ','.join(cand_row_inputs), ','.join(samp_row_inputs)))


def check_prediction_types(cand_rows, typ):
    line_counter = 0
    for row in cand_rows:
        line_counter = line_counter + 1
        prediction = row[-1]
        try:
            typ(prediction)
        except Exception as e:
            typ_name = typ.__name__
            err = str(e)
            raise Exception("line %d: candidate solution output '%s' does not parse cleanly as type '%s': %s"
                            % (line_counter, prediction, typ_name, err))


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Validate candidate solution")
    parser.add_argument("filename",
                        help="Path to candidate solution file")
    parser.add_argument("problem", type=int,
                        help="Problem number (either '1' or '2')")
    parser.add_argument("--samplefilepath",
                        help="Path to sample file for the problem (optional)")
    args = parser.parse_args()

    filename = args.filename
    problem = args.problem
    samplefilepath = args.samplefilepath
    
    assert problem in (1, 2)
    
    expected_name = "problem-one-answer.csv" if problem == 1 else "problem-two-answer.csv"
    typ = float if problem == 1 else int  # expected prediction type
    if samplefilepath is None:
        samplefilepath = ("problem-one-sample-answer.csv"
                          if problem == 1
                          else "problem-two-sample-answer.csv")


    print("Validating candidate solution %s for problem %d"
          % (filename, problem))
    print("-" * 79)
        
    try:
        cand_rows = load_csv(filename)
        samp_rows = load_csv(samplefilepath)

        check_name(filename, expected_name)
        compare(cand_rows, samp_rows)
        check_prediction_types(cand_rows, typ)
    except Exception as e:
        print("Invalid solution file ...")
        print("  " + str(e))
        exit(1)

    print("OK, solution is in the correct format")


if __name__ == '__main__':
    main()
