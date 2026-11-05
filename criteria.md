# Writing criteria for this guide

Every "for Mere Mortals" guide is written to the same nine-point
standard, so a reader who trusts one can trust the rest. Here it
is, with the verification notes for this particular guide below.

1. **Fix it first.** Reader outcomes lead, not action items: each
   chapter opens by naming the outcome it delivers, shows a check
   the reader can run to confirm they got it, and a reasonable
   reader finishes able to state what was done, what it means,
   and what to try next.
2. **Plain language.** Short sentences, everyday vocabulary,
   technical terms defined on first use. No slang, and no
   idioms that only make sense in one country — the reader may
   be translating as they go.
3. **No dead ends.** A guide never tells the reader to do
   something it cannot show them how to verify. Every claim a
   reader relies on — an install, a command, an output — is
   something this guide demonstrates or clearly labels
   documented-only below.
4. **Live-verified where it matters.** Procedures are run for
   real in the guide's lab wherever the build machine allows it,
   and the transcripts kept in the repository are the evidence.
   What could not be run is listed honestly below, never
   presented as if it had been.
5. **General audiences.** Nothing in this guide — examples,
   fixtures, names, addresses — is modelled on any particular
   reader or author's real life, network, or organisations.
   The lab's traffic is the lab talking to itself.
6. **Standalone.** A reader needs this guide, its lab, and
   nothing else. Where another guide would genuinely help, it
   is pointed to once, by name, and the chapter still completes
   without it.
7. **Honest about limits.** Chapter 13 names what the tool
   cannot do: a friendly view that re-indents bodies and
   re-sorts headers, so the picture is never the bytes; method
   and body defaults that decide silently (items imply POST,
   redirected stdin implies a body, redirects are not followed,
   the status check is on); session files that store passwords
   in clear text; basic authentication that is an encoding,
   not protection; and a client that is one request at a time,
   with no scripting of pages, no load machinery, and no
   state beyond the sessions it is handed.
8. **The one rule is in the text, early.** Chapter 1 and the
   README state the rule plainly — *the reply you are shown is
   a rendering; the request xh sent is the ground truth* —
   before any procedure depends on it, and later chapters point
   back to it where the rendering could be mistaken for the
   thing itself: re-indented JSON trusted as the server's own
   spacing, sorted headers argued from as wire order, a method
   inferred where the reader believed they had chosen.
9. **Builds clean.** The site builds with MkDocs in strict mode
   with no warnings, and a fresh reader following the chapters
   in order reaches the stated outcome of each.

## Verification notes for this guide

The build machine is an Ubuntu 24.04 sandbox. xh **0.25.3** was
the project's official release binary for Linux
(`xh-v0.25.3-x86_64-unknown-linux-musl.tar.gz` from the
ducaale/xh GitHub releases), run from a scratch folder rather
than installed system-wide; two symlinks to the same file,
named `xhs` and `https`, provided the HTTPS-by-default variant.
Companions: curl 8.5.0, Python 3.12.3, and jq (used in the
transcripts to project the fixture's reports to the fields
under discussion).

The fixture is the lab's own: `xh-lab/echo_server.py`, a
standard-library Python server on 127.0.0.1 port 18092 that
answers every request with a JSON report of what arrived —
method, path, raw and parsed query, headers in received order,
and the body parsed as JSON, as a form, or as multipart parts
with per-part SHA-256 fingerprints — with special paths for a
one-line JSON body, chosen status codes, a redirect, and a
file download, and a request log (`server-requests.log`) used
to prove a negative for offline mode. Fixtures
(`xh-lab/fixtures/`): a one-line stock label, the same note as
JSON, and a three-row stock CSV. Two helpers are in `xh-lab/`:
`render.sh` (strips escape codes so terminal output can be
printed) and `pty-run.sh` (runs a command under a real terminal
via `script(1)`). Every run was made with `XDG_CONFIG_HOME`
pointed at a folder inside the lab, so the session file lands
where chapter 8 can show it and the machine's real
configuration was never touched. All transcripts live in
`xh-lab/transcripts/`, numbered t00–t13.

Run for real, with transcripts as evidence:

- Version and the head of `--help`; the fixture answering curl
  before xh is pointed at it (t00). The `xhs` HTTPS default,
  proved by the two `--curl` translations printing `http://`
  and `https://` for the same address (t00, t09).
