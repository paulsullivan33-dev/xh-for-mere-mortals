# Glossary

Short definitions, in the guide's
own words, for the terms the
chapters use. Cross-references
point at the chapter that uses the
term most.

**API** — a service's published way
for programs to talk to it,
usually over HTTP (chapter 1).

**base64** — an encoding that
carries arbitrary text safely
inside a header. Reversible by
anyone; not encryption (chapter 7).

**bearer token** — a secret string
presented as-is in an
`Authorization: Bearer` header;
whoever holds it is trusted
(chapter 7).

**body** — the part of a request or
reply after the headers: the actual
data being sent or returned
(chapter 5).

**Content-Type** — the header that
says what kind of data a body is —
`application/json`, a form, and so
on (chapters 5–6).

**exit code** — the number a
program leaves behind for the
script or shell that ran it
(chapter 9).

**form data** — body packing as
name–value pairs in one line
(`name=hammer&count=3`), the way
web forms have always sent them
(chapter 6).

**header** — one labelled line of a
request or reply carrying
information *about* it, rather than
its body (chapter 3).

**HTTP** — the request-and-reply
language of the web; HTTPS is the
same language inside an encrypted
connection (chapter 1).

**HTTPie** — the friendly HTTP
client whose command language xh
reimplements (chapters 1, 12).

**item** — one key–separator–value
piece on xh's command line; the
separator says what the piece is
(chapter 4).

**JSON** — a text format for
structured data — objects, arrays,
strings, numbers, booleans, null —
that most modern APIs speak
(chapter 4).

**method** — the verb that opens a
request: GET, POST, PUT, PATCH,
DELETE, and others (chapter 5).

**multipart** — a body packing of
labelled parts separated by a
boundary string; the packing that
can carry whole files (chapter 6).

**query parameter** — a name–value
pair carried in the URL itself,
after the `?`, visible to every
hop on the way (chapter 4).

**redirect** — a reply (status
3xx) that points at another URL
instead of answering (chapter 9).

**request / response** — the
question a client sends and the
reply a server returns; one pair
makes one HTTP exchange
(chapter 1).

**session** — xh's named, saved
bundle of authentication, headers,
and cookies for one host
(chapter 8).

**SHA-256** — a fingerprint
function: the same bytes always
produce the same fingerprint, so
two matching fingerprints mean two
matching files (chapter 6).

**standard input (stdin)** — the
stream a program reads when it is
not reading a file or the keyboard;
in xh, a redirected stdin is a
request body (chapters 3, 5).

**status code** — the three-digit
verdict opening a reply: 2xx
success, 3xx redirect, 4xx the
request's fault, 5xx the server's
(chapter 9).

**User-Agent** — the header in
which a client names itself to the
server; xh sends `xh/0.25.3`
(chapter 3).
