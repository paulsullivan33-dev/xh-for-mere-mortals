# Methods and bodies

Outcome: you can name the method a
request should use, know how xh
chooses one when you do not, and put
a body on a request three ways —
items, a raw string, and standard
input.

## The methods are verbs

An HTTP request starts with a
**method**, a short verb that tells
the server what kind of asking this
is. The ones daily work uses:

| Method | The usual meaning |
|---|---|
| GET | read this — change nothing |
| POST | create or submit this |
| PUT | replace this with what's sent |
| PATCH | change this, in the ways sent |
| DELETE | remove this |

The meanings are conventions the
server chooses to honour, not laws
xh enforces — xh will send any of
them with any body you build. The
lab sent each of the four
writing verbs against the fixture
and read the method back off the
report (transcript
`xh-lab/transcripts/t03-methods-and-bodies.txt`):

```text
$ xh --ignore-stdin PUT :18092/echo name=hammer shelf:=4
{"method":"PUT","json":{"name":"hammer","shelf":4}}
$ xh --ignore-stdin PATCH :18092/echo shelf:=5
{"method":"PATCH","json":{"shelf":5}}
$ xh --ignore-stdin DELETE :18092/echo
{"method":"DELETE","body_length":0}
```

(The report is projected with `jq`
in these transcripts to the fields
that matter; chapter 12 talks about
that partnership.)

The method, when you name one, goes
*before* the URL, in capitals.
Any other verb a service documents
— HEAD, OPTIONS, a custom one — can
be named the same way.

## How xh picks, when you don't

Three rules, all proved in the lab:

1. **Data items imply POST.** Any
   `=` or `:=` item in the command
   makes an unnamed method a POST
   (t02).
2. **No items, no stdin: GET.** The
   plain read of chapter 3.
3. **Redirected stdin implies a
   body**, which implies POST when
   the method is unnamed — chapter
   3's surprise, and the reason
   `--ignore-stdin` is the lab's
   default posture.

Naming the method always wins over
rules 1 and 3 — with the chapter 4
caution that a named GET *keeps*
items as a body rather than moving
them anywhere.

## Bodies: JSON by default

Unless told otherwise, xh builds
bodies as **JSON**: the items
become one JSON object, the
`Content-Type` header says
`application/json`, and the `Accept`
header asks for JSON first. This is
the modern default because most
APIs speak JSON; chapter 6 covers
the `--form` and `--multipart`
alternatives for the ones that do
not.

Two more ways to supply a body,
both verified against the fixture:

- **`--raw` hands xh a finished
  body.** `xh --raw '{"direct":true}' POST …`
  sent those exact bytes as the
  body (t03). Items and `--raw` are
  alternatives — use items to build,
  `--raw` when the body already
  exists as text.
- **Standard input is a body.**
  `printf '{"from":"stdin"}' | xh POST …`
  delivered the piped text as the
  body and parsed as JSON at the
  server (t03). This is the one
  case where stdin is welcome —
  named method, no items, the pipe
  *is* the body. Mix items with a
  stdin body and xh refuses, with
  an error that names the remedy:

```text
xh: error: Request body (from stdin) and request data (key=value) cannot be mixed. Pass --ignore-stdin to ignore standard input.
```

That refusal is a kindness: the
alternative is silently sending a
request that is neither what the
items say nor what the pipe says.

Check: you can state the three
method rules, send each of the five
common verbs, and build a body from
items, from `--raw`, and from a
pipe — and say which of the three
the lab's transcripts deliberately
avoid mixing.
