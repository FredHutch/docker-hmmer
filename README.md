# docker-hmmer
Docker image running HMMer

### Wrapper scripts:

The purpose of the wrapper scripts is to automatically handle the process
of pulling and pushing to object storage, while also managing temporary
file space and cleaning up failed jobs cleanly.

#### HMMsearch

```
usage: hmmsearch.py [-h] [--query QUERY] [--profile PROFILE] [--output OUTPUT]
                    [--logfile LOGFILE] [--temp-folder TEMP_FOLDER]

Search an HMM profile against a FASTA file.

optional arguments:
  -h, --help            show this help message and exit
  --query QUERY         Location for input FASTA file.
  --profile PROFILE     Location for input HMM file.
  --output OUTPUT       Location for output HMM alignment.
  --logfile LOGFILE     (Optional) Write log to this file.
  --temp-folder TEMP_FOLDER
                        Temporary directory to use.
```

### HMMbuild

```
usage: hmmbuild.py [-h] [--input INPUT] [--output OUTPUT] [--logfile LOGFILE]
                   [--temp-folder TEMP_FOLDER]

Build an HMM profile from a multiple alignment.

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT         Location for input alignment file.
  --output OUTPUT       Location for output HMM profile.
  --logfile LOGFILE     (Optional) Write log to this file.
  --temp-folder TEMP_FOLDER
                        Temporary directory to use.
```