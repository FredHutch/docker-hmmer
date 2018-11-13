
import json
import logging
import os
import shutil
import subprocess
import sys
import traceback
import uuid


def run_cmds(commands, retry=0, catchExcept=False, stdout=None):
    """Run commands and write out the log, combining STDOUT & STDERR."""
    logging.info("Commands:")
    logging.info(' '.join(commands))
    if stdout is None:
        p = subprocess.Popen(commands,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        stdout, stderr = p.communicate()
    else:
        with open(stdout, "wt") as fo:
            p = subprocess.Popen(commands,
                                 stderr=subprocess.PIPE,
                                 stdout=fo)
            stdout, stderr = p.communicate()
        stdout = False
    exitcode = p.wait()
    if stdout:
        logging.info("Standard output of subprocess:")
        for line in stdout.decode("utf-8").split('\n'):
            logging.info(line)
    if stderr:
        logging.info("Standard error of subprocess:")
        for line in stderr.split('\n'):
            logging.info(line)

    # Check the exit code
    if exitcode != 0 and retry > 0:
        msg = "Exit code {}, retrying {} more times".format(exitcode, retry)
        logging.info(msg)
        run_cmds(commands, retry=retry - 1)
    elif exitcode != 0 and catchExcept:
        msg = "Exit code was {}, but we will continue anyway"
        logging.info(msg.format(exitcode))
    else:
        assert exitcode == 0, "Exit code {}".format(exitcode)


def exit_and_clean_up(temp_folder):
    """Log the error messages and delete the temporary folder."""
    # Capture the traceback
    logging.info("There was an unexpected failure")
    exc_type, exc_value, exc_traceback = sys.exc_info()
    for line in traceback.format_tb(exc_traceback):
        logging.info(line)

    # Delete any files that were created for this sample
    logging.info("Removing temporary folder: " + temp_folder)
    shutil.rmtree(temp_folder)

    # Exit
    logging.info("Exit type: {}".format(exc_type))
    logging.info("Exit code: {}".format(exc_value))
    sys.exit(exc_value)


def set_up_temp_folder(base_temp_folder):
    """Set up a temporary folder to use for scratch files."""
    assert os.path.exists(
        base_temp_folder), "Does not exist: " + base_temp_folder
    temp_folder = os.path.join(base_temp_folder, str(uuid.uuid4())[:8])
    assert os.path.exists(temp_folder) is False
    os.mkdir(temp_folder)
    return temp_folder


def set_up_logging(temp_folder, task_name):
    """Set up logging to a temp file."""

    # Set up logging
    logFormatter = logging.Formatter(
        '%(asctime)s %(levelname)-8s [' + task_name + '] %(message)s'
    )
    rootLogger = logging.getLogger()
    rootLogger.setLevel(logging.INFO)

    # Write to file
    log_fp = os.path.join(
        temp_folder, "log.{}.txt".format(str(uuid.uuid4())[:8])
    )
    fileHandler = logging.FileHandler(log_fp)
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

    # Write to STDOUT
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)

    return log_fp

def get_file(fp, temp_folder):
    """Fetch a file."""

    logging.info("Fetching {}".format(fp))

    # Get the filename
    filename = fp.split("/")[-1]

    # Make the local file name
    local_fp = os.path.join(
        temp_folder, "{}.{}".format(
            str(uuid.uuid4())[:8],
            filename
        )
    )

    if fp.startswith("s3://"):
        logging.info("Fetching from AWS S3")
        run_cmds(["aws", "s3", "cp", fp, local_fp])

    elif fp.startswith("ftp://"):
        logging.info("Fetching from FTP")
        run_cmds(["wget", "-O", local_fp, fp])

    else:
        logging.info("Copying from local path")
        run_cmds(["cp", fp, local_fp])

    assert os.path.exists(local_fp)

    return local_fp


def upload_file(local_fp, remote_fp):
    """Upload a file."""
    logging.info("Uploading {}".format(local_fp))

    if local_fp.startswith("s3://"):
        logging.info("Pushing to AWS S3")
        run_cmds(["aws", "s3", "cp", local_fp, remote_fp])
    else:
        logging.info("Copying from local path")
        run_cmds(["cp", local_fp, remote_fp])
