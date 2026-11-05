# Installing xh

Outcome: xh is on your machine,
`xh --version` answers, and you know
about the second name the same
binary answers to — `xhs` — and what
changes when you use it.

## The route the lab took

The lab installed nothing
system-wide. It downloaded the
project's official release file for
Linux —

```text
xh-v0.25.3-x86_64-unknown-linux-musl.tar.gz
```

— from the **ducaale/xh** GitHub
releases page, untarred it into the
lab folder, and ran the `xh` binary
inside. That is the whole install:
one file. (The musl build is the
static one; it runs on a Linux
machine regardless of its C library.
A gnu build is published alongside
it.) Transcript
`xh-lab/transcripts/t00-environment.txt`
opens with the result:

```text
$ xh --version
xh 0.25.3
-native-tls +rustls
```

The second line is the build's
feature report — among other things
it names the TLS libraries this copy
can use. You do not need to act on
it; it is there so that a bug report
can say exactly which xh you have.

## The package routes

Most people will meet xh through a
package manager instead, and the
project's README lists the routes:
a distribution package on recent
Debian, Ubuntu, Fedora, and Arch;
`cargo install xh` where Rust's
toolchain is present; Homebrew on
macOS; Scoop and winget on Windows;
and more. **Those routes are
documented-only in this guide** —
the lab ran the release binary, and
`criteria.md` says so. Two cautions
apply whichever route you take:

- A distribution package may be
  older than the current release.
  This guide's claims are about
  **0.25.3**; if your `xh --version`
  says something much older, the
  details — especially defaults —
  may differ.
- Download binaries only from the
  project's own releases page. A
  tool that carries your passwords
  (chapter 7) is not one to fetch
  from a mirror of a mirror.

## One binary, three names

Inside the release archive sits one
program. The lab linked two more
names to it — `xhs` and `https` —
because **the name xh is started
under changes its default**. Started
as `xh`, a scheme-less address gets
`http://`. Started as `xhs` (or
`https`), the same address gets
`https://`. Nothing else changes:
same version, same flags. The lab
proves it without touching the
network, using the `--curl`
translation from chapter 10, which
prints the address xh would use
(t00, and chapter 10's transcript):

```text
$ xh --curl example.com/echo
curl http://example.com/echo
$ xhs --curl example.com/echo
curl https://example.com/echo
```

The point of the second name is the
server that only speaks HTTPS: with
`xhs` you can leave the scheme off
your own notes and scripts the same
way you do for plain HTTP locally.
Package installs create the `xhs`
name for you; with the release
binary, a symlink or a copy of the
file under the new name is all it
takes — the program reads its own
name when it starts.

Check: `xh --version` answers
`xh 0.25.3` (or a newer release you
chose knowingly), and
`xhs --curl example.com/echo`
prints an `https://` address.
