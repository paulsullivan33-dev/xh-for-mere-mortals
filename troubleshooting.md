# Troubleshooting

Outcome: faced with the ways an xh
call usually goes wrong, you can
match the symptom to its cause and
its fix — most of them in one line,
because most of them are this
guide's own lessons arriving from
the other side.

| Symptom | Cause | Fix |
|---|---|---|
| A GET turned into a POST | stdin was redirected, so xh took it as a body (t12) | name the method, and add `--ignore-stdin` |
| `Request body (from stdin) and request data (key=value) cannot be mixed` | items and a stdin body at once | `--ignore-stdin`, or drop the items and let the pipe be the body |
| xh sits silent before sending | stdin is a stream that never closes; xh reads it to the end first | close it, redirect `</dev/null`, or `--ignore-stdin` |
| Exit 4 (or 3, 5) although a reply printed | the status check is on by default in 0.25.3 (t07) | read the code as the verdict, or `--no-check-status` to opt out |
| `xh: warning: HTTP 404 Not Found` but the output looks complete | the warning is real but separate: it goes to stderr, the body to stdout | nothing to fix — unless the exit code surprises a script; see the row above |
| A download left no file | in a pipe, `--download` writes the body to stdout (t08) | `--download --output <file>` |
| Headers print in a different order than the server sent; JSON spacing differs | the terminal view sorts and re-indents (t07) | pipe it, or `--pretty=none`, for the bytes as sent |
| Numbers arrived as strings at the server | `=` makes strings — or `--form`, where everything is a string (t02, t04) | `:=` for JSON values; JSON mode for typed fields |
| A field meant as a query went in the body | `=` items are body fields, even on GET | `==` for query parameters |
| An array arrived as separate last-one-wins fields | the `[]` suffix was left off | `key[]=a key[]=b` |
| The server got a file's text when it wanted the file | `=@` reads a file *into a value*; `@` after the key uploads it | `key=@file` for text, `key@file` for an upload |
| `Connection refused (os error 111)`, exit 1 | nothing listens at that address and port (t13) | read the error chain from the bottom; check the server is up and the port is right |
| A session did not apply | sessions are per host and port, and named — a different port is a different folder | check the name, and that the URL's host and port match the session's |
| A session did not learn a new header | it was opened `--session-read-only` (t06) | that is the flag working; repeat the call with plain `--session` to save |

## A word on reading xh's errors

Two of the symptoms above arrive
as xh's own error text, and both
reward reading closely. The
mixed-body error names its remedy
inside itself. The connection
error is a chain — each line a
layer further from the cause — and
reads best from the bottom up:
`Connection refused` is the fact;
the lines above are the route xh
took to reach it. When an error
is neither of those shapes, the
three inspection flags of chapter
10 are the next step: `--offline`
for what *would* be sent,
`--verbose` for what *was* sent
beside what returned, and `--curl`
for the same request in the
notation where nothing is left
implicit.

Check: pick any row and say the
fix without the table — and say
which transcript in the lab shows
the symptom being real.
