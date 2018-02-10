# `wotw-x11-comparison`

[![Build Status](https://travis-ci.org/wizardsoftheweb/wotw-x11-comparison.svg?branch=master)](https://travis-ci.org/wizardsoftheweb/wotw-x11-comparison) [![Coverage Status](https://coveralls.io/repos/github/wizardsoftheweb/wotw-x11-comparison/badge.svg?branch=master)](https://coveralls.io/github/wizardsoftheweb/wotw-x11-comparison?branch=master)

This repo holds a few X11 experiments (or will shortly) comparing `XCB` and `Xlib`. I'm really interested in building some automation tools for X11, but I have to get a handle on how the system works first.

## Libraries

I built this with Fedora 27. I'd eventually like to throw together some expanded RPM-centric instructions and make this work in the Debian world, but that's really far out.

### `Xlib`

You'll first need X11. You can generally find it via `libX11`. For active development, some of the protocol headers are very, very useful.

```shell-session
$ sudo dnf install -y 'libX11*'{,-devel}
$ sudo dnf install -y xorg-x11-proto-devel
```

X11 also has a ton of hardware-specific packages, which makes simple, catchall (and overkill) installations like this hard:

```shell-session
$ sudo dnf install --skip-broken 'xorg-x11-*'{,-devel}
```

If you'll notice, I left out `-y`; that will install a ton of cruft you might not need.

I spent a considerable amount of time looking around for a solid and dependable Python port. There are some great repos out there, but, like `Xlib`, they're opinionated, outdated, and not feature-complete. Rather than try to grok someone else's spin on `Xlib`, I just rolled my own via `ctypes`. To be fair, I have no idea what I'm doing, which is probably why I couldn't understand the other Python `Xlib` libraries.

### `XCB`

You'll first need `XCB`. You can generally find it via `libxcb`. There's a good chance there are also some ancillary packages you might need. On Fedora, you can get everything with something like this:

```shell-session
$ sudo dnf install -y {libxcb,'xcb-util-*'}{,-devel}
```

The [official Python project, `xpyb`](https://pypi.python.org/pypi/xpyb/1.3.1), is a nightmare to install, doesn't work with Python 3, and doesn't seem to be under active development. Instead I went with [`xcffib`, a `cffi` port](https://github.com/tych0/xcffib) that works insanely well. I replaced `xpyb` in a few minutes without any failed tests.
