[![Discord](https://img.shields.io/badge/Discord-Join-blue.svg)](https://discord.gg/gAvufS2)

# Linux to Windows x64 cross-compile helper script

This script automatically builds toolchain and target library/program without much user interaction.

See `./cross_compiler.py list -p` and `./cross_compiler.py list -d` for a full list of packages.

Support: If you need a VPN, maybe try https://www.azirevpn.com/ref/1OxiItOD6E? (Referral Link will help me)

---

# Notes:

- ##### If you have issues with any of the generated binaries, e.g *mpv-player* or *ffmpeg*, please report those issues here, not on their tracker.


## **Install**

Clone the repository:

```bash
git clone "https://github.com/DeadSix27/python_cross_compile_script.git"
chmod u+x python_cross_compile_script/cross_compiler.py
```

## **Usage**

Simple usage: `./cross_compiler.py -p <product>` (e.g mpv)

For more see: `./cross_compiler.py --help`

## **System requirements:**

* Python 3.6+
  * Required python packages: requests, progressbar2
* GNU/Linux (Tested on ArchLinux & Ubuntu 17+)
* 20+GB is recommended, but sizes vary depending on the packages
* Resulting binaries support Win7 and newer, 64bit only

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

### Thanks to:

- [mxe](https://github.com/mxe/mxe)
- [rdp](https://github.com/rdp/ffmpeg-windows-build-helpers)
- [ArchLinux](https://aur.archlinux.org/packages/)
- [MSYS](https://github.com/Alexpux/MSYS2-packages/)
- [Martchus](https://github.com/Martchus/PKGBUILDs/commits/master)
- [Alexpux](https://github.com/Alexpux/MINGW-packages)
- [shinchiro](https://github.com/shinchiro/mpv-winbuild-cmake)
- and more
