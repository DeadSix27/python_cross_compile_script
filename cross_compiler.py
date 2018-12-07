#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ####################################################
# Copyright (C) 2018 DeadSix27 (https://github.com/DeadSix27/python_cross_compile_script)
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
# ### Settings are located in cross_compiler.yaml ###
# ###### That file will be generated on start. ######
# ###################################################

# ###################################################
# ################ REQUIRED PACKAGES ################
# ###################################################
# Package dependencies (some may be missing):
# sudo apt install build-essential autogen libtool libtool-bin pkg-config texinfo yasm git make automake gcc pax cvs subversion flex bison patch mercurial cmake gettext autopoint libxslt1.1 docbook-utils rake docbook-xsl gperf gyp p7zip-full p7zip docbook-to-man pandoc rst2pdf

import progressbar # Run pip3 install progressbar2
import requests # Run pip3 install requests
import yaml

import os.path,logging,re,subprocess,sys,shutil,urllib.request,urllib.parse,stat
import hashlib,glob,traceback,time,zlib,codecs,argparse,ast
import http.cookiejar
from multiprocessing import cpu_count
from pathlib import Path
from urllib.parse import urlparse
from collections import OrderedDict

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

class MyLogFormatter(logging.Formatter):
	def __init__(self,l,ld):
		MyLogFormatter.log_format = l
		MyLogFormatter.log_date_format = ld
		MyLogFormatter.inf_fmt  = Colors.LIGHTCYAN_EX   + MyLogFormatter.log_format + Colors.RESET
		MyLogFormatter.err_fmt  = Colors.LIGHTRED_EX    + MyLogFormatter.log_format + Colors.RESET
		MyLogFormatter.dbg_fmt  = Colors.LIGHTYELLOW_EX + MyLogFormatter.log_format + Colors.RESET
		MyLogFormatter.war_fmt  = Colors.YELLOW         + MyLogFormatter.log_format + Colors.RESET
		super().__init__(fmt="%(levelno)d: %(msg)s", datefmt=MyLogFormatter.log_date_format, style='%')

	def format(self, record):
		if not hasattr(record,"type"):
			record.type = ""
		else:
			record.type = "[" + record.type.upper() + "]"
		
		format_orig = self._style._fmt
		if record.levelno == logging.DEBUG:
			self._style._fmt = MyLogFormatter.dbg_fmt
		elif record.levelno == logging.INFO:
			self._style._fmt = MyLogFormatter.inf_fmt
		elif record.levelno == logging.ERROR:
			self._style._fmt = MyLogFormatter.err_fmt
		elif record.levelno == logging.WARNING:
			self._style._fmt = MyLogFormatter.war_fmt
		result = logging.Formatter.format(self, record)
		self._style._fmt = format_orig
		return result

