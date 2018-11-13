#!/usr/bin/env bats

@test "HMMER in the PATH" {
  v="$(hmmsearch -h 2>&1 || true )"
  [[ "$v" =~ "HMMER" ]]
}
