#!/usr/bin/env python3

# #################################################################################################################
# Copyright (C) 2017 DeadSix27
#
# This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# #################################################################################################################


import os.path,logging,re,subprocess,sys,shutil,urllib.request,urllib.parse,stat
import hashlib,glob,traceback,time,zlib
import http.cookiejar
from multiprocessing import cpu_count
from pathlib import Path
from urllib.parse import urlparse
from collections import OrderedDict
_VERSION = "1.4"


#CURRENTLY REQUIRED PROJECTS INCLUDE BUT A RE NOT LIMITED TO:
# autogen, gperf, build-essential, ....

class Colors: # improperly named ansi colors. :)
	GREEN  = '\033[1;32;40m'
	RESET  = '\033[0;37;40m'
	YELLOW = '\033[1;33;40m'
	BLUE   = '\033[1;34;40m'
	CYAN   = '\033[1;36;40m'
	RED    = '\033[1;31;40m'

class MissingDependency(Exception):
	__module__ = 'exceptions'
	def __init__(self, message):
		self.message = message

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


# ################################################################################

_DEBUG = True
git_get_latest = True # to be implemented in a better way

PRODUCT_ORDER = ('mpv', 'curl', 'wget', 'ffmpeg_shared', 'ffmpeg_static')

#INDEPENDENT_DEPS =

