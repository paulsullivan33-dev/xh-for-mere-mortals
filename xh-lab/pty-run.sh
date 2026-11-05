#!/bin/sh
# pty-run.sh — run a command with a real terminal attached,
# using script(1), and capture what the terminal session
# showed (unlike a plain pipe, a terminal persuades xh to
# use colours and to print the response headers).
# Usage: ./pty-run.sh 'command to run' > capture.txt
exec script -qec "$1" /dev/null
