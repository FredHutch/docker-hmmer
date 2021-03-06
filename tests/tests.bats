#!/usr/bin/env bats

@test "HMMER in the PATH" {
  v="$(hmmsearch -h 2>&1 || true )"
  [[ "$v" =~ "HMMER" ]]
}

@test "hmmbuild.py in the PATH" {
  v="$(hmmbuild.py -h 2>&1 || true )"
  [[ "$v" =~ "Build an HMM profile" ]]
}

@test "run hmmbuild.py on example file" {
  hmmbuild.py \
  --input /usr/local/tests/globins4.sto \
  --output /usr/local/tests/globins4.hmm \
  --temp-folder /usr/local/tests/
}

@test "run hmmsearch.py on example file" {
  hmmsearch.py \
  --query /usr/local/tests/HBB_HUMAN.fasta \
  --profile /usr/local/tests/globins4.hmm \
  --output /usr/local/tests/globins4.HBB_HUMAN.aln \
  --output-tsv /usr/local/tests/globins4.HBB_HUMAN.tsv \
  --output-fasta /usr/local/tests/globins4.HBB_HUMAN.fasta \
  --temp-folder /usr/local/tests/

  [[ -s /usr/local/tests/globins4.HBB_HUMAN.aln ]]
  [[ -s /usr/local/tests/globins4.HBB_HUMAN.tsv ]]
  [[ -s /usr/local/tests/globins4.HBB_HUMAN.fasta ]]

}

@test "run hmmsearch.py on example file (GZIP)" {
  hmmsearch.py \
  --query /usr/local/tests/HBB_HUMAN.fasta \
  --profile /usr/local/tests/globins4.hmm \
  --output /usr/local/tests/globins4.HBB_HUMAN.aln.gz \
  --temp-folder /usr/local/tests/

  gzip -t /usr/local/tests/globins4.HBB_HUMAN.aln.gz

}
