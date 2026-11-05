# Authentication

Outcome: you can prove to a server
who you are, by password and by
token — and you can handle the
credentials so they do not leak into
the places commands get remembered.

## The warning, first

Everything in this chapter involves
a secret on a command line, and a
command line is *recorded*: in your
shell's history file, in the
terminal scrollback, in any log or
transcript that captured the
command, and briefly in the list of
running processes where other users
of the same machine can see it.
None of that makes the commands
below unusable — it makes them
worth handling with the habits at
the end of this chapter, stated
before the first password is typed
rather than after.

## Basic auth: a password, encoded

**HTTP basic authentication** sends
a user name and password joined by
a colon, **base64-encoded** — an
encoding that makes arbitrary text
safe to carry in a header, and that
anyone can reverse in a second. It
protects nothing by itself; it is
only safe inside an HTTPS
connection, which does the actual
protecting.

```text
$ xh --ignore-stdin --auth bench:tape :18092/echo
{"authorization":"Basic YmVuY2g6dGFwZQ=="}
$ echo YmVuY2g6dGFwZQ== | base64 -d
bench:tape
```

(transcript `xh-lab/transcripts/t05-auth.txt`.
The lab's credentials belong to an
imaginary workshop stock server and
protect nothing.) The header the
server received is the word `Basic`
and the encoding of `bench:tape`,
and the decode underneath it is the
chapter's whole security lesson in
two lines: **base64 is not
encryption** — treat a basic-auth
header as the password itself,
because for anyone reading it, it
is.

`--auth` accepts `user:password`,
and also just `user` — in which
case xh prompts for the password
as you type, so it never appears on
the command line at all. **That
prompt was not run in the lab** (an
interactive prompt leaves no
transcript a checker can verify),
so it is documented-only here; it
is the form to prefer by hand.

## Bearer tokens: a key, presented

Many services issue a **token** — a
long random string that works like
a key card: whoever presents it is
trusted, no password involved.

```text
$ xh --ignore-stdin --auth-type bearer --auth TOKEN :18092/echo
{"authorization":"Bearer TOKEN"}
```

`--auth-type bearer` changes what
`--auth` builds: the header is now
`Bearer` and the token exactly as
given. (The lab's token is the
literal word TOKEN; a real one is
long, random, and worth more than
a password while it lives, because
it usually cannot be changed
without revoking it outright.) A
token in a header item
(`Authorization:Bearer TOKEN`) does
the same job by hand; the flag
exists so the construction is not
retyped — and mistyped — per call.

A third type, **digest**
authentication — a challenge-and-
response scheme where the password
itself never crosses the wire — is
listed among `--auth-type`'s values.
The lab's fixture cannot issue a
digest challenge, so **digest is
documented-only** in this guide.

## The habits

- **Prefer the prompt** for
  passwords you type often:
  `--auth user` alone, and let xh
  ask.
- **Prefer a session** (chapter 8)
  for a service you call all day —
  one stored secret, not a password
  on every command line. Read that
  chapter's warning too: the stored
  secret sits in a file in clear
  text, so the saving is in
  *exposure*, not in secrecy.
- **Mind the history.** A shell
  history file with passwords in it
  is a credential store you did not
  mean to keep. Commands can be
  kept out of most shells' history
  by leading them with a space
  where that feature is on — but
  the reliable fix is not typing
  the secret in the first place.
- **Treat tokens like passwords**,
  and short-lived tokens as better
  than long-lived ones where the
  service offers the choice.

Check: you can send both a basic
and a bearer credential, decode a
basic header back to its password
to prove the point about encoding,
and say where a typed password
would otherwise be remembered.
