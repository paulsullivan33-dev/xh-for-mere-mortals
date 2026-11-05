# Offline mode and the curl translation

Outcome: you can make xh show you a
request instead of sending it —
printed as itself, and translated
into the curl command that would
send the same thing — and you know
what each view teaches.

## --offline: the request, unsent

`--offline` builds the whole
request and prints it — request
line, headers, body — and sends
nothing:

```text
$ xh --offline --ignore-stdin POST :18092/echo X-Workshop:North-Bench name=hammer count:=3
POST /echo HTTP/1.1
Accept-Encoding: gzip, deflate, br, zstd
User-Agent: xh/0.25.3
Connection: keep-alive
Accept: application/json, */*;q=0.5
Content-Type: application/json
X-Workshop: North-Bench
Content-Length: 27
Host: 127.0.0.1:18092

{"name":"hammer","count":3}
```

(transcript `xh-lab/transcripts/t10-offline-and-verbose.txt`.)
"Sends nothing" is a claim, and the
lab checked it the way negative
claims deserve: the fixture logs a
line per request it receives, and
the log stood at 51 lines before
the offline run and 51 after.

Read the printout once with fresh
eyes and it repays you: here are
the headers xh adds on your behalf,
the content type its defaults
chose, the exact body your items
became. This is the one rule made
into a flag — the request itself,
available for inspection *before*
it exists on any server. Reach for
it whenever a request is precious,
dangerous, or merely mysterious.

`--verbose` is the same picture
taken live: the request printed
first, then the reply as it comes
back (t10). Where offline asks
"what *would* I send?", verbose
asks "what did I send, and what
came back?" — the pair of them is
xh's answer to debugging a call
that did not do what you meant.

## --curl: the same request, in the other language

`--curl` prints nothing about xh
at all. It translates:

```text
$ xh --curl --ignore-stdin POST :18092/echo X-Workshop:North-Bench --auth bench:tape items[]=hammer items[]=nails count:=2
curl -X POST http://127.0.0.1:18092/echo -H 'x-workshop: North-Bench' --basic -u bench:tape -H 'content-type: application/json' -H 'accept: application/json, */*;q=0.5' -d '{"items":["hammer","nails"],"count":2}'
```

(transcript `xh-lab/transcripts/t09-curl-translation.txt`.)
Every piece of the grammar from
chapter 4 is visible in curl's
spelling: the items array became
one quoted JSON body, the auth
became `-u`, the header became
`-H`. The translation *is* a
lesson in what the item syntax was
doing for you.

And it is not merely illustrative.
The lab saved the printed command
and ran it, and the fixture server
reported the identical request —
same authorization, same header,
same body — as the xh original
(t09 shows both reports). Two
honest notes on the evidence: the
printed curl sends a few headers
of its own differently (its
`User-Agent` names curl, as it
should), and the translation
lower-cases header names, which
HTTP treats as the same names. The
request *you specified* arrives
unchanged; that is the claim, and
it is the proved one.

Three uses for a runnable
translation:

- **Sharing.** A bug report or a
  message to a colleague in curl
  is understood everywhere; the
  same request in xh is understood
  where xh is known.
- **Handing over.** A script that
  must run on a machine with curl
  but not xh can start life as the
  translation. (Chapter 11 weighs
  when that is the right call to
  begin with.)
- **Checking.** If a request
  behaves oddly, its translation
  shows the same request in a
  notation where nothing hides —
  no inference, no defaults left
  implicit.

`--curl-long` is the same
translation with curl's long
option names (`--request` for
`-X`, and so on) — quoted here
from `--help`; the lab ran the
short form.

Check: you can print a request
without sending it and say how the
lab knows nothing was sent, run a
translation where it counts, and
name one job for each of
`--offline`, `--verbose`, and
`--curl`.
