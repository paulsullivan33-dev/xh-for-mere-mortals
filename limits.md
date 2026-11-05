# Limits

Outcome: you can name what xh does
not do, and which of its defaults
will differ from what other tools
taught you to expect — before
either costs you an afternoon.

## The view is a rendering

Chapter 1's rule, as a limitation:
on a terminal, xh re-indents JSON
and re-sorts headers. The facts
survive; the bytes do not. Any
process that needs the reply *as
sent* — a signature check, a byte
count, a faithful archive — must
take the pipe view or
`--pretty=none`, and any
troubleshooting that argues from
the terminal view about order or
spacing is arguing about the
picture, not the reply.

## Defaults that decide for you

- **Method inference** (items imply
  POST, stdin implies a body) is a
  convenience that fires silently.
  A named method is the only full
  opt-out, and a named GET still
  carries items as a body rather
  than as query parameters.
- **Redirects stop at the first
  hop** without `--follow`, and an
  unfollowed redirect counts as a
  failed check (exit 3).
- **The status check is on** in
  this version: an answered 404 is
  exit 4, where curl and older
  habits say 0. Scripts inherited
  from those habits will report
  failures that are actually
  answers — or, with the check
  assumed and absent elsewhere,
  successes that are actually
  errors.
- **The download's filename is the
  server's suggestion** whenever
  you do not name one, and in a
  pipe there is no file at all.

## Sessions are a notebook, not a vault

A session file holds its password
in clear text (`raw_auth`, chapter
8), is scoped to one host and
port, and saves what it is shown
unless it is opened read-only.
That is a fair design for a
personal notebook; it is not a
credential manager, and a session
is not the place for a secret
whose leak would be an emergency.
The same honesty applies to basic
auth generally: the header is the
password, encoded, and only the
HTTPS around it keeps it private.
On a plain-HTTP connection, xh
will send credentials it can see
no protection for — the warning
about *where* you point a call is
the user's, and this guide's lab,
being all on one machine, can only
state it, not demonstrate it.

## Not a browser, not a suite

xh sends one request at a time,
at your typing. It does not run a
page's scripts, keep a browsing
history, discover links, retry on
a schedule, or test a service
under load. Its grammar covers
the request shapes of chapters 4
to 6 as far as the lab proved
them; arrays of objects and deeper
nesting than shown were not
exercised, and digest
authentication and cookie replay —
real features, listed in `--help`
and the session format — are
documented-only in this guide
because the fixture could not
exercise them (criteria.md keeps
the whole ledger).

Version scope, plainly: every
measured claim here is about
**xh 0.25.3**, the lab's binary.
Defaults — above all the status
check's — are exactly the kind of
thing a later release can change,
which is why the chapters cite
versions and transcripts rather
than asking to be believed.

Check: you can list the four
deciding defaults, say why a
session file deserves file
permissions like a password's, and
name two jobs you would not hand
to xh at all.
