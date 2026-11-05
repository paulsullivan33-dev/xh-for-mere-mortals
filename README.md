# xh for Mere Mortals

Every service on the modern internet
is asked questions in one language:
HTTP. Browsers ask them invisibly,
but anyone who runs, tests, or
automates a service ends up needing
to ask one directly — and the
traditional tool, curl, answers
with a pile of flags and an
unformatted reply. **xh** is the
friendly HTTP client: the request
built from small labelled **items**
instead of flags, and the reply
printed with its **status line**,
its **headers**, and its **JSON**
laid out and coloured — HTTPie's
celebrated way of asking,
reimplemented as one small, fast
Rust binary.

One rule governs everything it
does, and this guide states it in
chapter 1 and keeps pointing back
to it: **the reply you are shown is
a rendering; the request xh sent
is the ground truth.** The friendly
view re-indents the body and sorts
the headers; your own command —
its method, its items, and where
its standard input points — can
quietly change what is sent. The
lab behind this guide proves both
halves of that, because xh, to its
credit, ships the tools to inspect
itself: it can print the request
instead of sending it, show it
beside the reply, and translate it
into the curl command that sends
the same thing.

The lab ran the real thing: **xh
0.25.3**, the official release
binary from the project's GitHub
releases, against a fixture server
the lab wrote for the purpose — a
small program that answers every
request with a report of what
arrived, so each claim in the guide
is checked by the receiving end,
not by the sender's opinion of
itself. Against it the lab proved
every form of the item syntax from
the server's side of the wire;
sent forms and a file upload, and
matched the upload's SHA-256
fingerprint at both ends; watched
basic and bearer credentials land
in the headers they build; taught
a session and read its file,
password and all; measured the
exit codes for success, redirect,
client error, and server error
rather than reading them off a
table; and ran the `--curl`
translation to show it delivers
the identical request. The lab's
own first surprise — a GET that
became a POST because of where
its standard input pointed — is
chapter 3's centrepiece and the
reason every command in the guide
carries a habit worth stealing.

What the lab could not do, it did
not fake. Digest authentication
needs a server that challenges,
the fixture never sets a cookie,
and a download that is never
interrupted cannot be resumed for
the camera — those, the password
prompt, and the package installs
for each operating system are
named from the documentation and
labelled documented-only, with the
full ledger in `criteria.md`.

## What this guide covers

- [**What xh is**](what-xh-is.md) —
  asking servers questions, HTTPie's
  language in Rust, and the one rule
- [**Installing xh**](installing-xh.md) —
  the release file the lab used, the
  package routes, and the `xhs` name
  that changes the default scheme
- [**Your first request**](your-first-request.md) —
  the echo server, the friendly view
  taken apart, and the stdin surprise
- [**The item syntax**](the-item-syntax.md) —
  one small grammar: headers, query
  parameters, JSON of every shape,
  values from files
- [**Methods and bodies**](methods-and-bodies.md) —
  the five verbs, how xh chooses
  when you don't, and bodies from
  items, from `--raw`, and from a
  pipe
- [**Forms and uploads**](forms-and-uploads.md) —
  form packing where every value is
  a string, multipart uploads, and
  the checksum proof
- [**Authentication**](authentication.md) —
  basic and bearer credentials, the
  shell-history warning, and why
  base64 is not encryption
- [**Sessions**](sessions.md) —
  saved logins and headers, where
  the file lives, and the clear-text
  price of the convenience
- [**Output, downloads, and exit codes**](output-downloads-and-exit-codes.md) —
  asking for part of a reply, the
  piped-download trap, and the
  measured meaning of exits 0–5
- [**Offline mode and the curl translation**](offline-and-curl.md) —
  the request printed unsent, and
  the same request in curl's
  language, run for real
- [**xh in scripts**](xh-in-scripts.md) —
  the five script habits, and an
  honest account of when curl is
  the right tool instead
- [**The neighbours**](the-neighbours.md) —
  curl, HTTPie itself, jq as the
  usual partner, and the rest of
  the bench
- [**Limits**](limits.md) —
  the rendering, the deciding
  defaults, sessions as a notebook
  rather than a vault
- [**Troubleshooting**](troubleshooting.md) —
  symptom, cause, and fix for the
  ways an xh call usually goes
  wrong
- [**Glossary**](glossary.md)
- [**Writing criteria**](criteria.md) —
  the nine-point standard every
  guide in this series is written
  to, and this guide's verification
  notes