PRODUCTS = {
	'mpv' : {
		'repo_type' : 'git',
		'url' : 'https://github.com/mpv-player/mpv.git',
		'is_waf' : True,
		'env_exports' : {
			'DEST_OS' : 'win32',
			'TARGET'  : '{compile_target}',
		},
		'run_post_patch' : (
			'cp -nv "/usr/bin/pkg-config" "{cross_prefix_full}pkg-config"',#-n stands for --no-clobber, because --no-overwrite is too mainstream, also, yes we still need this odd work-around.
		),
		'configure_options': ' --enable-libmpv-shared --enable-sdl2 --disable-debug-build --prefix={product_prefix}/mpv_git.installed TARGET={compile_target} DEST_OS=win32',			
		'depends_on' : (
			'libffmpeg', 'luajit', 'vapoursynth',
		),
		'run_after_install': (
			'{cross_prefix_bare}strip -v {product_prefix}/mpv_git.installed/bin/mpv.exe',
			'{cross_prefix_bare}strip -v {product_prefix}/mpv_git.installed/lib/mpv-1.dll',
		)
	},
	'curl' : {
		'repo_type' : 'git',
		'url' : 'https://github.com/curl/curl',
		'rename_folder' : 'curl_git',
		'configure_options': '--with-gnutls --enable-static --disable-shared --with-winssl --target={bit_name2}-{bit_name_win}-gcc --host={compile_target} --build=x86_64-linux-gnu --prefix={product_prefix}/curl_git.installed --exec-prefix={product_prefix}/curl_git.installed',
		'depends_on': (
			'zlib',
		),
	},
	'wget' : {
		'repo_type' : 'git',
		'url' : 'https://git.savannah.gnu.org/git/wget.git',
		'rename_folder' : 'wget_git',
		'configure_options': '--with-ssl=gnutls --enable-nls --enable-dependency-tracking --with-metalink --target={bit_name2}-{bit_name_win}-gcc --host={compile_target} --build=x86_64-linux-gnu --prefix={product_prefix}/wget_git.installed --exec-prefix={product_prefix}/wget_git.installed',
		'cflag_addition' : '-DGNUTLS_INTERNAL_BUILD -DIN6_ARE_ADDR_EQUAL=IN6_ADDR_EQUAL',
		'patches' : (
			('https://raw.githubusercontent.com/DeadSix27/modular_cross_compile_script/master/patches/wget_1.19.1.18_strip_version.patch', 'p1'),
		),
		'depends_on': (
			'zlib', 'gnutls'
		),
	},
	'ffmpeg_static' : {
		'repo_type' : 'git',
		'url' : 'https://git.ffmpeg.org/ffmpeg.git',
		'rename_folder' : 'ffmpeg_static_git',
		'configure_options': 
			' --arch={bit_name2} --target-os=mingw32 --cross-prefix={cross_prefix_bare} --pkg-config=pkg-config --disable-w32threads --enable-libsoxr --enable-fontconfig --enable-libass --enable-libbluray --enable-iconv'
			' --enable-libtwolame --extra-cflags=-DLIBTWOLAME_STATIC --enable-libzvbi --enable-libcaca --enable-libmodplug --extra-libs=-lstdc++ --extra-libs=-lpng --enable-decklink --extra-libs=-loleaut32'
			' --enable-libmp3lame --enable-version3 --enable-zlib --enable-librtmp --enable-libvorbis --enable-libtheora --enable-libspeex --enable-libopenjpeg --enable-gnutls --enable-libgsm --enable-libfreetype'
			' --enable-libopus --enable-bzlib --enable-libopencore-amrnb --enable-libopencore-amrwb --enable-libvo-amrwbenc --enable-libschroedinger --enable-libvpx --enable-libilbc --enable-libwavpack --enable-libwebp'
			' --enable-dxva2 --enable-avisynth --enable-gray --enable-libopenh264 --enable-netcdf --enable-libflite --enable-lzma --enable-libsnappy --enable-libzimg --enable-gpl --enable-libx264 --enable-libx265'
			' --enable-frei0r --enable-filter=frei0r --enable-librubberband --enable-libvidstab --enable-libxavs --enable-libxvid --enable-libmfx --enable-avresample --extra-libs=-lpsapi --extra-libs=-lspeexdsp'
			' --prefix={product_prefix}/ffmpeg_static_git.installed --disable-shared --enable-static --enable-libgme --enable-runtime-cpudetect',
		'depends_on': (
			'zlib', 'bzlib2', 'liblzma', 'libzimg', 'libsnappy', 'libpng', 'gmp', 'libnettle', 'iconv', 'gnutls', 'frei0r', 'libsndfile', 'libbs2b', 'wavpack', 'libgme_game_music_emu', 'libwebp', 'flite', 'libgsm', 'sdl1', 'sdl2',
			'libopus', 'opencore-amr', 'vo-amrwbenc', 'libogg', 'libspeexdsp', 'ibspeex', 'libvorbis', 'libtheora', 'orc', 'libschroedinger', 'freetype', 'expat', 'libxml', 'libbluray', 'libxvid', 'xavs', 'libsoxr', # 'libebur128',
			'libx265', 'libopenh264', 'vamp_plugin', 'fftw3', 'libsamplerate', 'librubberband', 'liblame' ,'twolame', 'vidstab', 'netcdf', 'libcaca', 'libmodplug', 'zvbi', 'libvpx', 'libilbc', 'fontconfig', 'libfribidi', 'libass',
			'openjpeg', 'intel_quicksync_mfx', 'fdk_aac', 'rtmpdump', 'libx264', 
		),
	},
	'ffmpeg_shared' : {
		'repo_type' : 'git',
		'url' : 'https://git.ffmpeg.org/ffmpeg.git',
		'rename_folder' : 'ffmpeg_shared_git',
		'configure_options':
			' --arch={bit_name2} --target-os=mingw32 --cross-prefix={cross_prefix_bare} --pkg-config=pkg-config --disable-w32threads --enable-libsoxr --enable-fontconfig --enable-libass --enable-libbluray --enable-iconv'
			' --enable-libtwolame --extra-cflags=-DLIBTWOLAME_STATIC --enable-libzvbi --enable-libcaca --enable-libmodplug --extra-libs=-lstdc++ --extra-libs=-lpng --enable-decklink --extra-libs=-loleaut32'
			' --enable-libmp3lame --enable-version3 --enable-zlib --enable-librtmp --enable-libvorbis --enable-libtheora --enable-libspeex --enable-libopenjpeg --enable-gnutls --enable-libgsm --enable-libfreetype'
			' --enable-libopus --enable-bzlib --enable-libopencore-amrnb --enable-libopencore-amrwb --enable-libvo-amrwbenc --enable-libschroedinger --enable-libvpx --enable-libilbc --enable-libwavpack --enable-libwebp'
			' --enable-dxva2 --enable-avisynth --enable-gray --enable-libopenh264 --enable-netcdf --enable-libflite --enable-lzma --enable-libsnappy --enable-libzimg --enable-gpl --enable-libx264 --enable-libx265'
			' --enable-frei0r --enable-filter=frei0r --enable-librubberband --enable-libvidstab --enable-libxavs --enable-libxvid --enable-libmfx --enable-avresample --extra-libs=-lpsapi --extra-libs=-lspeexdsp'
			' --prefix={product_prefix}/ffmpeg_shared_git.installed --enable-shared --disable-static --disable-libgme --enable-runtime-cpudetect', #' --extra-cflags=-march=skylake'#' --extra-cflags=-O3' # dont seem needed		
		'depends_on': (
			'zlib', 'bzlib2', 'liblzma', 'libzimg', 'libsnappy', 'libpng', 'gmp', 'libnettle', 'iconv', 'gnutls', 'frei0r', 'libsndfile', 'libbs2b', 'wavpack', 'libgme_game_music_emu', 'libwebp', 'flite', 'libgsm', 'sdl1', 'sdl2',
			'libopus', 'opencore-amr', 'vo-amrwbenc', 'libogg', 'libspeexdsp', 'ibspeex', 'libvorbis', 'libtheora', 'orc', 'libschroedinger', 'freetype', 'expat', 'libxml', 'libbluray', 'libxvid', 'xavs', 'libsoxr', # 'libebur128',
			'libx265', 'libopenh264', 'vamp_plugin', 'fftw3', 'libsamplerate', 'librubberband', 'liblame' ,'twolame', 'vidstab', 'netcdf', 'libcaca', 'libmodplug', 'zvbi', 'libvpx', 'libilbc', 'fontconfig', 'libfribidi', 'libass',
			'openjpeg', 'intel_quicksync_mfx', 'fdk_aac', 'rtmpdump', 'libx264', 
		),
		'run_post_patch' : (
			'wget https://raw.githubusercontent.com/DeadSix27/modular_cross_compile_script/master/additional_headers/DeckLinkAPI.h -O {compile_prefix}/include/DeckLinkAPI.h',
			'wget https://raw.githubusercontent.com/DeadSix27/modular_cross_compile_script/master/additional_headers/DeckLinkAPI_i.c -O {compile_prefix}/include/DeckLinkAPI_i.c',
			'wget https://raw.githubusercontent.com/DeadSix27/modular_cross_compile_script/master/additional_headers/DeckLinkAPIVersion.h -O {compile_prefix}/include/DeckLinkAPIVersion.h',
		),
	}
	
}
DEPENDS = {
	'luajit': {
		'repo_type' : 'git',
		'url' : 'https://luajit.org/git/luajit-2.0.git',
		'needs_configure' : False,
		'custom_cflag' : '-O3', # doesn't like march's past ivybridge (yet), so we override it.
		'install_options' : 'CROSS={cross_prefix_bare} HOST_CC="gcc -m{bit_num}" TARGET_SYS=Windows BUILDMODE=static FILE_T=luajit.exe PREFIX={compile_prefix}',
		'make_options': 'CROSS={cross_prefix_bare} HOST_CC="gcc -m{bit_num}" TARGET_SYS=Windows BUILDMODE=static amalg',
	},
	'vapoursynth': {
		'repo_type' : 'git',
		'url' : 'https://github.com/vapoursynth/vapoursynth.git',
		'custom_cflag' : '-O3',
		'configure_options' : '--host={compile_target} --prefix={compile_prefix} --disable-shared --disable-vsscript --disable-python-module --enable-core',
		'patches' : (
			('https://raw.githubusercontent.com/DeadSix27/modular_cross_compile_script/master/patches/vapoursynth-0001-statically-link.patch', 'p1'),
		),
		#'download_header':(
		#	'https://raw.githubusercontent.com/meganz/mingw-std-threads/master/mingw.thread.h',
		#	'https://raw.githubusercontent.com/meganz/mingw-std-threads/master/mingw.mutex.h',
		#	'https://raw.githubusercontent.com/meganz/mingw-std-threads/master/mingw.condition_variable.h',
		#)
	},
	'libffmpeg' : { # static, as we use static on everything, my derp in the first place.
		'repo_type' : 'git',
		'url' : 'https://git.ffmpeg.org/ffmpeg.git',
		'rename_folder' : 'libffmpeg_git',
		'configure_options': 
			' --arch={bit_name2} --target-os=mingw32 --cross-prefix={cross_prefix_bare} --pkg-config=pkg-config --disable-w32threads --enable-libsoxr --enable-fontconfig --enable-libass --enable-libbluray --enable-iconv'
			' --enable-libtwolame --extra-cflags=-DLIBTWOLAME_STATIC --enable-libzvbi --enable-libcaca --enable-libmodplug --extra-libs=-lstdc++ --extra-libs=-lpng --enable-decklink --extra-libs=-loleaut32'
			' --enable-libmp3lame --enable-version3 --enable-zlib --enable-librtmp --enable-libvorbis --enable-libtheora --enable-libspeex --enable-libopenjpeg --enable-gnutls --enable-libgsm --enable-libfreetype'
			' --enable-libopus --enable-bzlib --enable-libopencore-amrnb --enable-libopencore-amrwb --enable-libvo-amrwbenc --enable-libschroedinger --enable-libvpx --enable-libilbc --enable-libwavpack --enable-libwebp'
			' --enable-dxva2 --enable-avisynth --enable-gray --enable-libopenh264 --enable-netcdf --enable-libflite --enable-lzma --enable-libsnappy --enable-libzimg --enable-gpl --enable-libx264 --enable-libx265'
			' --enable-frei0r --enable-filter=frei0r --enable-librubberband --enable-libvidstab --enable-libxavs --enable-libxvid --enable-libmfx --enable-avresample --extra-libs=-lpsapi --extra-libs=-lspeexdsp'
			' --prefix={compile_prefix} --disable-shared --enable-static --enable-libgme --enable-runtime-cpudetect'
		,
		'run_post_patch' : (
			'wget https://raw.githubusercontent.com/DeadSix27/modular_cross_compile_script/master/additional_headers/DeckLinkAPI.h -O {compile_prefix}/include/DeckLinkAPI.h',
			'wget https://raw.githubusercontent.com/DeadSix27/modular_cross_compile_script/master/additional_headers/DeckLinkAPI_i.c -O {compile_prefix}/include/DeckLinkAPI_i.c',
			'wget https://raw.githubusercontent.com/DeadSix27/modular_cross_compile_script/master/additional_headers/DeckLinkAPIVersion.h -O {compile_prefix}/include/DeckLinkAPIVersion.h',
		),
		'make_options': '',
		'depends_on': (
			'zlib', 'bzlib2', 'liblzma', 'libzimg', 'libsnappy', 'libpng', 'gmp', 'libnettle', 'iconv', 'gnutls', 'frei0r', 'libsndfile', 'libbs2b', 'wavpack', 'libgme_game_music_emu', 'libwebp', 'flite', 'libgsm', 'sdl1', 'sdl2',
			'libopus', 'opencore-amr', 'vo-amrwbenc', 'libogg', 'libspeexdsp', 'ibspeex', 'libvorbis', 'libtheora', 'orc', 'libschroedinger', 'freetype', 'expat', 'libxml', 'libbluray', 'libxvid', 'xavs', 'libsoxr', # 'libebur128',
			'libx265', 'libopenh264', 'vamp_plugin', 'fftw3', 'libsamplerate', 'librubberband', 'liblame' ,'twolame', 'vidstab', 'netcdf', 'libcaca', 'libmodplug', 'zvbi', 'libvpx', 'libilbc', 'fontconfig', 'libfribidi', 'libass',
			'openjpeg', 'intel_quicksync_mfx', 'fdk_aac', 'rtmpdump', 'libx264', 
		),
	},
	'bzlib2' : {
		'repo_type' : 'archive',
		'url' : 'https://fossies.org/linux/misc/bzip2-1.0.6.tar.gz',
		'patches' : (
			('https://raw.githubusercontent.com/DeadSix27/modular_cross_compile_script/master/patches/bzip2_cross_compile.diff', "p0"),
		),
		"needs_configure": False,
		"needs_make": True,
		"needs_make_install": False,
		'make_options': '{make_prefix_options} libbz2.a bzip2 bzip2recover install',
	},
	'zlib' : {
		'repo_type' : 'archive',
		'url' : 'https://sourceforge.net/projects/libpng/files/zlib/1.2.11/zlib-1.2.11.tar.gz',
		'configure_options': '--static --prefix={compile_prefix}',
		'make_options': '{make_prefix_options} ARFLAGS=rcs',
	},
	'liblzma' : {
		'repo_type' : 'archive',
		'url' : 'http://tukaani.org/xz/xz-5.2.3.tar.bz2',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
	},
	'libzimg' : {
		'repo_type' : 'git',
		'url' : 'https://github.com/sekrit-twc/zimg.git',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
	},
	'libsnappy' : {
		'repo_type' : 'archive',
		'url' : 'https://sourceforge.net/projects/ffmpegwindowsbi/files/dependency_libraries/google-snappy-1.1.3-14-g32d6d7d.tar.gz',
		'folder_name' : 'google-snappy-32d6d7d',
		'configure_options' : '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'make_options': '',
	},
	'libpng' : {
		'repo_type' : 'archive',
		'url' : 'https://sourceforge.net/projects/libpng/files/libpng16/1.6.28/libpng-1.6.28.tar.gz',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
	},
	'gmp' : { #todo try this.
		#export CC_FOR_BUILD=/usr/bin/gcc idk if we need this anymore, compiles fine without.
		#export CPP_FOR_BUILD=usr/bin/cpp
		#generic_configure "ABI=$bits_target"
		'repo_type' : 'archive',
		'url' : 'https://gmplib.org/download/gmp/gmp-6.1.2.tar.xz',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'make_options': '',
	},
	'libnettle' : {
		'repo_type' : 'archive',
		'url' : 'https://ftp.gnu.org/gnu/nettle/nettle-3.3.tar.gz',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static --disable-openssl --with-included-libtasn1',
		'make_options': '',
	},
	'iconv' : {
		'repo_type' : 'archive',
		# CFLAGS=-O2 # ??
		'url' : 'https://ftp.gnu.org/pub/gnu/libiconv/libiconv-1.15.tar.gz',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'make_options': '',
	},
		#    sed -i.bak 's/mkstemp(tmpfile)/ -1 /g' src/danetool.c # fix x86_64 absent? but danetool is just an exe AFAICT so this hack should be ok...
		#    # --disable-cxx don't need the c++ version, in an effort to cut down on size... XXXX test size difference... 
		#    # --enable-local-libopts to allow building with local autogen installed, 
		#    # --disable-guile is so that if it finds guile installed (cygwin did/does) it won't try and link/build to it and fail...
		#    # libtasn1 is some dependency, appears provided is an option [see also build_libnettle]
		#    # pks #11 hopefully we don't need kit
		
	'gnutls' : {
		'repo_type' : 'archive',
		'url' : 'https://www.gnupg.org/ftp/gcrypt/gnutls/v3.5/gnutls-3.5.10.tar.xz',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static --disable-cxx --disable-doc --enable-local-libopts --disable-guile -with-included-libtasn1 --without-p11-kit --with-included-unistring',
		'make_options': '',
		'run_after_install': ( # list of commands to run after make install variables can be found somewhere.
			"sed -i.bak 's/-lgnutls *$/-lgnutls -lnettle -lhogweed -lgmp -lcrypt32 -lws2_32 -liconv/' \"{pkg_config_path}/gnutls.pc\"",
		)
	},
	'frei0r' : {
		'repo_type' : 'archive',
		'needs_configure' : False,
		'is_cmake' : True,
		'run_post_patch': ( # runs commands post the patch process
			'sed -i.bak "s/find_package (Cairo)//g" CMakeLists.txt', #idk
		),
		'cmake_options': '{cmake_prefix_options}',
		'url' : 'https://files.dyne.org/frei0r/releases/frei0r-plugins-1.5.0.tar.gz',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'make_options': '',
	},
	'libsndfile' : {
		'repo_type' : 'git',
		'branch' : '1.0.27',
		'url' : 'https://github.com/erikd/libsndfile.git',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'make_options': '',
	},
	'libbs2b' : {
		'repo_type' : 'archive',
		'env_exports' : {
			"ac_cv_func_malloc_0_nonnull" : "yes", # fixes undefined reference to `rpl_malloc'
		},
		'url' : 'https://sourceforge.net/projects/bs2b/files/libbs2b/3.1.0/libbs2b-3.1.0.tar.gz',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'make_options': '',
	},
	'wavpack' : {
		'repo_type' : 'archive',
		'url' : 'https://github.com/dbry/WavPack/archive/5.1.0.tar.gz',
		'folder_name' : 'WavPack-5.1.0',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'make_options': '',
	},
	'libgme_game_music_emu' : {
		'repo_type' : 'archive',
		'needs_configure' : False,
		'is_cmake' : True,
		#'run_post_patch': ( # runs commands post the patch process
		#	'sed -i.bak "s|SHARED|STATIC|" gme/CMakeLists.txt',
		#),
		'cmake_options': '{cmake_prefix_options} -DBUILD_SHARED_LIBS=OFF',
		'url' : 'https://bitbucket.org/mpyne/game-music-emu/downloads/game-music-emu-0.6.1.tar.bz2',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'make_options': '',
	},
	'libwebp' : { # why can't everything be so easy to compile
		'repo_type' : 'archive',
		'url' : 'http://downloads.webmproject.org/releases/webp/libwebp-0.6.0.tar.gz',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'make_options': '',
	},
	'flite' : { # why can't everything be so easy to compile
		'repo_type' : 'archive',
		'url' : 'http://www.speech.cs.cmu.edu/flite/packed/flite-1.4/flite-1.4-release.tar.bz2',
		'patches' : ( # ordered list of patches, first one will be applied first..
			('https://raw.githubusercontent.com/DeadSix27/modular_cross_compile_script/master/patches/flite_64.diff', "p0"),
		),
		'cpu_count' : '1', #why do I even have to implement this, fix your stuff flite group.
		'needs_make_install' : False,
		'run_post_patch': (
			'sed -i.bak "s|i386-mingw32-|{cross_prefix_bare}|" configure',
		),
		"run_post_make": (
			'mkdir -pv "{compile_prefix}/include/flite"',
			'cp -v include/* "{compile_prefix}/include/flite"',
			'cp -v ./build/{bit_name}-mingw32/lib/*.a "{compile_prefix}/lib"',
		),
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'make_options': '',
	},
	'libgsm' : {
		'repo_type' : 'archive',
		'url' : 'http://www.quut.com/gsm/gsm-1.0.16.tar.gz',
		'folder_name' : 'gsm-1.0-pl16',
		'patches' : ( # ordered list of patches, first one will be applied first..
			('https://raw.githubusercontent.com/DeadSix27/modular_cross_compile_script/master/patches/gsm-1.0.16.patch', "p0"),
			('https://raw.githubusercontent.com/DeadSix27/modular_cross_compile_script/master/patches/gsm-1.0.16_Makefile.patch', 'p0'), # toast fails. so lets just patch it out of the makefile..
		),
		'needs_configure' : False,
		'needs_make_install' : False,
		"run_post_make": (
			'cp -v lib/libgsm.a {compile_prefix}/lib',
			'mkdir -pv {compile_prefix}/include/gsm',
			'cp -v inc/gsm.h {compile_prefix}/include/gsm',
		),
		'cpu_count' : '1',
		'make_options': '{make_prefix_options} INSTALL_ROOT={compile_prefix}',
	},
	'sdl1' : {
		'repo_type' : 'archive',
		'url' : 'https://www.libsdl.org/release/SDL-1.2.15.tar.gz',
		'custom_cflag' : '-DDECLSPEC=',# avoid SDL trac tickets 939 and 282, and not worried about optimizing yet...
		"run_after_install": (
			'sed -i.bak "s/-mwindows//" "{pkg_config_path}/sdl.pc"', # allow ffmpeg to output anything to console :|
			'sed -i.bak "s/-mwindows//" "{compile_prefix}/bin/sdl-config"', # update this one too for good measure, FFmpeg can use either, not sure which one it defaults to...
			'cp -v "{compile_prefix}/bin/sdl-config" "{cross_prefix_full}sdl-config"', # this is the only mingw dir in the PATH so use it for now [though FFmpeg doesn't use it?]
		),
		'make_options': '',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
	},
	'sdl2' : {
		'repo_type' : 'archive',
		'url' : 'https://www.libsdl.org/release/SDL2-2.0.5.tar.gz',
		'patches' : (
			('https://raw.githubusercontent.com/DeadSix27/modular_cross_compile_script/master/patches/SDL2-2.0.5.xinput.diff', "p0"),
		),
		'custom_cflag' : '-DDECLSPEC=', # avoid SDL trac tickets 939 and 282, and not worried about optimizing yet...
		"run_after_install": (
			'sed -i.bak "s/-mwindows//" "{pkg_config_path}/sdl2.pc"', # allow ffmpeg to output anything to console :|
			'sed -i.bak "s/-mwindows//" "{compile_prefix}/bin/sdl2-config"', # update this one too for good measure, FFmpeg can use either, not sure which one it defaults to...
			'cp -v "{compile_prefix}/bin/sdl2-config" "{cross_prefix_full}sdl2-config"', # this is the only mingw dir in the PATH so use it for now [though FFmpeg doesn't use it?]
		),
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
	},
	'libopus' : {
		'repo_type' : 'archive',
		'url' : 'https://github.com/xiph/opus/releases/download/v1.1.2/opus-1.1.2.tar.gz',
		'patches': ( 
			("https://raw.githubusercontent.com/DeadSix27/modular_cross_compile_script/master/patches/opus-1.1.2.patch", "p0"),
		),
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'make_options': '',
	},
	'opencore-amr' : {
		'repo_type' : 'archive',
		'url' : 'https://sourceforge.net/projects/opencore-amr/files/opencore-amr/opencore-amr-0.1.3.tar.gz',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'make_options': '',
	},
	'vo-amrwbenc' : {
		'repo_type' : 'archive',
		'url' : 'https://sourceforge.net/projects/opencore-amr/files/vo-amrwbenc/vo-amrwbenc-0.1.2.tar.gz',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'make_options': '',
	},
	'libogg' : {
		'repo_type' : 'archive',
		'url' : 'https://github.com/xiph/ogg/archive/v1.3.2.tar.gz',
		'folder_name' : 'ogg-1.3.2',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'make_options': '',
	},
	'libspeexdsp' : {
		'repo_type' : 'archive',
		'url' : 'https://github.com/xiph/speexdsp/archive/SpeexDSP-1.2rc3.tar.gz',
		'folder_name' : 'speexdsp-SpeexDSP-1.2rc3',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'make_options': '',
	},
	'ibspeex' : {
		'repo_type' : 'git', #"LDFLAGS=-lwinmm"
		'url' : 'https://github.com/xiph/speex.git',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'make_options': '',
	},
	'libvorbis' : {
		'repo_type' : 'git',
		'url' : 'https://github.com/xiph/vorbis.git',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'make_options': '',
	},
	'libtheora' : {
		'repo_type' : 'git',
		'url' : 'https://github.com/xiph/theora.git',
		'patches' : (
			('https://raw.githubusercontent.com/DeadSix27/modular_cross_compile_script/master/patches/theora_remove_rint_1.2.0alpha1.patch', 'p1'),
		),
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'make_options': '',
	},
	'orc' : {
		'repo_type' : 'archive',
		'url' : 'http://download.videolan.org/contrib/orc/orc-0.4.18.tar.gz',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'make_options': '',
	},
	'libschroedinger' : {
		'repo_type' : 'archive',
		'url' : 'http://download.videolan.org/contrib/schroedinger/schroedinger-1.0.11.tar.gz',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'make_options': '',
		'run_post_configure': (
			'sed -i.bak \'s/testsuite//\' Makefile',
		),
		'run_after_install': (
			'sed -i.bak \'s/-lschroedinger-1.0$/-lschroedinger-1.0 -lorc-0.4/\' "{pkg_config_path}/schroedinger-1.0.pc"',
		),
		
	},
	'freetype' : { #todo try playing with this.
		'repo_type' : 'archive',
		'url' : 'https://download.videolan.org/contrib/freetype2/freetype-2.6.3.tar.gz',
		'configure_options': '--host={compile_target} --build=x86_64-linux-gnu --prefix={compile_prefix} --disable-shared --enable-static --with-png=no', # cygwin = "--build=i686-pc-cygwin"  # hard to believe but needed...
		'cpu_count' : '1', # ye idk why it needs that
		#'make_options': '', # nor does it like the default make options..
		'run_after_install': (
			'sed -i.bak \'s/Libs: -L${{libdir}} -lfreetype.*/Libs: -L${{libdir}} -lfreetype -lexpat -lz -lbz2/\' "{pkg_config_path}/freetype2.pc"', # this should not need expat, but...I think maybe people use fontconfig's wrong and that needs expat? huh wuh? or dependencies are setup wrong in some .pc file?
		),
	},
	'expat' : {
		'repo_type' : 'archive',
		'url' : 'https://sourceforge.net/projects/expat/files/expat/2.2.0/expat-2.2.0.tar.bz2',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'make_options': '',
	},
	'libxml' : {
		'repo_type' : 'archive',
		'url' : 'http://xmlsoft.org/sources/libxml2-2.9.4.tar.gz',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static --without-python',
		'make_options': '',
	},
	'libbluray' : { 
		'repo_type' : 'archive',
		'url' : 'http://ftp.videolan.org/pub/videolan/libbluray/0.7.0/libbluray-0.7.0.tar.bz2',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'make_options': '',
		'run_after_install': (
			'sed -i.bak \'s/-lbluray.*$/-lbluray -lfreetype -lexpat -lz -lbz2 -lxml2 -lws2_32 -liconv/\' "{pkg_config_path}/libbluray.pc"', # not sure...is this a blu-ray bug, or VLC's problem in not pulling freetype's .pc file? or our problem with not using pkg-config --static ...
		),
	},
	'libxvid' : {
		'repo_type' : 'archive',
		'url' : 'http://downloads.xvid.org/downloads/xvidcore-1.3.4.tar.gz',
		'folder_name' : 'xvidcore',
		'rename_folder' : 'xvidcore-1.3.4', #why the weird name xvid? never heard of standards?
		'source_subfolder': './build/generic', # Why that subfolder.. come on
		'configure_options': '--host={compile_target} --prefix={compile_prefix}',
		'make_options': '',
		'cpu_count' : '1',
		'run_post_configure': (
			'sed -i.bak "s/-mno-cygwin//" platform.inc',
		),
		'run_after_install': (
			'rm -v {compile_prefix}/lib/xvidcore.dll.a',
			'mv -v {compile_prefix}/lib/xvidcore.a {compile_prefix}/lib/libxvidcore.a',
		),
	},
	'xavs' : {
		#compiles fine without LDFLAGS='-lm' apparently
		'repo_type' : 'svn',
		'url' : 'https://svn.code.sf.net/p/xavs/code/trunk',
		'folder_name' : 'xavs_svn',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static --cross-prefix={cross_prefix_bare}',
		'make_options': '',
		'run_after_install' : (
			'rm -f NUL', # I will not even ask.
		)
	},
	'libsoxr' : {
		'repo_type' : 'archive',
		'needs_configure' : False,
		'is_cmake' : True,
		'cmake_options': '{cmake_prefix_options} -DHAVE_WORDS_BIGENDIAN_EXITCODE=0 -DBUILD_SHARED_LIBS:bool=off -DBUILD_TESTS:BOOL=OFF -DCMAKE_AR={cross_prefix_full}ar', #not sure why it cries about AR
		'url' : 'https://sourceforge.net/projects/soxr/files/soxr-0.1.2-Source.tar.xz',
		'make_options': '',
	},
	# 'libebur128' : {
	# 	'repo_type' : 'git',
	# 	'url' : 'https://github.com/jiixyj/libebur128.git',
	# 	'cmake_options': '{cmake_prefix_options} -DENABLE_INTERNAL_QUEUE_H:BOOL=ON -DCMAKE_AR={cross_prefix_full}ar', #not sure why it cries about AR
	# 	'needs_configure' : False,
	# 	'is_cmake' : True,
	# 	'make_options': '',
	# 	'run_post_patch': (
	# 		'sed -i.bak \'s/ SHARED / STATIC /\' ebur128/CMakeLists.txt',
	# 	),
	# },
	'libx265' : { #should be a product actually :/ ill move/implement that later.
		'repo_type' : 'git',
		'url' : 'https://github.com/videolan/x265',
		'cmake_options': '{cmake_prefix_options} -DENABLE_SHARED=OFF -DCMAKE_AR={cross_prefix_full}ar', #not sure why it cries about AR
		'needs_configure' : False,
		'is_cmake' : True,
		'make_options': '',
		'source_subfolder': './source',
	},
	'libopenh264' : {
		'repo_type' : 'git',
		'url' : 'https://github.com/cisco/openh264.git',
		'needs_configure' : False,
		'make_options': '{make_prefix_options} OS=mingw_nt ARCH={bit_name} ASM=yasm',
		'install_options': '{make_prefix_options} OS=mingw_nt',
		'install_target' : 'install-static',
	},
	'vamp_plugin' : {
		'repo_type' : 'archive',
		'url' : 'https://dsix.tech/vamp-plugin-sdk-2.7.1.tar.gz', #todo obv move to a real host. (implement dl without filesize)
		'run_post_patch': (
			'cp -v build/Makefile.mingw64 Makefile',
		),
		'patches' : (
			('https://raw.githubusercontent.com/DeadSix27/modular_cross_compile_script/master/patches/vamp-plugin-sdk-2.7.1.patch','p0'), #They rely on M_PI which is gone since c99 or w/e, give them a self defined one.
		),
		'make_options': '{make_prefix_options} sdkstatic', # for DLL's add 'sdk rdfgen'
		'needs_make_install' : False, # doesnt s support xcompile installing
		'run_post_make' : ( # lets install it manually then I guess?
			'cp -v libvamp-sdk.a "{compile_prefix}/lib/"',
			'cp -v libvamp-hostsdk.a "{compile_prefix}/lib/"',
			'cp -rv vamp-hostsdk/ "{compile_prefix}/include/"',
			'cp -rv vamp-sdk/ "{compile_prefix}/include/"',
			'cp -rv vamp/ "{compile_prefix}/include/"',
			'cp -v pkgconfig/vamp.pc.in "{compile_prefix}/lib/pkgconfig/vamp.pc"',
			'cp -v pkgconfig/vamp-hostsdk.pc.in "{compile_prefix}/lib/pkgconfig/vamp-hostsdk.pc"',
			'cp -v pkgconfig/vamp-sdk.pc.in "{compile_prefix}/lib/pkgconfig/vamp-sdk.pc"',
			'sed -i.bak \'s/\%PREFIX\%/{compile_prefix_sed_escaped}/\' "{pkg_config_path}/vamp.pc"',
			'sed -i.bak \'s/\%PREFIX\%/{compile_prefix_sed_escaped}/\' "{pkg_config_path}/vamp-hostsdk.pc"',
			'sed -i.bak \'s/\%PREFIX\%/{compile_prefix_sed_escaped}/\' "{pkg_config_path}/vamp-sdk.pc"',
		)
	},
	'fftw3' : {
		'repo_type' : 'archive',
		#git tags/master require --enable-maintainer-mode we could but shouldn't use git I guess.
		'url' : 'http://fftw.org/fftw-3.3.6-pl1.tar.gz',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'make_options': '',
	},
	'libsamplerate' : {
		'repo_type' : 'git',
		'branch' : '477ce36f8e4bd6a177727f4ac32eba11864dd85d', # commit: Fix win32 compilation # fixed the cross compiling.
		'url' : 'https://github.com/erikd/libsamplerate.git',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'make_options': '',
	},	
	'librubberband' : {
		'repo_type' : 'archive',
		'download_header' : ( # some packages apparently do not come with specific headers.. like this one. so this function exists... files listed here will be downloaded into the {prefix}/include folder
			'https://raw.githubusercontent.com/DeadSix27/modular_cross_compile_script/master/additional_headers/ladspa.h',
		),
		'url' : 'http://code.breakfastquay.com/attachments/download/34/rubberband-1.8.1.tar.bz2',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'make_options': '',
		'needs_make_install' : False,
		'run_post_make' : ( 
			'cp lib/* "{compile_prefix}/lib"',
			'cp -r rubberband "{compile_prefix}/include"',
			'cp rubberband.pc.in "{pkg_config_path}/rubberband.pc"',
			'sed -i.bak "s|%PREFIX%|{compile_prefix_sed_escaped}|" "{pkg_config_path}/rubberband.pc"',
			'sed -i.bak \'s/-lrubberband *$/-lrubberband -lfftw3 -lsamplerate -lstdc++/\' "{pkg_config_path}/rubberband.pc"',
		),		
	},
	'liblame' : { # todo make it a product too.
		'repo_type' : 'archive',
		'url' : 'https://sourceforge.net/projects/lame/files/lame/3.99/lame-3.99.5.tar.gz',
		'patches' : (
			('https://raw.githubusercontent.com/DeadSix27/modular_cross_compile_script/master/patches/lame-3.99.5.patch', 'p0'),
		),
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static --enable-nasm',
		'make_options': '',
	},
	'twolame' : {
		'repo_type' : 'archive',
		'url' : 'https://sourceforge.net/projects/twolame/files/twolame/0.3.13/twolame-0.3.13.tar.gz',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static CPPFLAGS=-DLIBTWOLAME_STATIC',
		'make_options': '',
	},
	'vidstab' : {
		'repo_type' : 'git',
		'url' : 'https://github.com/georgmartius/vid.stab.git', #"Latest commit 97c6ae2  on May 29, 2015" .. master then I guess?
		'needs_configure' : False,
		'is_cmake' : True,
		'cmake_options': '{cmake_prefix_options} -DENABLE_SHARED=OFF -DCMAKE_AR={cross_prefix_full}ar -DUSE_OMP=OFF', #fatal error: omp.h: No such file or directory
		'make_options': '',
		'run_post_patch': (
			'sed -i.bak "s/SHARED/STATIC/g" CMakeLists.txt',
		),
	},
	'netcdf' : {
		'repo_type' : 'archive',
		'url' : 'https://gfd-dennou.org/arch/ucar/unidata/pub/netcdf/netcdf-4.4.1.tar.gz',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static --disable-netcdf-4 --disable-dap',
		'make_options': '',
	},
	'libcaca' : {
		'repo_type' : 'archive',
		'run_post_configure': (
			'sed -i.bak "s/int vsnprintf/int vnsprintf_disabled/" "caca/string.c"',
			'sed -i.bak "s/int vsnprintf/int vnsprintf_disabled/" "caca/figfont.c"',
			'sed -i.bak "s/__declspec(dllexport)//g" cxx/caca++.h',
			'sed -i.bak "s/__declspec(dllexport)//g" caca/caca.h',
			'sed -i.bak "s/__declspec(dllexport)//g" caca/caca0.h',
			'sed -i.bak "s/__declspec(dllimport)//g" caca/caca.h', 
			'sed -i.bak "s/__declspec(dllimport)//g" caca/caca0.h', 
		),
		'url' : 'http://pkgs.fedoraproject.org/repo/extras/libcaca/libcaca-0.99.beta19.tar.gz/a3d4441cdef488099f4a92f4c6c1da00/libcaca-0.99.beta19.tar.gz',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static --libdir={compile_prefix}/lib --disable-cxx --disable-csharp --disable-java --disable-python --disable-ruby --disable-imlib2 --disable-doc --disable-examples',
		'make_options': '',
	},
	
	
	#libcaca' : { #why is this thing so hard to compile geez... well works now | nvm.
	#	'repo_type' : 'archive',
	#	'patches' : (
	#		('https://raw.githubusercontent.com/DeadSix27/modular_cross_compile_script/master/patches/libcaca-0.99.beta19.patch', 'p1'),
	#	),
	#	'run_post_configure': (
	#		'sed -i.bak "s/ src examples/ src/" Makefile',
	#		'sed -i.bak "s/ doc test/ doc/" Makefile',
	#		'sed -i.bak "s/__declspec(dllexport)//g" *.h',
	#		'sed -i.bak "s/__declspec(dllimport)//g" *.h', 
	#	),
	#	#'cflag_addition' : '-DCACA_STATIC -D_WIN64 -D__LIBCACA__ -DDLL_EXPORT',
	#	'url' : 'http://pkgs.fedoraproject.org/repo/extras/libcaca/libcaca-0.99.beta19.tar.gz/a3d4441cdef488099f4a92f4c6c1da00/libcaca-0.99.beta19.tar.gz', #thanks fedora, I like you better than suse.
	#	'configure_options': '--host={compile_target} --prefix={compile_prefix} --libdir={compile_prefix}/lib --disable-cxx --disable-csharp --disable-java --disable-python --disable-ruby --disable-imlib2 --disable-doc --disable-examples',
	#	'make_options': '',
	#,
	'libmodplug' : {
		'repo_type' : 'archive',
		'url' : 'https://sourceforge.net/projects/modplug-xmms/files/libmodplug/0.8.8.5/libmodplug-0.8.8.5.tar.gz',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'make_options': '',
		'run_after_install': (
			# unfortunately this sed isn't enough, though I think it should be [so we add --extra-libs=-lstdc++ to FFmpegs configure] http://trac.ffmpeg.org/ticket/1539
			'sed -i.bak \'s/-lmodplug.*/-lmodplug -lstdc++/\' "{pkg_config_path}/libmodplug.pc"', # huh ?? c++?
			'sed -i.bak \'s/__declspec(dllexport)//\' "{compile_prefix}/include/libmodplug/modplug.h"', #strip DLL import/export directives
			'sed -i.bak \'s/__declspec(dllimport)//\' "{compile_prefix}/include/libmodplug/modplug.h"',
		),
	},
	'zvbi' : {
		'repo_type' : 'archive',
		'url' : 'https://sourceforge.net/projects/zapping/files/zvbi/0.2.35/zvbi-0.2.35.tar.bz2',
		'env_exports' : {
			'LIBS' : '-lpng',
		},
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static --disable-dvb --disable-bktr --disable-nls --disable-proxy --without-doxygen',
		'make_subdir' : 'src', #this will only run make and make install in said dir... geez..
		'make_options': '',
		'patches': (
		    ('https://raw.githubusercontent.com/DeadSix27/modular_cross_compile_script/master/patches/zvbi-0.2.35_win32.patch', 'p0'),
			('https://raw.githubusercontent.com/DeadSix27/modular_cross_compile_script/master/patches/zvbi-0.2.35_ioctl.patch', 'p0'),
		),
		#   there is no .pc for zvbi, so we add --extra-libs=-lpng to FFmpegs configure TODO there is a .pc file it just doesn't get installed [?]
		#   sed -i.bak 's/-lzvbi *$/-lzvbi -lpng/' "$PKG_CONFIG_PATH/zvbi.pc"
	},
	'libvpx' : {
		'repo_type' : 'git', #master seems to work.. suprisingly .. go back to somewhere around dcd6c87b80f2435ce4f206c5875f3be1f23b6999 if it stops.
		#'branch' : 'tags/v1.6.1',
		'url' : 'https://chromium.googlesource.com/webm/libvpx', #
		'configure_options': '--target={bit_name2}-{bit_name_win}-gcc --prefix={compile_prefix} --disable-shared --enable-static --enable-vp9-highbitdepth', # examples,tools crash with x86_64-w64-mingw32-ld: unrecognised emulation mode: 64
		'make_options': '', #well.. that made it work.. huh.. ok then.
		'env_exports' : {
			'CROSS' : '{cross_prefix_bare}',
		},
		'patches': (
			( 'https://raw.githubusercontent.com/DeadSix27/modular_cross_compile_script/master/patches/vpx_160_semaphore.patch', 'p1' ),
		),
	},
	'libilbc' : {
		'repo_type' : 'git',
		'url' : 'https://github.com/dekkers/libilbc.git',
		'run_post_patch': (
			'autoreconf -fiv',
		),
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'make_options': '',
	},
	'fontconfig' : {
		'repo_type' : 'archive',
		'url' : 'https://www.freedesktop.org/software/fontconfig/release/fontconfig-2.12.1.tar.gz',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static --disable-docs',
		'make_options': '',
		'run_after_install': (
			'sed -i.bak \'s/-L${{libdir}} -lfontconfig[^l]*$/-L${{libdir}} -lfontconfig -lfreetype -lexpat/\' "{pkg_config_path}/fontconfig.pc"',
		),		
	},
	'libfribidi' : {
		# seems like this patch is not needed anymore in 0.19.7
		# apply_patch https://raw.githubusercontent.com/rdp/ffmpeg-windows-build-helpers/master/patches/fribidi.diff
		'repo_type' : 'archive',
		'url' : 'https://fribidi.org/download/fribidi-0.19.7.tar.bz2',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'make_options': '',
	},
	'libass' : {
		'repo_type' : 'git',
		'url' : 'https://github.com/libass/libass.git',
		'branch' : '1be7dc0bdcf4ef44786bfc84c6307e6d47530a42', # latest still working on git
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'make_options': '',
		'run_after_install': (
			'sed -i.bak \'s/-lass -lm/-lass -lfribidi -lfontconfig -lfreetype -lexpat -lm/\' "{pkg_config_path}/libass.pc"',
		),	
	},
	'openjpeg' : {
		'repo_type' : 'archive',
		'url' : 'https://github.com/uclouvain/openjpeg/archive/v2.1.2.tar.gz',
		'folder_name': 'openjpeg-2.1.2',
		'needs_configure' : False,
		'is_cmake' : True,
		'cmake_options': '{cmake_prefix_options} -DBUILD_SHARED_LIBS:bool=off', #cmake .. "-DCMAKE_INSTALL_PREFIX=$mingw_w64_x86_64_prefix -DBUILD_SHARED_LIBS:bool=on -DCMAKE_SYSTEM_NAME=Windows"
		'make_options': '',		
	},
	'intel_quicksync_mfx' : {
		'repo_type' : 'git',
		'run_post_patch': (
			'autoreconf -fiv',
		),
		'url' : 'https://github.com/lu-zero/mfx_dispatch.git',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'make_options': '',
	},
	'fdk_aac' : {
		'repo_type' : 'git',
		'run_post_patch': (
			'autoreconf -fiv',
		),
		'url' : 'https://github.com/mstorsjo/fdk-aac.git',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'make_options': '',
	},
	'rtmpdump' : {
		'repo_type' : 'git',
		'url' : 'git://git.ffmpeg.org/rtmpdump',
		'needs_configure': False,
		'install_options' : 'SYS=mingw CRYPTO=GNUTLS OPT=-O2 CROSS_COMPILE={cross_prefix_bare} SHARED=no prefix={compile_prefix} LIB_GNUTLS="-L{compile_prefix}/lib -lgnutls -lnettle -lhogweed -lgmp -lcrypt32 -lws2_32 -liconv -lz"',
		'make_options': 'SYS=mingw CRYPTO=GNUTLS OPT=-O2 CROSS_COMPILE={cross_prefix_bare} SHARED=no prefix={compile_prefix} LIB_GNUTLS="-L{compile_prefix}/lib -lgnutls -lnettle -lhogweed -lgmp -lcrypt32 -lws2_32 -liconv -lz"',
		'run_after_install':(
			'sed -i.bak \'s/-lrtmp -lz/-lrtmp -lwinmm -lz/\' "{pkg_config_path}/librtmp.pc"',
		),
	},
	'rtmpdump' : {
		'repo_type' : 'git',
		'url' : 'git://git.ffmpeg.org/rtmpdump',
		'needs_configure': False,
		'install_options' : 'SYS=mingw CRYPTO=GNUTLS OPT=-O2 CROSS_COMPILE={cross_prefix_bare} SHARED=no prefix={compile_prefix} LIB_GNUTLS="-L{compile_prefix}/lib -lgnutls -lnettle -lhogweed -lgmp -lcrypt32 -lws2_32 -liconv -lz"',
		'make_options': 'SYS=mingw CRYPTO=GNUTLS OPT=-O2 CROSS_COMPILE={cross_prefix_bare} SHARED=no prefix={compile_prefix} LIB_GNUTLS="-L{compile_prefix}/lib -lgnutls -lnettle -lhogweed -lgmp -lcrypt32 -lws2_32 -liconv -lz"',
		'run_after_install':(
			'sed -i.bak \'s/-lrtmp -lz/-lrtmp -lwinmm -lz/\' "{pkg_config_path}/librtmp.pc"',
		),
	},
	'libx264' : { # this is just depedency x264, x264_10bit and x264 with lavf support is a product now check config of products.
		'repo_type' : 'git',
		'url' : 'http://git.videolan.org/git/x264.git',
		'configure_options': '--host={compile_target} --enable-static --cross-prefix={cross_prefix_bare} --prefix={compile_prefix} --enable-strip --disable-lavf', 
		'make_options': '',
	},
}
DOWNLOADERS = {
	'wget' : {
		'command_line' : 'wget {url} --retry-connrefused -nv --show-progress -O {output_dir}'
	},
	'curl' : {
		'command_line' : 'curl {url} --retry 50 -O -L --fail'
	}
}

