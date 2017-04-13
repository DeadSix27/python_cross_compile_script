# A GNU/Linux to Windows cross-compile helper script
## _almost_ fully written in Python 3

_python_cross_compile_script_ could be described as a wrapper for various build-helpers (Autotools,C-Make,Rake,..).
Products and dependencies are written in JSON and thus very easy to host remotely or modify quickly.
It comes with a CLI to compile specific lists of "products/dependencies" or a single one.
This project was heavily influenced by rdp's [ffmpeg-windows-build-helpers](https://github.com/rdp/ffmpeg-windows-build-helpers).


Menu:
[->How to use it<-](#usage)
[->How to configure it<-](#package-requirements-no-auto-check-yet)
[->What it requires<-](#system-requirements)

### **Currently this script builds these products from git-master**
- Aria2 
- cURL
- FFmpeg (shared & static)
- FLAC
- LAME3 
- MediaInfo _(Only .exe)_
- mkvToolNix _(Static with QT5)_
- mpv Player _(with VapourSynth, Python and LuaJIT)_
- SoX tools _(sox,play,..)
- Vobis tools _(oggenc,ogginfo,..)_
- wGet
- x264 & x265 (10bit)

#### See [->VERSIONS.md<-](VERSIONS.md) for a full list of dependencies, products and their respective versions

GCC Version is 6.3.0 and has mutex support.

---

## **System requirements:**

* Python3 (tested on Python 3.5.2)
* GNU/Linux (Tested on Ubuntu 16.10 (x86_64) and Fedora 25 (x86_64))
* Works fine in a VM, haven't tested using Win10's bash thing.
* For all products & dependencies at least 20GB of free space needed (SSD recommended)

## **Package requirements (no auto-check yet)**
```
Packages required, tested on:

(This list is possibly incomplete and differs from OS to OS)

Fedora 25    (Twenty Five)
Ubuntu 16.10 (Yakkety)

global      - texinfo yasm git make automake gcc gcc-c++ pax cvs svn flex bison patch libtoolize nasm hg cmake gettext-autopoint
mkvtoolnix  - libxslt docbook-util rake docbook-style-xsl
gnutls      - gperf
angle       - gyp
vapoursynth - p7zip
```

## **Usage**

### **The CLI mode**:

`cross_compiler.py -q -a` (Quiet CLI)

_**But wait, there is more!**_ Too much to explain here; to see the full help, type: `cross_compiler.py --help`

### **The simple, *"just build it all mode"***:
```
wget --content-disposition "https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/cross_compiler.py"
chmod u+x cross_compiler.py && ./cross_compiler.py
```

**Note:** This will build every product and it's dependencies as defined in `PRODUCT_ORDER`.
You can just remove or re-order products in it as you like.

## Configuration options:

General configs:

```python
_CPU_COUNT         = cpu_count() # the default automaticlaly sets it to your core-count but you can set it manually too # default: cpu_count()
_QUIET             = False # This is only for the 'just build it all mode', in CLI you should use "-q" # default: false 
_LOG_DATEFORMAT    = '%H:%M:%S' default: %H:%M:%S
_LOGFORMAT         = '[%(asctime)s][%(levelname)s] %(message)s' default: [%(asctime)s][%(levelname)s] %(message)s
_WORKDIR           = 'workdir' # default: workdir
_MINGW_DIR         = 'xcompilers' # default: xcompilers
_BITNESS           = ( 64, ) # as of now only 64 is tested, 32 could work, for multi-bit write it like (64, 32), this is completely untested .
_ORIG_CFLAGS       = '-march=nehalem -O3' # If you compile for AMD Ryzen and Skylake or newer system use: znver1, or skylake, if older use sandybridge or ivybridge or so, see: https://gcc.gnu.org/onlinedocs/gcc-6.3.0/gcc/x86-Options.html#x86-Options #default: -march=nehalem -O3
```

___


## Adding your own programs:

#### A simple make project can look like this:

```python
'foobar' : {
	'repo_type' : 'git',
	'url' : 'https://github.com/foo/bar.git',
	'configure_options': '--enable-foobar --prefix={product_prefix}/bar.installed',
},
```

However many more settings and variables are available, see this list of variables:

To the right is their value.

```python
cmake_prefix_options         # -G"Unix Makefiles" . -DENABLE_STATIC_RUNTIME=1 -DCMAKE_SYSTEM_NAME=Windows -DCMAKE_RANLIB={cross_prefix_full}ranlib -DCMAKE_C_COMPILER={cross_prefix_full}gcc -DCMAKE_CXX_COMPILER={cross_prefix_full}g++ -DCMAKE_RC_COMPILER={cross_prefix_full}windres -DCMAKE_INSTALL_PREFIX={compile_prefix}
make_prefix_options          # CC={cross_prefix_bare}gcc AR={cross_prefix_bare}ar PREFIX={compile_prefix} RANLIB={cross_prefix_bare}ranlib LD={cross_prefix_bare}ld STRIP={cross_prefix_bare}strip CXX={cross_prefix_bare}g++
pkg_config_path              # e.g workdir/xcompilers/mingw-w64-x86_64/x86_64-w64-mingw32/lib/pkgconfig
mingw_binpath                # e.g workdir/xcompilers/mingw-w64-x86_64/bin
cross_prefix_bare            # e.g x86_64-w64-mingw32-
cross_prefix_full            # e.g workdir/xcompilers/mingw-w64-x86_64/bin/x86_64-w64-mingw32-
compile_prefix               # e.g workdir/xcompilers/mingw-w64-x86_64/x86_64-w64-mingw32
compile_target               # e.g x86_64-w64-mingw32
bit_name                     # e.g x86_64
bit_name2                    # e.g x86/x86_64
bit_name3                    # e.g mingw64/mingw
bit_name_win                 # e.g win64/win32
bit_num                      # e.g 64
product_prefix               # x86_64_products
compile_pefix_sed_escaped    # compile_prefix with / escaped to \/
make_cpu_count               # -j 4
original_cflags              # value of _ORIG_CFLAGS
cflag_string                 # needed for x264/ffmpeg, produces a string like: "--extra-cflags=-march=skylake --extra-cflags=-O3"
```


and this information here:

`[FOPTIONAL]` means the setting can be set to False or completely removed.
All custom commands will be executed within the projects directory.
All commands,cflags,install/config/etc options can use the variables listed above.

You can always just check the predefined projects for ideas and wether I missed a setting here (please PR it to the README if you find one)

### Products and deps can have these options:

```python
'bar' : {
	'repo_type' : 'git',                          # ( Can be git, svn or archive )
	'url' : '[url]',                              # ( Must be a URL representing the above, e.g a git, svn or direct download link )
	'folder_name' : 'actualName'                  # ( Sometimes archives do not extract to the same dir as they're named, e.g test.zip won't be test, you can specify that here ) [FOPTIONAL]
	'rename_folder' : 'iLikeThisNameBetter',      # ( Renames the project folder to the specified string ) [FOPTIONAL]
	'make_subdir' : 'build',                      # ( If the build files are in a subfolder, e.g 'ProjectDir/build', specify it here and we will descend there beforehand ) [FOPTIONAL]
	'is_waf' : True,                              # ( Whether its a waf project, like mpv ) [FOPTIONAL]
	'is_cmake' : True,                            # ( Whether its a cmake project, often if not always requires 'needs_configure' to be false ) [FOPTIONAL]
	'env_exports' : {                             # ( Key/Value list of enviroment variables to be set during the build and removed after ) [FOPTIONAL]
		'DEST_OS' : 'win32',                      
	},
	'cflag_addition' : '-DFOOBAR',                # ( These will be appended to TARGET_CFLASG and reset after the build ) [FOPTIONAL]
	'custom_cflag' : '-O3',                       # ( This will completely overwrite TARGET_CLFAGS and be reset after the build ) [FOPTIONAL]
	'doBootStrap' : True,                         # ( Whether we should try to run a bootstrap script ) [FOPTIONAL]
	'run_pre_patch' : (                           # ( Commands to run before patches ) [FOPTIONAL]
		'cmd',
	),
	'patches' : (                                 # ( List of patches to run on the source before anything is being done, requires defining the type p1 or p0 ) [FOPTIONAL]
		('(url)', 'p1'),
	),
	'patches_post_configure' : (
		('(url)', 'p1'),                          # ( List of patches to run on the source agter configure ran, requires defining the type p1 or p0 ) [FOPTIONAL]
	),
	'run_post_patch' : (                          # ( List of commands to run before starting the build, will be executed inside the project folder ) [FOPTIONAL]
		'echo "foobar" > test.foobar',            
	), 
	'needs_configure' : False,                    # ( Whether it needs to run "configure"(incl. waf), cmake often doesn't. ) [FOPTIONAL]
	'configure_options': '--enable-static',       # ( Configure script options ) [FOPTIONAL]                                            
	'run_post_configure': (                       # ( List of commands to run after configure (only triggered when needs_configure is True) ) [FOPTIONAL]
		'cmd',
	),
	'cpu_count': '1',                             # ( If a project requires a specific cpu-count e.g 1 or it fails or so ) [FOPTIONAL]
	'needs_make' : True,                          # ( Whether it needs to run "make"(incl. waf), so far everything did. ) [FOPTIONAL]
	'make_options': 'CROSS={cross_prefix_bare}',  # ( Make options, things that get appended to the "make" command. ) [FOPTIONAL]
	'ignore_make_fail_and_run':(                  # ( Ignores failing make and runs a list of commands ) [FOPTIONAL]
		'cmd',
	),
	'run_post_make': (                            # ( List of commands to run after make (only triggered when needs_make is True) ) [FOPTIONAL]
		'cmd',
	),
	'needs_make_install' : True,                  # ( Whether it needs to run "make"(incl. waf), so far everything did. ) [FOPTIONAL]
	'install_options' : 'PREFIX=foobar',          # ( Make install options ) [FOPTIONAL]
	'install_target' : 'install-static',          # ( Will be called instead of "install" ) [FOPTIONAL]
	'run_after_install': (                        # ( List of commands to run after the build is installed (only triggered when needs_make_install is True) [FOPTIONAL]
		'echo "done" > project.done',             
	),
	'download_header' : {                         # ( List of c/h etc files to download into the include folder of our mingw install before starting the build. ) [FOPTIONAL]
		('(url)'),
	},
	'depends_on' : (                              # ( Things it depends on, e.g other configs like this ) [FOPTIONAL]
		'libfoobar',
	),
	'_already_built': True,                       # ( Set by system, but theoretically setting this to true will ALWAYS skip and NEVER build this project )
	'debug_exitafter': True,                      # ( True/False, will exit after this build, useful for testing ) [FOPTIONAL]
},
```