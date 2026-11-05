# xh in scripts, honestly

Outcome: you can write a script
around xh that behaves the same on
your terminal and at 3 a.m. under a
scheduler — and you can say plainly
when the pretty client is the wrong
tool and curl is the right one.

## The script traps are the lab's traps

Every surprise in this guide so far
was a difference between a person
at a terminal and a program that is
not. A script is permanently the
second case, so the lab's lessons
become a checklist:

- **Standard input is never a
  terminal in a script.** Without
  `--ignore-stdin`, a scheduler's
  empty stdin is a body waiting to
  happen (chapter 3). The lab's
  first run even sat *waiting* on
  an stdin that never closed
  (t12) — in a script, that is a
  hang with no error message.
  **First habit: `--ignore-stdin`
  on every scripted call** that is
  not deliberately piping a body.
- **The exit code is already a
  verdict** (chapter 9): 0, 3, 4, 5
  split success, redirect, client
  fault, and server fault with no
  parsing. Write the script to read
  it — and decide consciously
  whether a 3xx is failure for your
  purpose, because xh counts an
  unfollowed one as 3.
- **Output in a pipe is the body,
  as sent.** That is what a script
  wants to consume — pair it with a
  real parser (chapter 12's `jq`),
  never with patterns matched
  against the terminal view's
  reformatting.
- **Name your downloads.** Without
  `--output`, a piped `--download`
  writes to standard output and no
  file exists for the next line of
  the script to find (t08).
- **Quiet is a feature.** `--quiet`
  plus the exit code is a complete
  health-check in one line.

A script built on those habits
looks like this in shape (a
workshop stock check, in outline —
the fixture URL stands in for a
real one):

```bash
if xh --ignore-stdin --quiet --session-read-only bench :18092/echo >/dev/null; then
    echo "stock server answered"
else
    echo "stock check failed with xh exit $?" >&2
fi
```

Note the session is read-only:
the script replays fixed
credentials and can never write
new state back into the session
file (chapter 8) — and the
credentials themselves live in that
file, in clear text, so the file's
permissions are the script's real
security boundary.

## When xh is the wrong tool

Honesty about the home tool is a
series habit, and here it is cheap
to be specific, because `--curl`
(chapter 10) draws the comparison
for you:

- **The script must run anywhere.**
  curl is on effectively every
  machine you will ever touch; xh
  is on the machines you installed
  it on. A script that travels —
  installers, rescue environments,
  containers you do not control —
  speaks curl, or carries the
  xh binary with it deliberately.
- **The job is a transfer, not a
  conversation.** Mirroring,
  resuming large files across a
  flaky network, elaborate retry
  and rate machinery: that is
  curl's home ground, with a flag
  surface decades deep. xh's
  download is a convenience for
  the file a reply points at.
- **The reply needs machinery xh
  does not offer.** Anything that
  depends on HTTP features outside
  the request–reply basics of this
  guide — the limits chapter names
  xh's own edges — wants the tool
  built for it.
- **Nobody will ever read the
  output.** If a request is made a
  thousand times by a machine and
  read only on failure, the
  friendly view earns little; the
  exit codes still argue for xh,
  but the margin is thinner than
  xh's admirers (or this guide)
  might suggest.

None of that is an apology. xh's
ground — a person, or a script a
person must be able to read,
talking to an API and needing to
see what was said — is a large and
honest territory, and the
translation flag means choosing it
never locks a request in.

Check: you can recite the five
script habits from the checklist,
and give two situations where you
would start with curl instead —
with a reason for each that is
about the job, not about habit.
