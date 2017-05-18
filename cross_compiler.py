#!/usr/bin/env python3
#- * -coding: utf - 8 - * -

# ####################################################
# Copyright (C) 2017 DeadSix27 (https://github.com/DeadSix27/python_cross_compile_script)
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ###################################################

# ###################################################
# ################ REQUIRED PACKAGES ################
# ###################################################
# Package dependencies (some may be missing):
# 
# Ubuntu 17.04 (Zesty Zapus)
# Ubuntu 16.10 (Yakkety)
# Fedora 25    (Twenty Five)
# 
# global      - texinfo yasm git make automake gcc gcc-c++ pax cvs svn flex bison patch libtoolize nasm mercurial cmake gettext-autopoint
# mkvtoolnix  - libxslt docbook-util rake docbook-style-xsl
# gnutls      - gperf
# angle       - gyp
# vapoursynth - p7zip
# flac        - docbook-to-man
# youtube-dl  - pando
# filezilla   - wxrc (aka wx-common)

# ###################################################
# #################     TODO      ###################
# ###################################################

# ## Feel free to help out with whatever is in this list (or any other thing) ##

# List:
# - Fix libbluray in shared.
# - Basic optional config file.
# - Remote hosting of product/dependency hosting as json files.
# - Implement hash support for archives, mostly for the self hosted ones.

# ###################################################
# ################# CONFIGURATION ###################
# ###################################################

import os.path,logging,re,subprocess,sys,shutil,urllib.request,urllib.parse,stat
import hashlib,glob,traceback,time,zlib,codecs,argparse
import http.cookiejar
from multiprocessing import cpu_count
from pathlib import Path
from urllib.parse import urlparse
from collections import OrderedDict

_CPU_COUNT         = cpu_count() # the default automaticlaly sets it to your core-count but you can set it manually too # default: cpu_count()
_QUIET             = False # This is only for the 'just build it all mode', in CLI you should use "-q" # default: false 
_LOG_DATEFORMAT    = '%H:%M:%S' # default: %H:%M:%S
_LOGFORMAT         = '[%(asctime)s][%(levelname)s] %(message)s' # default: [%(asctime)s][%(levelname)s] %(message)s
_WORKDIR           = 'workdir' # default: workdir
_MINGW_DIR         = 'xcompilers' # default: xcompilers
_BITNESS           = ( 64, ) # as of now only 64 is tested, 32 could work, for multi-bit write it like (64, 32), this is completely untested .
_ORIG_CFLAGS       = '-march=sandybridge -O3' # I've had issues recently with the binaries not working on older systems despite using a old march, so stick to sandybridge for now, for others see: https://gcc.gnu.org/onlinedocs/gcc-6.3.0/gcc/x86-Options.html#x86-Options
_ENABLE_STATUSFILE = True # NOT IMPLEMENTED YET !
_STATUS_FILE       = os.getcwd() + "/status_file" # NOT IMPLEMENTED YET !

# Remove a product, re-order them or add your own, do as you like.
PRODUCT_ORDER      = ( 'cuetools', 'aria2','x265_multibit', 'flac', 'vorbis-tools', 'lame3', 'sox', 'mpv', 'youtube-dl', 'ffmpeg_static', 'ffmpeg_shared', 'curl', 'wget', 'mkvtoolnix' )
#
# ###################################################
# ###################################################
# ###################################################

class Colors: #ansi colors
	RESET           = '\033[0m'
	BLACK           = '\033[30m'
	RED             = '\033[31m'
	GREEN           = '\033[32m'
	YELLOW          = '\033[33m'
	BLUE            = '\033[34m'
	MAGENTA         = '\033[35m'
	CYAN            = '\033[36m'
	WHITE           = '\033[37m'
	LIGHTBLACK_EX   = '\033[90m' # those seem to work on the major OS so meh.
	LIGHTRED_EX     = '\033[91m'
	LIGHTGREEN_EX   = '\033[92m'
	LIGHTYELLOW_EX  = '\033[93m'
	LIGHTBLUE_EX    = '\033[94m'
	LIGHTMAGENTA_EX = '\033[95m'
	LIGHTCYAN_EX    = '\033[96m'
	LIGHTWHITE_EX   = '\033[9m'

class MissingDependency(Exception):
	__module__ = 'exceptions'
	def __init__(self, message):
		self.message = message
		
class MyFormatter(logging.Formatter):

	inf_fmt  = Colors.LIGHTCYAN_EX   + _LOGFORMAT + Colors.RESET
	err_fmt  = Colors.LIGHTRED_EX    + _LOGFORMAT + Colors.RESET
	dbg_fmt  = Colors.LIGHTYELLOW_EX + _LOGFORMAT + Colors.RESET
	war_fmt  = Colors.YELLOW         + _LOGFORMAT + Colors.RESET

	def __init__(self):
		super().__init__(fmt="%(levelno)d: %(msg)s", datefmt=_LOG_DATEFORMAT, style='%')  

	def format(self, record):
		format_orig = self._style._fmt
		if record.levelno == logging.DEBUG:
			self._style._fmt = MyFormatter.dbg_fmt
		elif record.levelno == logging.INFO:
			self._style._fmt = MyFormatter.inf_fmt
		elif record.levelno == logging.ERROR:
			self._style._fmt = MyFormatter.err_fmt
		elif record.levelno == logging.WARNING:
			self._style._fmt = MyFormatter.war_fmt
		result = logging.Formatter.format(self, record)
		self._style._fmt = format_orig
		return result

_BASE_URL         = 'https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master'

_MINGW_SCRIPT_URL = '/mingw_build_scripts/mingw-build-script-posix_threads.sh' # with win32 posix threading support
#_MINGW_SCRIPT_URL = '/mingw_build_scripts/mingw-build-script.sh' # without the above
#_MINGW_SCRIPT_URL = '/mingw_build_scripts/mingw-build-script-posix_threads-gcc7-test.sh' # if you want to test gcc7, make sure to set _GCC_VER to "7.0.1-RC-20170425"

_GCC_VER          = "7.1.0" # change to 7.0.1-RC-20170425 if you use the gcc7 script above.

_DEBUG = False # for.. debugging.. purposes this is the same as --debug in CLI, only use this if you do not use CLI.

_OUR_VER = ".".join(str(x) for x in sys.version_info[0:3])
_TESTED_VERS = ['3.5.3','3.5.2','3.6.0']

