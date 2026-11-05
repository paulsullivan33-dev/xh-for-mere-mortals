# Your first request

Outcome: you can make a request, read
the friendly view part by part, and
name the three things that view
quietly changes — plus the one thing
about your own command that can
change the request itself.

## The lab's other half: a server that reports back

Every request in this guide goes to
a fixture server the lab wrote: a
small Python program
(`xh-lab/echo_server.py`, standard
library only) listening on this
machine at `http://127.0.0.1:18092`.
It answers every request with a JSON
report of what arrived — the method,
the path, the query, the headers in
the order received, and the body,
parsed. That makes every claim in
the guide checkable: if a chapter
says a piece of syntax lands a
certain way, the server's report is
the witness. You can run the same
server yourself and repeat every
transcript; its special paths
(`/status/404`, `/redirect`,
`/download`, and friends) are the
lab's instruments, listed in
`examples/lab-notes.txt`.

## The friendly view

On a terminal, this asks for the
report with no extras (transcript
`xh-lab/transcripts/t01-first-look.txt`):

```text
$ xh http://127.0.0.1:18092/echo
HTTP/1.1 200 OK
Content-Length: 403
Content-Type: application/json
Date: Thu, 05 Nov 2026 09:30:26 GMT
Server: BaseHTTP/0.6 Python/3.12.3

{
    "method": "GET",
    "path": "/echo",
    ...
}
```

Anatomy, top to bottom:

- The **status line** — the HTTP
  version, the status code, and its
  short name (`200 OK`).
- The **response headers**, one per
  line — the server's labels for its
  own reply: what type the body is,
  how long it is, when it was sent.
- A blank line, then the **body** —
  here, the server's JSON report,
  re-indented and (on a real
  terminal) coloured.

No method was named, so xh sent a
**GET** — the request that asks for
something and carries no body. The
report shows what xh says about
itself on any request: a
`User-Agent` of `xh/0.25.3`, the
encodings it can accept, and, for a
bare GET like this one, an `Accept`
of `*/*` — "anything will do".

## What the view changes

The transcripts print the terminal
view *rendered* — the lab's
`render.sh` strips the colour codes
so the layout can be printed — and
once, *escape-visible*, so you can
see what the colours physically
are: the escape code `\033[34m`
(blue) wrapped around the status
numbers, `\033[36m` (cyan) around
`OK` and each header name (t01).
Colour is instructions mixed into
the text, never part of the reply.

Formatting edits two more things:

- **The body is re-indented.** The
  fixture server sends its JSON with
  two-space indent; the terminal
  view shows four. In a pipe the
  same body passes through with the
  server's own spacing untouched
  (t07 proves both, on a one-line
  body).
- **The headers are re-ordered.**
  On the terminal they print in
  alphabetical order. The server
  sent `Server` first; the pipe view
  keeps the server's order, the
  terminal view does not (t07).

Neither edit changes a single fact —
and both mean the friendly view is
a *picture* of the reply, per the
one rule. When the exact bytes
matter, chapter 9 shows the
switches that turn the editing off.

## The surprise in your own command

Now the direction nobody expects.
Run the same-looking request with
standard input redirected — from a
pipe, a file, anywhere that is not a
terminal:

```text
$ xh http://127.0.0.1:18092/echo < /dev/null | jq -c '{method, content_type, body_length}'
{"method":"POST","content_type":"application/json","body_length":0}
```

No method named, a terminal nowhere
in sight — and the server received
a **POST** with an empty JSON body.
xh takes redirected stdin as a
request body, and a request with a
body defaults to POST. Naming GET
out loud holds the method, but the
empty body still leaves fingerprints:
a JSON `Content-Type`, a
`Content-Length` of 0, and an
`Accept` that now asks for JSON
(t01, third run).

The lab hit this on its very first
call and spent its first transcript
set working it out (t12 tells the
whole story). The working habit,
used by every other command in this
guide: **`--ignore-stdin` unless
stdin is the body on purpose.**

Check: you can point at each part
of the friendly view and say what
it is, name the two ways it edits
the reply — and you can explain why
the lab's commands all carry
`--ignore-stdin`.