class CrossCompileScript:

	def __init__(self):
		sys.dont_write_bytecode     = True # Avoid __pycache__ folder, never liked that solution.	
		hdlr                        = logging.StreamHandler(sys.stdout)
		fmt                         = MyLogFormatter("[%(asctime)s][%(levelname)s]%(type)s %(message)s","%H:%M:%S")
		hdlr.setFormatter(fmt)
		self.logger                 = logging.getLogger(__name__)
		self.logger.addHandler(hdlr)
		self.logger.setLevel(logging.INFO)
		self.config                 = self.loadConfig()
		fmt                         = MyLogFormatter(self.config["script"]["log_format"],self.config["script"]["log_date_format"])
		hdlr.setFormatter(fmt)
		self.packages               = self.loadPackages(self.config["script"]["packages_folder"])
		self.init()
		
	def errorExit(self,msg):
		self.logger.error(msg)
		sys.exit(1)
	
		
	def loadPackages(self,packages_folder):
		def isPathDisabled(path):
			for part in path.parts:
				if part.lower().startswith("_disabled"):
					return True
			return False
			
		depsFolder = Path(os.path.join(packages_folder,"dependencies"))
		prodFolder = Path(os.path.join(packages_folder,"products"))
		varsPath   = Path(os.path.join(packages_folder,"variables.py"))
	
		if not os.path.isdir(packages_folder):
			self.errorExit("Packages folder '%s' does not exist." % (packages_folder))
		if not os.path.isdir(depsFolder): #TODO simplify code
			self.errorExit("Packages folder '%s' does not exist." % (depsFolder))
		if not os.path.isfile(varsPath):
			self.errorExit("Variables file '%s' does not exist." % (varsPath))
			
		tmpPkglist = { 'deps' : [], 'prods' : [], 'vars' : [] }
		packages = { 'deps' : {}, 'prods' : {}, 'vars' : {} }
			
		for path, subdirs, files in os.walk(depsFolder):
			for name in files:
				p = Path(os.path.join(path, name))
				if p.suffix == ".py" :
					if not isPathDisabled(p):
						tmpPkglist["deps"].append(p)
				
		for path, subdirs, files in os.walk(prodFolder):
			for name in files:
				p = Path(os.path.join(path, name))
				if p.suffix == ".py":
					if not isPathDisabled(p):
						tmpPkglist["prods"].append(p)
				
		if len(tmpPkglist["deps"]) < 1: #TODO simplify code
			self.errorExit("There's no packages in the folder '%s'." % (depsFolder))
				
		if len(tmpPkglist["prods"]) < 1:
			self.errorExit("There's no packages in the folder '%s'." % (prodFolder))
		
		with open(varsPath,"r",encoding="utf-8") as f:
			try:
				o = ast.literal_eval(f.read()) # was gonna use .json instead of eval on py files, but I like having multiline strings and comments.. so.
				if not isinstance(o, dict):
					self.errorExit("Variables file is misformatted")					
				packages["vars"] = o
			except SyntaxError:
				self.errorExit("Loading variables.py failed:\n\n" + traceback.format_exc())
			
		for d in tmpPkglist["deps"]:
			with open(d,"r",encoding="utf-8") as f:
				p = Path(d)
				package_name = p.stem.lower()
				try:
					o = ast.literal_eval(f.read())
					if not isinstance(o, dict):
						self.errorExit("Package file '%s' is misformatted" % (p.name))
						
					if "_info" not in o and not self.bool_key(o,"is_dep_inheriter"):
						self.logger.warning("Package '%s.py' is missing '_info' tag." % (package_name))
					
					if self.bool_key(o,"_disabled"):
						self.logger.debug("Package '%s.py' has option '_disabled' set, not loading." % (package_name))						
					else:
						packages["deps"][package_name] = o
						
				except SyntaxError as e:
					self.errorExit("Loading '%s.py' failed:\n\n%s" % ( package_name,traceback.format_exc() ))
		
		for d in tmpPkglist["prods"]:
			with open(d,"r",encoding="utf-8") as f:
				p = Path(d)
				package_name = p.stem.lower()
				try:
					o = ast.literal_eval(f.read())
					if not isinstance(o, dict):
						self.errorExit("Package file '%s' is misformatted" % (p.name))
						
					if "_info" not in o and not self.bool_key(o,"is_dep_inheriter"):
						self.logger.warning("Package '%s.py' is missing '_info' tag." % (package_name))
						
					if self.bool_key(o,"_disabled"):
						self.logger.debug("Package '%s.py' has option '_disabled' set, not loading." % (package_name))
					else:
						packages["prods"][package_name] = o
						
				except SyntaxError as e:
					self.errorExit("Loading '%s.py' failed:\n\n%s" % ( package_name,traceback.format_exc() ))
		
		self.logger.info("Loaded %d packages", len(packages["prods"])+len(packages["deps"]))
		return packages
		
	def confDiff(self,default,users): # very basic config comparison		
		for category in default:
			if category not in users:
				return ( False, "User config is missing '%s' category, please delete your config to regenerate a new one or add it manually." % (category) )
			elif category != "version":
				for option in default[category]:
					if option not in users[category]:
						return ( False, "User config is missing '%s' option in '%s' category, please delete your config to regenerate a new one or add it manually." % (option,category) )
		return ( True, 'Config Ok' )
		
	def loadConfig(self):
		self.config = { # Default config
			'version': 1.0,
			'script': {
				'debug' : False,
				'quiet': False,
				'log_date_format': '%H:%M:%S',
				'log_format': '[%(asctime)s][%(levelname)s]%(type)s %(message)s',
				'product_order': ['mpv', 'ffmpeg_static', 'ffmpeg_shared'],
				'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
				'mingw_script_url' : 'https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/mingw_toolchain_script/mingw_toolchain_script.py',
				'overwrite_mingw_script': True,
				'packages_folder' : 'packages',
			},
			'toolchain': {
				'bitness': [64,],
				'cpu_count': cpu_count(),
				'mingw_commit': None,
				'mingw_debug_build': False,
				'mingw_dir': 'toolchain',
				'work_dir': 'workdir',
				'original_cflags': '-O3',
			}
		}
		
		config_file = Path(__file__).stem + ".yaml"
		
		if not os.path.isfile(config_file):
			self.writeDefaultConfig(config_file)
		
		conf = None
		
		with open(config_file, 'r') as cs:
			try:
				conf = yaml.load(cs)
			except yaml.YAMLError as e:
				self.logger.error("Failed to load config file " + str(e))
				traceback.print_exc()
				sys.exit(1)
		import pprint
		
		confCheck = self.confDiff(self.config,conf)
		
		if confCheck[0]:
			return conf
		else:
			self.logger.error("%s" % (confCheck[1]))
			sys.exit(1)
			return None
				
	def writeDefaultConfig(self,config_file):
		with open(config_file,"w",encoding="utf-8") as f:
			f.write(yaml.dump(self.config))
		self.logger.info("Wrote default configuration file to: '%s'" % (config_file))

	def init(self):
		self.product_order          = self.config["script"]["product_order"]
		self.fullCurrentPath        = os.getcwd()
		self.fullPatchDir           = os.path.join(self.fullCurrentPath,"patches")
		self.fullWorkDir            = os.path.join(self.fullCurrentPath,self.config["toolchain"]["work_dir"])
		self.mingwDir               = self.config["toolchain"]["mingw_dir"]
		self.fullProductDir         = None
		self.targetBitness          = self.config["toolchain"]["bitness"]
		self.originalPATH           = os.environ["PATH"]
		self.mingwScriptURL         = self.config["script"]["mingw_script_url"]
		self.targetHost             = None
		self.targetPrefix           = None
		self.mingwBinpath           = None
		self.mingwBinpath2          = None
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
		self.quietMode              = self.config["script"]["quiet"]
		self.debugMode              = self.config["script"]["debug"]
		self.userAgent              = self.config["script"]["user_agent"]
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
							if val['repo_type'] == 'git' or val['repo_type'] == 'mercurial':
								if 'branch' in val:
									if val['branch'] != None:
										rTypeStr = 'git' if val['repo_type'] == 'git' else 'hg '
										cVer = rTypeStr + ' (' + val['branch'][0:6] + ')'
								else:
									cVer = 'git (master)' if val['repo_type'] == 'git' else 'hg (default)'
								val['_info']['version'] = cVer
								
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
							if val['repo_type'] == 'git' or val['repo_type'] == 'mercurial':
								if 'branch' in val:
									if val['branch'] != None:
										rTypeStr = 'git' if val['repo_type'] == 'git' else 'hg '
										cVer = rTypeStr + ' (' + val['branch'][0:6] + ')'
								else:
									cVer = 'git (master)' if val['repo_type'] == 'git' else 'hg (default)'
								val['_info']['version'] = cVer
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
							if val['repo_type'] == 'git' or val['repo_type'] == 'mercurial':
								if 'branch' in val:
									if val['branch'] != None:
										rTypeStr = 'git' if val['repo_type'] == 'git' else 'hg '
										cVer = rTypeStr + ' (' + val['branch'][0:6] + ')'
								else:
									cVer = 'git (master)' if val['repo_type'] == 'git' else 'hg (default)'
								val['_info']['version'] = cVer
							
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
							if val['repo_type'] == 'git' or val['repo_type'] == 'mercurial':
								if 'branch' in val:
									if val['branch'] != None:
										rTypeStr = 'git' if val['repo_type'] == 'git' else 'hg '
										cVer = rTypeStr + ' (' + val['branch'][0:6] + ')'
								else:
									cVer = 'git (master)' if val['repo_type'] == 'git' else 'hg (default)'
								val['_info']['version'] = cVer
							
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

		_epilog = 'Copyright (C) 2018 DeadSix27 (https://github.com/DeadSix27/python_cross_compile_script)\n\n This Source Code Form is subject to the terms of the Mozilla Public\n License, v. 2.0. If a copy of the MPL was not distributed with this\n file, You can obtain one at https://mozilla.org/MPL/2.0/.\n '

		parser = argparse.ArgumentParser(formatter_class=epiFormatter, epilog=_epilog)
		parser.set_defaults(which='main')
		parser.description = Colors.CYAN + 'Pythonic Cross Compile Helper (MPL2.0)' + Colors.RESET + '\n\nExample usages:' \
			'\n "{0} list -p"             - lists all the products' \
			'\n "{0} -a"                  - builds everything' \
			'\n "{0} -f -d libx264"       - forces the rebuilding of libx264' \
			'\n "{0} -pl x265_10bit,mpv"  - builds this list of products in that order' \
			'\n "{0} -q -p ffmpeg_static" - will quietly build ffmpeg-static'.format(parser.prog)

		subparsers = parser.add_subparsers(help='Sub commands')

		list_p = subparsers.add_parser('list', help= 'Type: \'' + parser.prog + ' list --help\' for more help')
		list_p.set_defaults(which='list_p')

		list_p.add_argument('-md', '--markdown', help='Print list in markdown format', action='store_true')
		list_p.add_argument('-cv', '--csv', help='Print list as CSV-like string', action='store_true')
		list_p_group1 = list_p.add_mutually_exclusive_group(required=True)
		list_p_group1.add_argument('-p', '--products',    nargs=0, help='List all products',     action=self.listify_pdeps(self.packages["prods"],"P"))
		list_p_group1.add_argument('-d', '--dependencies', nargs=0, help='List all dependencies', action=self.listify_pdeps(self.packages["deps"], "D"))


		chelps_p = subparsers.add_parser('chelps', help= 'Type: \'' + parser.prog + ' chelps --help\' for more help')
		list_p.set_defaults(which='chelps_p')
		chelps_p_group1 = chelps_p.add_mutually_exclusive_group(required=True)
		chelps_p_group1.add_argument('-p', '--products',    nargs=0, help='Write all product config helps to confighelps.txt',     action=self.assembleConfigHelps(self.packages["prods"],"P",self))
		chelps_p_group1.add_argument('-d', '--dependencies', nargs=0, help='Write all dependency config helps to confighelps.txt',  action=self.assembleConfigHelps(self.packages["deps"], "D",self))
		
		info_p = subparsers.add_parser('info', help= 'Type: \'' + parser.prog + ' info --help\' for more help')
		info_p.set_defaults(which='info_p')
		
		info_p_group1 = info_p.add_mutually_exclusive_group( required = True )
		info_p_group1.add_argument('-r', '--required-by', help='List all packages this dependency is required by')
		


		group2 = parser.add_mutually_exclusive_group( required = False )
		group2.add_argument( '-p',  '--build-product',         dest='PRODUCT',         help='Build the specificed product package(s)'                         )
		group2.add_argument( '-d',  '--build-dependency',      dest='DEPENDENCY',      help='Build the specificed dependency package(s)'                      )
		group2.add_argument( '-a',  '--build-all',                                     help='Build all products (according to order)'   , action='store_true' )
		parser.add_argument( '-q',  '--quiet',                                         help='Only show info lines'                      , action='store_true' )
		parser.add_argument( '-f',  '--force',                                         help='Force rebuild, deletes already files'      , action='store_true' )
		parser.add_argument( '-g',  '--debug',                                         help='Show debug information'                    , action='store_true' )
		parser.add_argument( '-s',  '--skip-depends',                                  help='Skip dependencies when building'           , action='store_true' )

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
			
			if args.which == "info_p":
				self.listRequiredBy(args.required_by)
				return
			
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

			finalPkgList = []

			if args.PRODUCT or args.DEPENDENCY:
				strPkgs = args.DEPENDENCY
				buildType = "DEPENDENCY"
				if args.PRODUCT != None:
					strPkgs = args.PRODUCT
					buildType = "PRODUCT"
				pkgList = re.split(r'(?<!\\),', strPkgs)
				for p in pkgList:
					if buildType == "PRODUCT":
						if p not in self.packages["prods"]:
							self.errorExit("Product package '%s' does not exist." % (p))
					if buildType == "DEPENDENCY":
						if p not in self.packages["deps"]:
							self.errorExit("Dependency package '%s' does not exist." % (p))
					
					finalPkgList.append(p.replace("\\,",","))

			elif args.build_all:
				self.defaultEntrace()
				return

			self.logger.info('Starting custom build process for: {0}'.format(",".join(finalPkgList)))
			
			skipDeps = False
			
			if args.skip_depends:
				skipDeps = True

			for thing in finalPkgList:
				for b in self.targetBitness:
					main.prepareBuilding(b)
					main.build_mingw(b)
					main.initBuildFolders()
					if buildType == "PRODUCT":
						self.build_thing(thing,self.packages["prods"][thing],buildType,forceRebuild,skipDeps)
					else:
						self.build_thing(thing,self.packages["deps"][thing],buildType,forceRebuild,skipDeps)
					main.finishBuilding()
					
	def listRequiredBy(self,o):
		ptype = None
		if o in self.packages["prods"]:
			ptype = "prods"
		elif o in self.packages["deps"]:
			ptype = "deps"
		else:
			self.logger.error("'%s' is not an existing package." % (o))
			sys.exit(1)
			
		prods_requiring_it = []
		deps_requiring_it = []
		
		for p in self.packages["deps"]:
			pkg = self.packages["deps"][p]
			if "depends_on" in pkg:
				if o in pkg["depends_on"]:
					deps_requiring_it.append(p)
		for p in self.packages["prods"]:
			pkg = self.packages["prods"][p]
			if "depends_on" in pkg:
				if o in pkg["depends_on"]:
					prods_requiring_it.append(p)
					
		if len(prods_requiring_it) > 0 or len(deps_requiring_it) > 0:
			self.logger.info("Packages requiring '%s':" % (o))
			if len(deps_requiring_it) > 0:
				self.logger.info("\tDependencies: %s" % (",".join(deps_requiring_it)))
			if len(prods_requiring_it) > 0:
				self.logger.info("\tProducts    : %s" % (",".join(prods_requiring_it)))
		else:
			self.logger.warning("There are no packages that require '%s'." % (o))
		
		sys.exit(0)

	def defaultEntrace(self):
		for b in self.targetBitness:
			self.prepareBuilding(b)
			self.build_mingw(b)
			self.initBuildFolders()
			for p in self.product_order:
				self.build_thing(p,self.packages["prods"][p],"PRODUCT")
			self.finishBuilding()

	def finishBuilding(self):
		self.cchdir("..")

	def prepareBuilding(self,b):
		self.logger.info('Starting build script')
		if not os.path.isdir(self.fullWorkDir):
			self.logger.info("Creating workdir: %s" % (self.fullWorkDir))
			os.makedirs(self.fullWorkDir, exist_ok=True)
		self.cchdir(self.fullWorkDir)

		self.bitnessDir         = "x86_64" if b is 64 else "i686" # e.g x86_64
		self.bitnessDir2        = "x86_64" if b is 64 else "x86" # just for vpx...
		self.bitnessDir3        = "mingw64" if b is 64 else "mingw" # just for openssl...
		self.winBitnessDir      = "win64" if b is 64 else "win32" # e.g win64
		self.targetHost         = "{0}-w64-mingw32".format ( self.bitnessDir ) # e.g x86_64-w64-mingw32
		self.targetPrefix       = "{0}/{1}/{2}-w64-mingw32/{3}".format( self.fullWorkDir, self.mingwDir, self.bitnessDir, self.targetHost ) # workdir/xcompilers/mingw-w64-x86_64/x86_64-w64-mingw32
		self.inTreePrefix       = "{0}".format( os.path.join(self.fullWorkDir,self.bitnessDir) ) # workdir/x86_64
		self.offtreePrefix      = "{0}".format( os.path.join(self.fullWorkDir,self.bitnessDir + "_offtree") ) # workdir/x86_64_offtree
		self.targetSubPrefix    = "{0}/{1}/{2}-w64-mingw32".format( self.fullWorkDir, self.mingwDir, self.bitnessDir ) # e.g workdir/xcompilers/mingw-w64-x86_64
		self.mingwBinpath       = "{0}/{1}/{2}-w64-mingw32/bin".format( self.fullWorkDir, self.mingwDir, self.bitnessDir ) # e.g workdir/xcompilers/mingw-w64-x86_64/bin
		self.mingwBinpath2      = "{0}/{1}/{2}-w64-mingw32/{2}-w64-mingw32/bin".format( self.fullWorkDir, self.mingwDir, self.bitnessDir ) # e.g workdir/xcompilers/x86_64-w64-mingw32/x86_64-w64-mingw32/bin
		self.fullCrossPrefix    = "{0}/{1}-w64-mingw32-".format( self.mingwBinpath, self.bitnessDir ) # e.g workdir/xcompilers/mingw-w64-x86_64/bin/x86_64-w64-mingw32-
		self.bareCrossPrefix    = "{0}-w64-mingw32-".format( self.bitnessDir ) # e.g x86_64-w64-mingw32-
		self.makePrefixOptions  = "CC={cross_prefix_bare}gcc AR={cross_prefix_bare}ar PREFIX={target_prefix} RANLIB={cross_prefix_bare}ranlib LD={cross_prefix_bare}ld STRIP={cross_prefix_bare}strip CXX={cross_prefix_bare}g++".format( cross_prefix_bare=self.bareCrossPrefix, target_prefix=self.targetPrefix )
		self.cmakePrefixOptions = "-G\"Unix Makefiles\" -DCMAKE_SYSTEM_PROCESSOR=\"{bitness}\" -DENABLE_STATIC_RUNTIME=1 -DCMAKE_SYSTEM_NAME=Windows -DCMAKE_RANLIB={cross_prefix_full}ranlib -DCMAKE_C_COMPILER={cross_prefix_full}gcc -DCMAKE_CXX_COMPILER={cross_prefix_full}g++ -DCMAKE_RC_COMPILER={cross_prefix_full}windres -DCMAKE_FIND_ROOT_PATH={target_prefix}".format(cross_prefix_full=self.fullCrossPrefix, target_prefix=self.targetPrefix,bitness=self.bitnessDir )
		self.pkgConfigPath      = "{0}/lib/pkgconfig".format( self.targetPrefix ) #e.g workdir/xcompilers/mingw-w64-x86_64/x86_64-w64-mingw32/lib/pkgconfig
		self.fullProductDir     = os.path.join(self.fullWorkDir,self.bitnessDir + "_products")
		self.currentBitness     = b
		self.mesonEnvFile       = os.path.join(self.targetSubPrefix, "meson_environment.txt")
		self.cpuCount           = self.config["toolchain"]["cpu_count"]
		self.originalCflags     = self.config["toolchain"]["original_cflags"]

		if self.debugMode:
			print('self.bitnessDir = \n'         + self.bitnessDir + '\n\n')
			print('self.bitnessDir2 = \n'        + self.bitnessDir2 + '\n\n')
			print('self.winBitnessDir = \n'      + self.winBitnessDir + '\n\n')
			print('self.targetHost = \n'      + self.targetHost + '\n\n')
			print('self.targetPrefix = \n'      + self.targetPrefix + '\n\n')
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
		#os.environ["PATH"]           = "{0}:{1}:{2}".format ( self.mingwBinpath, os.path.join(self.targetPrefix,'bin'), self.originalPATH ) #todo properly test this..
		os.environ["PKG_CONFIG_PATH"] = self.pkgConfigPath
		os.environ["PKG_CONFIG_LIBDIR"] = ""
		os.environ["COLOR"] = "ON" # Force coloring on (for CMake primarily)
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
			
	def bool_key(self,d,k):
		if k in d:
			if d[k]:
				return True
		return False

	def build_mingw(self,bitness):
		gcc_bin = os.path.join(self.mingwBinpath, self.bitnessDir + "-w64-mingw32-gcc")

		if os.path.isfile(gcc_bin):
			gccOutput = subprocess.check_output(gcc_bin + " -v", shell=True, stderr=subprocess.STDOUT).decode("utf-8")
			workingGcc = re.compile("^Target: .*-w64-mingw32$", re.MULTILINE).findall(gccOutput)
			if len(workingGcc) > 0:
				self.logger.info("MinGW-w64 install is working!")
				return
			else:
				raise Exception("GCC is not working properly, target is not mingw32.")
				exit(1)

		elif not os.path.isdir(self.mingwDir):
			self.logger.info("Building MinGW-w64 in folder '{0}'".format( self.mingwDir ))

			# os.makedirs(self.mingwDir, exist_ok=True)

			os.unsetenv("CFLAGS")

			# self.cchdir(self.mingwDir)
			
			download_toolchain_script = False
			if not os.path.isfile(os.path.join(self.fullCurrentPath,"mingw_toolchain_script.py")):
				download_toolchain_script = True
			elif self.config["script"]["overwrite_mingw_script"]:
				download_toolchain_script = True
				
			mingw_script_file = None
			
			if download_toolchain_script:
				mingw_script_file = self.download_file(self.mingwScriptURL,outputPath = self.fullCurrentPath)

			def toolchainBuildStatus(data):
				self.logger.info(data)

			from mingw_toolchain_script import MinGW64ToolChainBuilder

			toolchainBuilder = MinGW64ToolChainBuilder()

			toolchainBuilder.workDir = self.mingwDir
			if self.config["toolchain"]["mingw_commit"] != None:
				toolchainBuilder.setMinGWcheckout(self.config["toolchain"]["mingw_commit"])
			toolchainBuilder.setDebugBuild(self.config["toolchain"]["mingw_debug_build"])
			toolchainBuilder.onStatusUpdate += toolchainBuildStatus
			toolchainBuilder.build()

			# self.cchdir("..")
		else:
			self.logger.error("It looks like the previous MinGW build failed, please delete the folder '%s' and re-run this script" % self.mingwDir)
			sys.exit(1)
	#:

	def downloadHeader(self,url):
		destination = os.path.join(self.targetPrefix,"include")
		fileName = os.path.basename(urlparse(url).path)

		if not os.path.isfile(os.path.join(destination,fileName)):
			fname = self.download_file(url)
			self.logger.debug("Moving Header File: '{0}' to '{1}'".format( fname, destination ))
			shutil.move(fname, destination)
		else:
			self.logger.debug("Header File: '{0}' already downloaded".format( fileName ))

	def download_file(self,url=None, outputFileName=None, outputPath=None, bytes=False):
		def fmt_size(num, suffix="B"):
				for unit in ["","Ki","Mi","Gi","Ti","Pi","Ei","Zi"]:
					if abs(num) < 1024.0:
						return "%3.1f%s%s" % (num, unit, suffix)
					num /= 1024.0
				return "%.1f%s%s" % (num, "Yi", suffix)
		#:
		if not url:
			raise Exception("No URL specified.")

		if outputPath is None: # Default to current dir.
			outputPath = os.getcwd()
		else:
			if not os.path.isdir(outputPath):
				raise Exception('Specified path "{0}" does not exist'.format(outputPath))

		fileName = os.path.basename(url) # Get URL filename
		userAgent = self.userAgent

		if 'sourceforge.net' in url.lower():
			userAgent = 'wget/1.18' # sourceforce <3 wget

		if url.lower().startswith("ftp://"):
			self.logger.info("Requesting : {0}".format(url))
			if outputFileName != None:
				fileName = outputFileName
			fullOutputPath = os.path.join(outputPath,fileName)
			urllib.request.urlretrieve(url, fullOutputPath)
			return fullOutputPath

		if url.lower().startswith("file://"):
			url = url.replace("file://","")
			self.logger.info("Copying : {0}".format(url))
			if outputFileName != None:
				fileName = outputFileName
			fullOutputPath = os.path.join(outputPath,fileName)
			try:
				shutil.copyfile(url, fullOutputPath)
			except Exception as e:
				print(e)
				exit(1)
			return fullOutputPath

		req = requests.get(url, stream=True, headers = { "User-Agent": userAgent } )

		if req.status_code != 200:
			req.raise_for_status()

		if "content-disposition" in req.headers:
			reSponse = re.findall("filename=(.+)", req.headers["content-disposition"])
			if reSponse == None:
				fileName = os.path.basename(url)
			else:
				fileName = reSponse[0]

		size = None
		compressed = False
		if "Content-Length" in req.headers:
			size = int(req.headers["Content-Length"])

		if "Content-Encoding" in req.headers:
			if req.headers["Content-Encoding"] == "gzip":
				compressed = True

		self.logger.info("Requesting : {0} - {1}".format(url, fmt_size(size) if size!=None else "?" ))

		# terms = shutil.get_terminal_size((100,100))
		# filler = 0
		# if terms[0] > 100:
		# 	filler = int(terms[0]/4)

		widgetsNoSize = [
			progressbar.FormatCustomText("Downloading: {:25.25}".format(os.path.basename(fileName)))," ",
			progressbar.AnimatedMarker(markers='|/-\\'), " ",
			progressbar.DataSize()
			# " "*filler
		]
		widgets = [
			progressbar.FormatCustomText("Downloading: {:25.25}".format(os.path.basename(fileName)))," ",
			progressbar.Percentage(), " ",
			progressbar.Bar(fill=chr(9617), marker=chr(9608), left="[", right="]"), " ",
			progressbar.DataSize(), "/", progressbar.DataSize(variable="max_value"), " |",
			progressbar.AdaptiveTransferSpeed(), " | ",
			progressbar.ETA(),
			# " "*filler
		]
		pbar = None
		if size == None:
			pbar = progressbar.ProgressBar(widgets=widgetsNoSize,maxval=progressbar.UnknownLength)
		else:
			pbar = progressbar.ProgressBar(widgets=widgets,maxval=size)

		if outputFileName != None:
			fileName = outputFileName
		fullOutputPath = os.path.join(outputPath,fileName)

		updateSize = 0

		if isinstance(pbar.max_value, int):
			updateSize = pbar.max_value if pbar.max_value < 1024 else 1024

		if bytes == True:
			output = b""
			bytesrecv = 0
			pbar.start()
			for buffer in req.iter_content(chunk_size=1024):
				if buffer:
					 output += buffer
				if compressed:
					pbar.update(updateSize)
				else:
					pbar.update(bytesrecv)
				bytesrecv += len(buffer)
			pbar.finish()
			return output
		else:
			with open(fullOutputPath, "wb") as file:
				bytesrecv = 0
				pbar.start()
				for buffer in req.iter_content(chunk_size=1024):
					if buffer:
						file.write(buffer)
						file.flush()
					if compressed:
						pbar.update(updateSize)
					else:
						pbar.update(bytesrecv)
					bytesrecv += len(buffer)
				pbar.finish()

				return fullOutputPath
	#:
	
	def create_meson_environment_file(self):
		if not os.path.isfile(self.mesonEnvFile):
			self.logger.info("Creating Meson Environment file at: '%s'" % (self.mesonEnvFile))
			with open(self.mesonEnvFile, 'w') as f:
				f.write("[binaries]\n")
				f.write("c = '{0}gcc'\n".format(self.fullCrossPrefix))
				f.write("cpp = '{0}g++'\n".format(self.fullCrossPrefix))
				f.write("ld = '{0}ld'\n".format(self.fullCrossPrefix))
				f.write("ar = '{0}ar'\n".format(self.fullCrossPrefix))
				f.write("strip = '{0}strip'\n".format(self.fullCrossPrefix))
				f.write("windres = '{0}windres'\n".format(self.fullCrossPrefix))
				f.write("ranlib = '{0}ranlib'\n".format(self.fullCrossPrefix))
				f.write("pkgconfig = '{0}pkg-config'\n".format(self.fullCrossPrefix)) # ??
				f.write("dlltool = '{0}dlltool'\n".format(self.fullCrossPrefix))
				f.write("gendef = '{0}/gendef'\n".format(self.mingwBinpath))
				f.write("needs_exe_wrapper = false\n")
				f.write("#exe_wrapper = 'wine' # A command used to run generated executables.\n")
				f.write("\n")
				f.write("[host_machine]\n")
				f.write("system = 'windows'\n")
				f.write("cpu_family = '{0}'\n".format(self.bitnessDir))
				f.write("cpu = '{0}'\n".format(self.bitnessDir))
				f.write("endian = 'little'\n")
				f.write("\n")
				f.write("[target_machine]\n")
				f.write("system = 'windows'\n")
				f.write("cpu_family = '{0}'\n".format(self.bitnessDir))
				f.write("cpu = '{0}'\n".format(self.bitnessDir))
				f.write("endian = 'little'\n")
				f.write("\n")
				f.write("[properties]\n")
				f.write("c_link_args = ['-static', '-static-libgcc']\n")
				f.write("# sys_root = Directory that contains 'bin', 'lib', etc for the toolchain and system libraries\n")
				f.write("sys_root = '{0}'\n".format(self.targetSubPrefix))
				f.close()

	def download_file_old(self,link, targetName = None):
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
			self.logger.warning("WARNING: Using non-SSL http is not advised..") # gotta get peoples attention somehow eh?

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
			print("Error downloading: " + link)
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

	def download_file_v2(url=None, outputFileName=None, outputPath=None, bytes=False ):
		if not url:
			raise Exception('No url')
		if outputPath is None:
			outputPath = os.getcwd()
		else:
			if not os.path.isdir(outputPath):
				raise Exception('Path "" does not exist'.format(outputPath))
		fileName =  url.split('/')[-1] #base fallback name
		print("Connecting to: " + url)
		req = requests.get(url, stream=True, headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'})
		if req.status_code != 404:
			if 'content-disposition' in req.headers:
				fileName = req.headers['content-disposition']
			size = None
			if 'Content-Length' in req.headers:
				size = int(req.headers['Content-Length'])

			if 'Content-Encoding' in req.headers:
				if req.headers['Content-Encoding'] == "gzip":
					size = None

			print("Downloading: '{0}' {1}".format(url, fmt_size(size) if size!=None else "?" ))
			widgetsNoSize = [
				progressbar.Percentage(), " ",
				progressbar.Bar(fill=chr(9617), marker=chr(9608), left="[", right="]"), " ",
				progressbar.DataSize(),
			]
			widgets = [
				progressbar.Percentage(), " ",
				progressbar.Bar(fill=chr(9617), marker=chr(9608), left="[", right="]"), " ",
				progressbar.DataSize(), "/", progressbar.DataSize(variable="max_value"), " |",
				progressbar.AdaptiveTransferSpeed(), " | ",
				progressbar.ETA(),
			]
			pbar = None
			if size == None:
				pbar = progressbar.ProgressBar(widgets=widgetsNoSize,maxval=progressbar.UnknownLength)
			else:
				pbar = progressbar.ProgressBar(widgets=widgets,maxval=size)
			if outputFileName != None:
				fileName = outputFileName
			fullOutputPath = os.path.join(outputPath,fileName)

			if bytes == True:
				output = b''
				bytesrecv = 0
				pbar.start()
				for buffer in req.iter_content(chunk_size=1024):
					if buffer:
						 output += buffer
					pbar.update(bytesrecv)
					bytesrecv += len(buffer)
				pbar.finish()
				return output
			else:
				with open(fullOutputPath, "wb") as file:
					bytesrecv = 0
					pbar.start()
					for buffer in req.iter_content(chunk_size=1024):
						if buffer:
							file.write(buffer)
							file.flush()
						pbar.update(bytesrecv)
						bytesrecv += len(buffer)
					pbar.finish()

					return fullOutputPath
	#:

	def run_process(self,command,ignoreErrors = False, exitOnError = True):
		isSvn = False
		if not isinstance(command, str):
			command = " ".join(command) # could fail I guess
		if command.lower().startswith("svn"):
			isSvn = True
		self.logger.debug("Running '{0}' in '{1}'".format(command,os.getcwd()))
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

	def hash_file(self,fname,type = "sha256"):
		hash = None
		if type == "sha256":
			hash = hashlib.sha256()
		elif type == "sha512":
			hash = hashlib.sha512()
		elif type == "md5":
			hash = hashlib.md5()
		elif type == "blake2b":
			hash = hashlib.blake2b()
		with open(fname, "rb") as f:
			for chunk in iter(lambda: f.read(4096), b""):
				hash.update(chunk)
		return hash.hexdigest()

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
	def git_clone(self,url,virtFolderName=None,renameTo=None,desiredBranch=None,recursive=False,doNotUpdate=False,desiredPR=None):
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
			if desiredPR != None:
				self.logger.warning("####################")
				self.logger.info("Git repositiories with set PR will not auto-update, please delete the repo and retry to do so.")
				self.logger.warning("####################")
			elif doNotUpdate == True:
				self.logger.info("####################")
				self.logger.info("do_not_git_update == true")
				self.logger.info("####################")
			else:
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
					self.run_process('git clean -ffdx') #https://gist.github.com/nicktoumpelis/11214362
					self.run_process('git submodule foreach --recursive git clean -ffdx')
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
			if desiredPR != None:
				self.cchdir(realFolderName + ".tmp")
				self.logger.info("GIT Fetching PR: {0}".format(desiredPR))
				self.run_process('git fetch origin refs/pull/{0}/head'.format(desiredPR))
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
	def verify_hash(self,file,hash):
		if hash["type"] not in ["sha256","sha512","md5","blake2b"]:
			raise Exception("Unsupported hash type: " + hash["type"])
		newHash = self.hash_file(file,hash["type"])
		if hash["sum"] == newHash:
			return (True,hash["sum"],newHash)
		return (False,hash["sum"],newHash)

	def download_unpack_file(self,data,folderName = None,workDir = None):
		customFolder = False
		if folderName == None:
			folderName = os.path.basename(os.path.splitext(urlparse(self.get_primary_package_url(data)).path)[0]).rstrip(".tar")
		else:
			customFolder = True
		folderToCheck = folderName
		if workDir != None:
			folderToCheck = workDir

		if not os.path.isfile(os.path.join(folderToCheck,"unpacked.successfully")):
			dl_loc = self.get_best_mirror(data)
			url = dl_loc["url"]
			fileName = os.path.basename(urlparse(url).path)
			self.logger.info("Downloading {0} ({1})".format( fileName, url ))

			self.download_file(url,fileName)


			if "hashes" in dl_loc:
				if len(dl_loc["hashes"]) >= 1:
					for hash in dl_loc["hashes"]:
						self.logger.info("Comparing hashes..")
						hashReturn = self.verify_hash(fileName,hash)
						if hashReturn[0] == True:
							self.logger.info("Hashes matched: {0}...{1} (local) == {2}...{3} (remote)".format(hashReturn[1][0:5],hashReturn[1][-5:],hashReturn[2][0:5],hashReturn[2][-5:]))
						else:
							self.logger.error("File hashes didn't match: %s(local) != %s(remote)" % (hashReturn[1],hashReturn[2]))
							raise Exception("File download error: Hash mismatch")
							exit(1)

			self.logger.info("Unpacking {0}".format( fileName ))

			tars = (".gz",".bz2",".xz",".bz",".tgz") # i really need a better system for this.. but in reality, those are probably the only formats we will ever encounter.

			customFolderTarArg = ""

			if customFolder:
				customFolderTarArg = ' -C "' + folderName + '" --strip-components 1'
				os.makedirs(folderName)

			if fileName.endswith(tars):
				self.run_process('tar -xf "{0}"{1}'.format( fileName, customFolderTarArg ))
			else:
				self.run_process('unzip "{0}"'.format( fileName ))

			self.touch(os.path.join(folderName,"unpacked.successfully"))

			os.remove(fileName)

			return folderName

		else:
			self.logger.debug("{0} already downloaded".format( folderName ))
			return folderName
	#:

	def check_mirrors(self,dl_locations):
		for loc in dl_locations:
			userAgent = self.userAgent
			if 'sourceforge.net' in loc["url"].lower():
				userAgent = 'wget/1.18' # sourceforce <3 wget
			try:
				req = requests.request("GET", loc["url"], stream=True, allow_redirects=True, headers = { "User-Agent": self.userAgent } )
			except requests.exceptions.RequestException as e:
				self.logger.debug(e)
			else:
				if req.status_code == 200:
					return loc
				else:
					self.logger.debug(loc["url"] + " unable to reach: HTTP" + str(req.status_code))

		return dl_locations[0] # return the first if none could be found.

	def get_best_mirror(self,data): #returns the best online mirror of a file, and its hash.
		if "url" in data:
			self.logger.warning("Package has the old URL format, please update it.")
			return { "url" : data["url"], "hashes" : [] }
		elif "download_locations" not in data:
			raise Exception("download_locations not specificed for package: " + name)
		else:
			if not len(data["download_locations"]) >= 1:
				raise Exception("download_locations is empty for package: " + name)
			if "url" not in data["download_locations"][0]:
				raise Exception("download_location #1 of package '%s' has no url specified" % (name))

			return self.check_mirrors(data["download_locations"])

	def get_primary_package_url(self,data): # returns the URL of the first download_locations entry from a package, unlike get_best_mirror this one ignores the old url format
		if "url" in data:
			self.logger.debug("Package has the old URL format, please update it.")
			return data["url"]
		elif "download_locations" not in data:
			raise Exception("download_locations not specificed")
		else:
			if not len(data["download_locations"]) >= 1:
				raise Exception("download_locations is empty for package")
			if "url" not in data["download_locations"][0]:
				raise Exception("download_location #1 of package has no url specified")
			return data["download_locations"][0]["url"] #TODO: do not assume correct format
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
			doNotUpdate = False
			if 'do_not_git_update' in data:
				if data['do_not_git_update'] == True:
					doNotUpdate=True
			workDir    = self.git_clone(self.get_primary_package_url(data),folderName,renameFolder,branch,recursive,doNotUpdate)
		if data["repo_type"] == "svn":
			workDir = self.svn_clone(self.get_primary_package_url(data),data["folder_name"],renameFolder)
		if data['repo_type'] == 'mercurial':
			branch = self.getValueOrNone(data,'branch')
			workDir = self.mercurial_clone(self.get_primary_package_url(data),self.getValueOrNone(data,'folder_name'),renameFolder,branch)
		if data["repo_type"] == "archive":
			if "folder_name" in data:
				workDir = self.download_unpack_file(data,data["folder_name"],workDir)
			else:
				workDir = self.download_unpack_file(data,None,workDir)

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
					if libraryName not in self.packages["deps"]:
						raise MissingDependency("The dependency '{0}' of '{1}' does not exist in dependency config.".format( libraryName, name)) #sys.exc_info()[0]
					else:
						self.build_thing(libraryName,self.packages["deps"][libraryName],"DEPENDENCY")
		
		if 'is_dep_inheriter' in data:
			if data['is_dep_inheriter'] == True:
				print("Gothere")
				if type == "PRODUCT":
					self.packages["prods"][name]["_already_built"] = True
				else:
					self.packages["deps"][name]["_already_built"] = True
				
				return

		self.logger.info("Building {0} '{1}'".format(type.lower(),name))
		self.defaultCFLAGS()

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
			doNotUpdate = False
			if 'do_not_git_update' in data:
				if data['do_not_git_update'] == True:
					doNotUpdate=True
			desiredPRVal = None
			if 'desired_pr_id' in data:
				if data['desired_pr_id'] != None:
					desiredPRVal = data['desired_pr_id']
			workDir = self.git_clone(self.get_primary_package_url(data),folderName,renameFolder,branch,recursive,doNotUpdate,desiredPR=desiredPRVal)
		elif data["repo_type"] == "svn":
			workDir = self.svn_clone(self.get_primary_package_url(data),data["folder_name"],renameFolder)
		elif data['repo_type'] == 'mercurial':
			branch = self.getValueOrNone(data,'branch')
			workDir = self.mercurial_clone(self.get_primary_package_url(data),self.getValueOrNone(data,'folder_name'),renameFolder,branch)
		elif data["repo_type"] == "archive":
			if "folder_name" in data:
				workDir = self.download_unpack_file(data,data["folder_name"],workDir)
			else:
				workDir = self.download_unpack_file(data,None,workDir)
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

		oldPath = self.getKeyOrBlankString(os.environ,"PATH")
		currentFullDir = os.getcwd()

		if not self.anyFileStartsWith('already_configured'):
			if 'run_pre_patch' in data:
				if data['run_pre_patch'] != None:
					for cmd in data['run_pre_patch']:
						cmd = self.replaceVariables(cmd)
						self.logger.debug("Running pre-patch-command: '{0}'".format( cmd ))
						self.run_process(cmd)
						
		if force_rebuild:
			if os.path.isdir(".git"):
				self.run_process('git clean -ffdx') #https://gist.github.com/nicktoumpelis/11214362
				self.run_process('git submodule foreach --recursive git clean -ffdx')
				self.run_process('git reset --hard')
				self.run_process('git submodule foreach --recursive git reset --hard')
				self.run_process('git submodule update --init --recursive')

		if 'source_subfolder' in data:
			if data['source_subfolder'] != None:
				if not os.path.isdir(data['source_subfolder']):
					os.makedirs(data['source_subfolder'], exist_ok=True)
				self.cchdir(data['source_subfolder'])

		if force_rebuild:
			self.removeAlreadyFiles()
			self.removeConfigPatchDoneFiles()

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
				os.environ["LDFLAGS"] = data['custom_cflag']

		if 'custom_path' in data:
			if data['custom_path'] != None:
				self.logger.debug("Setting PATH to '{0}'".format( self.replaceVariables(data['custom_path']) ))
				os.environ["PATH"] = self.replaceVariables(data['custom_path'])

		if 'flipped_path' in data:
			if data['flipped_path'] == True:
				bef = os.environ["PATH"]
				os.environ["PATH"] = "{0}:{1}:{2}".format ( self.mingwBinpath, os.path.join(self.targetPrefix,'bin'), self.originalPATH ) #todo properly test this..
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
						if cmd.startswith("!SWITCHDIR"):
							self.cchdir("|".join(cmd.split("|")[1:]))
						else:
							cmd = self.replaceVariables(cmd)
							self.logger.debug("Running post-patch-command: '{0}'".format( cmd ))
							self.run_process(cmd)

		conf_system = "autoconf"
		build_system = "make"
		
		# conf_system_specifics = {
			# "gnumake_based_systems" : [ "cmake", "autoconf" ],
			# "ninja_based_systems" : [ "meson" ]
		# }
		
		if 'build_system' in data:                 # Kinda redundant, but ill keep it for now, maybe add an alias system for this.
			if data['build_system'] == "ninja":    #
				build_system = "ninja"             #
			if data['build_system'] == "waf":      #
				build_system = "waf"               #
			if data['build_system'] == "rake":     #
				build_system = "rake"              #
		if 'conf_system' in data:                  #
			if data['conf_system'] == "cmake":     #
				conf_system = "cmake"              #
			elif data['conf_system'] == "meson":   #
				conf_system = "meson"              #
			elif data['conf_system'] == "waf":     #
				conf_system = "waf"                #
			
		needs_conf = True
			
		if 'needs_configure' in data:
			if data['needs_configure'] == False:
				needs_conf = False
		
		if needs_conf:
			if conf_system == "cmake":
				self.cmake_source(name,data)
			elif conf_system == "meson":
				self.create_meson_environment_file()
				self.meson_source(name,data)
			else:
				self.configure_source(name,data,conf_system)

		if 'patches_post_configure' in data:
			if data['patches_post_configure'] != None:
				for p in data['patches_post_configure']:
					self.apply_patch(p[0],p[1],True)

		if 'make_subdir' in data:
			if data['make_subdir'] != None:
				if not os.path.isdir(data['make_subdir']):
					os.makedirs(data['make_subdir'], exist_ok=True)
				self.cchdir(data['make_subdir'])

		if 'needs_make' in data:
			if data['needs_make'] == True:
				self.build_source(name,data,build_system)
		else:
			self.build_source(name,data,build_system)
		
		if 'needs_make_install' in data:
			if data['needs_make_install'] == True:
				self.install_source(name,data,build_system)
		else:
			self.install_source(name,data,build_system)


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

		self.cchdir("..") #asecond into x86_64
		if type == "PRODUCT":
			self.packages["prods"][name]["_already_built"] = True
		else:
			self.packages["deps"][name]["_already_built"] = True

		self.logger.info("Building {0} '{1}': Done!".format(type.lower(),name))
		if 'debug_exitafter' in data:
			exit()

		if 'custom_path' in data:
			if data['custom_path'] != None:
				self.logger.debug("Re-setting PATH to '{0}'".format( oldPath ))
				os.environ["PATH"] = oldPath

		self.defaultCFLAGS()
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

	def configure_source(self,name,data,conf_system):
		touch_name = "already_configured_%s" % (self.md5(name,self.getKeyOrBlankString(data,"configure_options")))
		
		if not os.path.isfile(touch_name):
			self.removeAlreadyFiles()
			self.removeConfigPatchDoneFiles()

			doBootStrap = True
			if 'do_not_bootstrap' in data:
				if data['do_not_bootstrap'] == True:
					doBootStrap = False
			
			if doBootStrap:
				if conf_system == "waf":
					if not os.path.isfile("waf"):
						if os.path.isfile("bootstrap.py"):
							self.run_process('./bootstrap.py')
				else:
					self.bootstrap_configure()

			configOpts = ''
			if 'configure_options' in data:
				configOpts = self.replaceVariables(data["configure_options"])
			self.logger.info("Configuring '{0}' with: {1}".format(name, configOpts ),extra={'type': conf_system})

			confCmd = './configure'
			if conf_system == "waf":
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
				if conf_system == "waf":
					mCleanCmd = './waf --color=yes clean'
				self.run_process('{0} -j {1}'.format( mCleanCmd, self.cpuCount ),True)

			self.touch(touch_name)

	def apply_patch( self, url, type = "-p1", postConf = False, folderToPatchIn = None):
	
		originalFolder = os.getcwd()
		if folderToPatchIn != None:
			self.cchdir(folderToPatchIn)
			self.logger.info("Moving to patch folder: {0}" .format( os.getcwd() ))
			
		self.logger.debug("Applying patch '{0}' in '{1}'" .format( url, os.getcwd() ))
			
		patch_touch_name = "patch_%s.done" % (self.md5(url))
		
		ignoreErr = False
		exitOn = True
		ignore = ""

		if postConf:
			patch_touch_name = patch_touch_name + "_past_conf"
			ignore = "-N "
			ignoreErr = True
			exitOn = False
		
		if os.path.isfile(patch_touch_name):
			self.logger.debug("Patch '{0}' already applied".format( url ))
			self.cchdir(originalFolder)
			return

		pUrl = urlparse(url)
		if pUrl.scheme != '':
			fileName = os.path.basename(pUrl.path)
			self.logger.info("Downloading patch '{0}' to: {1}".format( url, fileName ))
			self.download_file(url,fileName)
		else:
			local_patch_path = os.path.join(self.fullPatchDir,url)
			fileName = os.path.basename(Path(local_patch_path).name)
			if os.path.isfile(local_patch_path):
				copyPath = os.path.join(os.getcwd(),fileName)
				self.logger.info("Copying patch from '{0}' to '{1}'".format(local_patch_path,copyPath))
				shutil.copyfile(local_patch_path,copyPath)
			else:
				fileName = os.path.basename(urlparse(url).path)
				url = "https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches" + url
				self.download_file(url,fileName)

		self.logger.info("Patching source using: '{0}'".format( fileName ))
		self.run_process('patch {2}{0} < "{1}"'.format(type, fileName, ignore ),ignoreErr,exitOn)
		
		if not postConf:
			self.removeAlreadyFiles()
			
		self.touch(patch_touch_name)
			
		if folderToPatchIn != None:
			self.cchdir(originalFolder)
	#:
	
	def meson_source(self,name,data):
		touch_name = "already_ran_meson_%s" % (self.md5(name,self.getKeyOrBlankString(data,"configure_options	")))

		if not os.path.isfile(touch_name):
			self.removeAlreadyFiles()

			makeOpts = ''
			if 'configure_options' in data:
				makeOpts = self.replaceVariables(data["configure_options"])
			self.logger.info("Meson'ing '{0}' with: {1}".format( name, makeOpts ))

			self.run_process('meson {0}'.format( makeOpts ))

			self.touch(touch_name)

	def cmake_source(self,name,data):
		touch_name = "already_ran_cmake_%s" % (self.md5(name,self.getKeyOrBlankString(data,"configure_options")))

		if not os.path.isfile(touch_name):
			self.removeAlreadyFiles()

			makeOpts = ''
			if 'configure_options' in data:
				makeOpts = self.replaceVariables(data["configure_options"])
			self.logger.info("C-Making '{0}' with: {1}".format( name, makeOpts ))

			self.run_process('cmake {0}'.format( makeOpts ))

			self.run_process("make clean",True)

			self.touch(touch_name)

	def build_source(self,name,data,build_system):
		touch_name = "already_ran_make_%s" % (self.md5(name,self.getKeyOrBlankString(data,"build_options")))
		if not os.path.isfile(touch_name):
			mkCmd = 'make'
			
			if build_system == "waf":
				mkCmd = './waf --color=yes'
			if build_system == "rake":
				mkCmd = 'rake'
			if build_system == "ninja":
				mkCmd = 'ninja'
			
			if build_system == "make":
				if os.path.isfile("configure"):
					self.run_process('{0} clean -j {1}'.format( mkCmd, self.cpuCount ),True)

			makeOpts = ''
			if 'build_options' in data:
				makeOpts = self.replaceVariables(data["build_options"])

			self.logger.info("Building '{0}' with: {1} in {2}".format(name, makeOpts, os.getcwd()),extra={'type': build_system})

			cpcnt = '-j {0}'.format(self.cpuCount)

			if 'cpu_count' in data:
				if data['cpu_count'] != None:
					cpcnt = ""

			if 'ignore_build_fail_and_run' in data:
				if len(data['ignore_build_fail_and_run']) > 0: #todo check if its a list too
					try:
						if build_system == "waf":
							mkCmd = './waf --color=yes build'
						self.run_process('{0} {2} {1}'.format( mkCmd, cpcnt, makeOpts ))
					except Exception as e:
						self.logger.info("Ignoring failed make process...")
						for cmd in data['ignore_build_fail_and_run']:
							cmd = self.replaceVariables(cmd)
							self.logger.info("Running post-failed-make-command: '{0}'".format( cmd ))
							self.run_process(cmd)
			else:
				if build_system == "waf":
					mkCmd = './waf --color=yes build'
				self.run_process('{0} {2} {1}'.format( mkCmd, cpcnt, makeOpts ))

			if 'run_post_build' in data:
				if data['run_post_build'] != None:
					for cmd in data['run_post_build']:
						cmd = self.replaceVariables(cmd)
						self.logger.info("Running post-build-command: '{0}'".format( cmd ))
						self.run_process(cmd)

			self.touch(touch_name)

	def install_source(self,name,data,build_system):
		touch_name = "already_ran_install_%s" % (self.md5(name,self.getKeyOrBlankString(data,"install_options")))
		if not os.path.isfile(touch_name):
			cpcnt = '-j {0}'.format(self.cpuCount)

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


			self.logger.info("Installing '{0}' with: {1}".format(name, makeInstallOpts ),extra={'type': build_system})

			mkCmd = "make"
			if build_system == "waf":
				mkCmd = "./waf"
			if build_system == "rake":
				mkCmd = "rake"	
			if build_system == "ninja":
				mkCmd = "ninja"

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
		self.logger.debug("Reset CFLAGS to: {0}".format( self.originalCflags ) )
		os.environ["CFLAGS"] = self.originalCflags
		os.environ["LDFLAGS"] = self.originalCflags
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
			if varName in self.packages["vars"]:
				cmdReplacer = self.packages["vars"][varName]
				mr = re.sub(r"\!VAR\((.*)\)VAR!", r"{0}".format(cmdReplacer), cmd, flags=re.DOTALL)
				cmd = mr

		cmd = cmd.format(
			cmake_prefix_options       = self.cmakePrefixOptions,
			make_prefix_options        = self.makePrefixOptions,
			pkg_config_path            = self.pkgConfigPath,
			mingw_binpath              = self.mingwBinpath,
			mingw_binpath2             = self.mingwBinpath2,
			cross_prefix_bare          = self.bareCrossPrefix,
			cross_prefix_full          = self.fullCrossPrefix,
			target_prefix              = self.targetPrefix,
			inTreePrefix               = self.inTreePrefix,
			offtree_prefix             = self.offtreePrefix,
			target_host                = self.targetHost,
			target_sub_prefix          = self.targetSubPrefix,
			bit_name                   = self.bitnessDir,
			bit_name2                  = self.bitnessDir2,
			bit_name3                  = self.bitnessDir3,
			bit_name_win               = self.winBitnessDir,
			bit_num                    = self.currentBitness,
			product_prefix             = self.fullProductDir,
			target_prefix_sed_escaped = self.targetPrefix.replace("/","\\/"),
			make_cpu_count             = "-j {0}".format(self.cpuCount),
			original_cflags            = self.originalCflags,
			cflag_string               = self.generateCflagString('--extra-cflags='),
			current_path               = os.getcwd(),
			current_envpath            = self.getKeyOrBlankString(os.environ,"PATH"),
			meson_env_file             = self.mesonEnvFile
		)
		# needed actual commands sometimes, so I made this custom command support, comparable to "``" in bash, very very shady.. needs testing, but seems to work just flawlessly.

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

if __name__ == "__main__":
	main = CrossCompileScript()
	main.commandLineEntrace()