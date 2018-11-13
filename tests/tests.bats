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
  --temp-folder /usr/local/tests/
}
