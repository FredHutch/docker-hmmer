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
