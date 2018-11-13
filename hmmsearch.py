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
                        help="Location for output HMM alignment (Text format).")
    parser.add_argument("--output-tsv",
                        type=str,
                        help="Location for output HMM alignment (TSV format).")
    parser.add_argument("--output-fasta",
                        type=str,
                        help="Location for output HMM alignment (Alignment).")
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
    output = {
        suffix: os.path.join(
            temp_folder,
            "{}.{}".format(str(uuid.uuid4())[:8], suffix)
        )
        for suffix in ["aln", "tsv", "fasta"]
    }
    try:
        run_cmds([
            "hmmsearch",
            "-o", output["aln"],
            "-A", output["fasta"],
            "--tblout", output["tsv"],
            input_hmm,
            input_fasta
        ])
    except:
        exit_and_clean_up(temp_folder)

    # Make sure the output exists
    assert os.path.exists(output["aln"])

    logging.info("Time elapsed: {:,} seconds".format(
        round(time.time() - start_time, 2)
    ))

    # Iterate over each of the items to upload
    for remote_path, local_path in [
        (args.output, output["aln"]),
        (args.output_tsv, output["tsv"]),
        (args.output_fasta, output["fasta"]),
        (args.logfile, log_fp),
    ]:
        # Skip items with no remote path specified
        if remote_path is None:
            continue

        # Optionally compress the results
        if remote_path.endswith(".gz"):
            logging.info('Compressing ' + local_path)
            try:
                run_cmds([
                    "gzip",
                    local_path
                ])
            except:
                exit_and_clean_up(temp_folder)
            local_path = local_path + ".gz"
            
        # Upload the results
        try:
            upload_file(local_path, remote_path)
        except:
            exit_and_clean_up(temp_folder)

    logging.info("Finished -- Deleteing temporary files and shutting down")
    shutil.rmtree(temp_folder)