- The first look, both ways: on a real terminal, status line,
  headers, and a four-space re-indent of a body the server sent
  at two spaces; the colour codes read out of the escapes
  (blue status, cyan names) (t01).
- The stdin trap, measured: the same command on a terminal is
  a GET; with stdin redirected it is a POST with an empty JSON
  body; an explicit GET still gains a JSON Content-Type, a
  Content-Length of 0, and a JSON Accept. Items plus stdin —
  even empty stdin — refused with the error quoted in chapter
  5. The lab's first call also sat waiting on an stdin that
  never closed (t01, t12).
- The whole item grammar in single requests, reported by the
  server: header, query, string and raw JSON fields, booleans
  and null, array elements, nested objects, a text file as a
  string value (trailing newline included), a JSON file as a
  parsed value, a backslash-escaped separator inside a key,
  query values URL-encoded (t02).
- Method inference and its trap: items with no method arrive
  as POST; an explicit GET keeps `=` items as a JSON body and
  does not move them to the query (t02). PUT, PATCH, DELETE; a
  `--raw` body delivered verbatim; a piped body delivered as
  JSON, and as form pairs under `--form` (t03).
- Forms and uploads: `--form` packing with all values strings;
  a multipart upload whose part fingerprint equals the source
  file's SHA-256 at both ends; a file field under plain
  `--form` promoting the request to multipart by itself, hash
  matching again; a `;type=` part content type (t04). First
  runs disagreed — the fixture's multipart parser was trimming
  framing bytes; it was fixed and the checks re-run, which is
  why the transcripts show the corrected numbers.
- Authentication: basic auth's header decoded back to the
  password with `base64 -d`; bearer auth's header verbatim; no
  auth, no header (t05).
- Sessions: a session taught by one call replaying its auth
  and header on the next; the session file found on disk and
  read whole, `raw_auth` in clear text; `--session-read-only`
  sending a one-off header that the following session call
  provably does not carry (t06).
- Output control: `--headers`, `--body`, `--quiet`; a one-line
  body passing through a pipe unchanged and reformatted under
  `--pretty=format`; `json.indent:2` honoured; response
  headers in the server's order in a pipe (three runs) and
  sorted on a terminal (two runs) (t07).
- Exit codes, measured under the default status check: 200 →
  0, unfollowed 302 → 3, 404 → 4 with its stderr warning,
  500 → 5; `--no-check-status` returning the same 404 to 0
  (t07). A connection refused: exit 1 and the full error chain
  (t13).
- Downloads: on a terminal, saved under the server's suggested
  name with a progress bar and the file read back; in a pipe,
  `--download` alone writing the body to stdout and no file
  appearing; `--download --output` naming the file (t08).
- The `--curl` translation of a request with a header, basic
  auth, and array items, then the printed command saved and
  run: the server reported the identical authorization, header,
  and body as the xh original (t09).
- `--offline` printing a full request while the server's log
  line count stood still at 51; `--verbose` printing the same
  request ahead of the live reply (t10). Redirects: the 302
  itself as the default answer, `--follow` landing on the
  target, `--all` showing both replies (t11).

Documented only — described from the project's documentation
or `--help` text, not run, and the text does not claim
otherwise:

- The package installation routes (distribution packages,
  cargo, Homebrew, Scoop, winget): the lab ran the release
  binary, and the project documents the wrappings.
- The password prompt (`--auth user` with no password): an
  interactive prompt leaves no transcript to verify.
- Digest authentication: the fixture cannot issue a digest
  challenge, so no exchange could be captured.
- Cookie persistence in sessions: the session file's
  `cookies` list is real and was empty; the fixture never sets
  a cookie, so replay was not exercised.
- `--continue` resuming a download: the fixture serves its
  small file whole or not at all; there was no interrupted
  transfer to resume.
- `--curl-long`: the lab ran the short-form translation.
- Deeper item nesting than chapter 4 shows (arrays of objects):
  the grammar composes the proved pieces, but the lab did not
  send them.
- The neighbouring tools in chapter 12 are characterised, not
  benchmarked; in particular the HTTPie comparison follows the
  projects' own documentation, the lab having run xh only.

Fixtures are this guide's own and deliberately generic: a
workshop stock bench — a claw hammer, a tape measure, wall
plugs, shelf numbers — and invented credentials (`bench:tape`)
that protect nothing. No example is modelled on any real
person, network, service or organisation.
