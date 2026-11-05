# The neighbours

Outcome: you can place xh among the
tools that share its desk — curl,
HTTPie itself, and jq — and say,
for each, the job it does that xh
does not.

## curl: the ground everyone stands on

curl predates the friendly clients
by well over a decade and is
installed essentially everywhere.
It speaks more protocols than HTTP,
transfers under conditions xh does
not attempt, and its flag language —
verbose to a fault, assembled piece
by piece — is the notation the
whole field shares: documentation,
bug reports, and chapter 10's
translations are written in it.

The relationship is not rivalry so
much as strata. xh is the client
you *think* in; curl is the one
your thinking can always be
translated into, the one that is
still there on the strange machine
at the bad moment. This series
covers curl on its own terms in
**curl for Mere Mortals**.

## HTTPie: the original

HTTPie invented the language this
guide teaches — the items, the
sessions, the friendly view — and
xh is a reimplementation of that
language, not its inventor. The
honest differences, stated the way
the project's own documentation
states them (this guide's lab ran
xh only, so the comparison is
characterised, not benchmarked):

- **Form.** xh is one native
  binary; HTTPie is a Python
  program, installed with its
  interpreter and libraries, and
  starts as a Python program
  starts. For a tool run dozens of
  times a day, startup is part of
  the feel.
- **Reach.** HTTPie has a plugin
  system and a longer feature
  history; xh covers the core
  language and states its edges
  (chapter 13) rather than growing
  by extension.
- **Compatibility.** The item
  grammar and most flags carry
  over, which is why this guide
  can teach "the HTTPie language,
  in xh" without hedging on every
  page — and why a reader moving
  between them should still check
  a flag's spelling in `--help`
  on the machine in front of them,
  because near-compatible is not
  identical.

If HTTPie is already yours, xh is
an easy second dialect; if neither
is, this guide's tool is the one
with the single-file install.

## jq: the partner, not a rival

The lab's transcripts reach for
`jq` constantly, and that is the
normal shape of work: **xh fetches,
jq answers.** xh gets a reply and
shows it whole; jq takes JSON and
projects it — one field, one
filter, one precise question —
into the small piece the next step
needs. The projection in transcript
t04 that pulled the parts list out
of a large report, and the
one-liners throughout the lab, are
jq doing its half.

Learning that half has its own
guide in this series: **jq for
Mere Mortals**. This chapter, per
the series rule, still completes
without it: everything xh itself
does is above.

## And the rest of the bench

Two more neighbours deserve a
sentence each. **wget** is the
retriever from curl's generation —
fetch this file, recursively,
patiently — and remains a sound
choice for pure downloading. And
when the conversation outgrows
single requests entirely — saved
collections, environments, a team
sharing the same calls — that is
the territory of workspace tools
like the one this series covers in
**Bruno for Mere Mortals**; xh's
sessions are a notebook page, not
a shared workspace, and are better
for knowing it.

Check: for each of curl, HTTPie,
and jq you can name the job it is
for in one phrase — and the phrase
for xh that is left over is the
one this guide has been about.
