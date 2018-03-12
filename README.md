[![Discord](https://img.shields.io/badge/Discord-Join-blue.svg)](https://discord.gg/gAvufS2)

# A Linux to Windows-x64 cross-compile helper script

_python_cross_compile_script_ is written in Python primarily for Linux.

It's main purpose is to simplify the cross compiling of various multi-OS programs (e.g mpv).

It comes with a relatively large preset of packages but can be easily expanded upon.

Currently it's mainly focusing on Media programs, e.g mpv and ffmpeg.

The packages are split into depends and products, products being things like 'mpv' and dependencies (their needed libraries, e.g 'libx264').

See `./cross_compiler.py list -p` and `./cross_compiler.py list -d` for a full list of packages.

---

## **Install**

Download the python file:

`wget 'https://github.com/DeadSix27/python_cross_compile_script/blob/master/cross_compiler.py' && chmod u+x cross_compiler.py`

and run it.

_Git-cloning this repo is not recommended nor needed, unless you want to submit patches or help working on the project._

## **Usage**

Simple usage: `./cross_compiler.py -p <product>` (e.g x264)

For more see: `./cross_compiler.py --help`

## **System requirements:**

* Python 3+ (Tested only on 3.6.4)
  * Required python packages: requests, progressbar2
* Linux (Tested only on ArchLinux)
* 20+GB is recommended, but sizes vary depending on the packages.
* Windows Vista 64-Bit or newer for the resulting binaries. (32-bit and Windows XP are not supported)

## **Package requirements (no auto-check yet)**
```
Packages required, tested on:

(This list is possibly incomplete and differs from OS to OS)

global      - texinfo yasm git make automake gcc gcc-c++ pax cvs svn flex bison patch libtoolize nasm hg cmake gettext-autopoint
mkvtoolnix  - libxslt docbook-util rake docbook-style-xsl
gnutls      - gperf
angle       - gyp
vapoursynth - p7zip
flac,expat  - docbook-to-man / docbook2x
youtube-dl  - pando
x264        - nasm 2.13
```

### Thanks to these people for some patches and hints:

- [mxe](https://github.com/mxe/mxe)
- [rdp](https://github.com/rdp/ffmpeg-windows-build-helpers)
- [ArchLinux](https://aur.archlinux.org/packages/)
- [MSYS](https://github.com/Alexpux/MSYS2-packages/)
- [Martchus](https://github.com/Martchus/PKGBUILDs/commits/master)
- [Alexpux](https://github.com/Alexpux/MINGW-packages)
- [shinchiro](https://github.com/shinchiro/mpv-winbuild-cmake)
- and many more..
