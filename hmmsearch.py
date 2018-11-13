#!/usr/bin/env python3
"""Search an HMM profile against a FASTA file."""

import argparse
import logging
import os
import shutil
import sys
import time
import uuid

from lib.helpers import run_cmds, exit_and_clean_up
from lib.helpers import set_up_temp_folder, set_up_logging
from lib.helpers import get_file, upload_file

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="""
        Search an HMM profile against a FASTA file.
        """)

    parser.add_argument("--query",
                        type=str,
                        help="Location for input FASTA file.")
    parser.add_argument("--profile",
                        type=str,
                        help="Location for input HMM file.")
    parser.add_argument("--output",
                        type=str,
                        help="Location for output HMM alignment.")
    parser.add_argument("--logfile",
                        type=str,
                        help="""(Optional) Write log to this file.""")
    parser.add_argument("--temp-folder",
                        type=str,
                        default="/share",
                        help="""Temporary directory to use.""")

    args = parser.parse_args(sys.argv[1:])

    start_time = time.time()

    # Set up a temp folder
    temp_folder = set_up_temp_folder(args.temp_folder)

    # Set up logging
    log_fp = set_up_logging(temp_folder, "HMMSEARCH")

    # Get the query FASTA
    try:
        input_fasta = get_file(args.query, temp_folder)
    except:
        exit_and_clean_up(temp_folder)

    # Get the query profile
    try:
        input_hmm = get_file(args.profile, temp_folder)
    except:
        exit_and_clean_up(temp_folder)

    # Run the alignment
    output_aln = os.path.join(
        temp_folder,
        "{}.aln".format(str(uuid.uuid4())[:8])
    )
    try:
        run_cmds([
            "hmmsearch",
            input_hmm,
            input_fasta
        ], 
            stdout=output_aln
        )
    except:
        exit_and_clean_up(temp_folder)

    # Make sure the output exists
    assert os.path.exists(output_aln)

    # Optionally compress the results
    if args.output.endswith(".gz"):
        logging.info('Compressing the output')
        try:
            run_cmds([
                "gzip",
                output_aln
            ])
        except:
            exit_and_clean_up(temp_folder)

        output_aln = output_aln + ".gz"

    # Upload the results
    try:
        upload_file(output_aln, args.output)
    except:
        exit_and_clean_up(temp_folder)

    # Upload the logs, if specified
    if args.logfile is not None:
        try:
            upload_file(log_fp, args.logfile)
        except:
            exit_and_clean_up(temp_folder)

    logging.info("Time elapsed: {:,} seconds".format(
        round(time.time() - start_time, 2)
    ))

    logging.info("Deleteing temporary files and shutting down")
    shutil.rmtree(temp_folder)
