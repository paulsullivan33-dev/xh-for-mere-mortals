# Output, downloads, and exit codes

Outcome: you can ask xh for exactly
the part of the reply you want,
save a download to a file you
chose, and read its exit code as
the server's verdict — the three
things scripting with xh turns on.

## Choosing what prints

Chapter 3 showed the default: the
whole reply on a terminal, the
body alone in a pipe. The selection
switches narrow that (transcript
`xh-lab/transcripts/t07-output-and-exit-codes.txt`):

- `--headers` (or `-h`): the status
  line and headers, no body.
- `--body` (or `-b`): the body,
  only — on a terminal too, where
  the default would show more.
- `--quiet`: nothing at all. The
  command still runs; only its
  output is silenced.
- `--print=…` combines parts by
  letter for finer control; the
  three switches above are its
  common cases, ready-made.

Formatting has its own dial.
`--pretty` takes `all`, `colors`,
`format`, or `none`, and chapter
3's two edits live behind it: in a
pipe the default is effectively
`none` — the body passes through as
sent, which the lab proved on a
body the fixture sends as one line:

```text
$ xh --ignore-stdin :18092/compact
{"order":"bench-12","items":[{"name":"claw hammer","qty":2},{"name":"tape measure","qty":1}],"gift":false}
$ xh --ignore-stdin --pretty=format :18092/compact
{
    "order": "bench-12",
    ...
}
```

`--pretty=format` reformats without
colour; `all` is format plus colour.
The reformat uses four-space
indent unless `--format-options`
says otherwise — `json.indent:2`
reproduced a two-space layout in
the same transcript. And `--headers`
carries chapter 3's warning with
it: on a terminal, the pretty
printer *sorts* the headers; the
pipe view is the one that keeps the
server's order (t07 shows both,
three runs each).

## Downloads

`--download` turns a reply into a
file. On a terminal it saves under
the name the server suggests (the
`Content-Disposition` header), with
a progress bar while it comes down:

```text
$ xh --ignore-stdin --download :18092/download
Downloading 81 B to "packing-list.txt"
Done. 81 B in 0.00037s
$ cat packing-list.txt
Packing list - bench order 12
2x claw hammer
...
```

(transcript `xh-lab/transcripts/t08-download.txt`.)
Two behaviours matter more than the
bar:

- **`--output` names the file
  yourself** — `named-copy.txt` in
  the lab. In scripts, always name
  it: a server-suggested name is
  the server's choice, not yours.
- **In a pipe, `--download` alone
  writes the body to standard
  output** and reports
  `Downloading 81 B to "<stdout>"`
  — no file appears (t08 proves the
  empty folder). That is pipe logic
  applied consistently, and a real
  trap for a script that expected a
  file. `--output` is the fix.

Resuming a partial download with
`--continue` exists, and is
documented-only here: the lab's
fixture serves its small file whole
or not at all, so there was no
interrupted transfer to resume.

## Exit codes: the verdict as a number

A script cannot read a pretty
reply; it reads the **exit code**.
curl's quiet convention is to exit
0 whenever a reply arrived at all —
a 404 is a successful *transfer*.
xh, in the version the lab ran,
defaults the other way: **the
status check is on unless you turn
it off** (`--help` marks
`--check-status` as "(default)",
and every code below was measured,
not read — t07):

| The server answered | Exit |
|---|---|
| 2xx — success | 0 |
| 3xx — a redirect you did not follow | 3 |
| 404, any 4xx — your request's fault, says the server | 4 |
| 500, any 5xx — the server's fault, it says | 5 |

A 4xx also prints a warning to
standard error
(`xh: warning: HTTP 404 Not Found`)
— visible in a terminal, silent in
the number alone. `--no-check-status`
restores the old convention exactly:
the same 404 exits 0. And a request
that cannot be sent at all — no
server at the address — is a
different failure altogether, exit
**1**, with an error chain that
reads from the specific cause
upward (transcript
`xh-lab/transcripts/t13-errors.txt`):

```text
xh: error: error sending request for url (http://127.0.0.1:18099/echo)
Caused by:
    0: client error (Connect)
    1: tcp connect error
    2: Connection refused (os error 111)
```

One default deserves emphasis
because it splits the difference
between tools: **redirects are not
followed** unless `--follow` is
given, and an unfollowed 302 is the
3 above. `--all` alongside
`--follow` prints every reply in
the chain, not just the last
(transcript `xh-lab/transcripts/t11-redirects.txt`).

Check: you can print headers only,
body only, or nothing; save a
download under your own filename
in a script; and say what exits 0,
3, 4, 5, and 1 each mean.