class CrossCompileScript:
		
	def __init__(self,product_order,products,depends,variables):
		self.PRODUCT_ORDER          = product_order
		self.PRODUCTS               = products
		self.DEPENDS                = depends
		self.VARIABLES              = variables
		self.init()
		
	def init(self):
		fmt                         = MyFormatter()
		hdlr                        = logging.StreamHandler(sys.stdout)
		hdlr.setFormatter(fmt)
		self.logger                 = logging.getLogger(__name__)
		self.logger.addHandler(hdlr) 
		self.fullCurrentPath        = os.getcwd()
		self.fullWorkDir            = os.path.join(self.fullCurrentPath,_WORKDIR)
		self.fullProductDir         = None
		self.targetBitness          = _BITNESS
		self.originalPATH           = os.environ["PATH"]
		self.mingwScriptURL         = _BASE_URL + _MINGW_SCRIPT_URL
		self.compileTarget          = None
		self.compilePrefix          = None
		self.mingwBinpath           = None
		self.fullCrossPrefix        = None
		self.makePrefixOptions      = None
		self.bitnessDir             = None
		self.bitnessDir2            = None
		self.winBitnessDir          = None
		self.pkgConfigPath          = None
		self.bareCrossPrefix        = None
		self.cpuCount               = None
		self.originalCflags         = None
		self.buildLogFile           = None
		self.quietMode              = _QUIET
		self.debugMode              = _DEBUG
		self.logger.setLevel(logging.INFO)
		if self.debugMode:
			self.init_debugMode()
		if self.quietMode:
			self.init_quietMode()

	def init_quietMode(self):
		self.logger.warning('Quiet mode is enabled')
		self.buildLogFile = codecs.open("raw_build.log","w","utf-8")
	def init_debugMode(self):
		self.logger.setLevel(logging.DEBUG)
		self.logger.debug('Debugging is on')
	
	def listify_pdeps(self,pdlist,type):
		class customArgsAction(argparse.Action):
			def __call__(self, parser, args, values, option_string=None):
				format = "CLI"
				if args.markdown:
					format = "MD"
				if args.csv:
					format = "CSV"
					
				if format == "CLI":
					longestName = 0
					longestVer = 1
					for key,val in pdlist.items():
						if '_info' in val:
							if 'version' in val['_info']:
								if len(val['_info']['version']) > longestVer:
									longestVer = len(val['_info']['version'])
							name = key
							if len(name) > longestName:
								longestName = len(name)
							# if 'fancy_name' in val['_info']:
								# if len(val['_info']['fancy_name']) > longestName:
									# longestName = len(val['_info']['fancy_name'])
						else:
							if len(key) > longestName:
								longestName = len(key)

					HEADER = "Product"
					if type == "D":
						HEADER = "Dependency"
					if longestName < len('Dependency'):
						longestName = len('Dependency')
					HEADER_V = "Version"
					if longestVer < len(HEADER_V):
						longestVer = len(HEADER_V)
						
					print(' {0} - {1}'.format(HEADER.rjust(longestName,' '),HEADER_V.ljust(longestVer, ' ')))
					print('')
					
					for key,val in sorted(pdlist.items()):
						ver = Colors.RED + "(no version)" + Colors.RESET
						if '_info' in val:
							if 'version' in val['_info']:
								ver = Colors.GREEN + val['_info']['version'] + Colors.RESET
						name = key
						# if '_info' in val:
							# if 'fancy_name' in val['_info']:
								# name = val['_info']['fancy_name']
						
						print(' {0} - {1}'.format(name.rjust(longestName,' '),ver.ljust(longestVer, ' ')))
				elif format == "MD":
					longestName = 0
					longestVer = 1
					for key,val in pdlist.items():
						if '_info' in val:
							if 'version' in val['_info']:
								if len(val['_info']['version']) > longestVer:
									longestVer = len(val['_info']['version'])
							if 'fancy_name' in val['_info']:
								if len(val['_info']['fancy_name']) > longestName:
									longestName = len(val['_info']['fancy_name'])
						else:
							if len(key) > longestName:
								longestName = len(key)
								
					HEADER = "Product"
					if type == "D":
						HEADER = "Dependency"
					if longestName < len('Dependency'):
						longestName = len('Dependency')
					HEADER_V = "Version"
					if longestVer < len(HEADER_V):
						longestVer = len(HEADER_V)
				
					print('| {0} | {1} |'.format(HEADER.ljust(longestName,' '),HEADER_V.ljust(longestVer,' ')))
					print('| {0}:|:{1} |'.format(longestName * '-', longestVer * '-'))
					for key,val in sorted(pdlist.items()):
						if '_info' in val:
							ver = "?"
							name = key
							if 'version' in val['_info']:
								ver = val['_info']['version']
							if 'fancy_name' in val['_info']:
								name = val['_info']['fancy_name']
							print('| {0} | {1} |'.format(name.ljust(longestName,' '),ver.ljust(longestVer,' ')))
				else:
					print(";".join( sorted(pdlist.keys()) ))
				setattr(args, self.dest, values)
				parser.exit()
		return customArgsAction
		
	def assembleConfigHelps(self,pdlist,type,main):
		class customArgsAction(argparse.Action):
			def __call__(self, parser, args, values, option_string=None):
				main.quietMode = True
				main.init_quietMode()
				main.prepareBuilding(64)
				main.build_mingw(64)
				main.initBuildFolders()
				for k,v in pdlist.items():
					if '_disabled' not in v:
						if '_info' in v:
							beforePath = os.getcwd()
							path = main.get_thing_path(k,v,type)
							print(path)
							main.cchdir(path)
							if os.path.isfile(os.path.join(path,"configure")):
								os.system("./configure --help")
							if os.path.isfile(os.path.join(path,"waf")):
								os.system("./waf --help")
							main.cchdir(beforePath)
							print("-------------------")
				setattr(args, self.dest, values)
				parser.exit()
		return customArgsAction
	
	def commandLineEntrace(self):
		class epiFormatter(argparse.RawDescriptionHelpFormatter):
			w = shutil.get_terminal_size((120, 10))[0]
			def __init__(self, max_help_position=w, width=w, *args, **kwargs):
				kwargs['max_help_position'] = max_help_position
				kwargs['width'] = width
				super(epiFormatter, self).__init__(*args, **kwargs)
			def _split_lines(self, text, width):
				return text.splitlines()
			
		_epilog = 'Copyright (C) 2017 DeadSix27 (https://github.com/DeadSix27/python_cross_compile_script)\n\n This Source Code Form is subject to the terms of the Mozilla Public\n License, v. 2.0. If a copy of the MPL was not distributed with this\n file, You can obtain one at https://mozilla.org/MPL/2.0/.\n '
		if _OUR_VER not in _TESTED_VERS:
			_epilog = Colors.RED + "Warning: This script is not tested on your Python Version: " + _OUR_VER + Colors.RESET + "\n\n" +_epilog
		parser = argparse.ArgumentParser(formatter_class=epiFormatter, epilog=_epilog)
		parser.description = Colors.CYAN + 'Pythonic Cross Compile Helper (MPL2.0)' + Colors.RESET + '\n\nExample usages:' \
			'\n "{0} list -p"             - lists all the products' \
			'\n "{0} -a"                  - builds everything' \
			'\n "{0} -f -d libx264"       - forces the rebuilding of libx264' \
			'\n "{0} -pl x265_10bit,mpv"  - builds this list of products in that order' \
			'\n "{0} -q -p ffmpeg_static" - will quietly build ffmpeg-static'.format(parser.prog)
			
		subparsers = parser.add_subparsers(help='Sub commands')
		
		list_p = subparsers.add_parser('list', help= 'Type: \'' + parser.prog + ' list --help\' for more help')
		
		list_p.add_argument('-md', '--markdown', help='Print list in markdown format', action='store_true')
		list_p.add_argument('-cv', '--csv', help='Print list as CSV-like string', action='store_true')
		list_p_group1 = list_p.add_mutually_exclusive_group(required=True)
		list_p_group1.add_argument('-p', '--products',    nargs=0, help='List all products',     action=self.listify_pdeps(self.PRODUCTS,"P"))
		list_p_group1.add_argument('-d', '--dependencies', nargs=0, help='List all dependencies', action=self.listify_pdeps(self.DEPENDS, "D"))
		
		
		chelps_p = subparsers.add_parser('chelps', help= 'Type: \'' + parser.prog + ' chelps --help\' for more help')
		chelps_p_group1 = chelps_p.add_mutually_exclusive_group(required=True)
		chelps_p_group1.add_argument('-p', '--products',    nargs=0, help='Write all product config helps to confighelps.txt',     action=self.assembleConfigHelps(self.PRODUCTS,"P",self))
		chelps_p_group1.add_argument('-d', '--dependencies', nargs=0, help='Write all dependency config helps to confighelps.txt',  action=self.assembleConfigHelps(self.DEPENDS, "D",self))
		
		
		group2 = parser.add_mutually_exclusive_group( required = True )
		group2.add_argument( '-p',  '--build_product_list',    dest='PRODUCT',         help='Build this product list'                                      )
		group2.add_argument( '-pl', '--build_product',         dest='PRODUCT_LIST',    help='Build this product (and dependencies)'                        )
		group2.add_argument( '-d',  '--build_dependency',      dest='DEPENDENCY',      help='Build this dependency'                                        )
		group2.add_argument( '-dl', '--build_dependency_list', dest='DEPENDENCY_LIST', help='Build this dependency list'                                   )
		group2.add_argument( '-a',  '--build_all',                                     help='Build all products (according to order)', action='store_true' )
		parser.add_argument( '-q',  '--quiet',                                         help='Only show info lines'                   , action='store_true' )
		parser.add_argument( '-f',  '--force',                                         help='Force rebuild, deletes already files'   , action='store_true' )
		parser.add_argument( '-g',  '--debug',                                         help='Show debug information'                 , action='store_true' )
		
		if len(sys.argv)==1:
			self.defaultEntrace()
		else:
			def errorOut(p,t,m=None):
				if m == None:
					fullStr = Colors.LIGHTRED_EX + 'Error:\n ' + Colors.CYAN + '\'{0}\'' + Colors.LIGHTRED_EX + ' is not a valid {2}\n Type: ' + Colors.CYAN + '\'{1} list --products/--dependencies\'' + Colors.LIGHTRED_EX + ' for a full list'
					print( fullStr.format ( p, os.path.basename(__file__), "Product" if t == "PRODUCT" else "Dependency" ) + Colors.RESET )
				else:
					print(m)
				exit(1)
			args = parser.parse_args()
			forceRebuild = False
			if args.debug:
				self.debugMode = True
				self.init_debugMode()
			if args.quiet:
				self.quietMode = True
				self.init_quietMode()
			if args.force:
				forceRebuild = True
			thingToBuild = None
			buildType = None

			finalThingList = []
			
			if args.PRODUCT:
				buildType = "PRODUCT"
				thingToBuild = args.PRODUCT
				if thingToBuild in self.PRODUCTS:
					finalThingList.append(thingToBuild)
				else:
					errorOut(thingToBuild,buildType)
					
			elif args.DEPENDENCY:
				buildType = "DEPENDENCY"
				thingToBuild = args.DEPENDENCY
				if thingToBuild in self.DEPENDS:
					finalThingList.append(thingToBuild)
				else:
					errorOut(thingToBuild,buildType)
					
			elif args.DEPENDENCY_LIST:
				buildType = "DEPENDENCY"
				thingToBuild = args.DEPENDENCY_LIST
				if "," not in thingToBuild:
					errorOut(None,None,"Error: are you sure the list format is correct? It must be dependency1;dependency2;dependency3;...")
				for d in thingToBuild.split(","):
					if d in self.DEPENDS:
						finalThingList.append(d)
					else:
						errorOut(thingToBuild,buildType)
					
			elif args.PRODUCT_LIST:
				buildType = "PRODUCT"
				thingToBuild = args.PRODUCT_LIST
				if "," not in thingToBuild:
					errorOut(None,None,"Error: are you sure the list format is correct? It must be product1;product2;product3,...")
				for d in thingToBuild.split(","):
					if d in self.PRODUCTS:
						finalThingList.append(d)
					else:
						errorOut(thingToBuild,buildType)
					
			elif args.build_all:
				self.defaultEntrace()
				return
			
			self.logger.warning('Starting custom build process for: {0}'.format(thingToBuild))
			
			for thing in finalThingList:
				for b in self.targetBitness:
					main.prepareBuilding(b)
					main.build_mingw(b)
					main.initBuildFolders()
					if buildType == "PRODUCT":
						self.build_thing(thing,self.PRODUCTS[thing],buildType,forceRebuild)
					else:
						self.build_thing(thing,self.DEPENDS[thing],buildType,forceRebuild)
					main.finishBuilding()
	
	def defaultEntrace(self):
		for b in self.targetBitness:
			self.prepareBuilding(b)
			self.build_mingw(b)
			self.initBuildFolders()
			for p in self.PRODUCT_ORDER:
				self.build_thing(p,self.PRODUCTS[p],"PRODUCT")
			self.finishBuilding()

	def finishBuilding(self):
		self.cchdir("..")

	def prepareBuilding(self,b):
		if not os.path.isdir(_WORKDIR):
			self.logger.info("Creating workdir: %s" % (_WORKDIR))
			os.makedirs(_WORKDIR, exist_ok=True)
		self.cchdir(_WORKDIR)

		self.bitnessDir         = "x86_64" if b is 64 else "i686" # e.g x86_64
		self.bitnessDir2        = "x86_64" if b is 64 else "x86" # just for vpx...
		self.bitnessDir3        = "mingw64" if b is 64 else "mingw" # just for openssl...
		self.winBitnessDir      = "win64" if b is 64 else "win32" # e.g win64
		self.compileTarget      = "{0}-w64-mingw32".format ( self.bitnessDir ) # e.g x86_64-w64-mingw32
		self.compilePrefix      = "{0}/{1}/mingw-w64-{2}/{3}".format( self.fullWorkDir, _MINGW_DIR, self.bitnessDir, self.compileTarget ) # workdir/xcompilers/mingw-w64-x86_64/x86_64-w64-mingw32
		self.offtreePrefix      = "{0}".format( os.path.join(self.fullWorkDir,self.bitnessDir + "_offtree") ) # workdir/x86_64_offtree
		self.hostTarget         = "{0}/{1}/mingw-w64-{2}".format( self.fullWorkDir, _MINGW_DIR, self.bitnessDir )
		self.mingwBinpath       = "{0}/{1}/mingw-w64-{2}/bin".format( self.fullWorkDir, _MINGW_DIR, self.bitnessDir ) # e.g workdir/xcompilers/mingw-w64-x86_64/bin
		self.fullCrossPrefix    = "{0}/{1}-w64-mingw32-".format( self.mingwBinpath, self.bitnessDir ) # e.g workdir/xcompilers/mingw-w64-x86_64/bin/x86_64-w64-mingw32-
		self.bareCrossPrefix    = "{0}-w64-mingw32-".format( self.bitnessDir ) # e.g x86_64-w64-mingw32-
		self.makePrefixOptions  = "CC={cross_prefix_bare}gcc AR={cross_prefix_bare}ar PREFIX={compile_prefix} RANLIB={cross_prefix_bare}ranlib LD={cross_prefix_bare}ld STRIP={cross_prefix_bare}strip CXX={cross_prefix_bare}g++".format( cross_prefix_bare=self.bareCrossPrefix, compile_prefix=self.compilePrefix )
		self.cmakePrefixOptions = "-G\"Unix Makefiles\" -DENABLE_STATIC_RUNTIME=1 -DCMAKE_SYSTEM_NAME=Windows -DCMAKE_RANLIB={cross_prefix_full}ranlib -DCMAKE_C_COMPILER={cross_prefix_full}gcc -DCMAKE_CXX_COMPILER={cross_prefix_full}g++ -DCMAKE_RC_COMPILER={cross_prefix_full}windres -DCMAKE_FIND_ROOT_PATH={compile_prefix}".format(cross_prefix_full=self.fullCrossPrefix, compile_prefix=self.compilePrefix )
		self.pkgConfigPath      = "{0}/lib/pkgconfig".format( self.compilePrefix ) #e.g workdir/xcompilers/mingw-w64-x86_64/x86_64-w64-mingw32/lib/pkgconfig
		self.fullProductDir     = os.path.join(self.fullWorkDir,self.bitnessDir + "_products")
		self.currentBitness     = b
		self.cpuCount           = _CPU_COUNT
		self.originalCflags     = _ORIG_CFLAGS

		if self.debugMode:
			print('self.bitnessDir = \n'         + self.bitnessDir + '\n\n')
			print('self.bitnessDir2 = \n'        + self.bitnessDir2 + '\n\n')
			print('self.winBitnessDir = \n'      + self.winBitnessDir + '\n\n')
			print('self.compileTarget = \n'      + self.compileTarget + '\n\n')
			print('self.compilePrefix = \n'      + self.compilePrefix + '\n\n')
			print('self.mingwBinpath = \n'       + self.mingwBinpath + '\n\n')
			print('self.fullCrossPrefix = \n'    + self.fullCrossPrefix + '\n\n')
			print('self.bareCrossPrefix = \n'    + self.bareCrossPrefix + '\n\n')
			print('self.makePrefixOptions = \n'  + self.makePrefixOptions + '\n\n')
			print('self.cmakePrefixOptions = \n' + self.cmakePrefixOptions + '\n\n')
			print('self.pkgConfigPath = \n'      + self.pkgConfigPath + '\n\n')
			print('self.fullProductDir = \n'     + self.fullProductDir + '\n\n')
			print('self.currentBitness = \n'     + str(self.currentBitness) + '\n\n')
			print('PATH = \n'                    + os.environ["PATH"] + '\n\n')

		os.environ["PATH"]           = "{0}:{1}".format ( self.mingwBinpath, self.originalPATH )
		#os.environ["PATH"]           = "{0}:{1}:{2}".format ( self.mingwBinpath, os.path.join(self.compilePrefix,'bin'), self.originalPATH ) #todo properly test this..
		os.environ["PKG_CONFIG_PATH"] = self.pkgConfigPath
		os.environ["PKG_CONFIG_LIBDIR"] = ""
	#:
	def initBuildFolders(self):
		if not os.path.isdir(self.bitnessDir):
			self.logger.info("Creating bitdir: {0}".format( self.bitnessDir ))
			os.makedirs(self.bitnessDir, exist_ok=True)

		if not os.path.isdir(self.bitnessDir + "_products"):
			self.logger.info("Creating bitdir: {0}".format( self.bitnessDir + "_products" ))
			os.makedirs(self.bitnessDir + "_products", exist_ok=True)

		if not os.path.isdir(self.bitnessDir + "_offtree"):
			self.logger.info("Creating bitdir: {0}".format( self.bitnessDir + "_offtree" ))
			os.makedirs(self.bitnessDir + "_offtree", exist_ok=True)

	def build_mingw(self,bitness):
		gcc_bin = os.path.join(self.mingwBinpath, self.bitnessDir + "-w64-mingw32-gcc")

		if os.path.isfile(gcc_bin):
			self.logger.info("MinGW-w64 is already installed")
			return

		if not os.path.isdir(_MINGW_DIR):
			self.logger.info("Building MinGW-w64 in folder '{0}'".format( _MINGW_DIR ))
			os.makedirs(_MINGW_DIR, exist_ok=True)

		os.unsetenv("CFLAGS")

		self.cchdir(_MINGW_DIR)

		mingw_script_file    = self.download_file(self.mingwScriptURL)
		#mingw_script_options = "--clean-build --disable-shared --default-configure --threads=pthreads-w32 --pthreads-w32-ver=2-9-1 --cpu-count={0} --mingw-w64-ver=git --gcc-ver=6.3.0 --enable-gendef".format ( _CPU_COUNT )
		mingw_script_options = "--clean-build --disable-shared --default-configure --threads=winpthreads --cpu-count={0} --mingw-w64-ver=git --gcc-ver={1} --enable-gendef".format ( _CPU_COUNT, _GCC_VER )
		self.chmodpux(mingw_script_file)
		try:
			self.run_process( [ "bash " + mingw_script_file, mingw_script_options, "--build-type={0}".format( self.winBitnessDir ) ], False, False )
		except Exception as e:
			self.logger.error("Previous MinGW build may have failed, delete the compiler folder named '{0}' and try again".format( _MINGW_DIR ))
			exit(1)

		self.cchdir("..")
	#:

	def downloadHeader(self,url):

		destination = os.path.join(self.compilePrefix,"include")
		fileName = os.path.basename(urlparse(url).path)

		if not os.path.isfile(os.path.join(destination,fileName)):
			fname = self.download_file(url)
			self.logger.debug("Moving Header File: '{0}' to '{1}'".format( fname, destination ))
			shutil.move(fname, destination)
		else:
			self.logger.debug("Header File: '{0}' already downloaded".format( fileName ))

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

		def sizeof_fmt(num, suffix='B'): # sizeof_fmt is courtesy of https://stackoverflow.com/a/1094933
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
			fname = os.path.basename(urlparse(link).path)
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

		fancyFileSize = None
		if fileSize != None:
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
						print(e)
						exit()

			f.write(chunk)
			if fileSize != None:
				done = int(50 * downloadedBytes / fileSize)
				fancySpeed = sizeof_fmt((downloadedBytes//(time.clock() - start))/8,"B/s").rjust(5, ' ')
				fancyDownloadedBytes = sizeof_fmt(downloadedBytes).rjust(len(fancyFileSize), ' ')
				print("[{0}] - {1}/{2} ({3})".format( '|' * done + '-' * (50-done), fancyDownloadedBytes,fancyFileSize,fancySpeed), end= "\r")
			else:
				print("{0}".format( sizeof_fmt(downloadedBytes) ), end="\r")

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
					if self.quietMode == True:
						self.buildLogFile.write(nextline.decode('utf-8','replace'))
					else:
						sys.stdout.write(nextline.decode('utf-8','replace'))
						sys.stdout.flush()
			else:
				if self.quietMode == True:
					self.buildLogFile.write(nextline.decode('utf-8','replace'))
				else:
					sys.stdout.write(nextline.decode('utf-8','replace'))
					sys.stdout.flush()

		return_code = process.returncode
		output = process.communicate()[0]
		process.wait()
		if (return_code == 0):
			return output
		else:
			if ignoreErrors:
				return output
			self.logger.error("Error [{0}] running process: '{1}' in '{2}'".format(return_code,command,os.getcwd()))
			self.logger.error("You can try deleting the product/dependency folder: '{0}' and re-run the script".format(os.getcwd()))
			if self.quietMode:
				self.logger.error("Please check the raw_build.log file")
			if exitOnError:
				exit(1)

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
	#:

	def mercurial_clone(self,url,virtFolderName=None,renameTo=None,desiredBranch=None):
		if virtFolderName == None:
			virtFolderName = self.sanitize_filename(os.path.basename(url))
			if not virtFolderName.endswith(".hg"): virtFolderName += ".hg"
			virtFolderName = virtFolderName.replace(".hg","_hg")
		else:
			virtFolderName = self.sanitize_filename(virtFolderName)

		realFolderName = virtFolderName
		if renameTo != None:
			realFolderName = renameTo
			
		branchString = ""
		if desiredBranch != None:
			branchString = " {0}".format( desiredBranch )

		if os.path.isdir(realFolderName):
			self.cchdir(realFolderName)
			hgVersion = subprocess.check_output('hg --debug id -i', shell=True)
			self.run_process('hg pull -u')
			self.run_process('hg update -C{0}'.format(" default" if desiredBranch == None else branchString))
			hgVersionNew = subprocess.check_output('hg --debug id -i', shell=True)
			if hgVersion != hgVersionNew:
				self.logger.debug("HG clone has code changes, updating")
				self.removeAlreadyFiles()
			else:
				self.logger.debug("HG clone already up to date")
			self.cchdir("..")
		else:
			self.logger.info("HG cloning '%s' to '%s'" % (url,realFolderName))
			self.run_process('hg clone {0} {1}'.format(url,realFolderName + ".tmp" ))
			if desiredBranch != None:
				self.cchdir(realFolderName + ".tmp")
				self.logger.debug("HG updating to:{0}".format(" master" if desiredBranch == None else branchString))
				self.run_process('hg up{0} -v'.format("" if desiredBranch == None else branchString))
				self.cchdir("..")
			self.run_process('mv "{0}" "{1}"'.format(realFolderName + ".tmp", realFolderName))
			self.logger.info("Finished HG cloning '%s' to '%s'" % (url,realFolderName))

		return realFolderName
	#:
	def git_clone(self,url,virtFolderName=None,renameTo=None,desiredBranch=None,recursive=False):
		if virtFolderName == None:
			virtFolderName = self.sanitize_filename(os.path.basename(url))
			if not virtFolderName.endswith(".git"): virtFolderName += ".git"
			virtFolderName = virtFolderName.replace(".git","_git")
		else:
			virtFolderName = self.sanitize_filename(virtFolderName)

		realFolderName = virtFolderName
		if renameTo != None:
			realFolderName = renameTo
			
		branchString = ""
		if desiredBranch != None:
			branchString = " {0}".format( desiredBranch )
			
		properBranchString = "master"
		if desiredBranch != None:
			properBranchString  = desiredBranch

		if os.path.isdir(realFolderName):
			self.cchdir(realFolderName)

			self.run_process('git remote update')
						
			UPSTREAM = '@{u}' # or branchName i guess
			if desiredBranch != None:
				UPSTREAM = properBranchString
			LOCAL    = subprocess.check_output('git rev-parse @',shell=True).decode("utf-8")
			REMOTE   = subprocess.check_output('git rev-parse "{0}"'.format(UPSTREAM),shell=True).decode("utf-8")
			BASE     = subprocess.check_output('git merge-base @ "{0}"'.format(UPSTREAM),shell=True).decode("utf-8")
			
			self.run_process('git checkout -f')
			self.run_process('git checkout {0}'.format(properBranchString))
			
			if LOCAL == REMOTE:
				self.logger.debug("####################")
				self.logger.debug("Up to date")
				self.logger.debug("LOCAL:  " + LOCAL)
				self.logger.debug("REMOTE: " + REMOTE)
				self.logger.debug("BASE:   " + BASE)
				self.logger.debug("####################")
			elif LOCAL == BASE:
				self.logger.debug("####################")
				self.logger.debug("Need to pull")
				self.logger.debug("LOCAL:  " + LOCAL)
				self.logger.debug("REMOTE: " + REMOTE)
				self.logger.debug("BASE:   " + BASE)
				self.logger.debug("####################")
				if desiredBranch != None:
					#bsSplit = properBranchString.split("/")
					#if len(bsSplit) == 2:
					#	self.run_process('git pull origin {1}'.format(bsSplit[0],bsSplit[1]))
					#else:
					self.run_process('git pull origin {0}'.format(properBranchString))
				else:
					self.run_process('git pull'.format(properBranchString))
				self.run_process('git clean -xfdf') #https://gist.github.com/nicktoumpelis/11214362
				self.run_process('git submodule foreach --recursive git clean -xfdf')
				self.run_process('git reset --hard')
				self.run_process('git submodule foreach --recursive git reset --hard')
				self.run_process('git submodule update --init --recursive')
			elif REMOTE == BASE:
				self.logger.debug("####################")
				self.logger.debug("need to push")
				self.logger.debug("LOCAL:  " + LOCAL)
				self.logger.debug("REMOTE: " + REMOTE)
				self.logger.debug("BASE:   " + BASE)
				self.logger.debug("####################")
			else:
				self.logger.debug("####################")
				self.logger.debug("diverged?")
				self.logger.debug("LOCAL:  " + LOCAL)
				self.logger.debug("REMOTE: " + REMOTE)
				self.logger.debug("BASE    " + BASE)
				self.logger.debug("####################")
			self.cchdir("..")
			
			
		else:
			recur = ""
			if recursive:
				recur = " --recursive"
			self.logger.info("GIT cloning '%s' to '%s'" % (url,os.getcwd() +"/"+ realFolderName))
			self.run_process('git clone{0} --progress "{1}" "{2}"'.format(recur,url,realFolderName + ".tmp" ))
			if desiredBranch != None:
				self.cchdir(realFolderName + ".tmp")
				self.logger.debug("GIT Checking out:{0}".format(" master" if desiredBranch == None else branchString))
				self.run_process('git checkout{0}'.format(" master" if desiredBranch == None else branchString))
				self.cchdir("..")
			self.run_process('mv "{0}" "{1}"'.format(realFolderName + ".tmp", realFolderName))
			self.logger.info("Finished GIT cloning '%s' to '%s'" % (url,realFolderName))

		return realFolderName
	#:
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

	def download_unpack_file(self,url,folderName = None,workDir = None):

		fileName = os.path.basename(urlparse(url).path)

		if folderName == None:
			folderName = os.path.basename(os.path.splitext(urlparse(url).path)[0]).rstrip(".tar")

		folderToCheck = folderName
		if workDir != None:
			folderToCheck = workDir

		if not os.path.isfile(os.path.join(folderToCheck,"unpacked.successfully")):
			self.logger.info("Downloading {0} ({1})".format( fileName, url ))

			self.download_file(url,fileName)

			self.logger.info("Unpacking {0}".format( fileName ))

			tars = (".gz",".bz2",".xz",".bz",".tgz") # i really need a better system for this.. but in reality, those are probably the only formats we will ever encounter.

			if fileName.endswith(tars):
				self.run_process('tar -xf "{0}"'.format( fileName ))
			else:
				self.run_process('unzip "{0}"'.format( fileName ))

			self.touch(os.path.join(folderName,"unpacked.successfully"))

			os.remove(fileName)

			return folderName

		else:
			self.logger.debug("{0} already downloaded".format( fileName ))
			return folderName
	#:
	
	def get_thing_path(self,name,data,type): # type = PRODUCT or DEPENDENCY		
		outPath = os.getcwd()
		workDir = None
		renameFolder = None
		if 'rename_folder' in data:
			if data['rename_folder'] != None:
				renameFolder = data['rename_folder']
		if type == "P": 
			outPath = os.path.join(outPath,self.bitnessDir + "_products")
			self.cchdir(self.bitnessDir + "_products")
		else:
			outPath = os.path.join(outPath,self.bitnessDir)
			self.cchdir(self.bitnessDir)
		
		if data["repo_type"] == "git":
			branch     = self.getValueOrNone(data,'branch')
			recursive  = self.getValueOrNone(data,'recursive_git')
			folderName = self.getValueOrNone(data,'folder_name')
			workDir    = self.git_clone(data["url"],folderName,renameFolder,branch,recursive)
		if data["repo_type"] == "svn":
			workDir = self.svn_clone(data["url"],data["folder_name"],renameFolder)
		if data['repo_type'] == 'mercurial':
			branch = self.getValueOrNone(data,'branch')
			workDir = self.mercurial_clone(data["url"],self.getValueOrNone(data,'folder_name'),renameFolder,branch)
		if data["repo_type"] == "archive":
			if "folder_name" in data:
				workDir = self.download_unpack_file(data["url"],data["folder_name"],workDir)
			else:
				workDir = self.download_unpack_file(data["url"],None,workDir)

		if workDir == None:
			print("Unexpected error when building {0}, please report this:".format(name), sys.exc_info()[0])
			raise

		if 'rename_folder' in data: # this should be moved inside the download functions, TODO.. but lazy
			if data['rename_folder'] != None:
				if not os.path.isdir(data['rename_folder']):
					shutil.move(workDir, data['rename_folder'])
				workDir = data['rename_folder']
		self.cchdir("..")
		return os.path.join(outPath,workDir)
	
	def build_thing(self,name,data,type,force_rebuild = False, skipDepends = False): # type = PRODUCT or DEPENDENCY # I couldn't come up with a better name :S
		#we are in workdir
		if '_already_built' in data:
			if data['_already_built'] == True:
				return				
		if self.debugMode:
			for tk in os.environ:
				print("############ " + tk + " : " + os.environ[tk])
		
		if 'skip_deps' in data:
			if data['skip_deps'] == True:
				skipDepends = True
		if "depends_on" in data and skipDepends == False: #dependception
			if len(data["depends_on"])>0:
				self.logger.info("Building dependencies of '%s'" % (name))
				for libraryName in data["depends_on"]:
					if libraryName not in self.DEPENDS:
						raise MissingDependency("The dependency '{0}' of '{1}' does not exist in dependency config.".format( libraryName, name)) #sys.exc_info()[0]
					else:
						self.build_thing(libraryName,self.DEPENDS[libraryName],"DEPENDENCY")
		if 'is_dep_inheriter' in data:
			if data['is_dep_inheriter'] == True:
				return
						
		self.logger.info("Building {0} '{1}'".format(type,name))
		
		if 'warnings' in data:
			if len(data['warnings']) > 0:
				for w in data['warnings']:
					self.logger.warning(w)

		workDir = None
		renameFolder = None
		if 'rename_folder' in data:
			if data['rename_folder'] != None:
				renameFolder = data['rename_folder']
				
		if type == "PRODUCT": 
			self.cchdir(self.bitnessDir + "_products") #descend into x86_64_products
		else:
			self.cchdir(self.bitnessDir) #descend into x86_64
		
		if data["repo_type"] == "git":
			branch     = self.getValueOrNone(data,'branch')
			recursive  = self.getValueOrNone(data,'recursive_git')
			folderName = self.getValueOrNone(data,'folder_name')
			workDir    = self.git_clone(data["url"],folderName,renameFolder,branch,recursive)
		elif data["repo_type"] == "svn":
			workDir = self.svn_clone(data["url"],data["folder_name"],renameFolder)
		elif data['repo_type'] == 'mercurial':
			branch = self.getValueOrNone(data,'branch')
			workDir = self.mercurial_clone(data["url"],self.getValueOrNone(data,'folder_name'),renameFolder,branch)
		elif data["repo_type"] == "archive":
			if "folder_name" in data:
				workDir = self.download_unpack_file(data["url"],data["folder_name"],workDir)
			else:
				workDir = self.download_unpack_file(data["url"],None,workDir)
		elif data["repo_type"] == "none":
			if "folder_name" in data:
				workDir = data["folder_name"]
				os.makedirs(workDir, exist_ok=True)
			else:
				print("Error: When using repo_type 'none' you have to set folder_name as well.")
				exit(1)
		
		if workDir == None:
			print("Unexpected error when building {0}, please report this:".format(name), sys.exc_info()[0])
			raise

		if 'rename_folder' in data: # this should be moved inside the download functions, TODO.. but lazy
			if data['rename_folder'] != None:
				if not os.path.isdir(data['rename_folder']):
					shutil.move(workDir, data['rename_folder'])
				workDir = data['rename_folder']

		if 'download_header' in data:
			if data['download_header'] != None:
				for h in data['download_header']:
					self.downloadHeader(h)
					
		self.cchdir(workDir) #descend into x86_64/[DEPENDENCY_OR_PRODUCT_FOLDER]
		if 'debug_downloadonly' in data:
			self.cchdir("..")
			exit()
			
		self.defaultCFLAGS()
		oldPath = self.getKeyOrBlankString(os.environ,"PATH")
		currentFullDir = os.getcwd()

		if not self.anyFileStartsWith('already_configured'):
			if 'run_pre_patch' in data:
				if data['run_pre_patch'] != None:
					for cmd in data['run_pre_patch']:
						cmd = self.replaceVariables(cmd)
						self.logger.debug("Running pre-patch-command: '{0}'".format( cmd ))
						self.run_process(cmd)
		
		if 'source_subfolder' in data:
			if data['source_subfolder'] != None:
				if not os.path.isdir(data['source_subfolder']):
					os.makedirs(data['source_subfolder'], exist_ok=True)
				self.cchdir(data['source_subfolder'])
		
		if force_rebuild:
			self.removeAlreadyFiles()
				
		if 'debug_confighelp_and_exit' in data:
			if data['debug_confighelp_and_exit'] == True:
				self.bootstrap_configure()
				self.run_process("./configure --help")
				exit()

		if 'cflag_addition' in data:
			if data['cflag_addition'] != None:
				self.logger.debug("Adding '{0}' to CFLAGS".format( data['cflag_addition'] ))
				os.environ["CFLAGS"] = os.environ["CFLAGS"] + " " + data['cflag_addition']

		if 'custom_cflag' in data:
			if data['custom_cflag'] != None:
				self.logger.debug("Setting CFLAGS to '{0}'".format( data['custom_cflag'] ))
				os.environ["CFLAGS"] = data['custom_cflag']
				
		if 'custom_path' in data:
			if data['custom_path'] != None:
				self.logger.debug("Setting PATH to '{0}'".format( self.replaceVariables(data['custom_path']) ))
				os.environ["PATH"] = self.replaceVariables(data['custom_path'])

		if 'flipped_path' in data:
			if data['flipped_path'] == True:
				bef = os.environ["PATH"]
				os.environ["PATH"] = "{0}:{1}:{2}".format ( self.mingwBinpath, os.path.join(self.compilePrefix,'bin'), self.originalPATH ) #todo properly test this..
				self.logger.debug("Flipping path to: '{0}' from '{1}'".format(bef,os.environ["PATH"]))

		if 'env_exports' in data:
			if data['env_exports'] != None:
				for key,val in data['env_exports'].items():
					val = self.replaceVariables(val)
					prevEnv = ''
					if key in os.environ:
						prevEnv = os.environ[key]
					self.logger.debug("Environment variable '{0}' has been set from {1} to '{2}'".format( key, prevEnv, val ))
					os.environ[key] = val

		if 'patches' in data:
			if data['patches'] != None:
				for p in data['patches']:
					self.apply_patch(p[0],p[1],False,self.getValueByIntOrNone(p,2))

		if not self.anyFileStartsWith('already_ran_make'):
			if 'run_post_patch' in data:
				if data['run_post_patch'] != None:
					for cmd in data['run_post_patch']:
						cmd = self.replaceVariables(cmd)
						self.logger.debug("Running post-patch-command: '{0}'".format( cmd ))
						self.run_process(cmd)

		if 'needs_configure' in data:
			if data['needs_configure'] == True:
				self.configure_source(name,data)
		else:
			self.configure_source(name,data)

		if 'patches_post_configure' in data:
			if data['patches_post_configure'] != None:
				for p in data['patches_post_configure']:
					self.apply_patch(p[0],p[1],True)

		if 'is_cmake' in data:
			if data['is_cmake'] == True:
				self.cmake_source(name,data)

		if 'make_subdir' in data:
			if data['make_subdir'] != None:
				if not os.path.isdir(data['make_subdir']):
					os.makedirs(data['make_subdir'], exist_ok=True)
				self.cchdir(data['make_subdir'])

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
					self.logger.debug("Environment variable '{0}' has been UNSET!".format( key, val ))
					del os.environ[key]
					
		if 'flipped_path' in data:
			if data['flipped_path'] == True:
				bef = os.environ["PATH"]
				os.environ["PATH"] = "{0}:{1}".format ( self.mingwBinpath, self.originalPATH )
				self.logger.debug("Resetting flipped path to: '{0}' from '{1}'".format(bef,os.environ["PATH"]))

		if 'source_subfolder' in data:
			if data['source_subfolder'] != None:
				if not os.path.isdir(data['source_subfolder']):
					os.makedirs(data['source_subfolder'], exist_ok=True)
				self.cchdir(currentFullDir)

		if 'make_subdir' in data:
			if data['make_subdir'] != None:
				self.cchdir(currentFullDir)

		if 'cflag_addition' in data:
			if data['cflag_addition'] != None:
				self.defaultCFLAGS()

		if 'custom_cflag' in data:
			if data['custom_cflag'] != None:
				self.defaultCFLAGS()

		self.cchdir("..") #asecond into x86_64
		if type == "PRODUCT": 
			self.PRODUCTS[name]["_already_built"] = True
		else:
			self.DEPENDS[name]["_already_built"] = True
			
		self.logger.info("Building {0} '{1}': Done!".format(type,name))
		if 'debug_exitafter' in data:
			exit()
			
		if 'custom_path' in data:
			if data['custom_path'] != None:
				self.logger.debug("Re-setting PATH to '{0}'".format( oldPath ))
				os.environ["PATH"] = oldPath
			
		self.cchdir("..") #asecond into workdir
	#:
	def bootstrap_configure(self):
		if not os.path.isfile("configure"):
			if os.path.isfile("bootstrap.sh"):
				self.run_process('./bootstrap.sh')
			elif os.path.isfile("autogen.sh"):
				self.run_process('./autogen.sh')
			elif os.path.isfile("buildconf"):
				self.run_process('./buildconf')
			elif os.path.isfile("bootstrap"):
				self.run_process('./bootstrap')
			elif os.path.isfile("bootstrap"):
				self.run_process('./bootstrap')
			elif os.path.isfile("configure.ac"):
				self.run_process('autoreconf -fiv')
	
	def configure_source(self,name,data):
		touch_name = "already_configured_%s" % (self.md5(name,self.getKeyOrBlankString(data,"configure_options")))


		isWaf = False
		if 'is_waf' in data:
			if data['is_waf'] == True:
				isWaf = True

		if not os.path.isfile(touch_name):
			self.removeAlreadyFiles()
			self.removeConfigPatchDoneFiles()

			doBootStrap = True
			if 'do_not_bootstrap' in data:
				if data['do_not_bootstrap'] == True:
					doBootStrap = False

			if doBootStrap:
				if isWaf:
					if not os.path.isfile("waf"):
						if os.path.isfile("bootstrap.py"):
							self.run_process('./bootstrap.py')
				else:
					self.bootstrap_configure()

			configOpts = ''
			if 'configure_options' in data:
				configOpts = self.replaceVariables(data["configure_options"])
			self.logger.info("Configuring '{0}' with: {1}".format( name, configOpts ))

			confCmd = './configure'
			if isWaf:
				confCmd = './waf --color=yes configure'
			elif 'configure_path' in data:
				if data['configure_path'] != None:
					confCmd = data['configure_path']
			
			self.run_process('{0} {1}'.format(confCmd, configOpts))

			if 'run_post_configure' in data:
				if data['run_post_configure'] != None:
					for cmd in data['run_post_configure']:
						cmd = self.replaceVariables(cmd)
						self.logger.info("Running post-configure-command: '{0}'".format( cmd ))
						self.run_process(cmd)
			
			doClean = True
			if 'clean_post_configure' in data:
				if data['clean_post_configure'] == False:
					doClean = False

			if doClean:
				mCleanCmd = 'make clean'
				if isWaf:
					mCleanCmd = './waf --color=yes clean'
				self.run_process('{0} -j {1}'.format( mCleanCmd, _CPU_COUNT ),True)
			
			self.touch(touch_name)
			self.logger.info("Finsihed configuring '{0}'".format( name ))

	def apply_patch(self,url,type = "-p1", postConf = False, folderToPatchIn = None): #p1 for github, p0 for idk

		originalFolder = os.getcwd()
		
		if folderToPatchIn != None:
			self.cchdir(folderToPatchIn)
			self.logger.info("Moving to patch folder: {0}" .format( os.getcwd() ))
	
		fileName = os.path.basename(urlparse(url).path)

		if not os.path.isfile(fileName):
			self.logger.info("Downloading patch '{0}' to: {1}".format( url, fileName ))
			self.download_file(url,fileName)

		patch_touch_name = "%s.done" % (fileName)

		ignoreErr = False
		exitOn = True
		ignore = ""

		if postConf:
			patch_touch_name = patch_touch_name + "_past_conf"
			ignore = "-N "
			ignoreErr = True
			exitOn = False

		if not os.path.isfile(patch_touch_name):
			self.logger.info("Patching source uising: '{0}'".format( fileName ))
			self.run_process('patch {2}-{0} < "{1}"'.format(type, fileName, ignore ),ignoreErr,exitOn)
			self.touch(patch_touch_name)
			if not postConf:
				self.removeAlreadyFiles()
		else:
			self.logger.debug("Patch '{0}' already applied".format( fileName ))
			
		if folderToPatchIn != None:
			self.cchdir(originalFolder)
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
			
			self.run_process("make clean",True)

			self.touch(touch_name)


	def make_source(self,name,data):
		touch_name = "already_ran_make_%s" % (self.md5(name,self.getKeyOrBlankString(data,"make_options")))
		if not os.path.isfile(touch_name):

			isWaf = False
			if 'is_waf' in data:
				if data['is_waf'] == True:
					isWaf = True
					
			isRake = False
			if 'is_rake' in data:
				if data['is_rake'] == True:
					isRake = True

			mkCmd = 'make'
			if isWaf:
				mkCmd = './waf --color=yes'
			if isRake:
				mkCmd = 'rake'

			if os.path.isfile("configure"):
				self.run_process('{0} clean -j {0}'.format( mkCmd, _CPU_COUNT ),True)

			makeOpts = ''
			if 'make_options' in data:
				makeOpts = self.replaceVariables(data["make_options"])

			self.logger.info("Making '{0}' with: {1} in {2}".format( name, makeOpts, os.getcwd() ))

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
					
			isRake = False
			if 'is_rake' in data:
				if data['is_rake'] == True:
					isRake = True

			mkCmd = "make"
			if isWaf:
				mkCmd = "./waf"
			if isRake:
				mkCmd = "rake"

			self.run_process('{0} {1} {2} {3}'.format(mkCmd, installTarget, makeInstallOpts, cpcnt ))

			if 'run_post_install' in data:
				if data['run_post_install'] != None:
					for cmd in data['run_post_install']:
						cmd = self.replaceVariables(cmd)
						self.logger.info("Running post-install-command: '{0}'".format( cmd ))
						self.run_process(cmd)

			self.touch(touch_name)
	#:

	def defaultCFLAGS(self):
		self.logger.debug("Reset CFLAGS to: {0}".format( _ORIG_CFLAGS ) )
		os.environ["CFLAGS"] = _ORIG_CFLAGS
		os.environ["PKG_CONFIG_LIBDIR"] = ""
	#:

	def anyFileStartsWith(self,wild):
		for file in os.listdir('.'):
			if file.startswith(wild):
				return True
		return False

	def removeAlreadyFiles(self):
		for af in glob.glob("./already_*"):
			os.remove(af)
	#:

	def removeConfigPatchDoneFiles(self):
		for af in glob.glob("./*.diff.done_past_conf"):
			os.remove(af)
		for af in glob.glob("./*.patch.done_past_conf"):
			os.remove(af)
	#:
	def generateCflagString(self, prefix = ""):
		cfs = os.environ["CFLAGS"]
		cfs = cfs.split(' ')
		out = ''
		if len(cfs) >= 1:
			for c in cfs:
				out+=prefix + c + ' '
			out.rstrip(' ')
			return out
		return ''
			
	def replaceVariables(self,cmd):
	
		m = re.search(r'\!VAR\((.*)\)VAR!',cmd)
		if m != None:
			varName = m.groups()[0]
			if varName in self.VARIABLES:
				cmdReplacer = self.VARIABLES[varName]
				mr = re.sub(r"\!VAR\((.*)\)VAR!", r"{0}".format(cmdReplacer), cmd, flags=re.DOTALL)
				cmd = mr
				
		cmd = cmd.format(
			cmake_prefix_options       = self.cmakePrefixOptions,
			make_prefix_options        = self.makePrefixOptions,
			pkg_config_path            = self.pkgConfigPath,
			mingw_binpath              = self.mingwBinpath,
			cross_prefix_bare          = self.bareCrossPrefix,
			cross_prefix_full          = self.fullCrossPrefix,
			compile_prefix             = self.compilePrefix,
			offtree_prefix             = self.offtreePrefix,
			compile_target             = self.compileTarget,
			host_target                = self.hostTarget,
			bit_name                   = self.bitnessDir,
			bit_name2                  = self.bitnessDir2,
			bit_name3                  = self.bitnessDir3,
			bit_name_win               = self.winBitnessDir,
			bit_num                    = self.currentBitness,
			product_prefix             = self.fullProductDir,
			compile_prefix_sed_escaped = self.compilePrefix.replace("/","\\/"),
			make_cpu_count             = "-j {0}".format(self.cpuCount),
			original_cflags            = self.originalCflags,
			cflag_string               = self.generateCflagString('--extra-cflags='),
			current_path               = os.getcwd(),
			current_envpath            = self.getKeyOrBlankString(os.environ,"PATH")
		)
		# needed actual commands sometimes, so I made this custom command support, compareable to "``" in bash, very very shady.. needs testing, but seems to work just flawlessly.
		
		m = re.search(r'\!CMD\((.*)\)CMD!',cmd)
		if m != None:
			cmdReplacer = subprocess.check_output(m.groups()[0], shell=True).decode("utf-8").replace("\n","").replace("\r","")
			mr = re.sub(r"\!CMD\((.*)\)CMD!", r"{0}".format(cmdReplacer), cmd, flags=re.DOTALL)
			cmd = mr
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
			
	def getValueByIntOrNone(self,db,key):
		if key >= 0 and key < len(db):
			return db[key]
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
	def cchdir(self,dir):
		if self.debugMode:
			print("Changing dir from {0} to {1}".format(os.getcwd(),dir))
		os.chdir(dir)
VARIABLES = {
	'ffmpeg_base_config' : # the base for all ffmpeg configurations.
		'--arch={bit_name2} --target-os=mingw32 --cross-prefix={cross_prefix_bare} --pkg-config=pkg-config --disable-w32threads '
		'--enable-libsoxr --enable-fontconfig --enable-libass --enable-iconv --enable-libtwolame '
		'--extra-cflags=-DLIBTWOLAME_STATIC --enable-libzvbi --enable-libcaca --enable-libmodplug --extra-libs=-lstdc++ '
		'--extra-libs=-lpng --extra-libs=-loleaut32 --enable-libmp3lame --enable-version3 --enable-zlib '
		'--enable-librtmp --enable-libvorbis --enable-libtheora --enable-libspeex --enable-libopenjpeg '
		'--enable-gnutls --enable-libgsm --enable-libfreetype --enable-libopus --enable-bzlib '
		'--enable-libopencore-amrnb --enable-libopencore-amrwb --enable-libvo-amrwbenc --enable-libschroedinger '
		'--enable-libvpx --enable-libilbc --enable-libwavpack --enable-libwebp --enable-dxva2 --enable-avisynth '
		'--enable-gray --enable-libopenh264 --enable-netcdf --enable-libflite --enable-lzma --enable-libsnappy '
		'--enable-libzimg --enable-gpl --enable-libx264 --enable-libx265 --enable-frei0r --enable-filter=frei0r '
		'--enable-librubberband --enable-libvidstab --enable-libxavs --enable-libxvid --enable-libmfx --enable-avresample '
		'--extra-libs=-lpsapi --extra-libs=-lspeexdsp --enable-libgme --enable-runtime-cpudetect '
		'--enable-libmfx --enable-libfribidi --enable-libbs2b'
	,
}
PRODUCTS = {
	'x264_10bit' : {
		'repo_type' : 'git',
		'url' : 'https://git.videolan.org/git/x264.git',
		'rename_folder' : 'x264_10bit',
		'configure_options': '--host={compile_target} --enable-static --cross-prefix={cross_prefix_bare} --prefix={product_prefix}/x264_10bit.installed --enable-strip --enable-lavf --bit-depth=10 {cflag_string}',
		'env_exports': {
			'LAVF_LIBS' : '!CMD(pkg-config --libs libavformat libavcodec libavutil libswscale)CMD!',
			'LAVF_CFLAGS' : '!CMD(pkg-config --cflags libavformat libavcodec libavutil libswscale)CMD!',
			'SWSCALE_LIBS' : '!CMD(pkg-config --libs libswscale)CMD!',
		},
		'depends_on' : (
			'libffmpeg',
		),
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'x264' },
	},
	'cuetools' : {
		'repo_type' : 'git',
		'url' : 'https://github.com/svend/cuetools.git',
		'configure_options': '--host={compile_target} --prefix={product_prefix}/cuetools_git.installed --disable-shared --enable-static',
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'cuetools' },
	},
	'curl' : {
		'repo_type' : 'git',
		'url' : 'https://github.com/curl/curl',
		'rename_folder' : 'curl_git',
		'configure_options': '--enable-static --disable-shared --target={bit_name2}-{bit_name_win}-gcc --host={compile_target} --build=x86_64-linux-gnu --with-libssh2 --with-gnutls --prefix={product_prefix}/curl_git.installed --exec-prefix={product_prefix}/curl_git.installed',
		'depends_on': (
			'zlib', 'libssh2',
		),
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'cURL' },
	},
	'wget' : {
		'repo_type' : 'git',
		'url' : 'https://git.savannah.gnu.org/git/wget.git',
		'branch' : 'tags/v1.19.1', #switch to stable branch until the gnutls issue is resolved.
		'rename_folder' : 'wget_git',
		'configure_options': '--target={bit_name2}-{bit_name_win}-gcc --host={compile_target} --build=x86_64-linux-gnu --with-ssl=gnutls --enable-nls --enable-dependency-tracking --with-metalink --prefix={product_prefix}/wget_git.installed --exec-prefix={product_prefix}/wget_git.installed',
		'cflag_addition' : '-DGNUTLS_INTERNAL_BUILD -DIN6_ARE_ADDR_EQUAL=IN6_ADDR_EQUAL',
		#'patches_post_configure' : ( this patch idea is on hold for now.. too fiddly.
		#	('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/wget_1.19.1.18_strip_version.patch', 'p1'),
		#)
		'depends_on': (
			'zlib', 'gnutls'
		),
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'wget' },
	},
	'aria2' : {
		'repo_type' : 'git',
		'url' : 'https://github.com/aria2/aria2.git',
		'configure_options':
			' --host={compile_target} --prefix={product_prefix}/aria2_git.installed'
			' --without-included-gettext --disable-nls --disable-shared --enable-static'
			' --without-openssl --with-libexpat --with-libz --with-libgmp --without-libgcrypt'
			' --with-sqlite3 --with-libxml2'	
			' --without-libnettle --with-cppunit-prefix={compile_prefix} ARIA2_STATIC=yes' # --without-gnutls --with-libssh2 --with-libcares
		,
		'run_post_patch' : [
			'autoreconf -fiv'
		],
		'run_post_install': [
			'{cross_prefix_bare}strip -v {product_prefix}/aria2_git.installed/bin/aria2c.exe',
		],
		'depends_on': [
			'zlib', 'libxml2', 'expat', 'gmp', 'gnutls', 'libsqlite3', 'libssh2', # 'c-ares', 'libsqlite3', 'openssl_1_1'
		],
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'aria2' },
	},
	'ffmpeg_static' : {
		'repo_type' : 'git',
		'url' : 'git://git.ffmpeg.org/ffmpeg.git',
		'rename_folder' : 'ffmpeg_static_git',
		'configure_options': '!VAR(ffmpeg_base_config)VAR! --enable-libbluray --prefix={product_prefix}/ffmpeg_static_git.installed --disable-shared --enable-static',
		'depends_on': [ 'ffmpeg_depends' ],
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'ffmpeg (static)' },
	},
	'ffmpeg_static_opencl' : {
		'repo_type' : 'git',
		'url' : 'git://git.ffmpeg.org/ffmpeg.git',
		'rename_folder' : 'ffmpeg_static_opencl_git',
		'configure_options': '!VAR(ffmpeg_base_config)VAR! --enable-libbluray --prefix={product_prefix}/ffmpeg_static_opencl_git.installed --disable-shared --enable-static --enable-opencl',
		'depends_on': [ 'ffmpeg_depends', 'opencl_icd' ],
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'ffmpeg (static (OpenCL))' },
	},
	'ffmpeg_static_non_free_opencl' : { # with decklink, fdk-aac and opencl
		'repo_type' : 'git',
		'url' : 'git://git.ffmpeg.org/ffmpeg.git',
		'rename_folder' : 'ffmpeg_static_non_free_opencl',
		'configure_options': '!VAR(ffmpeg_base_config)VAR! --enable-libbluray --prefix={product_prefix}/ffmpeg_static_non_free_opencl.installed --disable-shared --enable-static --enable-opencl --enable-nonfree --enable-libfdk-aac --enable-decklink',
		'depends_on': [ 'ffmpeg_depends', 'decklink_headers', 'fdk_aac', 'opencl_icd' ],
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'ffmpeg NonFree (static (OpenCL))' },
	},
	'ffmpeg_shared' : {
		'repo_type' : 'git',
		'url' : 'git://git.ffmpeg.org/ffmpeg.git',
		'rename_folder' : 'ffmpeg_shared_git',
		'configure_options': '!VAR(ffmpeg_base_config)VAR! --prefix={product_prefix}/ffmpeg_shared_git.installed --enable-shared --disable-static --disable-libgme',
		'depends_on': [ 'ffmpeg_depends' ],
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'ffmpeg (shared)' },
	},
	'vlc' : { # not working
		'repo_type' : 'git',
		'url' : 'https://github.com/videolan/vlc.git', # https://git.videolan.org/git/vlc.git is slow..
		'configure_options':
			'--host={compile_target} --prefix={product_prefix}/vlc_git.installed --disable-lua --enable-qt --disable-ncurses --disable-dbus --disable-sdl --disable-telx --enable-nls LIBS="-lbcrypt -lbz2"'
		,
		'depends_on' : [
			'lua', 'a52dec',
		],
		# 'patches' : [
			# ('https://raw.githubusercontent.com/Alexpux/MINGW-packages/master/mingw-w64-vlc-git/0002-MinGW-w64-lfind-s-_NumOfElements-is-an-unsigned-int.patch','p1'),
			# ('https://raw.githubusercontent.com/Alexpux/MINGW-packages/master/mingw-w64-vlc-git/0003-MinGW-w64-don-t-pass-static-to-pkg-config-if-SYS-min.patch','p1'),
			# ('https://raw.githubusercontent.com/Alexpux/MINGW-packages/master/mingw-w64-vlc-git/0004-Revert-Win32-prefer-the-static-libraries-when-creati.patch','p1'),
		# ],
		'env_exports' : {
			'LIBS' : '-lbcrypt -lbz2', # add the missing bcrypt Link, is windows SSL api, could use gcrypt or w/e idk what that lib is, i'd probably rather use openssl_1_1
		},
		'download_header' : [
			'https://raw.githubusercontent.com/gongminmin/UniversalDXSDK/master/Include/dxgi1_3.h',
			'https://raw.githubusercontent.com/gongminmin/UniversalDXSDK/master/Include/dxgi1_4.h',
			'https://raw.githubusercontent.com/gongminmin/UniversalDXSDK/master/Include/dxgi1_5.h',
			'https://raw.githubusercontent.com/gongminmin/UniversalDXSDK/master/Include/dxgi1_6.h',
		],
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'VLC (git)' },
		'_disabled' : True,
	},
	'x265_10bit' : {
		'repo_type' : 'mercurial',
		'url' : 'https://bitbucket.org/multicoreware/x265',
		'rename_folder' : 'x265_10bit',
		'cmake_options': '. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={product_prefix}/x265_10bit.installed -DENABLE_SHARED=OFF -DHIGH_BIT_DEPTH=ON -DCMAKE_AR={cross_prefix_full}ar',
		'needs_configure' : False,
		'is_cmake' : True,
		'source_subfolder': 'source',
		'_info' : { 'version' : 'mercurial (default)', 'fancy_name' : 'x265' },
	},
	'x265_multibit' : {
		'repo_type' : 'mercurial',
		'url' : 'https://bitbucket.org/multicoreware/x265',
		'rename_folder' : 'x265_multibit',
		'source_subfolder': 'source',
		'cmake_options': '. {cmake_prefix_options} -DCMAKE_AR={cross_prefix_full}ar -DENABLE_SHARED=OFF -DEXTRA_LIB="x265_main10.a;x265_main12.a" -DEXTRA_LINK_FLAGS="-L{offtree_prefix}/libx265_10bit/lib;-L{offtree_prefix}/libx265_12bit/lib" -DLINKED_10BIT=ON -DLINKED_12BIT=ON -DCMAKE_INSTALL_PREFIX={product_prefix}/x265_multibit.installed',
		'needs_configure' : False,
		'is_cmake' : True,
		'_info' : { 'version' : 'mercurial (default)', 'fancy_name' : 'x265 (multibit 12/10/8)' },
		'depends_on' : [ 'libx265_multibit_10', 'libx265_multibit_12' ],
	},
	'mkvtoolnix': {
		'repo_type' : 'git',
		'recursive_git' : True,
		'is_rake' : True,
		'url' : 'https://github.com/mbunkus/mkvtoolnix.git',
		'configure_options':
			'--host={compile_target} --prefix={product_prefix}/mkvtoolnix_git.installed --disable-shared --enable-static'
			' --with-boost={compile_prefix} --with-boost-system=boost_system --with-boost-filesystem=boost_filesystem --with-boost-date-time=boost_date_time --with-boost-regex=boost_regex --enable-optimization --enable-qt --enable-static-qt'
			' --with-moc={mingw_binpath}/moc --with-uic={mingw_binpath}/uic --with-rcc={mingw_binpath}/rcc --with-qmake={mingw_binpath}/qmake'
			' QT_LIBS="-lws2_32 -lprcre"'
		,
		'depends_on' : [
			'libfile','libflac','boost','qt5', 'gettext'
		],
		'packages': {
			'ubuntu' : [ 'xsltproc', 'docbook-utils', 'rake' ],
		},
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'mkvtoolnix' },
	},
	'flac' : {
		'repo_type' : 'git',
		'url' : 'https://git.xiph.org/flac.git',
		'configure_options': '--host={compile_target} --prefix={product_prefix}/flac_git.installed --disable-shared --enable-static',
		'depends_on': [
			'libogg',
		],
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'FLAC' },
		'packages': {
			'ubuntu' : [ 'docbook-to-man' ],
		},
	},
	'lame3' : {
		'repo_type' : 'archive',
		'url' : 'https://sourceforge.net/projects/lame/files/lame/3.99/lame-3.99.5.tar.gz',
		'patches' : (
			('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/lame-3.99.5.patch', 'p0'),
		),
		'configure_options': '--host={compile_target} --prefix={product_prefix}/lame-3.99.5.installed --disable-shared --enable-static --enable-nasm',
	},
	'vorbis-tools' : {
		'repo_type' : 'git',
		'url' : 'https://github.com/xiph/vorbis-tools.git',
		'configure_options': '--host={compile_target} --prefix={product_prefix}/vorbis-tools_git.installed --disable-shared --enable-static --without-libintl-prefix',
		'patches' : (
			('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/vorbis_tools_odd_locale.patch','p1'),
		),
		'depends_on': [
			'libvorbis',
		],
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'vorbis-tools' },
	},
	'sox' : {
		'repo_type' : 'git',
		'rename_folder' : 'sox_git',
		'url' : 'git://git.code.sf.net/p/sox/code',
		'configure_options': '--host={compile_target} --prefix={product_prefix}/sox_git.installed --disable-shared --enable-static --without-gsm',
		'run_post_patch' : (
			'autoreconf -fiv',
			'if [ -f "{compile_prefix}/lib/libgsm.a" ] ; then mv {compile_prefix}/lib/libgsm.a {compile_prefix}/lib/libgsm.a.disabled ; fi',
			'if [ -d "{compile_prefix}/include/gsm" ] ; then mv {compile_prefix}/include/gsm {compile_prefix}/include/gsm.disabled ; fi',
		),
		'run_post_install' : (
			'if [ -f "{compile_prefix}/lib/libgsm.a.disabled" ] ; then mv {compile_prefix}/lib/libgsm.a.disabled {compile_prefix}/lib/libgsm.a ; fi',
			'if [ -d "{compile_prefix}/include/gsm.disabled" ] ; then mv {compile_prefix}/include/gsm.disabled {compile_prefix}/include/gsm ; fi',
		),
		'depends_on': [
			'libvorbis','gettext',
		],
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'SoX' },
	},
	'mpd' : { # doesn't compile, feel free to contribute patches or w/e if you care.
		'repo_type' : 'git',
		'url' : 'https://github.com/MaxKellermann/MPD.git',
		'configure_options' : '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static --disable-wavpack --disable-gme --disable-bzip2 --disable-cdio-paranoia --disable-sqlite --enable-silent-rules --disable-icu LDFLAGS="-static" LIBS="-static-libgcc -static-libstdc++ -lz -lole32"',
		'env_exports' : {
			'LDFLAGS' : '-static',
			'LIBS' : '-static-libgcc -static-libstdc++ -lz -lole32',
			'CXXFLAGS' : '-O2 -g',
		},
		'_disabled' : True,
	},
	'clementine' : { # requires qt4....... so no. we'll keep it for future reference.
		'repo_type' : 'git',
		'url' : 'https://github.com/clementine-player/Clementine.git',
		'needs_configure' : False,
		'needs_make_install':False,
		'is_cmake' : True,
		'cmake_options': '. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={compile_prefix} -DBUILD_SHARED_LIBS=OFF',
		'depends_on': [
			'qt4',
		],
		'_disabled': True,
	},
	'amarok' : { # requires qt4....... so no. we'll keep it for future reference.
		'repo_type' : 'git',
		'url' : 'git://anongit.kde.org/amarok.git',
		'needs_configure' : False,
		'needs_make_install':False,
		'is_cmake' : True,
		'cmake_options': '. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={compile_prefix}',
		# 'custom_cflag' : '-DTAGLIB_STATIC',
		'env_exports' : {
			'CPPDEFINES' : '-DTAGLIB_STATIC',
			# build.env.Append(CPPDEFINES = 'TAGLIB_STATIC')
		},
		'depends_on': [
			'taglib',
		],
	},
	
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
		'configure_options':
			'--enable-libmpv-shared --disable-debug-build --prefix={product_prefix}/mpv_git.installed'
			' --enable-sdl2 --enable-egl-angle-lib --enable-rubberband --enable-lcms2 --enable-dvdread --enable-openal --enable-dvdnav'
			' --enable-libbluray --enable-cdda --enable-libass --enable-lua --enable-encoding --enable-uchardet --enable-libarchive'
			' --enable-encoding TARGET={compile_target} DEST_OS=win32',
		'depends_on' : (
			'angle', 'python36_libs', 'vapoursynth_libs','sdl2_hg', 'libffmpeg', 'luajit', 'lcms2', 'libdvdnav', 'libbluray', 'openal-soft', 'libass', 'libcdio-paranoia', 'libjpeg-turbo', 'uchardet', 'libarchive',
		),
		'run_post_configure': (
			'sed -i.bak -r "s/(--prefix=)([^ ]+)//g;s/--color=yes//g" build/config.h',
		),
		'run_post_install': (
			'{cross_prefix_bare}strip -v {product_prefix}/mpv_git.installed/bin/mpv.com',
			'{cross_prefix_bare}strip -v {product_prefix}/mpv_git.installed/bin/mpv.exe',
			'{cross_prefix_bare}strip -v {product_prefix}/mpv_git.installed/bin/mpv-1.dll',
		),
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'mpv' },
	},
	'mediainfo' : {
		'repo_type' : 'git',
		'branch' : 'v0.7.94',
		'custom_cflag' : '',
		'recursive_git' : True,
		'url' : 'https://github.com/MediaArea/MediaInfo.git',
		'source_subfolder' : 'Project/GNU/CLI',
		'rename_folder' : 'mediainfo_git',
		'configure_options': '--host={compile_target} --prefix={product_prefix}/mediainfo_git.installed --disable-shared --disable-static-libs',
		'depends_on': [
			'libmediainfo',
		],
		'run_post_configure' : [
			'sed -i.bak \'s/ -DSIZE_T_IS_LONG//g\' Makefile',
		],
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'MediaInfo' },
		'_disabled' : True,
	},
	'filezilla' : { # note, this builds fine on my build-box running ubuntu 17.04 64-bit .. I did not yet test this on any other system.
		'repo_type' : 'svn',
		'folder_name' : 'filezilla_svn',
		'url' : 'https://svn.filezilla-project.org/svn/FileZilla3/trunk',
		'configure_options': '--host={compile_target} --prefix={product_prefix}/filezilla_svn.installed --disable-shared --enable-static --disable-manualupdatecheck --disable-autoupdatecheck --with-pugixml=builtin host_os=mingw',
		'run_post_patch' : [
			'autoreconf -fiv',
			'sed -i.bak \'s/extern _SYM_EXPORT gnutls_free/extern gnutls_free/\' "{compile_prefix}/include/gnutls/gnutls.h"', #edit gnutls.h and remove the _SYM_EXPORT part apparently...? : https://forum.filezilla-project.org/viewtopic.php?t=1227&start=180
		],
		'depends_on' : [ 'libfilezilla', 'gnutls', 'wxwidgets', 'libsqlite3' ],
		'env_exports' : {
			'LIBGNUTLS_LIBS' : '"-L{compile_prefix}/lib -lgnutls -lnettle -lhogweed -lgmp -lcrypt32 -lws2_32 -lz"',
			'LIBS' : '-lgnutls',
			'CXXFLAGS' : '-g -Wall -O2',
		},
		'patches' : [
			('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/filezilla/0001-filezilla_svn_disable_32bit.patch','p1'),
		],
		'run_post_install' : [
			'mv "{compile_prefix}/include/gnutls/gnutls.h.bak" "{compile_prefix}/include/gnutls/gnutls.h"'
		],
		'packages': {
			'ubuntu' : [ 'wxrc' ],
		},
		'_info' : { 'version' : 'svn (master)', 'fancy_name' : 'FileZilla (64Bit only)' },
		
	},
	'youtube-dl' : {
		'repo_type' : 'git',
		'url' : 'https://github.com/rg3/youtube-dl.git',
		'install_options' : 'PREFIX="{product_prefix}/youtube-dl_git.installed"',
		'run_post_install' : [
			'if [ -f "{product_prefix}/youtube-dl_git.installed/bin/youtube-dl" ] ; then mv "{product_prefix}/youtube-dl_git.installed/bin/youtube-dl" "{product_prefix}/youtube-dl_git.installed/bin/youtube-dl.py" ; fi',
		],
		'needs_configure' : False,
		'packages': {
			'ubuntu' : [ 'pandoc' ],
		},
	},
	'mpv_gui_qt5' : {
		'repo_type' : 'git',
		'url' : 'https://github.com/DeadSix27/Baka-MPlayer',
		'rename_folder' : 'mpv_gui_qt5_git',
		'configure_options' :
			'CONFIG+=embed_translations lupdate="{host_target}/bin/lupdate" lrelease="{host_target}/bin/lrelease" PKG_CONFIG={cross_prefix_full}pkg-config INSTALL_ROOT={product_prefix}/mpv_gui_qt5_git.installed'
			' LIBS+=-L{host_target}/lib INCLUDEPATH+=-I{host_target}/include'
		,
		'run_post_patch' : [
			'cp -nv "/usr/bin/pkg-config" "{cross_prefix_full}pkg-config"'
		],
		'install_options' : 'INSTALL_ROOT={product_prefix}/mpv_gui_qt5_git.installed',
		'env_exports' : {
			'QTROOT' : '{host_target}/bin',
			'QMAKE' : '{host_target}/bin/qmake',
			'PKG_CONFIG' : '{cross_prefix_full}pkg-config'
		},
		'depends_on' : [
			'qt5', 'libmpv', 'libzip'
		],
	},
	'mediainfo_dll' : {
		# 'debug_downloadonly': True,
		'repo_type' : 'git',
		'branch' : 'v0.7.94',
		'source_subfolder' : 'Project/GNU/Library',
		'rename_folder' : 'mediainfo_dll',
		'url' : 'https://github.com/MediaArea/MediaInfoLib.git',
		'configure_options' : '--host={compile_target} --target={bit_name2}-{bit_name_win}-gcc --prefix={product_prefix}/mediainfo_dll.installed --disable-static --enable-shared', # --enable-static --disable-shared --enable-shared=no
		'run_post_patch' : [
			'sed -i.bak \'s/Windows.h/windows.h/\' ../../../Source/MediaInfo/Reader/Reader_File.h',
			'sed -i.bak \'s/Windows.h/windows.h/\' ../../../Source/MediaInfo/Reader/Reader_File.cpp',
		],
		'run_post_configure' : [
			'sed -i.bak \'s/ -DSIZE_T_IS_LONG//g\' Makefile',
		],
		'make_options': '{make_prefix_options}',
		'depends_on': [
			'zenlib', 'libcurl',
		],
		'patches' : [
			('libmediainfo-1-fixes.patch','p1', '../../..'),
		],
		'env_exports' : { 'PKG_CONFIG' : 'pkg-config' },
		#'_info' : { 'version' : 'git (master)', 'fancy_name' : 'MediaInfoDLL' },
	},
}
DEPENDS = {
	'zenlib' : {
		'repo_type' : 'git',
		'branch' : 'v0.4.35',
		'source_subfolder' : 'Project/GNU/Library',
		'url' : 'https://github.com/MediaArea/ZenLib.git',
		'configure_options' : '--host={compile_target} --prefix={compile_prefix} --enable-static --disable-shared --enable-shared=no',
		'run_post_configure' : [
			'sed -i.bak \'s/ -DSIZE_T_IS_LONG//g\' Makefile',
		],
		'patches' : (
			('libzen-1-fixes.patch', 'p1','../../..'),
		),
		# 'run_post_patch' : [
			# 'sed -i.bak \'/#include <windows.h>/ a\#include <time.h>\' ../../../Source/ZenLib/Ztring.cpp',
		# ],
		'_info' : { 'version' : 'git (v4.35)', 'fancy_name' : 'zenlib' },
	},
	'libfilezilla' : {
		'repo_type' : 'svn',
		'folder_name' : 'libfilezilla_svn',
		'url' : 'https://svn.filezilla-project.org/svn/libfilezilla/trunk',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'run_post_patch' : [
			'autoreconf -fiv',
		],
		'env_exports' : {
			'CXXFLAGS' : '-O0',
		},
		'_info' : { 'version' : 'svn (master)', 'fancy_name' : 'FileZilla (libary)' },
	},
	'freeglut' : {
		'repo_type' : 'archive',
		'url' : 'https://downloads.sourceforge.net/project/freeglut/freeglut/3.0.0/freeglut-3.0.0.tar.gz',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'needs_configure' : False,
		'cmake_options': '. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={compile_prefix} -DBUILD_SHARED_LIBS=OFF -DENABLE_STATIC_RUNTIME=ON -DFREEGLUT_GLES=OFF -DFREEGLUT_BUILD_DEMOS=OFF -DFREEGLUT_REPLACE_GLUT=ON -DFREEGLUT_BUILD_STATIC_LIBS=ON -DFREEGLUT_BUILD_SHARED_LIBS=OFF',
		'is_cmake' : True,
		'_info' : { 'version' : '3.7', 'fancy_name' : 'FreeGLUT (libary?)' },
	},
	
	'wxwidgets' : {
		'repo_type' : 'archive',
		'url' : 'https://github.com/wxWidgets/wxWidgets/releases/download/v3.0.3.1/wxWidgets-3.0.3.1.tar.bz2',
		'configure_options':
			' --host={compile_target} --build=x86_64-unknown-linux-gnu --prefix={host_target} --disable-shared --enable-static --build='
			' --with-msw --with-opengl --disable-mslu --enable-unicode --with-regex=builtin --disable-precomp-headers'
			' --enable-graphics_ctx --enable-webview --enable-mediactrl --with-libpng=sys --with-libxpm=builtin --with-libjpeg=sys'
			' --with-libtiff=builtin --without-mac --without-dmalloc --without-wine --with-sdl --with-themes=all --disable-stl --enable-threads --enable-gui'
		,
		# 'run_post_install' : [
			# 'cp -fv "{host_target}/bin/wxrc-3.0" "{host_target}/bin/wxrc"',
		# ],
		'patches' : [
			('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/wxwidgets/0001-wxWidgets-c++11-PR2222.patch','p1'),
		],
		'env_exports': {
			'CXXFLAGS' : '-std=gnu++11',
			'CXXCPP' : '{cross_prefix_bare}g++ -E -std=gnu++11',
		},
		'_info' : { 'version' : '3.0.3.1', 'fancy_name' : 'wxWidgets (libary)' },
		'depends_on' : [ 'libjpeg-turbo', 'libpng', 'zlib' ],
	},
	'ffmpeg_depends' : { # this is fake dependency used to just inherit other dependencies, you could make other programs depend on this and have a smaller config for example.
		'is_dep_inheriter' : True,
		'depends_on' : [
			'zlib', 'bzip2', 'liblzma', 'libzimg', 'libsnappy', 'libpng', 'gmp', 'libnettle', 'iconv', 'gnutls', 'frei0r', 'libsndfile', 'libbs2b', 'wavpack', 'libgme_game_music_emu', 'libwebp', 'flite', 'libgsm', 'sdl1', 'sdl2_hg',
			'libopus', 'opencore-amr', 'vo-amrwbenc', 'libogg', 'libspeexdsp', 'libspeex', 'libvorbis', 'libtheora', 'orc', 'libschroedinger', 'freetype2', 'expat', 'libxml2', 'libbluray', 'libxvid', 'xavs', 'libsoxr',
			'libx265_multibit', 'libopenh264', 'vamp_plugin', 'fftw3', 'libsamplerate', 'librubberband', 'liblame' ,'twolame', 'vidstab', 'netcdf', 'libcaca', 'libmodplug', 'zvbi', 'libvpx', 'libilbc', 'fontconfig', 'libfribidi', 'libass',
			'openjpeg', 'intel_quicksync_mfx', 'rtmpdump', 'libx264', 'libcdio',
		],
	},
	'taglib' : {
		'repo_type' : 'archive',
		'url' : 'http://taglib.org/releases/taglib-1.11.1.tar.gz',
		'needs_configure' : False,
		'is_cmake' : True,
		'cmake_options': '. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={compile_prefix} -DBUILD_SHARED_LIBS=OFF -DENABLE_STATIC_RUNTIME=ON -DWITH_MP4=ON -DWITH_ASF=ON',
	},
	
	'opencl_icd' : {
		'repo_type' : 'git',
		'url' : 'https://github.com/KhronosGroup/OpenCL-ICD-Loader.git',
		'needs_configure' : False,
		'needs_make_install':False,
		'is_cmake' : True,
		'cmake_options': '. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={compile_prefix} -DBUILD_SHARED_LIBS=OFF',
		'depends_on' : [ 'opencl_headers' ],
		'run_post_make' : [
			'if [ ! -f "already_ran_make_install" ] ; then cp -vf "libOpenCL.dll.a" "{compile_prefix}/lib/libOpenCL.dll.a" ; fi',
			'if [ ! -f "already_ran_make_install" ] ; then touch already_ran_make_install ; fi',
		],
		'patches' : [
			('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/opencl/0001-OpenCL-git-prefix.patch','p1'),
		],
	},
	'opencl_headers' : {
		'repo_type' : 'git',
		'url' : 'https://github.com/KhronosGroup/OpenCL-Headers.git',
		'run_post_patch' : (
			'if [ ! -f "already_ran_make_install" ] ; then if [ ! -d "{compile_prefix}/include/CL" ] ; then mkdir "{compile_prefix}/include/CL" ; fi ; fi',
			'if [ ! -f "already_ran_make_install" ] ; then cp -v *.h "{compile_prefix}/include/CL/" ; fi',
			'if [ ! -f "already_ran_make_install" ] ; then touch already_ran_make_install ; fi',
		),
		'needs_make':False,
		'needs_make_install':False,
		'needs_configure':False,
	},
	'libzip' : {
		'repo_type' : 'git',
		'url' : 'https://github.com/nih-at/libzip.git',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'patches' : [
			('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/libzip/0001-libzip-git-20170415-fix-static-build.patch','p1'),
		],
		'run_post_patch' : (
			'autoreconf -fiv',
		),
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'libjpeg-turbo' },
	},
	'libmpv' : {
		'repo_type' : 'git',
		'url' : 'https://github.com/mpv-player/mpv.git',
		'is_waf' : True,
		'rename_folder' : "libmpv_git",
		'env_exports' : {
			'DEST_OS' : 'win32',
			'TARGET'  : '{compile_target}',
		},
		'run_post_patch' : (
			'cp -nv "/usr/bin/pkg-config" "{cross_prefix_full}pkg-config"',
		),
		'configure_options':
			'--enable-libmpv-shared --disable-debug-build --prefix={compile_prefix}'
			' --enable-sdl2 --enable-egl-angle-lib --enable-rubberband --enable-lcms2 --enable-dvdread --enable-openal --enable-dvdnav'
			' --enable-libbluray --enable-cdda --enable-libass --enable-lua --enable-encoding --enable-uchardet --enable-libarchive'
			' TARGET={compile_target} DEST_OS=win32',
		'depends_on' : (
			'angle', 'python36_libs', 'vapoursynth_libs', 'libffmpeg', 'luajit', 'lcms2', 'libdvdnav', 'libbluray', 'openal-soft', 'libass', 'libcdio-paranoia', 'libjpeg-turbo', 'uchardet', 'libarchive',
		),
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'mpv (library)' },
	},
	'libmediainfo' : {
		'repo_type' : 'git',
		'branch' : 'v0.7.94',
		'source_subfolder' : 'Project/GNU/Library',
		'url' : 'https://github.com/MediaArea/MediaInfoLib.git',
		'configure_options' : '--host={compile_target} --prefix={compile_prefix} --enable-shared --enable-static --with-libcurl --with-libmms --with-libmediainfo-name=MediaInfo.dll', # --enable-static --disable-shared --enable-shared=no
		'run_post_patch' : [
			'sed -i.bak \'s/Windows.h/windows.h/\' ../../../Source/MediaInfo/Reader/Reader_File.h',
			'sed -i.bak \'s/Windows.h/windows.h/\' ../../../Source/MediaInfo/Reader/Reader_File.cpp',
		],
		'run_post_configure' : [
			'sed -i.bak \'s/ -DSIZE_T_IS_LONG//g\' Makefile',
		],
		'depends_on': [
			'zenlib', 'libcurl',
		],
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'libmediainfo' },
	},
	'libssh2' : {
		'repo_type' : 'git',
		'url' : 'https://github.com/libssh2/libssh2.git',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static --without-openssl',
		'env_exports' : {
			'LIBS' : '-lbcrypt' # add the missing bcrypt Link, is windows SSL api, could use gcrypt or w/e idk what that lib is, i'd probably rather use openssl_1_1
		},
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'libssh2' },
	},
	'libsqlite3' : {
		'repo_type' : 'archive',
		'cflag_addition' : '-fexceptions -DSQLITE_ENABLE_COLUMN_METADATA=1 -DSQLITE_USE_MALLOC_H=1 -DSQLITE_USE_MSIZE=1 -DSQLITE_DISABLE_DIRSYNC=1 -DSQLITE_ENABLE_RTREE=1 -fno-strict-aliasing',
		'url' : 'https://sqlite.org/2017/sqlite-autoconf-3180000.tar.gz',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static --enable-threadsafe --disable-editline --enable-readline --enable-json1 --enable-fts5 --enable-session',
		'depends_on': (
			'zlib',
		),
		'_info' : { 'version' : '3.1.8', 'fancy_name' : 'libsqlite3)' },
	},
	'libcurl' : {
		'repo_type' : 'git',
		'url' : 'https://github.com/curl/curl',
		'rename_folder' : 'curl_git',
		'configure_options': '--enable-static --disable-shared --target={bit_name2}-{bit_name_win}-gcc --host={compile_target} --build=x86_64-linux-gnu --with-libssh2 --with-gnutls --prefix={compile_prefix} --exec-prefix={compile_prefix}',
		'depends_on': (
			'zlib',
		),
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'libcurl' },
	},
	'boost' : { # oh god no.. 
		'repo_type' : 'archive',
		'url' : 'https://sourceforge.net/projects/boost/files/boost/1.64.0/boost_1_64_0.tar.bz2',
		'needs_make':False,
		'needs_make_install':False,
		'needs_configure':False,
		'run_post_patch': ( # this is a very good example for a fully custom dependency
			'if [ ! -f "already_configured_0" ] ; then ./bootstrap.sh mingw --prefix={compile_prefix} ; fi',
			'if [ ! -f "already_configured_0" ] ; then sed -i.bak \'s/case \*       : option = -pthread ; libs = rt ;/case *      : option = -pthread ;/\' tools/build/src/tools/gcc.jam ; fi',
			'if [ ! -f "already_configured_0" ] ; then touch already_configured_0 ; fi',
			'if [ ! -f "already_ran_make_0" ] ; then'
				' echo "using gcc : mingw : {cross_prefix_bare}g++ : <rc>{cross_prefix_bare}windres <archiver>{cross_prefix_bare}ar <ranlib>{cross_prefix_bare}ranlib ;" > user-config.jam'
			' ; fi',
			'if [ ! -f "already_ran_make_0" ] ; then'
				' ./b2 toolset=gcc-mingw link=static threading=multi target-os=windows --prefix={compile_prefix} variant=release --with-system --with-filesystem --with-regex --with-date_time --with-thread --user-config=user-config.jam install'
			' ; fi',
			#'if [ ! -f "already_ran_make_0" ] ; then'
			#	' ./b2 -a -d+2 --debug-configuration --prefix={compile_prefix} variant=release target-os=windows toolset=gcc-mingw address-model=64'
			#	' link=shared runtime-link=shared threading=multi threadapi=win32 architecture=x86 binary-format=pe --with-system --with-filesystem --with-regex'
			#	' --with-date_time --with-thread --with-test --user-config=user-config.jam install'
			#' ; fi',
			#'if [ ! -f "already_ran_make_0" ] ; then'
			#	' ./b2 -a -d+2 --debug-configuration --prefix={compile_prefix} variant=debug target-os=windows toolset=gcc-mingw address-model=64'
			#	' link=shared runtime-link=shared threading=multi threadapi=win32 architecture=x86 binary-format=pe boost.locale.winapi=on boost.locale.std=on'
			#	' boost.locale.icu=on boost.locale.iconv=on boost.locale.posix=off --with-locale --user-config=user-config.jam install'
			#' ; fi',
			'if [ ! -f "already_ran_make_0" ] ; then touch already_ran_make_0 ; fi',
		),
		'_info' : { 'version' : '1.64', 'fancy_name' : 'Boost' },
	},
	'angle' : { # implenting gyp support just for this would be a waste of time, so a mnaual process shall suffice.
		'repo_type' : 'git',
		'url' : 'https://chromium.googlesource.com/angle/angle',
		'patches' : (
			#('https://raw.githubusercontent.com/shinchiro/mpv-winbuild-cmake/master/packages/angle-0001-custom-gyp.patch','p1'),
			#('https://raw.githubusercontent.com/shinchiro/mpv-winbuild-cmake/master/packages/angle-0002-install.patch','p1'),
			#('https://raw.githubusercontent.com/shinchiro/mpv-winbuild-cmake/master/packages/angle-0003-add-option-for-targeting-cpu-architecture.patch','p1'),
			('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/angle-0001-Cross-compile-hacks-for-mpv.patch','p1'),
			('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/angle-0002-std-c-14-is-required-for-GCC-lt-6.patch','p1'),
			('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/angle-0004-string_utils-cpp.patch','p1'),
			#('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/angle-0003-RendererD3D-cpp.patch','p1'),
		),
		'branch' : 'origin/chromium/3103', 
		'needs_make':False,
		'needs_make_install':False,
		'needs_configure':False,
		#'run_pre_patch' : {
		#	'if [ -f "Makefile" ] ; then make uninstall PREFIX={compile_prefix} ; fi',
		#	'if [ -f "Makefile" ] ; then rm Makefile ; fi',
		#	'if [ ! -f "already_done" ] ; then git clean -fxd ; fi',
		#	'if [ ! -f "already_done" ] ; then git reset --hard origin/master ; fi',
		#},
		'run_post_patch': (
			'if [ ! -f "already_done" ] ; then sed -i.bak \'s/sprintf_s(adapterLuidString/sprintf(adapterLuidString/\' "src/libANGLE/renderer/d3d/RendererD3D.cpp" ; fi',
			'if [ ! -f "already_done" ] ; then make uninstall PREFIX={compile_prefix} ; fi',
			'if [ ! -f "already_done" ] ; then cmake -E remove_directory generated ; fi',			
			'if [ ! -f "already_done" ] ; then gyp -Duse_ozone=0 -DOS=win -Dangle_gl_library_type=static_library -Dangle_use_commit_id=1 --depth . -I gyp/common.gypi src/angle.gyp --no-parallel --format=make --generator-output=generated -Dangle_enable_vulkan=0 -Dtarget_cpu=x64 ; fi',
			'if [ ! -f "already_done" ] ; then make -C generated/ commit_id ; fi',
			'if [ ! -f "already_done" ] ; then cmake -E copy generated/out/Debug/obj/gen/angle/id/commit.h src/id/commit.h ; fi',
			'if [ ! -f "already_done" ] ; then make -C generated {make_prefix_options} BUILDTYPE=Release {make_cpu_count} ; fi',
			'if [ ! -f "already_done" ] ; then chmod u+x ./move-libs.sh && ./move-libs.sh {bit_name}-w64-mingw32 ; fi',
			'if [ ! -f "already_done" ] ; then make install PREFIX={compile_prefix} ; fi',
			'if [ ! -f "already_done" ] ; then touch already_done ; fi',
		),
		'packages': {
			'ubuntu' : [ 'gyp' ],
		},
		'_info' : { 'version' : 'git (3103)', 'fancy_name' : 'Angle' },
	},
	#'angle_full' : { # ugh
	#	'repo_type' : 'git',
	#	'url' : 'https://chromium.googlesource.com/angle/angle',
	#	'patches' : (
	#		('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/angle-0001-Cross-compile-hacks-for-mpv.patch','p1'),
	#		('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/angle-0002-std-c-14-is-required-for-GCC-lt-6.patch','p1'),
	#		('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/angle-0003-RendererD3D-cpp.patch','p1'),
	#		('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/angle-0004-string_utils-cpp.patch','p1'),
	#	),
	#	'recursive_git' : True,
	#	'needs_make':False,
	#	'needs_make_install':False,
	#	'needs_configure':False,
	#	'custom_path' : '{current_path}/depot_tools:{current_envpath}',
	#	'env_exports' : {
	#		'GYP_GENERATORS':'ninja',
	#		'AR' : '{cross_prefix_bare}ar',
	#		'CC' : '{cross_prefix_bare}gcc',
	#		'PREFIX' : '{compile_prefix}',
	#		'RANLIB' : '{cross_prefix_bare}ranlib',
	#		'LD'     : '{cross_prefix_bare}ld',
	#		'STRIP'  : '{cross_prefix_bare}strip',
	#		'CXX'    : '{cross_prefix_bare}g++',
	#	},
	#	'run_post_patch': (
	#		'if [ ! -f "already_done"                             ] ; then echo $PATH ; fi',
	#		'if [ ! -f "already_done"                             ] ; then make uninstall PREFIX={compile_prefix} ; fi',
	#		'if [ ! -f "already_done"                             ] ; then cmake -E remove_directory generated ; fi',
	#		'if [ ! -d "depot_tools"                              ] ; then git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git ; fi',
	#		'if [ ! -f "already_done"                             ] ; then python scripts/bootstrap.py ; fi',
	#		# 'if [ ! -d "third_party/vulkan-validation-layers/src" ] ; then git clone https://github.com/KhronosGroup/Vulkan-LoaderAndValidationLayers.git third_party/vulkan-validation-layers/src ; fi',
	#		# 'if [ ! -d "third_party/glslang-angle/src"            ] ; then git clone https://github.com/google/glslang.git third_party/glslang-angle/src ; fi',
	#		# 'if [ ! -d "third_party/deqp/src"                     ] ; then git clone -b deqp-dev https://android.googlesource.com/platform/external/deqp/ third_party/deqp/src ; fi',
	#		# 'if [ ! -d "third_party/spirv-headers/src"            ] ; then git clone https://github.com/KhronosGroup/SPIRV-Headers.git third_party/spirv-headers/src ; fi',
	#		'if [ ! -d "third_party/spirv-tools-angle/src"        ] ; then git clone https://chromium.googlesource.com/external/github.com/KhronosGroup/SPIRV-Tools third_party/spirv-tools-angle/src ; fi',
	#		'if [ ! -f "already_done"                             ] ; then gyp -Duse_ozone=0 -Duse_x11=0 -DOS=win -Dangle_gl_library_type=static_library --depth . -I gyp/common.gypi src/angle.gyp --generator-output=generated -Dangle_enable_vulkan=1 ; fi',
	#		'if [ ! -f "already_done"                             ] ; then ninja -C generated/out/Release_x64 -j 4 ; fi',
	#		
	#		#'if [ ! -f "already_done" ] ; then make -C generated/ commit_id ; fi',
	#		#'if [ ! -f "already_done" ] ; then cmake -E copy generated/out/Debug/obj/gen/angle/id/commit.h src/id/commit.h ; fi',
	#		#'if [ ! -f "already_done" ] ; then make -C generated {make_prefix_options} BUILDTYPE=Release {make_cpu_count} ; fi',
	#		#'if [ ! -f "already_done" ] ; then chmod u+x ./move-libs.sh && ./move-libs.sh {bit_name}-w64-mingw32 ; fi',
	#		#'if [ ! -f "already_done" ] ; then make install PREFIX={compile_prefix} ; fi',
	#		#'if [ ! -f "already_done" ] ; then touch already_done ; fi',
	#	),
	#	'packages': {
	#		'ubuntu' : [ 'gyp' ],
	#	},
	#	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'Angle' },
	#},
	
	'qt5' : { # too... many.... patches....
		'warnings' : [
			'Qt5 buidling CAN fail sometimes with multiple threads.. so if this failed try re-running it',
			'For more information see: https://bugreports.qt.io/browse/QTBUG-53393',
			'(You could add \'cpu_count\' : \'1\', to the config of QT5 if the slower speed is acceptable for you)'
		],
		'clean_post_configure' : False,
		'repo_type' : 'archive',
		'url' : 'https://download.qt.io/official_releases/qt/5.8/5.8.0/single/qt-everywhere-opensource-src-5.8.0.tar.gz',
		'configure_options' :
			' -opensource'
			' -force-pkg-config'
			' -confirm-license'
			' -c++std c++11'
			' -xplatform win32-g++'
			' -device-option CROSS_COMPILE={cross_prefix_bare}'
			' -no-use-gold-linker'
			' -debug-and-release'
			' -static'
			' -hostprefix {host_target}'
			' -hostdatadir {host_target}/lib/qt'
			' -hostbindir {host_target}/bin'
			' -prefix {host_target}'
			' -bindir {host_target}/bin'
			' -archdatadir {host_target}/lib/qt'
			' -datadir {host_target}/share/qt'
			' -docdir {host_target}/share/doc/qt'
			' -examplesdir {host_target}/share/qt/examples'
			' -headerdir {host_target}/include/qt'
			' -libdir {host_target}/lib'
			' -plugindir {host_target}/lib/qt/plugins'
			' -sysconfdir {host_target}/etc'
			' -translationdir {host_target}/share/qt/translations'
			' -no-icu'
			' -opengl desktop'
			' -no-glib'
			' -accessibility'
			' -make tools'
			' -nomake examples'
			' -nomake tests'
			' -system-zlib'
			' -system-libjpeg'
			' -no-pch'
			' -no-dbus'
			' -no-direct2d'
			' -no-openssl'
			' !CMD(pkg-config --cflags-only-I freetype2 zlib)CMD!'
		,
		'custom_cflag' : '',
		'depends_on' : [ 'libwebp', 'freetype2', 'libpng', 'libjpeg-turbo', 'pcre'], #openssl, only supports 1.0.1, so no. https://wiki.qt.io/Qt_5.8_Tools_and_Versions # -openssl -openssl-linked -I{compile_prefix}/include/openssl -L{compile_prefix}/lib/
		'patches' : [ #thanks to the Arch & mxe community for some of those patches!: https://aur.archlinux.org/packages/mingw-w64-qt5-base-angle/                                                                                            'p0'),
			 ('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/qt5/base/qtbase-1-fixes_different.patch'                                                                        ,'p1','qtbase'),			
			 ('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/qt5/winextras/qtwinextras-1.patch'                                                                              ,'p1','qtwinextras'),
			 ('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/qt5/activeqt/qtactiveqt-1.patch'                                                                                ,'p1','qtactiveqt'),		
			#('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/qt5/winextras/0001-Fix-condition-for-_WIN32_IE-SHCreateItemFromParsingN.patch'                                  ,'p1','qtwinextras'),
			#('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/qt5/webengine/0044-qt-5.4.0-win32-g%2B%2B-enable-qtwebengine-build.patch'                                       ,'p1'),
			#('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/qt5/tools/0001-Fix-linguist-macro.patch'                                                                        ,'p1','qttools'),
			#('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/qt5/multimedia/0001-Recorder-includes-to-prevent-conflict-with-vsnprintf.patch'                                 ,'p1','qtmultimedia'),
			#('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/qt5/multimedia/0002-Fix-build-with-ANGLE.patch'                                                                 ,'p1','qtmultimedia'),
			#('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/qt5/location/0001-Ensure-static-3rdparty-libs-are-linked-correctly.patch'                                       ,'p1','qtlocation'),
			#('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/qt5/declarative/0001-Build-QML-dev-tools-as-shared-library.patch'                                               ,'p1','qtdeclarative'),
			#('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/qt5/declarative/0002-Ensure-static-plugins-are-exported.patch'                                                  ,'p1','qtdeclarative'),
			#('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/qt5/declarative/0003-Prevent-exporting-QML-parser-symbols-on-static-build.patch'                                ,'p1','qtdeclarative'),
			#('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/qt5/activeqt/qt5-activeqt-fix-compilation.patch'                                                                ,'p0','qtactiveqt'),
			#('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/qt5/activeqt/qtactiveqt-fix-build.patch'                                                                        ,'p1','qtactiveqt'),
			#('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/qt5/activeqt/qtactiveqt-win64.patch'                                                                            ,'p1','qtactiveqt'),
			#('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/qt5/base/0001-Add-profile-for-cross-compilation-with-mingw-w64.patch'                                           ,'p1','qtbase'),
			#('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/qt5/base/0002-Ensure-GLdouble-is-defined-when-using-dynamic-OpenGL.patch'                                       ,'p1','qtbase'),
			#('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/qt5/base/0003-Use-external-ANGLE-library.patch'                                                                 ,'p1','qtbase'),
			#('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/qt5/base/0004-Fix-too-many-sections-assemler-error-in-OpenGL-facto.patch'                                       ,'p1','qtbase'),
			 ('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/qt5/base/0005-Make-sure-.pc-files-are-installed-correctly.patch'                                                ,'p1','qtbase'),
			#('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/qt5/base/0006-Don-t-add-resource-files-to-LIBS-parameter.patch'                                                 ,'p1','qtbase'),
			 ('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/qt5/base/0007-Prevent-debug-library-names-in-pkg-config-files.patch'                                            ,'p1','qtbase'),
			#('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/qt5/base/0008_5-hacky_non_priv_libs.patch'                                                                      ,'p1','qtbase'),
			#('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/qt5/base/0008-Fix-linking-against-shared-static-libpng.patch'                                                   ,'p1','qtbase'),
			#('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/qt5/base/0009-Fix-linking-against-static-D-Bus.patch'                                                           ,'p1','qtbase'),
			 ('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/qt5/base/0010-Fix-linking-against-static-freetype2.patch'                                                       ,'p1','qtbase'),
			#('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/qt5/base/0011-Fix-linking-against-static-harfbuzz.patch'                                                        ,'p1','qtbase'),
			 ('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/qt5/base/0012-Fix-linking-against-static-pcre.patch'                                                            ,'p1','qtbase'),
			#('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/qt5/base/0013-Fix-linking-against-shared-static-MariaDB.patch'                                                  ,'p1','qtbase'),
			#('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/qt5/base/0014-Fix-linking-against-shared-static-PostgreSQL.patch'                                               ,'p1','qtbase'),
			#('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/qt5/base/0015-Rename-qtmain-to-qt5main.patch'                                                                   ,'p1','qtbase'),
			#('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/qt5/base/0016-Build-dynamic-host-libraries.patch'                                                               ,'p1','qtbase'),
			#('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/qt5/base/0017-Enable-rpath-for-build-tools.patch'                                                               ,'p1','qtbase'),
			#('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/qt5/base/0018-Use-system-zlib-for-build-tools.patch'                                                            ,'p1','qtbase'),
			#('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/qt5/base/0019-Disable-determing-default-include-and-lib-dirs-at-qm.patch'                                       ,'p1','qtbase'),
			#('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/qt5/base/0020-Use-.dll.a-as-import-lib-extension.patch'                                                         ,'p1','qtbase'),
			#('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/qt5/base/0021-Merge-shared-and-static-library-trees.patch'                                                      ,'p1','qtbase'),
			#('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/qt5/base/0022-Allow-usage-of-static-version-with-CMake.patch'                                                   ,'p1','qtbase'),
			#('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/qt5/base/0023-Use-correct-pkg-config-static-flag.patch'                                                         ,'p1','qtbase'),
			#('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/qt5/base/0024-Fix-qt5_wrap_ui-macro.patch'                                                                      ,'p1','qtbase'),
			#('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/qt5/base/0025-Ignore-errors-about-missing-feature-static.patch'                                                 ,'p1','qtbase'),
			#('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/qt5/base/0026-Enable-and-fix-use-of-iconv.patch'                                                                ,'p1','qtbase'),
			#('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/qt5/base/0027-Ignore-failing-pkg-config-test.patch'                                                             ,'p1','qtbase'),
			#('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/qt5/base/0028-Include-uiviewsettingsinterop.h-correctly.patch'                                                  ,'p1','qtbase'),
			#('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/qt5/base/0029-Hardcode-linker-flags-for-libqwindows.dll.patch'                                                  ,'p1','qtbase'),
			#('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/qt5/base/0030-Prevent-qmake-from-messing-static-lib-dependencies.patch'                                         ,'p1','qtbase'),
		],
		#'run_post_patch' : [
		#	'rm -rf src/3rdparty/angle include/QtANGLE/EGL',
		#	'rm -rf src/3rdparty/angle include/QtANGLE/GLES2',
		#	'rm -rf src/3rdparty/angle include/QtANGLE/GLES3',
		#	'rm -rf src/3rdparty/angle include/QtANGLE/KHR',
		#	'rm -rf src/3rdparty/pcre',
		#	'rm -rf src/3rdparty/zlib',
		#],
		#'run_post_patch' : [
		#	'if [ ! -f "{mingw_binpath}/pkg-config" ] ; then cp -nv "!CMD(which pkg-config)CMD!" "{mingw_binpath}/pkg-config" ; fi',
		#	'if [ ! -f "{compile_prefix}/include/UIViewSettingsInterop.h" ] ; then cp -nv "{compile_prefix}/include/uiviewsettingsinterop.h" "{compile_prefix}/include/UIViewSettingsInterop.h" ; fi', # no clue why its lower case and why qt5 doesn't know either #fatal error: UIViewSettingsInterop.h: No such file or directory
		#],
		'env_exports' : {
			'PKG_CONFIG' : '{cross_prefix_full}pkg-config',
			'PKG_CONFIG_SYSROOT_DIR' : '/',
			'PKG_CONFIG_LIBDIR' : '{compile_prefix}/lib/pkgconfig',
			'CROSS_COMPILE' : '{cross_prefix_bare}',
			#'OPENSSL_LIBS' : '!CMD({cross_prefix_full}pkg-config --libs-only-l openssl)CMD!',
		},
		'_info' : { 'version' : '5.8.0', 'fancy_name' : 'QT5' },
	},
	'libjpeg-turbo' : {
		'repo_type' : 'git',
		'url' : 'https://github.com/libjpeg-turbo/libjpeg-turbo.git',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static --with-jpeg8',
		'run_post_patch' : (
			'autoreconf -fiv',
		),
		'patches': [
			('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/libjpeg-turbo-1.3.1-header-compat.mingw.patch',  'p1'),
			('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/libjpeg-turbo-1.3.1-libmng-compatibility.patch', 'p1'),
		],
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'libjpeg-turbo' },
	},
	'libpng' : {
		'repo_type' : 'archive',
		'url' : 'https://sourceforge.net/projects/libpng/files/libpng16/1.6.29/libpng-1.6.29.tar.gz',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'patches' : [
			('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/libpng/libpng-1.6.29-apng.patch', 'p1'),
		],
		'depends_on' : [ 'zlib', ],
		'_info' : { 'version' : '1.6.29', 'fancy_name' : 'libpng' },
	},
	'harfbuzz' : {
		'repo_type' : 'archive',
		'url' : 'https://www.freedesktop.org/software/harfbuzz/release/harfbuzz-1.4.6.tar.bz2',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --with-freetype --disable-shared --with-icu=no --with-glib=no --with-gobject=no --disable-gtk-doc-html', #--with-graphite2 --with-cairo --with-icu --with-gobject 
		'env_exports' : {
			'CFLAGS'   : '-DGRAPHITE2_STATIC',
			'CXXFLAGS' : '-DGRAPHITE2_STATIC',
		},
		'_info' : { 'version' : '1.4.6', 'fancy_name' : 'harfbuzz' },
	},
	'pcre' : {
		'repo_type' : 'archive',
		'url' : 'https://ftp.pcre.org/pub/pcre/pcre-8.40.tar.gz',
		'configure_options' : '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static --enable-unicode-properties --enable-jit --enable-pcre16 --enable-pcre32 --enable-pcregrep-libz --enable-pcregrep-libbz2',
		'depends_on' : [
			'bzip2',
		],
		'_info' : { 'version' : '8.40', 'fancy_name' : 'pcre' },
	},
	
	'd-bus' : {
		'repo_type' : 'archive',
		'url' : 'https://dbus.freedesktop.org/releases/dbus/dbus-1.10.18.tar.gz',
		'configure_options' : '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static --with-xml=expat --disable-systemd --disable-tests --disable-Werror --disable-asserts --disable-verbose-mode --disable-xml-docs --disable-doxygen-docs --disable-ducktype-docs',
		'_info' : { 'version' : '1.10.18', 'fancy_name' : 'D-bus (Library)' },
	},
	'glib2' : {
		'repo_type' : 'archive',
		'url' : 'https://ftp.gnome.org/pub/gnome/sources/glib/2.52/glib-2.52.0.tar.xz',
		'configure_options' : '--host={compile_target} --prefix={compile_prefix} --with-pcre=system --with-threads=win32 --disable-fam --disable-shared',
		'depends_on' : [ 'pcre' ],
		'patches' : [
			('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/glib2/0001-Use-CreateFile-on-Win32-to-make-sure-g_unlink-always.patch','Np1'),
			('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/glib2/0004-glib-prefer-constructors-over-DllMain.patch'               ,'Np1'),
			('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/glib2/0017-GSocket-Fix-race-conditions-on-Win32-if-multiple-thr.patch','p1' ),
			('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/glib2/0027-no_sys_if_nametoindex.patch'                               ,'Np1'),
			('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/glib2/0028-inode_directory.patch'                                     ,'Np1'),
			('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/glib2/revert-warn-glib-compile-schemas.patch'                         ,'Rp1'),
			('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/glib2/use-pkgconfig-file-for-intl.patch'                              ,'p0' ),

		],
		'run_post_patch' : [
			'./autogen.sh NOCONFIGURE=1',
		],
		'_info' : { 'version' : '2.52.0', 'fancy_name' : 'glib2' },
	},
	'openssl_1_1' : {
		'repo_type' : 'archive',
		'url' : 'https://www.openssl.org/source/openssl-1.1.0e.tar.gz',
		'configure_options' : '{bit_name3} --prefix={compile_prefix} --cross-compile-prefix={cross_prefix_bare} no-shared no-asm',
		'configure_path' : './Configure',
		'install_target' : 'install_sw', # we don't need the docs..
		'env_exports' : {
			'CROSS_COMPILE' : '{cross_prefix_bare}',
		},
		'_info' : { 'version' : '1.1.0e', 'fancy_name' : 'openssl' },
	},
	'mingw-libgnurx' : {
		'repo_type' : 'archive',
		'folder_name' : 'mingw-libgnurx-2.5.1',
		'url' : 'https://sourceforge.net/projects/mingw/files/Other/UserContributed/regex/mingw-regex-2.5.1/mingw-libgnurx-2.5.1-src.tar.gz',
		'configure_options': '--host={compile_target} --prefix={compile_prefix}', # --disable-shared --enable-static --enable-fsect-man5
		'cpu_count' : '1', #...
		'needs_make' : False,
		'needs_make_install' : False,
		'run_post_configure' : [
			'make -f Makefile.mingw-cross-env -j 1 TARGET={compile_target} bin_PROGRAMS= sbin_PROGRAMS= noinst_PROGRAMS= install-static'
			#'{cross_prefix_bare}ranlib libregex.a'
			#'make -f "Makefile.mingw-cross-env" libgnurx.a V=1'
		],
		'patches' : [
			( 'https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/mingw-libgnurx-static.patch', 'p1' ),
			( 'https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/libgnurx-1-build-static-lib.patch', 'p1' ),
		],
		'_info' : { 'version' : '2.5.1', 'fancy_name' : 'mingw-libgnurx' },
	},
	'gettext' : {
		'repo_type' : 'archive',
		'url' : 'https://ftp.gnu.org/pub/gnu/gettext/gettext-0.19.8.1.tar.xz',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static --enable-threads=win32 --without-libexpat-prefix --without-libxml2-prefix CPPFLAGS=-DLIBXML_STATIC',
		'version' : '0.19.8.1',
		'_info' : { 'version' : '0.19.8.1', 'fancy_name' : 'gettext' },
		'depends_on' : [ 'iconv' ],
	},
	'libfile_local' : { # local non cross-compiled, to bootstrap libfile-cross-compiled, it needs the actual linux build first uh..
		'repo_type' : 'git',
		'url' : 'https://github.com/file/file.git',
		'rename_folder' : 'libfile_local.git',
		'configure_options': '--prefix={compile_prefix} --disable-shared --enable-static',
		'needs_make' : False,
		'custom_cflag' : '', # doesn't like march in cflag, but target_cflags.
		'env_exports' : { 'TARGET_CFLAGS' : '{original_cflags}' },
		'run_post_patch' : [ 'autoreconf -fiv' ],
		
	},
	'libfile' : {
		'repo_type' : 'git',
		'url' : 'https://github.com/file/file.git',
		'rename_folder' : 'libfile.git',
		'patches' : [
			( 'https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/file-win32.patch', 'p1' ),
		],
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static --enable-fsect-man5',
		'depends_on' : [ 'mingw-libgnurx', 'libfile_local' ],
		'custom_cflag' : '', # doesn't like march in cflag, but target_cflags.
		'env_exports' : { 'TARGET_CFLAGS' : '{original_cflags}' },
		'run_post_patch' : [ 'autoreconf -fiv' ],
		'flipped_path' : True,
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'file' },
	},
	'libflac' : {
		'repo_type' : 'git',
		'url' : 'https://git.xiph.org/flac.git',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'depends_on': [
			'libogg',
		],
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'flac (library)' },
	},
	'libarchive': {
		'repo_type' : 'archive',
		'url' : 'https://www.libarchive.org/downloads/libarchive-3.3.1.tar.gz',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static --disable-bsdtar --disable-bsdcat --disable-bsdcpio --without-openssl', #--without-xml2 --without-nettle
		'depends_on' : [
			'bzip2', 'expat', 'zlib', 'liblzma', 'lzo'
		],
		'run_post_install' : [
			'sed -i.bak \'s/Libs: -L${{libdir}} -larchive/Libs: -L${{libdir}} -larchive -llzma/\' "{pkg_config_path}/libarchive.pc"', # libarchive complaints without this.
		],
		'_info' : { 'version' : '3.3.1', 'fancy_name' : 'libarchive' },
	},
	'lzo': {
		'repo_type' : 'archive',
		'url' : 'https://www.oberhumer.com/opensource/lzo/download/lzo-2.10.tar.gz',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'version' : '2.10',
		'_info' : { 'version' : '2.10', 'fancy_name' : 'lzo' },
	},
	'uchardet': {
		'repo_type' : 'git',
		'url' : 'https://github.com/BYVoid/uchardet.git',
		'needs_configure' : False,
		'is_cmake' : True,
		'cmake_options': '. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={compile_prefix} -DBUILD_SHARED_LIBS=OFF',
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'uchardet' },
	},
	'libcdio' : {
		'repo_type' : 'git',
		'url' : 'git://git.savannah.gnu.org/libcdio.git', # old: http://git.savannah.gnu.org/cgit/libcdio.git/snapshot/libcdio-release-0.94.tar.gz
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static', #  --enable-maintainer-mode
		'run_post_patch' : (
			'touch doc/version.texi', # took me far to long to come up with and find this workaround
			'touch src/cd-info.1 src/cd-drive.1 src/iso-read.1 src/iso-info.1 src/cd-read.1', # .....
			#'if [ ! -f "configure" ] ; then ./autogen.sh ; fi',
			#'make -C doc stamp-vti', # idk why it needs this... odd thing: https://lists.gnu.org/archive/html/libcdio-devel/2016-03/msg00007.html
		),
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'libcdio' },
	},
	'libcdio-paranoia' : {
		'repo_type' : 'git',
		'url' : 'https://github.com/rocky/libcdio-paranoia.git',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'depends_on': (
			'libcdio',
		),
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'libcdio-paranoia' },
	},
	'libdvdcss' : {
		'repo_type' : 'git',
		'url' : 'https://code.videolan.org/videolan/libdvdcss.git',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static --disable-doc',
		'run_post_patch' : (
			'autoreconf -i',
		),
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'libdvdcss' },
	},
	'libdvdread' : {
		'repo_type' : 'git',
		'url' : 'https://code.videolan.org/videolan/libdvdread.git',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static --with-libdvdcss',
		'depends_on' : (
			'libdvdcss',
		),
		'run_post_patch' : (
			'autoreconf -i',
		),
		'run_post_install' : (
			'sed -i.bak \'s/-ldvdread/-ldvdread -ldvdcss/\' "{pkg_config_path}/dvdread.pc"', # fix undefined reference to `dvdcss_close'
		),
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'libdvdread' },
	},
	'libdvdnav' : {
		'repo_type' : 'git',
		'url' : 'https://code.videolan.org/videolan/libdvdnav.git',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static --with-libdvdcss',
		'depends_on' : (
			'libdvdread',
		),
		'run_post_patch' : (
			'autoreconf -i',
		),
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'libdvdnav' },
	},
	'libbluray' : {
		'repo_type' : 'git',
		'recursive_git' : True,
		'url' : 'https://git.videolan.org/git/libbluray.git',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static --disable-examples --disable-doxygen-doc --disable-bdjava-jar --enable-udf', #--without-libxml2 --without-fontconfig .. optional.. I guess
		'patches' : (
			('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/libbluray_git_remove_strtok_s.patch', 'p1'),
		),
		'run_post_install' : (
			'sed -i.bak \'s/-lbluray.*$/-lbluray -lfreetype -lexpat -lz -lbz2 -lxml2 -lws2_32 -lgdi32 -liconv/\' "{pkg_config_path}/libbluray.pc"', # fix undefined reference to `xmlStrEqual' and co
		),
		'depends_on' : (
			'freetype2',
		),
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'libbluray' },
	},
	'openal-soft' : {
		'repo_type' : 'git',
		'url' : 'https://github.com/kcat/openal-soft.git',
		'needs_configure' : False,
		'is_cmake' : True,
		'cmake_options': 
			'. {cmake_prefix_options} -DCMAKE_TOOLCHAIN_FILE=XCompile.txt -DHOST={compile_target}'
			' -DCMAKE_INSTALL_PREFIX={compile_prefix} -DCMAKE_FIND_ROOT_PATH='
			' -DLIBTYPE=STATIC -DALSOFT_UTILS=OFF -DALSOFT_EXAMPLES=OFF',
		'patches' : (
			('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/openal-soft-privlibs.patch', 'p1'),
		),
		'run_post_patch' : [
			"sed -i.bak 's/CMAKE_INSTALL_PREFIX \"\${{CMAKE_FIND_ROOT_PATH}}\"/CMAKE_INSTALL_PREFIX \"\"/' XCompile.txt",
		],
		'install_options' : 'DESTDIR={compile_prefix}',
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'openal-soft' },
	},
	'lcms2' : {
		'repo_type' : 'git',
		'url' : 'https://github.com/mm2/Little-CMS.git',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'Little-CMS2' },
	},
	'python36_libs': {
		'repo_type' : 'git',
		'url' : 'https://github.com/DeadSix27/python_mingw_libs.git',
		'needs_configure' : False,
		'needs_make_install' : False,
		'make_options': 'PREFIX={compile_prefix} GENDEF={mingw_binpath}/gendef DLLTOOL={mingw_binpath}/{cross_prefix_bare}dlltool',
		'_info' : { 'version' : '3.6', 'fancy_name' : 'Python (library-only)' },
	},
	'vapoursynth_libs': {
		'repo_type' : 'git',
		'url' : 'https://github.com/DeadSix27/vapoursynth_mingw_libs.git',
		'needs_configure' : False,
		'needs_make_install' : False,
		'make_options': 'PREFIX={compile_prefix} GENDEF={mingw_binpath}/gendef DLLTOOL={mingw_binpath}/{cross_prefix_bare}dlltool',
		'packages': {
			'ubuntu' : [ 'p7zip-full' ],
			'fedora' : [ 'p7zip.' ],
		},
		'_info' : { 'version' : '37', 'fancy_name' : 'VapourSynth (library-only)' },
	},
	'luajit': {
		'repo_type' : 'git',
		'url' : 'https://luajit.org/git/luajit-2.0.git',
		'needs_configure' : False,
		'custom_cflag' : '-O3', # doesn't like march's past ivybridge (yet), so we override it.
		'install_options' : 'CROSS={cross_prefix_bare} HOST_CC="gcc -m{bit_num}" TARGET_SYS=Windows BUILDMODE=static FILE_T=luajit.exe PREFIX={compile_prefix}',
		'make_options': 'CROSS={cross_prefix_bare} HOST_CC="gcc -m{bit_num}" TARGET_SYS=Windows BUILDMODE=static amalg',
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'LuaJIT2' },
	},
	'lua' : {
		'repo_type' : 'archive',
		'url' : 'https://www.lua.org/ftp/lua-5.3.4.tar.gz',
		'needs_configure' : False,
		'make_options': 'CC={cross_prefix_bare}gcc PREFIX={compile_prefix} RANLIB={cross_prefix_bare}ranlib LD={cross_prefix_bare}ld STRIP={cross_prefix_bare}strip CXX={cross_prefix_bare}g++ AR="{cross_prefix_bare}ar rcu" mingw', # LUA_A=lua53.dll LUA_T=lua.exe LUAC_T=luac.exe
		'install_options' : 'TO_BIN="lua.exe luac.exe lua53.dll" TO_LIB="liblua.a" INSTALL_TOP="{compile_prefix}"', #TO_LIB="liblua.a liblua.dll.a"
		'install_target' : 'install',
		'packages': {
			'ubuntu' : [ 'lua5.2' ],
		},
		'_info' : { 'version' : '5.3.4', 'fancy_name' : 'lua' },
	},
	'a52dec' : {
		'repo_type' : 'archive',
		'url' : 'http://liba52.sourceforge.net/files/a52dec-0.7.4.tar.gz',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static CFLAGS=-std=gnu89',
		'run_post_patch' : [
			'rm configure',
		],
		'make_options': 'bin_PROGRAMS= sbin_PROGRAMS= noinst_PROGRAMS=',
		'install_options': 'bin_PROGRAMS= sbin_PROGRAMS= noinst_PROGRAMS=',
		'_info' : { 'version' : '0.7.4', 'fancy_name' : 'a52dec' },
	},
	'vapoursynth': {
		'repo_type' : 'git',
		'url' : 'https://github.com/vapoursynth/vapoursynth.git',
		'custom_cflag' : '-O3',
		'configure_options' : '--host={compile_target} --prefix={compile_prefix} --disable-shared --disable-python-module --enable-core',
		'patches' : (
			('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/vapoursynth-0001-statically-link.patch', 'p1'),
			('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/vapoursynth-0002-api.patch', 'p1'),
			('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/vapoursynth-0003-windows-header.patch', 'p1'),
		),

	},
	'libffmpeg' : {
		'repo_type' : 'git',
		'url' : 'git://git.ffmpeg.org/ffmpeg.git',
		'rename_folder' : 'libffmpeg_git',
		'configure_options': '!VAR(ffmpeg_base_config)VAR! --prefix={compile_prefix} --disable-shared --enable-static --disable-doc --disable-programs',
		'depends_on': [ 'ffmpeg_depends' ],
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'FFmpeg (library)' },
	},
	'bzip2' : {
		'repo_type' : 'archive',
		'url' : 'http://www.bzip.org/1.0.6/bzip2-1.0.6.tar.gz',
		'patches' : (
			('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/bzip2_cross_compile.diff', "p0"),
		),
		"needs_configure": False,
		"needs_make": True,
		"needs_make_install": False,
		'make_options': '{make_prefix_options} libbz2.a bzip2 bzip2recover install',
		'_info' : { 'version' : '1.0.6', 'fancy_name' : 'BZip2 (library)' },
	},
	'decklink_headers' : { # seem to be broken in ffmpeg anyway
		'repo_type' : 'none',
		'folder_name' : 'decklink_headers',
		'run_post_patch' : (
			'if [ ! -f "already_done" ] ; then wget https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/additional_headers/DeckLinkAPI.h ; fi',
			'if [ ! -f "already_done" ] ; then wget https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/additional_headers/DeckLinkAPI_i.c ; fi',
			'if [ ! -f "already_done" ] ; then wget https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/additional_headers/DeckLinkAPIVersion.h ; fi',
			'if [ ! -f "already_done" ] ; then cp -nv "DeckLinkAPI.h" "{compile_prefix}/include/DeckLinkAPI.h" ; fi',
			'if [ ! -f "already_done" ] ; then cp -nv "DeckLinkAPI_i.c" "{compile_prefix}/include/DeckLinkAPI_i.c" ; fi',
			'if [ ! -f "already_done" ] ; then cp -nv "DeckLinkAPIVersion.h" "{compile_prefix}/include/DeckLinkAPIVersion.h" ; fi',
			'if [ ! -f "already_done" ] ; then touch  "already_done" ; fi',
		),
		'needs_make' : False,
		'needs_make_install' : False,
		'needs_configure' : False,
	},
	'zlib' : {
		'repo_type' : 'archive',
		'url' : 'https://sourceforge.net/projects/libpng/files/zlib/1.2.11/zlib-1.2.11.tar.gz',
		'env_exports' : {
			'AR' : '{cross_prefix_bare}ar',
			'CC' : '{cross_prefix_bare}gcc',
			'PREFIX' : '{compile_prefix}',
			'RANLIB' : '{cross_prefix_bare}ranlib',
			'LD'     : '{cross_prefix_bare}ld',
			'STRIP'  : '{cross_prefix_bare}strip',
			'CXX'    : '{cross_prefix_bare}g++',
		},
		'configure_options': '--static --prefix={compile_prefix}',
		'make_options': '{make_prefix_options} ARFLAGS=rcs',
		'_info' : { 'version' : '1.2.11', 'fancy_name' : 'zlib' },
	},
	'liblzma' : {
		'repo_type' : 'archive',
		'url' : 'https://tukaani.org/xz/xz-5.2.3.tar.bz2',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'_info' : { 'version' : '5.2.3', 'fancy_name' : 'lzma' },
	},
	'libzimg' : {
		'repo_type' : 'git',
		'url' : 'https://github.com/sekrit-twc/zimg.git',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'zimg' },
	},
	'libsnappy' : {
		'repo_type' : 'git',
		'url' : 'https://github.com/google/snappy.git', #old: https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/sources/google-snappy-1.1.3-14-g32d6d7d.tar.gz
		#'folder_name' : 'google-snappy-32d6d7d',
		'run_post_make' : [
			'cp -n README.md README'
		],
		'configure_options' : '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'libsnappy' },
	},
	'gmp' : {
		#export CC_FOR_BUILD=/usr/bin/gcc idk if we need this anymore, compiles fine without.
		#export CPP_FOR_BUILD=usr/bin/cpp
		#generic_configure "ABI=$bits_target"
		'repo_type' : 'archive',
		'url' : 'https://gmplib.org/download/gmp/gmp-6.1.2.tar.xz',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'_info' : { 'version' : '6.1.2', 'fancy_name' : 'gmp' },
	},
	'libnettle' : {
		'repo_type' : 'archive',
		'url' : 'https://ftp.gnu.org/gnu/nettle/nettle-3.3.tar.gz',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static --disable-openssl --with-included-libtasn1',
		'depends_on' : [
			'gmp',
		],
		'_info' : { 'version' : '3.3', 'fancy_name' : 'nettle' },
	},
	'iconv' : {
		'repo_type' : 'archive',
		# CFLAGS=-O2 # ??
		'url' : 'https://ftp.gnu.org/pub/gnu/libiconv/libiconv-1.15.tar.gz',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'_info' : { 'version' : '1.15', 'fancy_name' : 'libiconv' },
	},
	'gnutls' : {
		'repo_type' : 'archive',
		'url' : 'https://www.gnupg.org/ftp/gcrypt/gnutls/v3.5/gnutls-3.5.12.tar.xz',
		'configure_options':
			'--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static --with-included-unistring '
			'--disable-rpath --disable-nls --disable-guile --disable-doc --disable-tests --enable-local-libopts --with-included-libtasn1 --with-libregex-libs="-lgnurx" --without-p11-kit --disable-silent-rules '
			'CPPFLAGS="-DWINVER=0x0501 -DAI_ADDRCONFIG=0x0400 -DIPV6_V6ONLY=27" LIBS="-lws2_32" ac_cv_prog_AR="{cross_prefix_full}ar"'
		,
		'run_post_install': [
			"sed -i.bak 's/-lgnutls *$/-lgnutls -lnettle -lhogweed -lgmp -lcrypt32 -lws2_32 -liconv/' \"{pkg_config_path}/gnutls.pc\"",
		],
		'patches' : [
			('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/gnutls/0001-gnutls-3.5.11-arpainet_pkgconfig.patch', 'p1'),
		],
		'depends_on' : [
			'gmp', 'libnettle',
		],
		'env_exports' : {
			'CPPFLAGS' : '-DWINVER=0x0501 -DAI_ADDRCONFIG=0x0400 -DIPV6_V6ONLY=27',
			'LIBS' : '-lws2_32',
			'ac_cv_prog_AR' : '{cross_prefix_full}ar',
		},
		'packages': {
			'ubuntu' : [ 'xsltproc', 'docbook-utils', 'rake', 'gperf' ],
		},
		'_info' : { 'version' : '3.5.12', 'fancy_name' : 'gnutls' },
	},
	'gnutls_old' : { # in case the other breaks
		'repo_type' : 'archive',
		'url' : 'ftp://ftp.gnutls.org/gcrypt/gnutls/v3.5/gnutls-3.5.11.tar.xz',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static --disable-cxx --disable-doc --enable-local-libopts --disable-guile -with-included-libtasn1 --without-p11-kit --with-included-unistring',
		'run_post_install': [
			"sed -i.bak 's/-lgnutls *$/-lgnutls -lnettle -lhogweed -lgmp -lcrypt32 -lws2_32 -liconv/' \"{pkg_config_path}/gnutls.pc\"",
		],
		'depends_on' : [
			'gmp', 'libnettle',
		],
		'packages': {
			'ubuntu' : [ 'xsltproc', 'docbook-utils', 'rake', 'gperf' ],
		},
		'_info' : { 'version' : '3.5.11', 'fancy_name' : 'gnutls' },
		'_disabled' : True,
	},
	'frei0r' : {
		'repo_type' : 'archive',
		'url' : 'https://files.dyne.org/frei0r/frei0r-plugins-1.6.0.tar.gz',
		'needs_configure' : False,
		'is_cmake' : True,
		'run_post_patch': ( # runs commands post the patch process
			'sed -i.bak "s/find_package (Cairo)//g" CMakeLists.txt', #idk
		),
		'cmake_options': '. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={compile_prefix}',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'_info' : { 'version' : '1.6.0', 'fancy_name' : 'frei0r-plugins' },
	},
	'libsndfile' : {
		'repo_type' : 'git',
		'branch' : '1.0.28',
		'url' : 'https://github.com/erikd/libsndfile.git',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static --enable-sqlite --disable-test-coverage --enable-external-libs --enable-experimental',
		#'patches' : [ #patches courtesy of https://github.com/Alexpux/MINGW-packages/tree/master/mingw-w64-libsndfile
			#('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/libsndfile/0001-more-elegant-and-foolproof-autogen-fallback.all.patch', "p0"),
			#('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/libsndfile/0003-fix-source-searches.mingw.patch', "p0"),
		#],
		'run_post_patch': [
			'autoreconf -fi -I M4',
		],
		'run_post_install' : [
			'sed -i.bak \'s/Libs: -L${{libdir}} -lsndfile/Libs: -L${{libdir}} -lsndfile -lFLAC -lvorbis -lvorbisenc -logg -lspeex/\' "{pkg_config_path}/sndfile.pc"', #issue with rubberband not using pkg-config option "--static" or so idk?
		],
		'depends_on': 
		[
			'libspeex',
		],
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'libsndfile' },
	},
	'libbs2b' : {
		'repo_type' : 'archive',
		'env_exports' : {
			"ac_cv_func_malloc_0_nonnull" : "yes", # fixes undefined reference to `rpl_malloc'
		},
		'url' : 'https://sourceforge.net/projects/bs2b/files/libbs2b/3.1.0/libbs2b-3.1.0.tar.gz',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'_info' : { 'version' : '3.1.0', 'fancy_name' : 'libbs2b' },
	},
	'wavpack' : {
		'repo_type' : 'git',
		'url' : 'https://github.com/dbry/WavPack.git',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'wavpack' },
	},
	'libgme_game_music_emu' : {
		'repo_type' : 'archive',
		'url' : 'https://bitbucket.org/mpyne/game-music-emu/downloads/game-music-emu-0.6.1.tar.bz2', # ffmpeg doesnt like git
		'needs_configure' : False,
		'is_cmake' : True,
		#'run_post_patch': ( # runs commands post the patch process
		#	'sed -i.bak "s|SHARED|STATIC|" gme/CMakeLists.txt',
		#),
		'cmake_options': '. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={compile_prefix} -DBUILD_SHARED_LIBS=OFF',
		'_info' : { 'version' : '0.6.1', 'fancy_name' : 'game-music-emu' },
	},
	'libwebp' : { # why can't everything be so easy to compile
		'repo_type' : 'git',
		#'url' : 'http://downloads.webmproject.org/releases/webp/libwebp-0.6.0.tar.gz',
		'url' : 'https://chromium.googlesource.com/webm/libwebp',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static --enable-swap-16bit-csp --enable-experimental --enable-libwebpmux --enable-libwebpdemux --enable-libwebpdecoder --enable-libwebpextras',
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'libwebp' },
	},
	'flite' : { # why can't everything be so easy to compile
		'repo_type' : 'archive',
		'url' : 'http://www.speech.cs.cmu.edu/flite/packed/flite-1.4/flite-1.4-release.tar.bz2',
		'patches' : ( # ordered list of patches, first one will be applied first..
			('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/flite_64.diff', "p0"),
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
		'_info' : { 'version' : '1.4', 'fancy_name' : 'flite' },
	},
	'libgsm' : {
		'repo_type' : 'archive',
		'url' : 'http://www.quut.com/gsm/gsm-1.0.16.tar.gz',
		'folder_name' : 'gsm-1.0-pl16',
		'patches' : ( # ordered list of patches, first one will be applied first..
			('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/gsm-1.0.16.patch', "p0"),
			('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/gsm-1.0.16_Makefile.patch', 'p0'), # toast fails. so lets just patch it out of the makefile..
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
		'_info' : { 'version' : '1.0.16', 'fancy_name' : 'gsm' },
	},
	'sdl1' : {
		'repo_type' : 'archive',
		'url' : 'https://www.libsdl.org/release/SDL-1.2.15.tar.gz',
		'custom_cflag' : '-DDECLSPEC=',# avoid SDL trac tickets 939 and 282, and not worried about optimizing yet...
		"run_post_install": (
			'sed -i.bak "s/-mwindows//" "{pkg_config_path}/sdl.pc"', # allow ffmpeg to output anything to console :|
			'sed -i.bak "s/-mwindows//" "{compile_prefix}/bin/sdl-config"', # update this one too for good measure, FFmpeg can use either, not sure which one it defaults to...
			'cp -v "{compile_prefix}/bin/sdl-config" "{cross_prefix_full}sdl-config"', # this is the only mingw dir in the PATH so use it for now [though FFmpeg doesn't use it?]
		),
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'_info' : { 'version' : '1.2.15', 'fancy_name' : 'SDL1' },
	},
	'sdl2' : {
		'repo_type' : 'archive',
		'url' : 'https://www.libsdl.org/release/SDL2-2.0.5.tar.gz',
		'patches' : (
			('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/sdl2/0001-SDL2-2.0.5.xinput.diff', "p0"),
		),
		'custom_cflag' : '-DDECLSPEC=', # avoid SDL trac tickets 939 and 282, and not worried about optimizing yet...
		"run_post_install": (
			'sed -i.bak "s/-mwindows/-ldinput8 -ldxguid -ldxerr8 -luser32 -lgdi32 -lwinmm -limm32 -lole32 -loleaut32 -lshell32 -lversion -luuid/" "{pkg_config_path}/sdl2.pc"', # allow ffmpeg to output anything to console :|
			'sed -i.bak "s/-mwindows/-ldinput8 -ldxguid -ldxerr8 -luser32 -lgdi32 -lwinmm -limm32 -lole32 -loleaut32 -lshell32 -lversion -luuid/" "{compile_prefix}/bin/sdl2-config"', # update this one too for good measure, FFmpeg can use either, not sure which one it defaults to...
			'cp -v "{compile_prefix}/bin/sdl2-config" "{cross_prefix_full}sdl2-config"', # this is the only mingw dir in the PATH so use it for now [though FFmpeg doesn't use it?]
		),
		'configure_options': '--prefix={compile_prefix} --host={compile_target} --disable-shared --enable-static',
		'_info' : { 'version' : '2.0.5', 'fancy_name' : 'SDL2' },
	},
	'sdl2_hg' : {
		'folder_name' : 'sdl2_merc',
		'repo_type' : 'mercurial',
		'source_subfolder' : '_build',
		'url' : 'https://hg.libsdl.org/SDL',
		'configure_path' : '../configure',
		'patches' : (
			('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/sdl2/0001-SDL2_hg.xinput_state_ex.patch', 'p1', '..'),
		),
		'custom_cflag' : '-DDECLSPEC=', # avoid SDL trac tickets 939 and 282, and not worried about optimizing yet...
		"run_post_install": (
			'sed -i.bak "s/-mwindows/-ldinput8 -ldxguid -ldxerr8 -luser32 -lgdi32 -lwinmm -limm32 -lole32 -loleaut32 -lshell32 -lversion -luuid/" "{pkg_config_path}/sdl2.pc"', # allow ffmpeg to output anything to console :|
			'sed -i.bak "s/-mwindows/-ldinput8 -ldxguid -ldxerr8 -luser32 -lgdi32 -lwinmm -limm32 -lole32 -loleaut32 -lshell32 -lversion -luuid/" "{compile_prefix}/bin/sdl2-config"', # update this one too for good measure, FFmpeg can use either, not sure which one it defaults to...
			'cp -v "{compile_prefix}/bin/sdl2-config" "{cross_prefix_full}sdl2-config"', # this is the only mingw dir in the PATH so use it for now [though FFmpeg doesn't use it?]
		),
		'configure_options': '--prefix={compile_prefix} --host={compile_target} --disable-shared --enable-static',
		'_info' : { 'version' : 'mercurial (default)', 'fancy_name' : 'SDL2' },
	},
	'libopus' : {
		'repo_type' : 'git',
		'url' : 'https://github.com/xiph/opus.git',
		'patches': (
			("https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/opus/opus_git_strip_declspec.patch", "p1"),
		),
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'opus' },
	},
	'opencore-amr' : {
		'repo_type' : 'archive',
		'url' : 'https://sourceforge.net/projects/opencore-amr/files/opencore-amr/opencore-amr-0.1.5.tar.gz',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'_info' : { 'version' : '0.1.5', 'fancy_name' : 'opencore-amr' },
	},
	'vo-amrwbenc' : {
		'repo_type' : 'archive',
		'url' : 'https://sourceforge.net/projects/opencore-amr/files/vo-amrwbenc/vo-amrwbenc-0.1.3.tar.gz',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'_info' : { 'version' : '0.1.3', 'fancy_name' : 'vo-amrwbenc' },
	},
	'libogg' : {
		'repo_type' : 'git',
		'url' : 'https://github.com/xiph/ogg.git',
		# 'folder_name' : 'ogg-1.3.2',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'ogg' },
	},
	'libspeexdsp' : {
		'repo_type' : 'git',
		'url' : 'https://github.com/xiph/speexdsp.git',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'speexdsp' },
	},
	'libspeex' : {
		'repo_type' : 'git', #"LDFLAGS=-lwinmm"
		'url' : 'https://github.com/xiph/speex.git',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'speex' },
	},
	'libvorbis' : {
		'repo_type' : 'git',
		'url' : 'https://github.com/xiph/vorbis.git',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'vorbis' },
	},
	'libtheora' : {
		'repo_type' : 'git',
		'url' : 'https://github.com/xiph/theora.git',
		'patches' : (
			('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/theora_remove_rint_1.2.0alpha1.patch', 'p1'),
		),
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'theora' },
	},
	'orc' : {
		'repo_type' : 'archive',
		'url' : 'https://gstreamer.freedesktop.org/src/orc/orc-0.4.26.tar.xz',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'_info' : { 'version' : '0.4.26', 'fancy_name' : 'orc' },
	},
	'libschroedinger' : {
		'repo_type' : 'archive',
		'url' : 'https://download.videolan.org/contrib/schroedinger/schroedinger-1.0.11.tar.gz',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'run_post_configure': (
			'sed -i.bak \'s/testsuite//\' Makefile',
		),
		'run_post_install': (
			'sed -i.bak \'s/-lschroedinger-1.0$/-lschroedinger-1.0 -lorc-0.4/\' "{pkg_config_path}/schroedinger-1.0.pc"',
		),
		'_info' : { 'version' : '1.0.11', 'fancy_name' : 'schroedinger' },

	},
	'freetype2' : {
		'repo_type' : 'archive',
		'url' : 'https://download.savannah.gnu.org/releases/freetype/freetype-2.8.tar.gz',
		'configure_options': '--host={compile_target} --build=x86_64-linux-gnu --prefix={compile_prefix} --disable-shared --enable-static --with-zlib={compile_prefix} --without-png', # cygwin = "--build=i686-pc-cygwin"  # hard to believe but needed...
		'cpu_count' : '1', # ye idk why it needs that
		'patches' : [
			#('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/freetype2/0001-Enable-table-validation-modules.patch?h=mingw-w64-freetype2',    'Np1'),
			#('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/freetype2/0002-Enable-subpixel-rendering.patch?h=mingw-w64-freetype2',          'Np1'),
			#('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/freetype2/0003-Enable-infinality-subpixel-hinting.patch?h=mingw-w64-freetype2', 'Np1'),
		],
		#'run_post_install': (
		#	'sed -i.bak \'s/Libs: -L${{libdir}} -lfreetype.*/Libs: -L${{libdir}} -lfreetype -lexpat -lz -lbz2/\' "{pkg_config_path}/freetype2.pc"', # this should not need expat, but...I think maybe people use fontconfig's wrong and that needs expat? huh wuh? or dependencies are setup wrong in some .pc file?
		#),
		'_info' : { 'version' : '2.8', 'fancy_name' : 'freetype2' },
	},
	'expat' : {
		'repo_type' : 'archive',
		'url' : 'https://sourceforge.net/projects/expat/files/expat/2.2.0/expat-2.2.0.tar.bz2',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'_info' : { 'version' : '2.2.0', 'fancy_name' : 'expat' },
	},
	'libxml2' : {
		'repo_type' : 'archive',
		'url' : 'http://xmlsoft.org/sources/libxml2-2.9.4.tar.gz',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static --without-python --enable-tests=no --enable-programs=no',
		'patches' : [
			('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/libxml2/0001-libxml2-2.9.4-add_prog_test_toggle.patch', 'p1'),
		],
		'run_post_patch' : [
			'autoreconf -fiv',
		],
		'run_post_install' : (
			'sed -i.bak \'s/Libs: -L${{libdir}} -lxml2/Libs: -L${{libdir}} -lxml2 -lz -llzma -liconv -lws2_32/\' "{pkg_config_path}/libxml-2.0.pc"', # libarchive complaints without this.
		),
		'depends_on': [
			'liblzma', 'iconv'
		],
		'_info' : { 'version' : '2.9.4', 'fancy_name' : 'libxml2' },
	},
	'libxvid' : {
		'repo_type' : 'archive',
		'url' : 'http://downloads.xvid.org/downloads/xvidcore-1.3.4.tar.gz',
		'folder_name' : 'xvidcore',
		'rename_folder' : 'xvidcore-1.3.4',
		'source_subfolder': 'build/generic',
		'configure_options': '--host={compile_target} --prefix={compile_prefix}',
		'cpu_count' : '1',
		'run_post_configure': (
			'sed -i.bak "s/-mno-cygwin//" platform.inc',
		),
		'run_post_install': (
			'rm -v {compile_prefix}/lib/xvidcore.dll.a',
			'mv -v {compile_prefix}/lib/xvidcore.a {compile_prefix}/lib/libxvidcore.a',
		),
		'_info' : { 'version' : '1.3.4', 'fancy_name' : 'xvidcore' },
	},
	'xavs' : {
		#LDFLAGS='-lm'
		'repo_type' : 'svn',
		'url' : 'https://svn.code.sf.net/p/xavs/code/trunk',
		'folder_name' : 'xavs_svn',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static --cross-prefix={cross_prefix_bare}',
		'run_post_install' : (
			'rm -f NUL', # uh???
		),
		'_info' : { 'version' : 'svn (master)', 'fancy_name' : 'xavs' },
	},
	'libsoxr' : {
		'repo_type' : 'archive',
		'needs_configure' : False,
		'is_cmake' : True,
		'cmake_options': '. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={compile_prefix} -DHAVE_WORDS_BIGENDIAN_EXITCODE=0 -DBUILD_SHARED_LIBS:bool=off -DBUILD_TESTS:BOOL=OFF -DCMAKE_AR={cross_prefix_full}ar', #not sure why it cries about AR
		'url' : 'https://sourceforge.net/projects/soxr/files/soxr-0.1.2-Source.tar.xz',
		'_info' : { 'version' : '0.1.2', 'fancy_name' : 'soxr' },
	},
	'libebur128' : { # uneeded
		'repo_type' : 'git',
		'url' : 'https://github.com/jiixyj/libebur128.git',
		'cmake_options': '. {cmake_prefix_options} -DENABLE_INTERNAL_QUEUE_H:BOOL=ON -DCMAKE_AR={cross_prefix_full}ar', #not sure why it cries about AR
		'needs_configure' : False,
		'is_cmake' : True,
		'run_post_patch': (
			'sed -i.bak \'s/ SHARED / STATIC /\' ebur128/CMakeLists.txt',
		),
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'libebur128' },
	},
	'libx265' : {
		'repo_type' : 'mercurial',
		'url' : 'https://bitbucket.org/multicoreware/x265',
		'rename_folder' : 'libx265_hg',
		'cmake_options': '. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={compile_prefix} -DENABLE_CLI:BOOL=OFF -DENABLE_SHARED=OFF -DCMAKE_AR={cross_prefix_full}ar', # no cli, as this is just for the library.
		'needs_configure' : False,
		'is_cmake' : True,
		'source_subfolder': 'source',
		'_info' : { 'version' : 'mercurial (default)', 'fancy_name' : 'x265 (library)' },
	},
	'libx265_multibit' : {
		'repo_type' : 'mercurial',
		'url' : 'https://bitbucket.org/multicoreware/x265',
		'rename_folder' : 'libx265_hg_multibit',
		'source_subfolder': 'source',
		'cmake_options': '. {cmake_prefix_options} -DCMAKE_AR={cross_prefix_full}ar -DENABLE_SHARED=OFF -DENABLE_CLI:BOOL=OFF -DEXTRA_LIB="x265_main10.a;x265_main12.a" -DEXTRA_LINK_FLAGS="-L{offtree_prefix}/libx265_10bit/lib;-L{offtree_prefix}/libx265_12bit/lib" -DLINKED_10BIT=ON -DLINKED_12BIT=ON -DCMAKE_INSTALL_PREFIX={compile_prefix}',
		'needs_configure' : False,
		'is_cmake' : True,
		'run_post_make' : [
			'mv -vf libx265.a libx265_main.a',
			'cp -vf {offtree_prefix}/libx265_10bit/lib/libx265_main10.a libx265_main10.a',
			'cp -vf {offtree_prefix}/libx265_12bit/lib/libx265_main12.a libx265_main12.a',
			'"{cross_prefix_full}ar" -M <<EOF\nCREATE libx265.a\nADDLIB libx265_main.a\nADDLIB libx265_main10.a\nADDLIB libx265_main12.a\nSAVE\nEND\nEOF',
		],
		'depends_on' : [ 'libx265_multibit_10', 'libx265_multibit_12' ],
		'_info' : { 'version' : 'mercurial (default)', 'fancy_name' : 'x265 (multibit library 12/10/8)' },
	},
	'libx265_multibit_10' : {
		'repo_type' : 'mercurial',
		'url' : 'https://bitbucket.org/multicoreware/x265',
		'rename_folder' : 'libx265_hg_10bit',
		'source_subfolder' : 'source',
		'cmake_options': '. {cmake_prefix_options} -DCMAKE_AR={cross_prefix_full}ar -DHIGH_BIT_DEPTH=ON -DEXPORT_C_API=OFF -DENABLE_SHARED=OFF -DENABLE_CLI=OFF -DCMAKE_INSTALL_PREFIX={offtree_prefix}/libx265_10bit',
		'run_post_install' : [
			'mv -vf "{offtree_prefix}/libx265_10bit/lib/libx265.a" "{offtree_prefix}/libx265_10bit/lib/libx265_main10.a"'
		],
		'needs_configure' : False,
		'is_cmake' : True,
		'_info' : { 'version' : 'mercurial (default)', 'fancy_name' : 'x265 (library (10))' },
	},
	'libx265_multibit_12' : {
		'repo_type' : 'mercurial',
		'url' : 'https://bitbucket.org/multicoreware/x265',
		'rename_folder' : 'libx265_hg_12bit',
		'source_subfolder' : 'source',
		'cmake_options': '. {cmake_prefix_options} -DCMAKE_AR={cross_prefix_full}ar -DHIGH_BIT_DEPTH=ON -DEXPORT_C_API=OFF -DENABLE_SHARED=OFF -DENABLE_CLI=OFF -DMAIN12=ON -DCMAKE_INSTALL_PREFIX={offtree_prefix}/libx265_12bit',
		'run_post_install' : [
			'mv -vf "{offtree_prefix}/libx265_12bit/lib/libx265.a" "{offtree_prefix}/libx265_12bit/lib/libx265_main12.a"'
		],
		'needs_configure' : False,
		'is_cmake' : True,
		'_info' : { 'version' : 'mercurial (default)', 'fancy_name' : 'x265 (library (12))' },
	},
	'libopenh264' : {
		'repo_type' : 'git',
		'url' : 'https://github.com/cisco/openh264.git',
		'needs_configure' : False,
		'make_options': '{make_prefix_options} OS=mingw_nt ARCH={bit_name} ASM=yasm',
		'install_options': '{make_prefix_options} OS=mingw_nt',
		'install_target' : 'install-static',
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'openh264' },
	},
	'vamp_plugin' : {
		'repo_type' : 'archive',
		'url' : 'https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/sources/vamp-plugin-sdk-2.7.1.tar.gz',
		'run_post_patch': (
			'cp -v build/Makefile.mingw64 Makefile',
		),
		'patches' : (
			('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/vamp-plugin-sdk-2.7.1.patch','p0'), #They rely on M_PI which is gone since c99 or w/e, give them a self defined one and hope for the best.
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
		),
		'_info' : { 'version' : '2.7.1', 'fancy_name' : 'vamp-plugin-sdk' },
	},
	'fftw3' : {
		'repo_type' : 'archive',
		#git tags/master require --enable-maintainer-mode we could but shouldn't use git I guess.
		'url' : 'http://fftw.org/fftw-3.3.6-pl2.tar.gz',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'_info' : { 'version' : '3.3.6-pl2', 'fancy_name' : 'fftw3' },
	},
	'libsamplerate' : {
		'repo_type' : 'git',
		'branch' : '477ce36f8e4bd6a177727f4ac32eba11864dd85d', # commit: Fix win32 compilation # fixed the cross compiling.
		'url' : 'https://github.com/erikd/libsamplerate.git',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'_info' : { 'version' : 'git (477ce3)', 'fancy_name' : 'fftw3' },
		'depends_on' : [
			'libflac',
		],
	},
	'librubberband' : {
		'repo_type' : 'archive',
		'url' : 'http://code.breakfastquay.com/attachments/download/34/rubberband-1.8.1.tar.bz2',
		'download_header' : ( # some packages apparently do not come with specific headers.. like this one. so this function exists... files listed here will be downloaded into the {prefix}/include folder
			'https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/additional_headers/ladspa.h',
		),
		'env_exports' : {
			'AR' : '{cross_prefix_bare}ar',
			'CC' : '{cross_prefix_bare}gcc',
			'PREFIX' : '{compile_prefix}',
			'RANLIB' : '{cross_prefix_bare}ranlib',
			'LD'     : '{cross_prefix_bare}ld',
			'STRIP'  : '{cross_prefix_bare}strip',
			'CXX'    : '{cross_prefix_bare}g++',
		},
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'make_options': '{make_prefix_options}',
		'needs_make_install' : False,
		'run_post_make' : (
			'cp lib/* "{compile_prefix}/lib"',
			'cp -r rubberband "{compile_prefix}/include"',
			'cp rubberband.pc.in "{pkg_config_path}/rubberband.pc"',
			'sed -i.bak "s|%PREFIX%|{compile_prefix_sed_escaped}|" "{pkg_config_path}/rubberband.pc"',
			'sed -i.bak \'s/-lrubberband *$/-lrubberband -lfftw3 -lsamplerate -lstdc++/\' "{pkg_config_path}/rubberband.pc"',
		),
		'depends_on': [
			'libsndfile',
		],
		'_info' : { 'version' : '1.8.1', 'fancy_name' : 'librubberband' },
	},
	'liblame' : { # todo make it a product too.
		'repo_type' : 'archive',
		'url' : 'https://sourceforge.net/projects/lame/files/lame/3.99/lame-3.99.5.tar.gz',
		'patches' : (
			('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/lame-3.99.5.patch', 'p0'),
		),
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static --enable-nasm --disable-frontend',
		'_info' : { 'version' : '3.99.5', 'fancy_name' : 'lame (library)' },
	},
	'twolame' : {
		'repo_type' : 'archive',
		'url' : 'https://sourceforge.net/projects/twolame/files/twolame/0.3.13/twolame-0.3.13.tar.gz',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static CPPFLAGS=-DLIBTWOLAME_STATIC',
		'_info' : { 'version' : '0.3.13', 'fancy_name' : 'twolame' },
	},
	'vidstab' : {
		'repo_type' : 'git',
		'url' : 'https://github.com/georgmartius/vid.stab.git', #"Latest commit 97c6ae2  on May 29, 2015" .. master then I guess?
		'needs_configure' : False,
		'is_cmake' : True,
		'cmake_options': '{cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={compile_prefix} -DENABLE_SHARED=OFF -DCMAKE_AR={cross_prefix_full}ar -DUSE_OMP=OFF', #fatal error: omp.h: No such file or directory
		'run_post_patch': (
			'sed -i.bak "s/SHARED/STATIC/g" CMakeLists.txt',
		),
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'vid.stab' },
	},
	'netcdf' : {
		'repo_type' : 'archive',
		'url' : 'ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-4.4.1.1.tar.gz', 
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static --disable-netcdf-4 --disable-dap',
		'_info' : { 'version' : '4.4.1.1', 'fancy_name' : 'netcdf' },
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
		'url' : 'https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/sources/libcaca-0.99.beta19.tar.gz',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static --libdir={compile_prefix}/lib --disable-cxx --disable-csharp --disable-java --disable-python --disable-ruby --disable-imlib2 --disable-doc --disable-examples',
		'_info' : { 'version' : '0.99.beta19', 'fancy_name' : 'libcaca' },
	},
	'libmodplug' : {
		'repo_type' : 'archive',
		'url' : 'https://sourceforge.net/projects/modplug-xmms/files/libmodplug/0.8.9.0/libmodplug-0.8.9.0.tar.gz',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'run_post_install': (
			# unfortunately this sed isn't enough, though I think it should be [so we add --extra-libs=-lstdc++ to FFmpegs configure] https://trac.ffmpeg.org/ticket/1539
			'sed -i.bak \'s/-lmodplug.*/-lmodplug -lstdc++/\' "{pkg_config_path}/libmodplug.pc"', # huh ?? c++?
			'sed -i.bak \'s/__declspec(dllexport)//\' "{compile_prefix}/include/libmodplug/modplug.h"', #strip DLL import/export directives
			'sed -i.bak \'s/__declspec(dllimport)//\' "{compile_prefix}/include/libmodplug/modplug.h"',
		),
		'_info' : { 'version' : '0.8.9.0', 'fancy_name' : 'libmodplug' },
	},
	'zvbi' : {
		'repo_type' : 'archive',
		'url' : 'https://sourceforge.net/projects/zapping/files/zvbi/0.2.35/zvbi-0.2.35.tar.bz2',
		'env_exports' : {
			'LIBS' : '-lpng',
		},
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static --disable-dvb --disable-bktr --disable-nls --disable-proxy --without-doxygen',
		'make_subdir' : 'src',
		'patches': (
		    ('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/zvbi-0.2.35_win32.patch', 'p0'),
			('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/zvbi-0.2.35_ioctl.patch', 'p0'),
		),
		#there is no .pc for zvbi, so we add --extra-libs=-lpng to FFmpegs configure TODO there is a .pc file it just doesn't get installed [?]
		#sed -i.bak 's/-lzvbi *$/-lzvbi -lpng/' "$PKG_CONFIG_PATH/zvbi.pc"
		'_info' : { 'version' : '0.2.35', 'fancy_name' : 'zvbi' },
	},
	'libvpx' : {
		'repo_type' : 'git', #master seems to work.. suprisingly .. go back to somewhere around f22b828d685adee4c7a561990302e2d21b5e0047 if it stops.
		#'branch' : 'tags/v1.6.1',
		'url' : 'https://chromium.googlesource.com/webm/libvpx', #
		'configure_options': '--target={bit_name2}-{bit_name_win}-gcc --prefix={compile_prefix} --disable-shared --enable-static --enable-vp9-highbitdepth', # examples,tools crash with x86_64-w64-mingw32-ld: unrecognised emulation mode: 64
		'env_exports' : {
			'CROSS' : '{cross_prefix_bare}',
		},
		'patches': (
			( 'https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/vpx_160_semaphore.patch', 'p1' ),
		),
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'libvpx' },
	},
	'libilbc' : {
		'repo_type' : 'git',
		'url' : 'https://github.com/dekkers/libilbc.git',
		'run_post_patch': (
			'autoreconf -fiv',
		),
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'libilbc' },
	},
	'fontconfig' : {
		'repo_type' : 'archive',
		'url' : 'https://www.freedesktop.org/software/fontconfig/release/fontconfig-2.12.1.tar.gz',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static --disable-docs',
		'run_post_install': (
			'sed -i.bak \'s/-L${{libdir}} -lfontconfig[^l]*$/-L${{libdir}} -lfontconfig -lfreetype -lexpat/\' "{pkg_config_path}/fontconfig.pc"',
		),
		'_info' : { 'version' : '2.12.1', 'fancy_name' : 'fontconfig' },
	},
	'libfribidi' : {
		#https://raw.githubusercontent.com/rdp/ffmpeg-windows-build-helpers/master/patches/fribidi.diff
		'repo_type' : 'archive',
		'url' : 'https://fribidi.org/download/fribidi-0.19.7.tar.bz2',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'_info' : { 'version' : '0.19.7', 'fancy_name' : 'libfribidi' },
	},
	'libass' : {
		'repo_type' : 'git',
		'url' : 'https://github.com/libass/libass.git',
		'branch' : '1be7dc0bdcf4ef44786bfc84c6307e6d47530a42', # latest still working on git..
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static --enable-silent-rules',
		'run_post_install': (
			'sed -i.bak \'s/-lass -lm/-lass -lfribidi -lfontconfig -lfreetype -lexpat -lm/\' "{pkg_config_path}/libass.pc"',
		),
		'depends_on' : [ 'harfbuzz', 'libfribidi','freetype2', 'iconv', ],
		'_info' : { 'version' : 'git (1be7dc)', 'fancy_name' : 'libass' },
	},
	'openjpeg' : {
		'env_exports' : {
			'AR' : '{cross_prefix_bare}ar',
			'CC' : '{cross_prefix_bare}gcc',
			'PREFIX' : '{compile_prefix}',
			'RANLIB' : '{cross_prefix_bare}ranlib',
			'LD'     : '{cross_prefix_bare}ld',
			'STRIP'  : '{cross_prefix_bare}strip',
			'CXX'    : '{cross_prefix_bare}g++',
		},
		'repo_type' : 'archive',
		'url' : 'https://github.com/uclouvain/openjpeg/archive/v2.1.2.tar.gz',
		'folder_name': 'openjpeg-2.1.2',
		'needs_configure' : False,
		'is_cmake' : True,
		'cmake_options': '. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={compile_prefix} -DBUILD_SHARED_LIBS:bool=off', #cmake .. "-DCMAKE_INSTALL_PREFIX=$mingw_w64_x86_64_prefix -DBUILD_SHARED_LIBS:bool=on -DCMAKE_SYSTEM_NAME=Windows"
		'_info' : { 'version' : '2.1.2', 'fancy_name' : 'openjpeg' },
	},
	'intel_quicksync_mfx' : {
		'repo_type' : 'git',
		'run_post_patch': (
			'autoreconf -fiv',
		),
		'url' : 'https://github.com/lu-zero/mfx_dispatch.git',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'intel_quicksync_mfx' },
	},
	'fdk_aac' : {
		'repo_type' : 'git',
		'run_post_patch': (
			'autoreconf -fiv',
		),
		'url' : 'https://github.com/mstorsjo/fdk-aac.git',
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'fdk-aac' },
	},
	'rtmpdump' : {
		'repo_type' : 'git',
		'url' : 'git://git.ffmpeg.org/rtmpdump',
		'needs_configure': False,
		'install_options' : 'SYS=mingw CRYPTO=GNUTLS OPT=-O2 CROSS_COMPILE={cross_prefix_bare} SHARED=no prefix={compile_prefix} LIB_GNUTLS="-L{compile_prefix}/lib -lgnutls -lnettle -lhogweed -lgmp -lcrypt32 -lws2_32 -liconv -lz"',
		'make_options': 'SYS=mingw CRYPTO=GNUTLS OPT=-O2 CROSS_COMPILE={cross_prefix_bare} SHARED=no prefix={compile_prefix} LIB_GNUTLS="-L{compile_prefix}/lib -lgnutls -lnettle -lhogweed -lgmp -lcrypt32 -lws2_32 -liconv -lz"',
		'run_post_install':(
			'sed -i.bak \'s/-lrtmp -lz/-lrtmp -lwinmm -lz/\' "{pkg_config_path}/librtmp.pc"',
		),
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'rtmpdump' },
	},
	'libx264' : {
		'repo_type' : 'git',
		'url' : 'https://git.videolan.org/git/x264.git',
		'rename_folder' : 'libx264_git',
		'configure_options': '--host={compile_target} --enable-static --cross-prefix={cross_prefix_bare} --prefix={compile_prefix} --enable-strip --disable-lavf',
		'_info' : { 'version' : 'git (master)', 'fancy_name' : 'x264 (library)' },
	},
}


if __name__ == "__main__": # use this as an example on how to implement this in custom building scripts.
	main = CrossCompileScript(PRODUCT_ORDER,PRODUCTS,DEPENDS,VARIABLES)
	main.commandLineEntrace()