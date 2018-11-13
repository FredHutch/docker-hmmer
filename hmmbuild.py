#!/usr/bin/env python3
"""Build an HMM profile from a multiple alignment."""

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
        Build an HMM profile from a multiple alignment.
        """)

    parser.add_argument("--input",
                        type=str,
                        help="Location for input alignement file.")
    parser.add_argument("--output",
                        type=str,
                        help="Location for output HMM profile.")
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
    log_fp = set_up_logging(temp_folder, "HMMBUILD")

    # Get the input file
    try:
        input_fp = get_file(args.input, temp_folder)
    except:
        exit_and_clean_up(temp_folder)

    # Make the HMM
    output_hmm = os.path.join(
        temp_folder, 
        "{}.hmm".format(str(uuid.uuid4())[:8])
    )
    try:
        run_cmds([
            "hmmbuild",
            output_hmm,
            input_fp
        ])
    except:
        exit_and_clean_up(temp_folder)

    # Make sure the output exists
    assert os.path.exists(output_hmm)

    # Upload the results
    try:
        upload_file(output_hmm, args.output)
    except:
        exit_and_clean_up(temp_folder)

    # Upload the logs, if specified
    if args.logfile is not None:
        try:
            upload_file(log_fp, args.logfile)
        except:
            exit_and_clean_up(temp_folder)

    logging.info("Deleteing temporary files and shutting down")
    shutil.rmtree(temp_folder)