class CrossCompileScript:
	"""A simple cross compiler helper made in python(3.6)"""
	
	def __init__(self):
		print("Starting {0} v{1}".format( self.__class__.__name__,_VERSION ))
		
		self.logger = logging.getLogger(__name__)
		logging.basicConfig(level=logging.INFO,  format=Colors.CYAN + _LOGFORMAT + Colors.RESET, datefmt=_LOG_DATEFORMAT)
		logging.basicConfig(level=logging.ERROR, format=Colors.RED  + _LOGFORMAT + Colors.RESET, datefmt=_LOG_DATEFORMAT)

		self.fullCurrentPath   = os.getcwd()
		self.fullWorkDir       = os.path.join(self.fullCurrentPath,_WORKDIR)
		self.fullProductDir    = None
		self.targetBitness     = _BITNESS
		self.originalPATH      = os.environ["PATH"]
		
		#init some stuff.
		self.compileTarget     = None
		self.compilePrefix     = None
		self.mingwBinpath      = None
		self.fullCrossPrefix   = None
		self.makePrefixOptions = None
		self.bitnessDir        = None
		self.bitnessDir2       = None
		self.winBitnessDir     = None
		self.pkgConfigPath     = None
		self.bareCrossPrefix   = None
		
		#main starting point
		for b in self.targetBitness:		
		
			if not os.path.isdir(_WORKDIR):
				self.logger.info("Creating workdir: %s" % (_WORKDIR))
				os.makedirs(_WORKDIR, exist_ok=True)
			os.chdir(_WORKDIR)
		
			self.bitnessDir         = "x86_64" if b is 64 else "i686" # e.g x86_64
			self.bitnessDir2        = "x86_64" if b is 64 else "x86" # just for vpx...
			self.winBitnessDir      = "win64" if b is 64 else "win32" # e.g win64
			self.compileTarget      = "{0}-w64-mingw32".format ( self.bitnessDir ) # e.g x86_64-w64-mingw32
			self.compilePrefix      = "{0}/{1}/mingw-w64-{2}/{3}".format( self.fullWorkDir, _MINGW_DIR, self.bitnessDir, self.compileTarget ) # workdir/xcompilers/mingw-w64-x86_64/x86_64-w64-mingw32
			self.mingwBinpath       = "{0}/{1}/mingw-w64-{2}/bin".format( self.fullWorkDir, _MINGW_DIR, self.bitnessDir ) # e.g workdir/xcompilers/mingw-w64-x86_64/bin
			self.fullCrossPrefix    = "{0}/{1}-w64-mingw32-".format( self.mingwBinpath, self.bitnessDir ) # e.g workdir/xcompilers/mingw-w64-x86_64/bin/x86_64-w64-mingw32-
			self.bareCrossPrefix    = "{1}-w64-mingw32-".format( self.mingwBinpath, self.bitnessDir ) # e.g x86_64-w64-mingw32-
			self.makePrefixOptions  = "CC={cross_prefix_bare}gcc AR={cross_prefix_bare}ar PREFIX={compile_prefix} RANLIB={cross_prefix_bare}ranlib LD={cross_prefix_bare}ld STRIP={cross_prefix_bare}strip CXX={cross_prefix_bare}g++".format( cross_prefix_bare=self.bareCrossPrefix, compile_prefix=self.compilePrefix )
			self.cmakePrefixOptions = "-G\"Unix Makefiles\" . -DENABLE_STATIC_RUNTIME=1 -DCMAKE_SYSTEM_NAME=Windows -DCMAKE_RANLIB={cross_prefix_full}ranlib -DCMAKE_C_COMPILER={cross_prefix_full}gcc -DCMAKE_CXX_COMPILER={cross_prefix_full}g++ -DCMAKE_RC_COMPILER={cross_prefix_full}windres -DCMAKE_INSTALL_PREFIX={compile_prefix}".format(cross_prefix_full=self.fullCrossPrefix, compile_prefix=self.compilePrefix )
			self.pkgConfigPath      = "{0}/lib/pkgconfig".format( self.compilePrefix ) #e.g workdir/xcompilers/mingw-w64-x86_64/x86_64-w64-mingw32/lib/pkgconfig
			self.fullProductDir     = os.path.join(self.fullWorkDir,self.bitnessDir + "_products")
			self.currentBitness     = b
					
			self.build_mingw(b)
			
			self.defaultCFLAGS()
			
			self.initProcess(b) 
		
			os.chdir("..")
		
	#:

	def initProcess(self,bitness):
		
		os.environ["PATH"]           = "{0}:{1}".format ( self.mingwBinpath, self.originalPATH )
		os.environ["PKG_CONFIG_PATH"] = self.pkgConfigPath
		os.environ["PKG_CONFIG_LIBDIR"] = ""
		
		if not os.path.isdir(self.bitnessDir):
			self.logger.info("Creating bitdir: {0}".format( self.bitnessDir ))
			os.makedirs(self.bitnessDir, exist_ok=True)
			
		if not os.path.isdir(self.bitnessDir + "_products"):
			self.logger.info("Creating bitdir: {0}".format( self.bitnessDir + "_products" ))
			os.makedirs(self.bitnessDir + "_products", exist_ok=True)
		for p in PRODUCT_ORDER:
			self.build_product(p,PRODUCTS[p])
	#:
	
	def build_mingw(self,bitness):
		# gcc_bin_x86_64 = os.path.join(self.mingwBinpath, "x86_64-w64-mingw32-gcc")
		# gcc_bin_i686   = os.path.join(self.mingwBinpath,   "i686-w64-mingw32-gcc")
		gcc_bin = os.path.join(self.mingwBinpath, self.bitnessDir + "-w64-mingw32-gcc")
		
		#if os.path.isfile(gcc_bin_i686) and os.path.isdir(gcc_bin_x86_64):
		if os.path.isfile(gcc_bin):
			self.logger.info("MinGW-w64 is already installed")
			return
		
		if not os.path.isdir(_MINGW_DIR):
			self.logger.info("Building MinGW-w64 in folder '{0}'".format( _MINGW_DIR ))
			os.makedirs(_MINGW_DIR, exist_ok=True)
			
		os.unsetenv("CFLAGS")
		
		os.chdir(_MINGW_DIR)
		
		mingw_script_file    = self.download_file(_MINGW_SCRIPT_URL)
		#mingw_script_options = "--clean-build --disable-shared --default-configure --threads=pthreads-w32 --pthreads-w32-ver=2-9-1 --cpu-count={0} --mingw-w64-ver=git --gcc-ver=6.3.0 --enable-gendef".format ( _CPU_COUNT )
		mingw_script_options = "--clean-build --disable-shared --default-configure --threads=winpthreads --cpu-count={0} --mingw-w64-ver=git --gcc-ver=6.3.0 --enable-gendef".format ( _CPU_COUNT )
		self.chmodpux(mingw_script_file)
		try:
			self.run_process( [ "bash " + mingw_script_file, mingw_script_options, "--build-type={0}".format( self.winBitnessDir ) ], False, False )
		except Exception as e:
			self.logger.error("Previous MinGW build may have failed, delete the compiler folder named '{0}' and try again".format( _MINGW_DIR ))
			exit(1)

		os.chdir("..")
	#:

	def downloadHeader(self,url):
	
		destination = os.path.join(self.compilePrefix,"include")
		fileName = os.path.basename(urlparse(url).path)
		
		if not os.path.isfile(os.path.join(destination,fileName)):
			fname = self.download_file(url)
			self.logger.info("Moving Header File: '{0}' to '{1}'".format( fname, destination ))
			shutil.move(fname, destination)
		else:
			self.logger.info("Header File: '{0}' already downloaded".format( fileName ))
	
	def download_file(self,link, targetName = None):
		_MAX_REDIRECTS = 5
		cj = http.cookiejar.CookieJar()
		class RHandler(urllib.request.HTTPRedirectHandler):
			def http_error_301(self, req, fp, code, msg, headers):  
				result = urllib.request.HTTPRedirectHandler.http_error_301(
					self, req, fp, code, msg, headers)              
				result.status = code
				return result                                       

			def http_error_302(self, req, fp, code, msg, headers):
				result = urllib.request.HTTPRedirectHandler.http_error_302(
					self, req, fp, code, msg, headers)              
				result.status = code                                
				return result       
	
		def sizeof_fmt(num, suffix='B'): # sizeof_fmt is courtesy of http://stackoverflow.com/a/1094933
			for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
				if abs(num) < 1024.0:
					return "%3.1f%s%s" % (num, unit, suffix)
				num /= 1024.0
			return "%.1f%s%s" % (num, 'Yi', suffix)
		
		link = urllib.parse.unquote(link)
		_CHUNKSIZE = 10240

		if not link.lower().startswith("https") and not link.lower().startswith("file"):
			print("WARNING: Using non-SSL http is not advised..") # gotta get peoples attention somehow eh?
		
		fname = None
		
		if targetName == None:
			fname = os.path.basename(link)
		else:
			fname = targetName
			
		#print("Downloading {0} to {1} ".format( link, fname) )
		
		ua = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
		if 'sourceforge.net' in link.lower():
			ua = 'wget/1.18' # sourceforge gives direct dls to wget agents.
		
		f = open(fname,'ab')
		hdrs = [ # act like chrome
				('Connection'                , 'keep-alive'),
				('Pragma'                    , 'no-cache'),
				('Cache-Control'             , 'no-cache'),
				('Upgrade-Insecure-Requests' , '1'),
				('User-Agent'                , ua),
				('Accept'                    , 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),
				# ('Accept-Encoding'           , 'gzip'),
				('Accept-Language'           , 'en-US,en;q=0.8'),
		]

		opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj)) #),RHandler()
		
		
		opener.addheaders = hdrs
		
		response = None
		
		request = urllib.request.Request(link)
		
		try:
			response = opener.open(request)
			
			olink = link
			for i in range(0, _MAX_REDIRECTS): # i have no idea of this is something I should be doing.
				if olink == response.geturl():
					break
				else:
					print("Following redirect to: {0}".format(response.geturl()))
					response = opener.open(urllib.request.Request(response.geturl()))
					
					olink = response.geturl()
				
		except Exception as e:
			traceback.print_exc()
			f.close()
			
			exit()
		
		headers = str(response.info())
		length = re.search(r'Content-Length: ([0-9]+)', headers, re.IGNORECASE)
		
		fileSize = None
		if length == None:
			pass #tbd
		else:	
			fileSize = int(length.groups()[0])
			
		#fileSizeDigits = int(math.log10(fileSize))+1
			
		downloadedBytes = 0
		
		start = time.clock()
		
		fancyFileSize = sizeof_fmt(fileSize)
		fancyFileSize = fancyFileSize.ljust(len(fancyFileSize))
		
		isGzipped = False
		if "content-encoding" in response.headers:
			if response.headers["content-encoding"] == "gzip":
				isGzipped = True
		
		while True:
			chunk = response.read(_CHUNKSIZE)
			downloadedBytes += len(chunk)
			if isGzipped:
				if len(chunk):
					try:
						chunk = zlib.decompress(chunk, 15+32)
					except Exception as e:
						fullChunk = response.read()
						# decompressor = zlib.decompressobj()
						test = zlib.decompress(fullChunk, zlib.MAX_WBITS | 16)
						print(test)
						print(e)
						exit()
					
			f.write(chunk)
			fancyDownloadedBytes = sizeof_fmt(downloadedBytes).rjust(len(fancyFileSize), ' ')
			
			fancySpeed = sizeof_fmt((downloadedBytes//(time.clock() - start))/8,"B/s").rjust(5, ' ')
			
			done = int(50 * downloadedBytes / fileSize)
			
			print("[{0}] - {1}/{2} ({3})".format( '|' * done + '-' * (50-done), fancyDownloadedBytes,fancyFileSize,fancySpeed), end= "\r")
			
			if not len(chunk):
				break
		print("")
		
		response.close()
		
		f.close()	
		#print("File fully downloaded to:",fname)
		
		return os.path.basename(link)
	#:

	def run_process(self,command,ignoreErrors = False, exitOnError = True):
		isSvn = False
		if not isinstance(command, str):
			command = " ".join(command) # could fail I guess
		if command.lower().startswith("svn"):
			isSvn = True
		process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
		while True:
			nextline = process.stdout.readline()
			if nextline == b'' and process.poll() is not None:
				break
			if isSvn:
				if not nextline.decode('utf-8').startswith('A    '):
					sys.stdout.write(nextline.decode('utf-8','replace'))
					sys.stdout.flush()
			else:
				sys.stdout.write(nextline.decode('utf-8','replace'))
				sys.stdout.flush()
				
		output = process.communicate()[0]
		return_code = process.returncode
		process.wait()
		if (return_code == 0):
			return output
		else:
			if ignoreErrors:
				return output
			self.logger.error("Error [%d] running process: '%s'" % (return_code,command))
			traceback.print_exc()
			if exitOnError:
				raise
		
		#p = subprocess.Popen(command, stdout=subprocess.PIPE,stderr=subprocess.STDOUT, universal_newlines = True, shell = True)
		#for line in iter(p.stdout.readline, b''):
		#	sys.stdout.write(line)
		#	sys.stdout.flush()
		#p.close()

	def get_process_result(self,command):
		if not isinstance(command, str):
			command = " ".join(command) # could fail I guess
		process = subprocess.Popen(command, stdout=subprocess.PIPE, universal_newlines=True, shell=True)
		out = process.stdout.readline().rstrip("\n").rstrip("\r")
		process.stdout.close()
		return_code = process.wait()
		if (return_code == 0):
			return out
		else:
			self.logger.error("Error [%d] creating process '%s'" % (return_code,command))
			exit()

	def sanitize_filename(self,f):
		return re.sub(r'[/\\:*?"<>|]', '', f)
		
	def md5(self,*args):
		msg = ''.join(args).encode("utf-8")
		m = hashlib.md5()
		m.update(msg)
		return m.hexdigest()

	def touch(self,f):
		Path(f).touch()
		
	def chmodpux(self,file):
		st = os.stat(file)
		os.chmod(file, st.st_mode | stat.S_IXUSR) #S_IEXEC would be just +x
		
	def git_clone(self, url, dir = None, desiredBranch = None):
		if dir == None:
			dir = self.sanitize_filename(os.path.basename(url))
			if not dir.endswith(".git"): dir += ".git"
			dir = dir.replace(".git","_git")
		else:
			dir = self.sanitize_filename(dir)
		if os.path.isdir(dir):
			os.chdir(dir)
			if git_get_latest == True: # to be implemented
				self.logger.info("Git fetching in '%s'" % (dir))
				self.run_process('git fetch')
			else:
				self.logger.info("Not doing git get latest pull for latest code '%s'" % (dir))
		elif not os.path.isdir(dir):
			self.logger.info("Git cloning '%s' to '%s'" % (url,dir))
			
			if os.path.isdir('%s.tmp' % (dir)):
				shutil.rmtree('%s.tmp' % (dir))
			
			self.run_process('git clone "%s" "%s.tmp"' % (url, dir))
			shutil.move('%s.tmp' % dir, dir)
			self.logger.info("Finished git cloning '%s' to '%s'" % (url,dir))
			os.chdir(dir)
		else:
			print("Unexpected error, please report this:", sys.exc_info()[0])
			raise
		
		oldGitVersion = self.get_process_result('git rev-parse HEAD')	
		if desiredBranch == None:
			self.logger.info("Checking out git master")
			self.run_process('git checkout master')
			if git_get_latest == True: # to be implemented
			  self.logger.info("Updating to latest '%s' git version [origin/master]..." % (dir))
			  self.run_process('git merge origin/master')
		else:
			self.logger.info('git checkout\'ing "%s"' % (desiredBranch))
			self.run_process('git checkout "%s"'% (desiredBranch))
			self.run_process('git merge "%s"' % (desiredBranch))
			
		newGitVersion = self.get_process_result('git rev-parse HEAD')
		if oldGitVersion != newGitVersion:
			self.logger.info("Got upstream changes, rebuilding..")
			self.removeAlreadyFiles()
		else:	
			self.logger.info("No git changes")
		os.chdir("..")
		return dir
	
	def svn_clone(self, url, dir, desiredBranch = None): # "branch".. "clone"..
		dir = self.sanitize_filename(dir)
		if not dir.endswith("_svn"): dir += "_svn"
		
		if not os.path.isdir(dir):
			self.logger.info("SVN checking out to %s" % (dir))
			if desiredBranch == None:
				self.run_process('svn co "%s" "%s.tmp" --non-interactive --trust-server-cert' % (url,dir))
			else:
				self.run_process('svn co -r "%s" "%s" "%s.tmp" --non-interactive --trust-server-cert' % (desiredBranch,url,dir))
			shutil.move('%s.tmp' % dir, dir)
		else:
			pass
			#svn up?
		return dir
	#:
	
	def download_unpack_file(self,url,folderName = None):
		
		fileName = os.path.basename(urlparse(url).path)
		
		if folderName == None:
			folderName = os.path.basename(os.path.splitext(urlparse(url).path)[0]).rstrip(".tar")
			
		if not os.path.isfile(os.path.join(folderName,"unpacked.successfully")):
		
			self.logger.info("Downloading {0} ({1})".format( fileName, url ))
			
			self.download_file(url,fileName)
			
			self.logger.info("Unpacking {0}".format( fileName ))
			
			tars = (".gz",".bz2",".xz", "bz") # i really need a better system for this.. but in reality, those are probably the only formats we will ever encounter.
			
			if fileName.endswith(tars):
				self.run_process('tar -xf "{0}"'.format( fileName ))
			else:
				self.run_process('unzip "{0}"'.format( fileName ))
				
			self.touch(os.path.join(folderName,"unpacked.successfully"))
			
			os.remove(fileName)
			
			return folderName
			
		else:
			self.logger.info("{0} already downloaded".format( fileName ))
			return folderName
	#:
	
	def build_depend(self,name,data):
	
		if '_already_built' in data:
			if data['_already_built'] == True:
				return # we already built this dep this run (skips unessesary re-checks if 2 things have the same dep. took me too long to figure out this quick and easy idea :|
	
		if "depends_on" in data: #dependception
			if len(data["depends_on"])>0:
				self.logger.info("Building dependencies of '%s'" % (name))
				for libraryName in data["depends_on"]:
					if libraryName not in DEPENDS:
						raise MissingDependency("The dependency '{0}' of '{1}' does not exist in dependency config.".format( libraryName, name)) #sys.exc_info()[0]
					else:
						self.build_depend(libraryName,DEPENDS[libraryName])
	
		if _DEBUG:
			for tk in os.environ:
				print("############ " + tk + " : " + os.environ[tk])
	
		workDir = None
		skipDownload = False #probably can be made easier by checking if its downloaded outside the download functions, but thats effort.
		
		self.logger.info("Building library '%s'" % (name))
		
		if 'rename_folder' in data:
			if data['rename_folder'] != None:
				if os.path.isdir(data['rename_folder']):
					skipDownload = True
					workDir = data['rename_folder']
		
		if skipDownload == False:
			if data["repo_type"] == "git":
				branch = self.getValueOrNone(data,'branch')
				workDir = self.git_clone(data["url"],None,branch)
			if data["repo_type"] == "svn":
				workDir = self.svn_clone(data["url"],data["folder_name"])
			if data["repo_type"] == "archive":
				if "folder_name" in data:
					workDir = self.download_unpack_file(data["url"],data["folder_name"])
				else:
					workDir = self.download_unpack_file(data["url"])
					
		if workDir == None:
			print("Unexpected error when building {0}, please report this:".format(name), sys.exc_info()[0])
			raise
			
		if 'rename_folder' in data:
			if data['rename_folder'] != None:
				shutil.move(workDir, data['rename_folder'])
				workDir = data['rename_folder']
		
		if 'download_header' in data:
			if data['download_header'] != None:
				for h in data['download_header']:
					self.downloadHeader(h)
		
		os.chdir(workDir)
		
		currentFullDir = os.getcwd()
		
		if 'source_subfolder' in data:
			if data['source_subfolder'] != None:
				os.chdir(data['source_subfolder'])
			
		if 'cflag_addition' in data:
			if data['cflag_addition'] != None:
				self.logger.info("Adding '{0}' to CFLAGS".format( data['cflag_addition'] ))
				os.environ["TARGET_CFLAGS"] = os.environ["TARGET_CFLAGS"] + " " + data['cflag_addition']
				
		if 'custom_cflag' in data:
			if data['custom_cflag'] != None:
				self.logger.info("Setting CFLAGS to '{0}'".format( data['custom_cflag'] ))
				os.environ["TARGET_CFLAGS"] = data['custom_cflag']
			
		if 'env_exports' in data:
			if data['env_exports'] != None:
				for key,val in data['env_exports'].items():
					val = self.replaceVariables(val)
					prevEnv = ''
					if key in os.environ:
						prevEnv = os.environ[key]
					self.logger.info("Environment variable '{0}' has been set from {1} to '{2}'".format( key, prevEnv, val ))
					os.environ[key] = val
		
		
		if 'patches' in data:
			if data['patches'] != None:
				for p in data['patches']:
					self.apply_patch(p[0],p[1])
					
		if not self.wildCardIsFile('already_ran_make'):
			if 'run_post_patch' in data:
				if data['run_post_patch'] != None:
					for cmd in data['run_post_patch']:
						cmd = self.replaceVariables(cmd)
						self.logger.info("Running post-patch-command: '{0}'".format( cmd ))
						self.run_process(cmd)
					
		if 'needs_configure' in data:
			if data['needs_configure'] == True:
				self.configure_source(name,data)
		else:
			self.configure_source(name,data)

		if 'is_cmake' in data:
			if data['is_cmake'] == True:
				self.cmake_source(name,data)
				
		if 'make_subdir' in data:
			if data['make_subdir'] != None:
				os.chdir(data['make_subdir'])
		
		if 'needs_make' in data: # there has to be a cleaner way than if'ing it all the way, lol, but im lazy
			if data['needs_make'] == True:
				self.make_source(name,data)
		else:
			self.make_source(name,data)
			
		if 'needs_make_install' in data:
			if data['needs_make_install'] == True:
				self.make_install_source(name,data)
		else:
			self.make_install_source(name,data)
		
		if 'env_exports' in data:
			if data['env_exports'] != None:
				for key,val in data['env_exports'].items():
					self.logger.info("Environment variable '{0}' has been UNSET!".format( key, val ))
					del os.environ[key]
		
		if 'source_subfolder' in data:
			if data['source_subfolder'] != None:
				os.chdir(currentFullDir)
				
		if 'make_subdir' in data:
			if data['make_subdir'] != None:
				os.chdir(currentFullDir)
		
		if 'cflag_addition' in data:
			if data['cflag_addition'] != None:
				self.defaultCFLAGS()
				
		if 'custom_cflag' in data:
			if data['custom_cflag'] != None:
				self.defaultCFLAGS()
				
		os.chdir("..")
		
		if 'debug_exitafter' in data:
			exit()
	
		DEPENDS[name]["_already_built"] = True
	
	#:
	
	def build_product(self,name,data):
	
		if _DEBUG:
			for tk in os.environ:
				print("############ " + tk + " : " + os.environ[tk])

		
		if "depends_on" in data:
			if len(data["depends_on"])>0:
			
				os.chdir(self.bitnessDir)
				
				self.logger.info("Building dependencies of '%s'" % (name))
				for libraryName in data["depends_on"]:
					if libraryName not in DEPENDS:
						raise MissingDependency("The dependency '{0}' of '{1}' does not exist in dependency config.".format( libraryName, name)) #sys.exc_info()[0]
					else:
						self.build_depend(libraryName,DEPENDS[libraryName])
			
				os.chdir("..")
		
		os.chdir(self.bitnessDir + "_products")
		
		workDir = None
		skipDownload = False #probably can be made easier by checking if its downloaded outside the download functions, but thats effort.
		self.logger.info("Building PRODUCT '%s'" % (name))
		
		if 'rename_folder' in data:
			if data['rename_folder'] != None:
				if os.path.isdir(data['rename_folder']):
					skipDownload = True
					workDir = data['rename_folder']
		if skipDownload == False:
			if data["repo_type"] == "git":
				branch = self.getValueOrNone(data,'branch')
				workDir = self.git_clone(data["url"],None,branch)
			if data["repo_type"] == "svn":
				workDir = self.svn_clone(data["url"],data["folder_name"])
			if data["repo_type"] == "archive":
				if "folder_name" in data:
					workDir = self.download_unpack_file(data["url"],data["folder_name"])
				else:
					workDir = self.download_unpack_file(data["url"])
					
		if workDir == None:
			print("Unexpected error when building {0}, please report this:".format(name), sys.exc_info()[0])
			raise
			
		if 'rename_folder' in data:
			if data['rename_folder'] != None:
				shutil.move(workDir, data['rename_folder'])
				workDir = data['rename_folder']
		
		if 'download_header' in data:
			if data['download_header'] != None:
				for h in data['download_header']:
					self.downloadHeader(h)
		
		os.chdir(workDir)
		
		currentFullDir = os.getcwd()
		
		if 'source_subfolder' in data:
			if data['source_subfolder'] != None:
				os.chdir(data['source_subfolder'])
			
		if 'cflag_addition' in data:
			if data['cflag_addition'] != None:
				self.logger.info("Adding '{0}' to TARGET_CFLAGS".format( data['cflag_addition'] ))
				os.environ["TARGET_CFLAGS"] = os.environ["TARGET_CFLAGS"] + " " + data['cflag_addition']
				
		if 'custom_cflag' in data:
			if data['custom_cflag'] != None:
				self.logger.info("Setting TARGET_CFLAGS to '{0}'".format( data['custom_cflag'] ))
				os.environ["TARGET_CFLAGS"] = data['custom_cflag']
			
		if 'env_exports' in data:
			if data['env_exports'] != None:
				for key,val in data['env_exports'].items():
					val = self.replaceVariables(val)
					prevEnv = ''
					if key in os.environ:
						prevEnv = os.environ[key]
					self.logger.info("Environment variable '{0}' has been set from {1} to '{2}'".format( key, prevEnv, val ))
					os.environ[key] = val
		
		
		if 'patches' in data:
			if data['patches'] != None:
				for p in data['patches']:
					self.apply_patch(p[0],p[1])
					
		if not self.wildCardIsFile('already_ran_make'):
			if 'run_post_patch' in data:
				if data['run_post_patch'] != None:
					for cmd in data['run_post_patch']:
						cmd = cmd.replaceVariables(val)
						self.logger.info("Running post-patch-command: '{0}'".format( cmd ))
						self.run_process(cmd)
					
					
		if 'needs_configure' in data:
			if data['needs_configure'] == True:
				self.configure_source(name,data)
		else:
			self.configure_source(name,data)
			
		if 'is_cmake' in data:
			if data['is_cmake'] == True:
				self.cmake_source(name,data)
				
		if 'make_subdir' in data:
			if data['make_subdir'] != None:
				os.chdir(data['make_subdir'])		
		
		if 'needs_make' in data: # there has to be a cleaner way than if'ing it all the way, lol, but im lazy
			if data['needs_make'] == True:
				self.make_source(name,data)
		else:
			self.make_source(name,data)
			
		if 'needs_make_install' in data:
			if data['needs_make_install'] == True:
				self.make_install_source(name,data)
		else:
			self.make_install_source(name,data)
		
		if 'env_exports' in data:
			if data['env_exports'] != None:
				for key,val in data['env_exports'].items():
					self.logger.info("Environment variable '{0}' has been UNSET!".format( key, val ))
					del os.environ[key]
		
		if 'source_subfolder' in data:
			if data['source_subfolder'] != None:
				os.chdir(currentFullDir)
				
		if 'make_subdir' in data:
			if data['make_subdir'] != None:
				os.chdir(currentFullDir)
		
		if 'cflag_addition' in data:
			if data['cflag_addition'] != None:
				self.defaultCFLAGS()
				
		if 'custom_cflag' in data:
			if data['custom_cflag'] != None:
				self.defaultCFLAGS()
		
		os.chdir("..")
		
		os.chdir("..")
		
	def configure_source(self,name,data):
		touch_name = "already_configured_%s" % (self.md5(name,self.getKeyOrBlankString(data,"configure_options")))
		
		
		isWaf = False
		if 'is_waf' in data:
			if data['is_waf'] == True:
				isWaf = True
		
		if not os.path.isfile(touch_name):
			self.removeAlreadyFiles()
			
			if isWaf:
				if not os.path.isfile("waf"):
					if os.path.isfile("bootstrap.py"):
						self.run_process('./bootstrap.py')
			else:
				if not os.path.isfile("configure"):
					if os.path.isfile("bootstrap.sh"):
						self.run_process('./bootstrap.sh')
					if os.path.isfile("autogen.sh"):
						self.run_process('./autogen.sh')
					if os.path.isfile("buildconf"):
						self.run_process('./buildconf')
					if os.path.isfile("bootstrap"):
						self.run_process('./bootstrap')	
					
			configOpts = ''
			if 'configure_options' in data:
				configOpts = self.replaceVariables(data["configure_options"])
			self.logger.info("Configuring '{0}' with: {1}".format( name, configOpts ))
			
			confCmd = './configure'
			if isWaf:
				confCmd = './waf --color=yes configure'
			
			self.run_process('{0} {1}'.format(confCmd, configOpts))
			
			if 'run_post_configure' in data:
				if data['run_post_configure'] != None:
					for cmd in data['run_post_configure']:
						cmd = self.replaceVariables(cmd)
						self.logger.info("Running post-configure-command: '{0}'".format( cmd ))
						self.run_process(cmd)
			
			mCleanCmd = 'make clean'
			if isWaf:
				mCleanCmd = './waf --color=yes clean'
			
			self.run_process('{0} -j {1}'.format( mCleanCmd, _CPU_COUNT ),True)
			
			self.touch(touch_name)
			
	def apply_patch(self,url,type = "-p1"): #p1 for github, p0 for idk
		fileName = os.path.basename(urlparse(url).path)
		
		if not os.path.isfile(fileName):
			self.logger.info("Downloading patch '{0}' to: {1}".format( url, fileName ))
			self.download_file(url,fileName)
			
		patch_touch_name = "%s.done" % (fileName)
			
		if not os.path.isfile(patch_touch_name):
			self.logger.info("Patching source uising: '{0}'".format( fileName ))
			self.run_process('patch -{0} < "{1}"'.format(type, fileName )) 
			self.touch(patch_touch_name)
			self.removeAlreadyFiles()
		else:
			self.logger.info("Patch '{0}' already applied".format( fileName ))	
	#:
	
	def cmake_source(self,name,data):
		touch_name = "already_ran_cmake_%s" % (self.md5(name,self.getKeyOrBlankString(data,"make_options")))
		
		if not os.path.isfile(touch_name):
			self.removeAlreadyFiles()

			makeOpts = ''
			if 'cmake_options' in data:
				makeOpts = self.replaceVariables(data["cmake_options"])
			self.logger.info("C-Making '{0}' with: {1}".format( name, makeOpts ))
	
			self.run_process('cmake {0}'.format( makeOpts ))
			
			self.touch(touch_name)			
			
			
	def make_source(self,name,data):
		touch_name = "already_ran_make_%s" % (self.md5(name,self.getKeyOrBlankString(data,"make_options")))
		if not os.path.isfile(touch_name):
		
			isWaf = False
			if 'is_waf' in data:
				if data['is_waf'] == True:
					isWaf = True
			
			mkCmd = 'make'
			if isWaf:
				mkCmd = './waf --color=yes'
			
			if os.path.isfile("configure"):
				self.run_process('{0} clean -j {0}'.format( mkCmd, _CPU_COUNT ),True)

			makeOpts = ''
			if 'make_options' in data:
				makeOpts = self.replaceVariables(data["make_options"]) 
				
			self.logger.info("Making '{0}' with: {1}".format( name, makeOpts ))
			
			cpcnt = '-j {0}'.format(_CPU_COUNT)
			
			if 'cpu_count' in data:
				if data['cpu_count'] != None:
					cpcnt = ""
			
			if 'ignore_make_fail_and_run' in data:
				if len(data['ignore_make_fail_and_run']) > 0: #todo check if its a list too
					try:
						if isWaf:
							mkCmd = './waf --color=yes build'
						self.run_process('{0} {2} {1}'.format( mkCmd, cpcnt, makeOpts ))
					except Exception as e:
						#print("GOT HERE")
						#exit()
						self.logger.info("Ignoring failed make process...")
						for cmd in data['ignore_make_fail_and_run']:
							cmd = self.replaceVariables(cmd)
							self.logger.info("Running post-failed-make-command: '{0}'".format( cmd ))
							self.run_process(cmd)
			else:
				if isWaf:
					mkCmd = './waf --color=yes build'
				self.run_process('{0} {2} {1}'.format( mkCmd, cpcnt, makeOpts ))
			
			if 'run_post_make' in data:
				if data['run_post_make'] != None:
					for cmd in data['run_post_make']:
						cmd = self.replaceVariables(cmd)
						self.logger.info("Running post-make-command: '{0}'".format( cmd ))
						self.run_process(cmd)
			
			self.touch(touch_name)
	#:
			
	def make_install_source(self,name,data):
		touch_name = "already_ran_make_install_%s" % (self.md5(name,self.getKeyOrBlankString(data,"install_options")))
		if not os.path.isfile(touch_name):
		
		
			cpcnt = '-j {0}'.format(_CPU_COUNT)
			
			if 'cpu_count' in data:
				if data['cpu_count'] != None:
					cpcnt = ""
			
			makeInstallOpts  = ''
			if 'install_options' in data:
				if data['install_options'] != None:
					makeInstallOpts = self.replaceVariables(data["install_options"])
			installTarget = "install"
			if 'install_target' in data:
				if data['install_target'] != None:
					installTarget = data['install_target']
					
				
			self.logger.info("Make installing '{0}' with: {1}".format( name, makeInstallOpts ))
			
			isWaf = False
			if 'is_waf' in data:
				if data['is_waf'] == True:
					isWaf = True
			
			mkCmd = "make"
			if isWaf:
				mkCmd = "./waf"
			
			self.run_process('{0} {1} {2} {3}'.format(mkCmd, installTarget, makeInstallOpts, cpcnt ))
			
			if 'run_after_install' in data:
				if data['run_after_install'] != None:
					for cmd in data['run_after_install']:
						cmd = self.replaceVariables(cmd)
						self.logger.info("Running post-install-command: '{0}'".format( cmd ))
						self.run_process(cmd)
			
			self.touch(touch_name)
	#:
	
	def defaultCFLAGS(self):
		self.logger.debug("Reset CFLAGS to: {0}".format( _ORIG_CFLAGS ) )
		os.environ["TARGET_CFLAGS"] = _ORIG_CFLAGS
	#:
	
	def wildCardIsFile(self,wild):
		for file in os.listdir('.'):
			if file.startswith(wild):
				return True
		return False
	
	def removeAlreadyFiles(self):
		for af in glob.glob("./already_*"):
			os.remove(af)
	#:	
	
	def replaceVariables(self,cmd):
		cmd = cmd.format( 
			cmake_prefix_options      = self.cmakePrefixOptions,
			make_prefix_options       = self.makePrefixOptions,
			pkg_config_path           = self.pkgConfigPath,
			mingw_binpath             = self.mingwBinpath,
			cross_prefix_bare         = self.bareCrossPrefix,
			cross_prefix_full         = self.fullCrossPrefix,
			compile_prefix            = self.compilePrefix,
			compile_target            = self.compileTarget,
			bit_name                  = self.bitnessDir,
			bit_name2                 = self.bitnessDir2,
			bit_name_win              = self.winBitnessDir,
			bit_num                   = self.currentBitness,
			product_prefix            = self.fullProductDir,
			compile_pefix_sed_escaped = self.compilePrefix.replace("/","\\/"),
		)
		return cmd
	#:
	def getValueOrNone(self,db,k):
		if k in db:
			if db[k] == None:
				return None
			else:
				return db[k]
		else:
			return None
			
	def reReplaceInFile(self,infile,oldString,newString,outfile):
		with open(infile, 'rw') as f:
			for line in f:
				line = re.sub(oldString, newString, line)
				print(line)
		exit()
	
	def getKeyOrBlankString(self,db,k):
		if k in db:
			if db[k] == None:
				return ""
			else:
				return db[k]
		else:
			return ""
	#:
	
if __name__ == "__main__":
	main = CrossCompileScript()