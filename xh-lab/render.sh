#!/bin/sh
# render.sh — show what xh's decorated output looks like as
# plain text, by stripping the ANSI colour escapes. The guide
# prints decorated output this way; the transcripts also keep
# escape-visible excerpts wherever the colours themselves are
# the point.
exec sed 's/\x1b\[[0-9;]*m//g'
