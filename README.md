[![Discord](https://img.shields.io/badge/Discord-Join-blue.svg)](https://discord.gg/gAvufS2)

# Linux to Windows x64 cross-compile helper script

This script automatically builds toolchain and target library/program without much user interaction.

See `./cross_compiler.py list -p` and `./cross_compiler.py list -d` for a full list of packages.

---

## **Install**

Download the python file:

```bash
git clone "https://github.com/DeadSix27/python_cross_compile_script.git"
chmod u+x python_cross_compile_script/cross_compiler.py
```

## **Usage**

Simple usage: `./cross_compiler.py -p <product>` (e.g x264)

For more see: `./cross_compiler.py --help`

## **System requirements:**

* Python 3.4+ (Tested only on 3.6.4)
  * Required python packages: requests, progressbar2
* Linux (Tested on ArchLinux & Ubuntu 17+)
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

### Thanks to these people:

- [mxe](https://github.com/mxe/mxe)
- [rdp](https://github.com/rdp/ffmpeg-windows-build-helpers)
- [ArchLinux](https://aur.archlinux.org/packages/)
- [MSYS](https://github.com/Alexpux/MSYS2-packages/)
- [Martchus](https://github.com/Martchus/PKGBUILDs/commits/master)
- [Alexpux](https://github.com/Alexpux/MINGW-packages)
- [shinchiro](https://github.com/shinchiro/mpv-winbuild-cmake)
- and many more..