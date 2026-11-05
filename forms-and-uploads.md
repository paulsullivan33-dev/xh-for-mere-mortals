# Forms and uploads

Outcome: you can send the older
form style of body when a service
expects it, and upload a file in a
multipart request — and prove, by
checksum, that the file arrived
exactly as it left.

## When the body is a form

Before JSON, web forms sent their
fields as **form data**: pairs of
names and values in one line of
text, `name=hammer&count=3`, under
the content type
`application/x-www-form-urlencoded`.
Many services still expect exactly
that. xh speaks it with one flag:

```text
$ xh --ignore-stdin --form POST :18092/echo name=hammer count=3
{"content_type":"application/x-www-form-urlencoded","form":{"name":["hammer"],"count":["3"]}}
```

(transcript `xh-lab/transcripts/t04-forms-and-uploads.txt`;
the item syntax is unchanged — only
the packing differs.) Note what the
report shows: under `--form`, **every
value is a string**. The `count`
that chapter 4 sent as the number 3
with `:=` arrives here as `"3"`,
because form fields have no types —
a form cannot say "this is a
number". If the receiving service
cares, that is its business to
convert; yours is to know which
packing you used.

A body that already exists in form
shape can also arrive by pipe:
`printf 'name=hammer&count=3' | xh --form POST …`
delivered the same pairs (t03).

## Multipart: the packing that carries files

**Multipart** form data packs each
field as its own labelled part,
separated by a generated boundary
string, and that is what lets a
part be a whole file. Ask for it
with `--multipart` — or don't ask,
and see below. An upload item is
written `key@file` (chapter 4's
table): the `@` follows the key
with no `=` in between.

```text
$ xh --ignore-stdin --multipart POST :18092/echo kind=restock label@fixtures/label.txt
```

The fixture server takes each part
apart and reports its name, its
filename, and a **SHA-256** — a
fingerprint of the part's exact
bytes. The lab's check is the
strongest one in this guide:

```text
$ sha256sum fixtures/label.txt
128c42f6541337643f8d6d63288a5c1ac837232ffdf84827450dd4d511436f3c  fixtures/label.txt
(part as received) "sha256":"128c42f6541337643f8d6d63288a5c1ac837232ffdf84827450dd4d511436f3c","size":41
```

The fingerprints match. The file
that arrived is byte-for-byte the
file that left — all 41 bytes,
trailing newline included — and the
plain field beside it (`kind`)
arrived as an ordinary text part.
That is what "the upload worked"
means, proved rather than assumed.

Two more behaviours from the same
transcript:

- **A file field switches the
  packing by itself.** The second
  upload ran under plain `--form`,
  and xh promoted the request to
  multipart on its own, because a
  form-encoded body cannot carry a
  file. The CSV's fingerprint
  matched too.
- **A part's type can be set.** In
  the lab's runs an untyped file
  part carried no `Content-Type`
  header of its own — the receiving
  server decides what to make of
  that.
  `label@fixtures/label.txt;type=text/plain`
  set the part's `Content-Type`
  explicitly, and the report shows
  it. Quote that item: the shell
  reads `;` as a command separator
  otherwise.

One honesty note the lab owes: its
first multipart parser trimmed
bytes it should not have, and the
checksums *disagreed* until the
fixture was fixed — the lesson is
in the method, not the mishap.
When a transfer matters, fingerprint
both ends; agreement is the proof,
and disagreement is information.

Check: you can send a form body and
say why its numbers are strings,
upload a file beside a plain field,
and verify the upload the way the
lab did — same SHA-256 at both ends.
