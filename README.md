# A (somewhat) Modular cross-compile helper
#### written in Python 3

**This script as of now only is tested on Ubuntu 16.10.**
**It does NOT check for packages like `gperf` or `autogen` for you (or even `gcc` etc) you'll have to do that yourself.**
 (Automation will be added later for that).
 
Project was very influenced by https://github.com/rdp/ffmpeg-windows-build-helpers
Basically does the same thing, just in a pythonic way with a JSON-like program/depency system.

**Current main products (you can add your own) are: MPV, FFMPEG(Static,Shared GPL), WGET and CURL.**

**It successfully builds them (for me) you can test it and report issues and I'll happily fix them (if I can)!**

---


### A simple make project can look like this:

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
bit_name_win                 # e.g win64/win32
bit_num                      # e.g 64
product_prefix               # x86_64_products
compile_pefix_sed_escaped    # compile_prefix with / escaped to \/
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
	'url' : '[url]',                              # ( Must be a URL represending the above, e.g a git, svn or direct download link )
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
	'cpu_count': '1',                             # ( If a prroject requires a specific cpu-count e.g 1 or it fails or so ) [FOPTIONAL]
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
	'debug_exitafter': True,                      # ( True/False, will exit after this build, useful for testing ) [FOPTIONAL]
	'_already_built': True                        # ( Set by system, but theoretically setting this to true will ALWAYS skip and NEVER build this proejct )
},
```


# Configuration options:

```python
_CPU_COUNT = cpu_count() # cpu_count() automaticlaly sets it to your core-count but you can set it manually too
#_MINGW_SCRIPT_URL = "https://raw.githubusercontent.com/DeadSix27/modular_cross_compile_script/master/mingw-build-script.sh" #without mutex support, original, includes weak ref patch
_MINGW_SCRIPT_URL = "https://raw.githubusercontent.com/DeadSix27/modular_cross_compile_script/master/mingw-build-script-posix.sh" #modified for mutex support, includes weak ref patch, vapoursynth requires this, so just keep this.
_LOGFORMAT = '[%(asctime)s][%(levelname)s] %(message)s'
_LOG_DATEFORMAT = '%H:%M:%S'
_QUIET = False #not recommended, but sure looks nice...
_WORKDIR = "workdir"
_MINGW_DIR = "xcompilers"
_BITNESS = ( 64, ) # as of now only 64 is tested, 32 could work, for multi-bit write it like (64, 32)
_DOWNLOADER = "wget" # wget or curl, currently it just uses the internal downloader, so just ignore this
_ORIG_CFLAGS = "-march=skylake -O3" # If you compile for AMD Ryzen and Skylake or newer system use: znver1, or skylake, if older use sandybridge or ivybridge or so, see: https://gcc.gnu.org/onlinedocs/gcc-6.3.0/gcc/x86-Options.html#x86-Options
```

# System requirements:

* Python3 (tested on Python 3.5.2)
* GNU/Linux (tested on Ubuntu 16.10)
* wget, sed, diff
