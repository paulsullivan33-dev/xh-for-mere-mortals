# Sessions

Outcome: you can teach xh a named
bundle of credentials and headers
once, have later calls replay it,
find the file it lives in — and
read, in that file, the honest
price of the convenience.

## Teaching a session

Some services you call all day,
always with the same login and the
same extra headers. A **session**
is xh's memory for that: name one,
use it on a call, and the call's
authentication and headers are
saved under the name. Later calls
that name the session replay what
it holds. The lab taught one in a
single call (transcript
`xh-lab/transcripts/t06-sessions.txt`):

```text
$ xh --ignore-stdin --session bench --auth bench:tape :18092/echo X-Workshop:North-Bench
{"auth":"Basic YmVuY2g6dGFwZQ==","ws":"North-Bench"}
$ xh --ignore-stdin --session bench :18092/echo
{"auth":"Basic YmVuY2g6dGFwZQ==","ws":"North-Bench"}
```

The second command names neither
the password nor the header — and
the fixture server received both.
The session supplied them. (Items
given *on* a session call are also
considered for saving, which is how
the first call taught it; a call can
carry one-off items too, and the
next section shows how to keep them
one-off.)

## Where the memory lives

A session is a plain JSON file. In
the lab, with configuration pointed
at the lab's own folder, it landed
at:

```text
xh/sessions/127.0.0.1_18092/bench.json
```

— one folder per host and port, one
file per session name. On a real
machine the same file starts from
`~/.config/xh/sessions/` (the
config folder follows the usual
per-platform conventions). Its
contents are worth reading once in
full:

```json
{
    "__meta__": { "about": "xh session file", "xh": "0.25.3" },
    "auth": { "type": "basic", "raw_auth": "bench:tape" },
    "cookies": [],
    "headers": [
        { "name": "x-workshop", "value": "North-Bench" }
    ]
}
```

Two things to take from it. First,
the format is open and editable:
you can write or correct a session
file by hand, and delete one by
deleting the file. Second — the
price, in clear view — **`raw_auth`
holds the password as plain text.**
A session moves the secret off your
command lines and out of your shell
history, which is a real gain
(chapter 7), and concentrates it in
one file that anyone who can read
your home folder can read whole.
Guard it the way you would a
password file, because that is what
it is. The file also reserves a
`cookies` list — sessions are where
xh keeps cookies a server sets, so
a logged-in conversation can
continue. The lab's fixture never
sets a cookie, so **cookie replay
is documented-only** here; the
empty list in the real file is as
far as the evidence goes.

## Using one without teaching it

`--session-read-only` replays a
session without saving anything
new into it. The lab proved the
distinction rather than assuming
it: a header sent once under
`--session-read-only bench`
(`X-Extra:once`) arrived at the
server, and the next ordinary
session call did not carry it
(t06). Read-only is the mode for
scripts and shared machines: the
session is a fixed, reviewable
input, not a notebook that grows
with every call.

Check: you can teach a session,
replay it, locate its file on
disk, and say — from the file
itself, not from memory — exactly
what secret it stores and in what
form.
