# The item syntax

Outcome: you can build a request out
of small labelled pieces — headers,
query parameters, JSON fields of
every shape, and values read from
files — and predict exactly what
each piece becomes on the wire.

## One small grammar

After the method and the URL, every
further word on an xh command line
is a **request item**: a key, a
separator, and a value. The
separator is the whole language —
it says what the piece *is*:

| You type | It becomes | Example lands as |
|---|---|---|
| `key:value` | a header | `X-Workshop: North-Bench` sent |
| `key==value` | a query parameter | `?size=big` on the URL |
| `key=value` | a JSON string field | `"name": "hammer"` |
| `key:=value` | a JSON value, raw | `"count": 3`, `"gift": true` |
| `key[]=value` | one element of a JSON array | `"tags": ["red", "heavy"]` |
| `key[sub]=value` | a field of a nested object | `"dims": {"unit": "cm"}` |
| `key=@file` | a string field, the file's text | trailing newline included |
| `key:=@file` | a JSON value, the file parsed | an object, not a string |
| `key@file` | a file upload (multipart) | chapter 6 |

Every row of that table is one the
lab sent and the fixture server
reported back (transcript
`xh-lab/transcripts/t02-item-syntax.txt`).
One request carried nearly all of
them at once:

```text
$ xh --ignore-stdin POST :18092/echo X-Workshop:North-Bench size==big name=hammer count:=3 gift:=true note:=null tags[]=red tags[]=heavy dims[width]:=30 dims[unit]=cm
```

and the server reported the query as
`{"size": ["big"]}`, the header
present, and this body:

```json
{
  "name": "hammer",
  "count": 3,
  "gift": true,
  "note": null,
  "tags": ["red", "heavy"],
  "dims": {"width": 30, "unit": "cm"}
}
```

Two habits are visible already.
`:18092/echo` is xh's shorthand for
`http://127.0.0.1:18092/echo` — a
leading colon and a port means
"this machine". And the items are
quoted nowhere in that command
because none of them contains a
space or a shell special character;
when one does, quote it
(`'kind==wall plugs'` — the server
received `kind=wall+plugs`, the
encoding done for you).

## Strings, and values that are not strings

The `=` separator always makes a
**string**, even when the value
looks like a number: `count=3`
sends `"count": "3"`. The `:=`
separator takes the value as
**JSON, exactly as typed**: `3`
arrives as the number 3, `true` as
the boolean, `null` as null — and a
word like `count:=three` would be
sent as invalid JSON, which most
servers will refuse; if you mean
the word, `=` is the separator you
want. This is the distinction the
whole grammar turns on, and the one
worth practising until it is
automatic.

## Structure: arrays and nests

Repeat `tags[]=` to grow an array —
the order you type is the order
that arrives. Write `dims[width]:=`
to build inside an object, and mix
the two (`dims[unit]=cm` sits
beside `dims[width]:=30` in the
same object in the proof above).
Each deeper level is one more
bracket pair. The lab did not test
arrays of objects or deeper nests;
the grammar composes the pieces
shown, and anything you build
beyond them deserves a look at what
the server reports — which is the
one rule again.

## Values from files, and keys with separators in them

`label=@fixtures/label.txt` read
the lab's one-line stock label into
a string field — **trailing newline
and all**, which the server's
report shows as the `\n` at the end
of the value. `meta:=@fixtures/raw-note.json`
read a JSON file and landed it as a
real object. The `@` forms answer
"the value is in a file"; whether
the file's text stays text or is
parsed is the `=`/`:=` distinction
as usual.

A key that itself contains a
separator character is written with
a backslash: `'weird\=key=plain'`
sent the key `weird=key` (t02). The
backslash escapes the first `=`, so
xh splits on the second.

## The trap this grammar sets

Items decide the method when you do
not. A request with data items and
no method is a **POST** (t02) —
sensible, and worth knowing before
it surprises you. What it does *not*
do: an explicit GET does not move
`=` items into the query string
where a reader might expect them.
`xh GET … q=hammer` sent a GET
*with a JSON body* of
`{"q": "hammer"}` — legal, unusual,
and almost never what was meant.
Query parameters have their own
separator; use `==`.

Check: given a request to build —
a header, a query parameter, a
number, an array, a value from a
file — you can write the item for
each without looking back, and say
which separator makes a string and
which makes JSON.
