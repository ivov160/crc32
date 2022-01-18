#!/bin/bash

set -e -u

function run_test {
    local file_path="$1"
    local success="$2"
    local fail="$3"

    rm -f /tmp/out
    echo -en "\n $file_path - "
    ./app "./files/$file_path" > /tmp/out 2>&1 && echo "[$success]" || echo "[$fail]"
    [ -f /tmp/out ] && cat /tmp/out
}

reset
run_test "good.dat" "PASSED" "FAILED"
run_test "bad.dat" "FAILED" "PASSED"
run_test "empty.dat" "FAILED" "PASSED"
run_test "size.dat" "FAILED" "PASSED"