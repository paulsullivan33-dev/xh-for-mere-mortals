# What xh is

Outcome: you can say what an HTTP
client at the command line is for,
where xh came from, and the one rule
this guide keeps coming back to —
before any command depends on it.

## Asking a server a question

A great deal of computing is one
machine asking another a question
over **HTTP**, the request-and-reply
language of the web. A browser asks
those questions all day, but it only
shows you the finished page. When you
want to ask the question yourself —
to test a small web service, fetch a
file, post a reading to an API, see
exactly what a server answers — you
need a program whose whole job is to
send one request and show you the
reply. That program is an **HTTP
client**, and at the command line the
long-standing one is **curl**.

curl is excellent and everywhere, and
its language is nobody's idea of
friendly: a request is a pile of
flags, a JSON body is a quoted string
you assemble by hand, and the reply
arrives unformatted. In 2012 a tool
called **HTTPie** asked what the same
job would look like designed for
reading: the request built from small
labelled pieces, the reply printed
with its headers, its status, and its
JSON laid out and coloured. People
liked the language so much that it
became the thing other tools are
compared against.

**xh** is that language, rewritten.
It is HTTPie's way of asking —
deliberately compatible, item for
item in most cases — implemented in
Rust as one small, fast, self-contained
binary. You type the request the
HTTPie way; xh sends it, and prints
the reply the friendly way: status
line, headers, and a body with JSON
reformatted and coloured on a
terminal, passed through plainly in a
pipe.

## The one rule

Everything in this guide hangs on
one observation, and the lab will
keep proving it:

**The reply you are shown is a
rendering. The request xh sent is
the ground truth.**

The rendering is genuinely helpful —
and it is edited. On a terminal xh
re-indents JSON it did not write,
sorts the reply's headers into
alphabetical order, and wraps tokens
in colour codes. None of that is
what arrived on the wire. The same
editing runs in the other direction:
xh assembles the request from your
method, your items, *and where your
standard input points* — and one of
those can quietly change what is
sent (chapter 3 shows a GET turning
into a POST because of it).

So the habit this guide teaches is:
when it matters, look at the request
itself. xh unusually *wants* to show
you — it can print the request
instead of sending it, print it
alongside the reply, and even
translate it into the curl command
that would send the same thing
(chapter 10). A client that shows
its workings is one you can trust
with the rest.

## What xh is not

xh is not a browser: it does not run
JavaScript, follow a page's links,
or keep a page's state beyond what
you ask it to save (chapter 8). It
is not a load tester or a crawler.
And it is not the only friendly
client — chapter 12 puts it next to
curl, HTTPie itself, and the tools
that usually sit beside it, honestly.

Check: you can say, in one sentence,
what xh does — and you know why this
guide will keep asking "but what did
it actually send?"
