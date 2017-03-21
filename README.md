# A (somewhat) Modular cross-compile helper

#### Written almost entirely in Python (3.6)


Project was very influenced by https://github.com/rdp/ffmpeg-windows-build-helpers

Basically does the same thing, just in a pythonic way with a JSON-like program/depency system.

As of now it works, however it has no programs defined, later on the defaults will be ffmpeg and mpv.

Required-packages are also not implemented yet, I highly discourage using this unless you know what you're doing.

However later on, in theory all a user has to touch is said JSON-like configuration which can be..

..easy as:

```python
'libwebp' : {
    'repo_type' : 'archive',
    'url' : 'http://downloads.webmproject.org/releases/webp/libwebp-0.6.0.tar.gz',
    'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
    'make_options': '{make_prefix_options}',
},
```
or as advanced as:
```python
'flite' : {
	'repo_type' : 'archive',
	'url' : 'http://www.speech.cs.cmu.edu/flite/packed/flite-1.4/flite-1.4-release.tar.bz2',
	'patches' : ( # ordered list of patches, first one will be applied first..
		('https://raw.githubusercontent.com/rdp/ffmpeg-windows-build-helpers/master/patches/flite_64.diff', "p0"),
	),
	'cpu_count' : '1', #why do I even have to implement this, fix your stuff flite group.
	'needs_make_install' : False,
	'run_post_patch': (
		'sed -i.bak "s|i386-mingw32-|{cross_prefix}|" configure',
	),
	"run_post_make": (
		'mkdir -pv "{compile_prefix}/include/flite"',
		'cp -v include/* "{compile_prefix}/include/flite"',
		'cp -v ./build/{bit_namne}-mingw32/lib/*.a "{compile_prefix}/lib"',
	),
	'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
	'make_options': '{make_prefix_options}',
},
```
# Configuration options:

```python
_MINGW_SCRIPT_URL = "https://raw.githubusercontent.com/DeadSix27/modular_cross_compile_script/master/mingw-build-script.sh" #mingw script, keep the default one, unless you know what you're doing
_LOGFORMAT = '[%(asctime)s][%(levelname)s] %(message)s' + Colors.RESET
_LOG_DATEFORMAT = '%H:%M:%S'
_QUIET = False #not recommended, but sure looks nice...
_WORKDIR = "workdir"
_MINGW_DIR = "xcompilers"
_BITNESS = ( 64, ) # as of now only 64 is tested, 32 could work, for multi-bit write it like (64, 32)
_DOWNLOADER = "wget" # wget or curl
_ORIG_CFLAGS = "-march=skylake -O3" # If you compile for AMD Ryzen and Skylake or newer system use: znver1, or skylake, if older use sandybridge or ivybridge or so, see: https://gcc.gnu.org/onlinedocs/gcc-6.3.0/gcc/x86-Options.html#x86-Options
```

# System requirements:

* Python 3 (tested on Python 3.5.2)
* GNU/Linux (tested on Ubuntu 16.10)
* Patience
