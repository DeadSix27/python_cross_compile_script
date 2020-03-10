#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ####################################################
# Copyright (C) 2018-2020 DeadSix27 (https://github.com/DeadSix27/python_cross_compile_script)
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

import argparse
import ast
import codecs
import glob
import hashlib
import importlib
import logging
import os.path
import re
import shutil
import stat
import subprocess
import sys
import traceback
import urllib.parse
import urllib.request
from collections import defaultdict
from multiprocessing import cpu_count
from pathlib import Path
from urllib.parse import urlparse

import progressbar  # Run pip3 install progressbar2
import requests  # Run pip3 install requests
import yaml


class Colors:  # ansi colors
	RESET = '\033[0m'
	BLACK = '\033[30m'
	RED = '\033[31m'
	GREEN = '\033[32m'
	YELLOW = '\033[33m'
	BLUE = '\033[34m'
	MAGENTA = '\033[35m'
	CYAN = '\033[36m'
	WHITE = '\033[37m'
	LIGHTBLACK_EX = '\033[90m'  # those seem to work on the major OS so meh.
	LIGHTRED_EX = '\033[91m'
	LIGHTGREEN_EX = '\033[92m'
	LIGHTYELLOW_EX = '\033[93m'
	LIGHTBLUE_EX = '\033[94m'
	LIGHTMAGENTA_EX = '\033[95m'
	LIGHTCYAN_EX = '\033[96m'
	LIGHTWHITE_EX = '\033[9m'


class MissingDependency(Exception):
	__module__ = 'exceptions'

	def __init__(self, message):
		self.message = message


class MyLogFormatter(logging.Formatter):
	def __init__(self, l, ld):
		MyLogFormatter.log_format = l
		MyLogFormatter.log_date_format = ld
		MyLogFormatter.inf_fmt = Colors.LIGHTCYAN_EX + MyLogFormatter.log_format + Colors.RESET
		MyLogFormatter.err_fmt = Colors.LIGHTRED_EX + MyLogFormatter.log_format + Colors.RESET
		MyLogFormatter.dbg_fmt = Colors.LIGHTYELLOW_EX + MyLogFormatter.log_format + Colors.RESET
		MyLogFormatter.war_fmt = Colors.YELLOW + MyLogFormatter.log_format + Colors.RESET
		super().__init__(fmt="%(levelno)d: %(msg)s", datefmt=MyLogFormatter.log_date_format, style='%')

	def format(self, record):
		if not hasattr(record, "type"):
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
		sys.dont_write_bytecode = True  # Avoid __pycache__ folder, never liked that solution
		hdlr = logging.StreamHandler(sys.stdout)
		fmt = MyLogFormatter("[%(asctime)s][%(levelname)s]%(type)s %(message)s", "%H:%M:%S")
		hdlr.setFormatter(fmt)
		self.logger = logging.getLogger(__name__)
		self.logger.addHandler(hdlr)
		self.logger.setLevel(logging.INFO)
		self.config = self.loadConfig()
		fmt = MyLogFormatter(self.config["script"]["log_format"], self.config["script"]["log_date_format"])
		hdlr.setFormatter(fmt)
		self.packages = self.loadPackages(self.config["script"]["packages_folder"])
		self.lastError = None
		self.init()

	def errorExit(self, msg):
		self.logger.error(msg)
		sys.exit(1)

	def loadPackages(self, packages_folder):
		def isPathDisabled(path):
			for part in path.parts:
				if part.lower().startswith("_disabled"):
					return True
			return False

		depsFolder = Path(os.path.join(packages_folder, "dependencies"))
		prodFolder = Path(os.path.join(packages_folder, "products"))
		varsPath = Path(os.path.join(packages_folder, "variables.py"))

		if not os.path.isdir(packages_folder):
			self.errorExit("Packages folder '%s' does not exist." % (packages_folder))
		if not os.path.isdir(depsFolder):  # TODO simplify code
			self.errorExit("Packages folder '%s' does not exist." % (depsFolder))
		if not os.path.isfile(varsPath):
			self.errorExit("Variables file '%s' does not exist." % (varsPath))

		tmpPkglist = {'deps': [], 'prods': [], 'vars': []}
		packages = {'deps': {}, 'prods': {}, 'vars': {}}

		for path, subdirs, files in os.walk(depsFolder):
			for name in files:
				p = Path(os.path.join(path, name))
				if p.suffix == ".py":
					if not isPathDisabled(p):
						tmpPkglist["deps"].append(p)

		for path, subdirs, files in os.walk(prodFolder):
			for name in files:
				p = Path(os.path.join(path, name))
				if p.suffix == ".py":
					if not isPathDisabled(p):
						tmpPkglist["prods"].append(p)

		if len(tmpPkglist["deps"]) < 1:  # TODO simplify code
			self.errorExit("There's no packages in the folder '%s'." % (depsFolder))

		if len(tmpPkglist["prods"]) < 1:
			self.errorExit("There's no packages in the folder '%s'." % (prodFolder))

		with open(varsPath, "r", encoding="utf-8") as f:
			try:
				o = ast.literal_eval(f.read())  # was gonna use .json instead of eval on py files, but I like having multiline strings and comments.. so.
				if not isinstance(o, dict):
					self.errorExit("Variables file is misformatted")
				packages["vars"] = o
			except SyntaxError:
				self.errorExit("Loading variables.py failed:\n\n" + traceback.format_exc())

		for d in tmpPkglist["deps"]:
			with open(d, "r", encoding="utf-8") as f:
				p = Path(d)
				packageName = p.stem.lower()
				try:
					o = ast.literal_eval(f.read())
					if not isinstance(o, dict):
						self.errorExit("Package file '%s' is misformatted" % (p.name))

					if "_info" not in o and not self.boolKey(o, "is_dep_inheriter"):
						self.logger.warning("Package '%s.py' is missing '_info' tag." % (packageName))

					if self.boolKey(o, "_disabled"):
						self.logger.debug("Package '%s.py' has option '_disabled' set, not loading." % (packageName))
					else:
						packages["deps"][packageName] = o

				except SyntaxError:
					self.errorExit("Loading '%s.py' failed:\n\n%s" % (packageName, traceback.format_exc()))

		for d in tmpPkglist["prods"]:
			with open(d, "r", encoding="utf-8") as f:
				p = Path(d)
				packageName = p.stem.lower()
				try:
					o = ast.literal_eval(f.read())
					if not isinstance(o, dict):
						self.errorExit("Package file '%s' is misformatted" % (p.name))

					if "_info" not in o and not self.boolKey(o, "is_dep_inheriter"):
						self.logger.warning("Package '%s.py' is missing '_info' tag." % (packageName))

					if self.boolKey(o, "_disabled"):
						self.logger.debug("Package '%s.py' has option '_disabled' set, not loading." % (packageName))
					else:
						packages["prods"][packageName] = o

				except SyntaxError:
					self.errorExit("Loading '%s.py' failed:\n\n%s" % (packageName, traceback.format_exc()))

		self.logger.info("Loaded %d packages", len(packages["prods"]) + len(packages["deps"]))
		return packages

	def confDiff(self, default, users):  # very basic config comparison
		for category in default:
			if category not in users:
				return (False, F"User config is missing '{category}' category, please delete your config to regenerate a new one OR add it manually.")
			elif category != "version":
				for option in default[category]:
					if option not in users[category]:
						return (False, F"User config is missing '{option}' option in '{category}' category, please delete your config to regenerate a new one OR add it manually.")
		return (True, 'Config Ok')

	def loadConfig(self):
		self.config = {  # Default config
			'version': 1.0,
			'script': {
				'debug': False,
				'quiet': False,
				'log_date_format': '%H:%M:%S',
				'log_format': '[%(asctime)s][%(levelname)s]%(type)s %(message)s',
				'product_order': ['mpv', 'ffmpeg'],
				'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
				'mingw_toolchain_path': 'mingw_toolchain_script/mingw_toolchain_script.py',
				'packages_folder': 'packages',
			},
			'toolchain': {
				'output_path': '{work_dir}/{bit_name_win}_output',
				'bitness': [64, ],
				'cpu_count': cpu_count(),
				'mingw_commit': None,
				'mingw_debug_build': False,
				'mingw_dir': 'toolchain',
				'mingw_custom_cflags': None,
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
				conf = yaml.safe_load(cs)
			except yaml.YAMLError as e:
				self.logger.error("Failed to load config file " + str(e))
				traceback.print_exc()
				sys.exit(1)

		confCheck = self.confDiff(self.config, conf)

		if confCheck[0]:
			return conf
		else:
			self.logger.error("%s" % (confCheck[1]))
			sys.exit(1)
			return None

	def writeDefaultConfig(self, config_file):
		with open(config_file, "w", encoding="utf-8") as f:
			f.write(yaml.dump(self.config))
		self.logger.info("Wrote default configuration file to: '%s'" % (config_file))

	def init(self):
		self.product_order = self.config["script"]["product_order"]
		self.projectRoot = Path(os.getcwd())
		self.fullPatchDir = self.projectRoot.joinpath("patches")
		self.fullWorkDir = self.projectRoot.joinpath(self.config["toolchain"]["work_dir"])
		self.mingwDir = self.config["toolchain"]["mingw_dir"]
		self.targetBitness = self.config["toolchain"]["bitness"]
		self.originalPATH = os.environ["PATH"]
		self.quietMode = self.config["script"]["quiet"]
		self.debugMode = self.config["script"]["debug"]
		self.userAgent = self.config["script"]["user_agent"]
		if self.debugMode:
			self.initDebugMode()
		if self.quietMode:
			self.initQuietMode()

	def initQuietMode(self):
		self.logger.warning('Quiet mode is enabled')
		self.buildLogFile = codecs.open("raw_build.log", "w", "utf-8")

	def initDebugMode(self):
		self.logger.setLevel(logging.DEBUG)
		self.logger.debug('Debugging is on')

	def listifyPackages(self, pdlist, type):
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
					for key, val in pdlist.items():
						if '_info' in val:
							if val['repo_type'] == 'git' or val['repo_type'] == 'mercurial':
								if 'branch' in val:
									if val['branch'] is not None:
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

					print(' {0} - {1}'.format(HEADER.rjust(longestName, ' '), HEADER_V.ljust(longestVer, ' ')))
					print('')

					for key, val in sorted(pdlist.items()):
						ver = Colors.RED + "(no version)" + Colors.RESET
						if '_info' in val:
							if val['repo_type'] == 'git' or val['repo_type'] == 'mercurial':
								if 'branch' in val:
									if val['branch'] is not None:
										rTypeStr = 'git' if val['repo_type'] == 'git' else 'hg '
										cVer = rTypeStr + ' (' + val['branch'][0:6] + ')'
								else:
									cVer = 'git (master)' if val['repo_type'] == 'git' else 'hg (default)'
								val['_info']['version'] = cVer
							if 'version' in val['_info']:
								ver = Colors.GREEN + val['_info']['version'] + Colors.RESET
						name = key

						print(' {0} - {1}'.format(name.rjust(longestName, ' '), ver.ljust(longestVer, ' ')))
				elif format == "MD":
					longestName = 0
					longestVer = 1
					for key, val in pdlist.items():
						if '_info' in val:
							if val['repo_type'] == 'git' or val['repo_type'] == 'mercurial':
								if 'branch' in val:
									if val['branch'] is not None:
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

					print('| {0} | {1} |'.format(HEADER.ljust(longestName, ' '), HEADER_V.ljust(longestVer, ' ')))
					print('| {0}:|:{1} |'.format(longestName * '-', longestVer * '-'))
					for key, val in sorted(pdlist.items()):
						if '_info' in val:
							ver = "?"
							name = key
							if val['repo_type'] == 'git' or val['repo_type'] == 'mercurial':
								if 'branch' in val:
									if val['branch'] is not None:
										rTypeStr = 'git' if val['repo_type'] == 'git' else 'hg '
										cVer = rTypeStr + ' (' + val['branch'][0:6] + ')'
								else:
									cVer = 'git (master)' if val['repo_type'] == 'git' else 'hg (default)'
								val['_info']['version'] = cVer

							if 'version' in val['_info']:
								ver = val['_info']['version']
							if 'fancy_name' in val['_info']:
								name = val['_info']['fancy_name']
							print('| {0} | {1} |'.format(name.ljust(longestName, ' '), ver.ljust(longestVer, ' ')))
				else:
					print(";".join(sorted(pdlist.keys())))
				setattr(args, self.dest, values)
				parser.exit()
		return customArgsAction

	def assembleConfigHelps(self, pdlist, type, main):
		class customArgsAction(argparse.Action):
			def __call__(self, parser, args, values, option_string=None):
				main.quietMode = True
				main.init_quietMode()
				main.prepareBuilding(64)
				main.build_mingw(64)
				main.initBuildFolders()
				for k, v in pdlist.items():
					if '_disabled' not in v:
						if '_info' in v:
							beforePath = os.getcwd()
							path = main.getPackagePath(k, v, type)
							main.cchdir(path)
							if os.path.isfile(os.path.join(path, "configure")):
								os.system("./configure --help")
							if os.path.isfile(os.path.join(path, "waf")):
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

		_epilog = 'Copyright (C) 2018-2019 DeadSix27 (https://github.com/DeadSix27/python_cross_compile_script)\n\n This Source Code Form is subject to the terms of the Mozilla Public\n License, v. 2.0. If a copy of the MPL was not distributed with this\n file, You can obtain one at https://mozilla.org/MPL/2.0/.\n '

		parser = argparse.ArgumentParser(formatter_class=epiFormatter, epilog=_epilog)
		parser.set_defaults(which='main')
		parser.description = Colors.CYAN + 'Pythonic Cross Compile Helper (MPL2.0)' + Colors.RESET + '\n\nExample usages:' \
			'\n "{0} list -p"             - lists all the products' \
			'\n "{0} -a"                  - builds everything' \
			'\n "{0} -f -d libx264"       - forces the rebuilding of libx264' \
			'\n "{0} -pl x265_10bit,mpv"  - builds this list of products in that order' \
			'\n "{0} -q -p ffmpeg_static" - will quietly build ffmpeg-static'.format(parser.prog)

		subparsers = parser.add_subparsers(help='Sub commands')

		list_p = subparsers.add_parser('list', help='Type: \'' + parser.prog + ' list --help\' for more help')
		list_p.set_defaults(which='list_p')

		list_p.add_argument('-md', '--markdown', help='Print list in markdown format', action='store_true')
		list_p.add_argument('-cv', '--csv', help='Print list as CSV-like string', action='store_true')
		list_p_group1 = list_p.add_mutually_exclusive_group(required=True)
		list_p_group1.add_argument('-p', '--products', nargs=0, help='List all products', action=self.listifyPackages(self.packages["prods"], "P"))
		list_p_group1.add_argument('-d', '--dependencies', nargs=0, help='List all dependencies', action=self.listifyPackages(self.packages["deps"], "D"))

		chelps_p = subparsers.add_parser('chelps', help='Type: \'' + parser.prog + ' chelps --help\' for more help')
		list_p.set_defaults(which='chelps_p')
		chelps_p_group1 = chelps_p.add_mutually_exclusive_group(required=True)
		chelps_p_group1.add_argument('-p', '--products', nargs=0, help='Write all product config helps to confighelps.txt', action=self.assembleConfigHelps(self.packages["prods"], "P", self))
		chelps_p_group1.add_argument('-d', '--dependencies', nargs=0, help='Write all dependency config helps to confighelps.txt', action=self.assembleConfigHelps(self.packages["deps"], "D", self))

		info_p = subparsers.add_parser('info', help='Type: \'' + parser.prog + ' info --help\' for more help')
		info_p.set_defaults(which='info_p')

		info_p_group1 = info_p.add_mutually_exclusive_group(required=True)
		info_p_group1.add_argument('-r', '--required-by', help='List all packages this dependency is required by', default=None)
		info_p_group1.add_argument('-d', '--depends-on', help='List all packages this package depends on (recursively)', default=None)

		group2 = parser.add_mutually_exclusive_group(required=False)
		group2.add_argument('-p', '--build-product', dest='PRODUCT', help='Build the specificed product package(s)')
		group2.add_argument('-d', '--build-dependency', dest='DEPENDENCY', help='Build the specificed dependency package(s)')
		group2.add_argument('-a', '--build-all', help='Build all products (according to order)', action='store_true')
		parser.add_argument('-q', '--quiet', help='Only show info lines', action='store_true')
		parser.add_argument('-f', '--force', help='Force rebuild, deletes already files', action='store_true')
		parser.add_argument('-g', '--debug', help='Show debug information', action='store_true')
		parser.add_argument('-s', '--skip-depends', help='Skip dependencies when building', action='store_true')

		if len(sys.argv) == 1:
			self.defaultEntrace()
		else:
			def errorOut(p, t, m=None):
				if m is None:
					fullStr = Colors.LIGHTRED_EX + 'Error:\n ' + Colors.CYAN + '\'{0}\'' + Colors.LIGHTRED_EX + ' is not a valid {2}\n Type: ' + Colors.CYAN + '\'{1} list --products/--dependencies\'' + Colors.LIGHTRED_EX + ' for a full list'
					print(fullStr.format(p, os.path.basename(__file__), "Product" if t == "PRODUCT" else "Dependency") + Colors.RESET)
				else:
					print(m)
				exit(1)
			args = parser.parse_args()

			if args.which == "info_p":
				if args.required_by:
					self.listRequiredBy(args.required_by)
				if args.depends_on:
					self.listDependsOn(args.depends_on)
				return

			forceRebuild = False
			if args.debug:
				self.debugMode = True
				self.initDebugMode()
			if args.quiet:
				self.quietMode = True
				self.initQuietMode()
			if args.force:
				forceRebuild = True
			buildType = None

			finalPkgList = []

			if args.PRODUCT or args.DEPENDENCY:
				strPkgs = args.DEPENDENCY
				buildType = "DEPENDENCY"
				if args.PRODUCT is not None:
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

					finalPkgList.append(p.replace("\\,", ","))

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
					main.buildMingw(b)
					main.initBuildFolders()
					if buildType == "PRODUCT":
						self.buildThing(thing, self.packages["prods"][thing], buildType, forceRebuild, skipDeps)
					else:
						self.buildThing(thing, self.packages["deps"][thing], buildType, forceRebuild, skipDeps)
					main.finishBuilding()

	def listDependsOn(self, pkgName):
		if pkgName not in self.packages["prods"] and pkgName not in self.packages["deps"]:
			self.logger.error("'%s' is not an existing package." % (pkgName))
			sys.exit(1)

		deps = {}

		def getDeps(x):
			oobj = {}
			if "depends_on" in self.packages["deps"][x]:
				for x in self.packages["deps"][x]["depends_on"]:
					oobj[x] = None
					if "depends_on" in self.packages["deps"][x]:
						oobj[x] = {}
						for _newPkgName in self.packages["deps"][x]["depends_on"]:
							oobj[x][_newPkgName] = getDeps(_newPkgName)
			return oobj

		import pprint
		pprint.pprint(getDeps(pkgName))

	def listRequiredBy(self, o):
		# ptype = None
		# if o in self.packages["prods"]:
		# 	ptype = "prods"
		# elif o in self.packages["deps"]:
		# 	ptype = "deps"
		# else:
		if o not in self.packages["prods"] and o not in self.packages["deps"]:
			self.logger.error("'%s' is not an existing package." % (o))
			sys.exit(1)

		prodsRequiringIt = []
		depsRequiringIt = []

		for p in self.packages["deps"]:
			pkg = self.packages["deps"][p]
			if "depends_on" in pkg:
				if o in pkg["depends_on"]:
					depsRequiringIt.append(p)
		for p in self.packages["prods"]:
			pkg = self.packages["prods"][p]
			if "depends_on" in pkg:
				if o in pkg["depends_on"]:
					prodsRequiringIt.append(p)

		if len(prodsRequiringIt) > 0 or len(depsRequiringIt) > 0:
			self.logger.info("Packages requiring '%s':" % (o))
			if len(depsRequiringIt) > 0:
				self.logger.info("\tDependencies: %s" % (",".join(depsRequiringIt)))
			if len(prodsRequiringIt) > 0:
				self.logger.info("\tProducts    : %s" % (",".join(prodsRequiringIt)))
		else:
			self.logger.warning("There are no packages that require '%s'." % (o))

		sys.exit(0)

	def defaultEntrace(self):
		for b in self.targetBitness:
			self.prepareBuilding(b)
			self.buildMingw(b)
			self.initBuildFolders()
			for p in self.product_order:
				self.buildThing(p, self.packages["prods"][p], "PRODUCT")
			self.finishBuilding()

	def finishBuilding(self):
		self.cchdir("..")

	def formatConfig(self, c: dict):
		def fmt(d):
			if isinstance(d, dict):
				return {self.replaceToolChainVars(k): fmt(v) for k, v in d.items()}
			elif isinstance(d, list):
				return [fmt(o) for o in d]
			else:
				if isinstance(d, str):
					return self.replaceToolChainVars(d)
				else:
					return d
		try:
			return fmt(c)
		except KeyError as e:
			self.errorExit(F"Failed to parse config file, the variable {e} does not exist.")

	def prepareBuilding(self, bitness):
		self.logger.info('Starting build script')
		if not self.fullWorkDir.exists():
			self.logger.info("Creating workdir: %s" % (self.fullWorkDir))
			self.fullWorkDir.mkdir()
		self.cchdir(self.fullWorkDir)

		self.currentBitness = bitness
		self.bitnessStr = "x86_64" if bitness == 64 else "i686"  # e.g x86_64
		self.bitnessPath = self.fullWorkDir.joinpath("x86_64" if bitness == 64 else "i686")  # e.g x86_64
		self.bitnessStr2 = "x86_64" if bitness == 64 else "x86"  # just for vpx...
		self.bitnessStr3 = "mingw64" if bitness == 64 else "mingw"  # just for openssl...
		self.bitnessStrWin = "win64" if bitness == 64 else "win32"  # e.g win64
		self.targetHostStr = F"{self.bitnessStr}-w64-mingw32"  # e.g x86_64-w64-mingw32

		self.targetPrefix = self.fullWorkDir.joinpath(self.mingwDir, self.bitnessStr + "-w64-mingw32", self.targetHostStr)  # workdir/xcompilers/mingw-w64-x86_64/x86_64-w64-mingw32

		self.inTreePrefix = self.fullWorkDir.joinpath(self.bitnessStr)  # workdir/x86_64

		self.offtreePrefix = self.fullWorkDir.joinpath(self.bitnessStr + "_offtree")  # workdir/x86_64_offtree

		self.targetSubPrefix = self.fullWorkDir.joinpath(self.mingwDir, self.bitnessStr + "-w64-mingw32")  # e.g workdir/xcompilers/mingw-w64-x86_64

		self.mingwBinpath = self.fullWorkDir.joinpath(self.mingwDir, self.bitnessStr + "-w64-mingw32", "bin")  # e.g workdir/xcompilers/mingw-w64-x86_64/bin

		self.mingwBinpath2 = self.fullWorkDir.joinpath(self.mingwDir, self.bitnessStr + "-w64-mingw32", self.bitnessStr + "-w64-mingw32", "bin")  # e.g workdir/xcompilers/x86_64-w64-mingw32/x86_64-w64-mingw32/bin

		self.fullCrossPrefixStr = F"{self.mingwBinpath}/{self.bitnessStr}-w64-mingw32-"  # e.g workdir/xcompilers/mingw-w64-x86_64/bin/x86_64-w64-mingw32-

		self.shortCrossPrefixStr = F"{self.bitnessStr}-w64-mingw32-"  # e.g x86_64-w64-mingw32-

		self.autoConfPrefixOptions = F'--with-sysroot="{self.targetSubPrefix}" --host={self.targetHostStr} --prefix={self.targetPrefix} --disable-shared --enable-static'

		self.makePrefixOptions = F'CC={self.shortCrossPrefixStr}gcc ' \
			F"AR={self.shortCrossPrefixStr}ar " \
			F"PREFIX={self.targetPrefix} " \
			F"RANLIB={self.shortCrossPrefixStr}ranlib " \
			F"LD={self.shortCrossPrefixStr}ld " \
			F"STRIP={self.shortCrossPrefixStr}strip " \
			F'CXX={self.shortCrossPrefixStr}g++'  # --sysroot="{self.targetSubPrefix}"'

		self.pkgConfigPath = "{0}/lib/pkgconfig".format(self.targetPrefix)  # e.g workdir/xcompilers/mingw-w64-x86_64/x86_64-w64-mingw32/lib/pkgconfig

		self.localPkgConfigPath = self.aquireLocalPkgConfigPath()

		self.mesonEnvFile = self.fullWorkDir.joinpath("meson_environment.txt")
		self.cmakeToolchainFile = self.fullWorkDir.joinpath("mingw_toolchain.cmake")
		self.cmakePrefixOptions = F'-DCMAKE_TOOLCHAIN_FILE="{self.cmakeToolchainFile}" -G\"Ninja\"'
		self.cmakePrefixOptionsOld = "-G\"Unix Makefiles\" -DCMAKE_SYSTEM_PROCESSOR=\"{bitness}\" -DCMAKE_SYSTEM_NAME=Windows -DCMAKE_RANLIB={cross_prefix_full}ranlib -DCMAKE_C_COMPILER={cross_prefix_full}gcc -DCMAKE_CXX_COMPILER={cross_prefix_full}g++ -DCMAKE_RC_COMPILER={cross_prefix_full}windres -DCMAKE_FIND_ROOT_PATH={target_prefix}".format(cross_prefix_full=self.fullCrossPrefixStr, target_prefix=self.targetPrefix, bitness=self.bitnessStr)
		self.cpuCount = self.config["toolchain"]["cpu_count"]
		self.originalCflags = self.config["toolchain"]["original_cflags"]
		self.originbalLdLibPath = os.environ["LD_LIBRARY_PATH"] if "LD_LIBRARY_PATH" in os.environ else ""

		self.fullProductDir = self.fullWorkDir.joinpath(self.bitnessStr + "_products")

		self.formatDict = defaultdict(lambda: "")
		self.formatDict.update(
			{
				'cmake_prefix_options': self.cmakePrefixOptions,
				'cmake_prefix_options_old': self.cmakePrefixOptionsOld,
				'make_prefix_options': self.makePrefixOptions,
				'autoconf_prefix_options': self.autoConfPrefixOptions,
				'pkg_config_path': self.pkgConfigPath,
				'local_pkg_config_path': self.localPkgConfigPath,
				'local_path': self.originalPATH,
				'mingw_binpath': self.mingwBinpath,
				'mingw_binpath2': self.mingwBinpath2,
				'cross_prefix_bare': self.shortCrossPrefixStr,
				'cross_prefix_full': self.fullCrossPrefixStr,
				'target_prefix': self.targetPrefix,
				'project_root': self.projectRoot,
				'work_dir': self.fullWorkDir,
				'inTreePrefix': self.inTreePrefix,
				'offtree_prefix': self.offtreePrefix,
				'target_host': self.targetHostStr,
				'target_sub_prefix': self.targetSubPrefix,
				'bit_name': self.bitnessStr,
				'bit_name2': self.bitnessStr2,
				'bit_name3': self.bitnessStr3,
				'bit_name_win': self.bitnessStrWin,
				'bit_num': self.currentBitness,
				'product_prefix': self.fullProductDir,
				'target_prefix_sed_escaped': str(self.targetPrefix).replace("/", "\\/"),
				'make_cpu_count': "-j {0}".format(self.cpuCount),
				'original_cflags': self.originalCflags,
				'cflag_string': self.generateCflagString('--extra-cflags='),
				'current_path': os.getcwd(),
				'current_envpath': self.getKeyOrBlankString(os.environ, "PATH"),
				'meson_env_file': self.mesonEnvFile
			}
		)

		self.config = self.formatConfig(self.config)
		self.fullOutputDir = self.projectRoot.joinpath(self.replaceToolChainVars(self.config["toolchain"]["output_path"]))
		self.formatDict['output_prefix'] = str(self.fullOutputDir)

		os.environ["PATH"] = "{0}:{1}".format(self.mingwBinpath, self.originalPATH)
		# os.environ["PATH"] = "{0}:{1}:{2}".format (self.mingwBinpath, os.path.join(self.targetPrefix, 'bin'), self.originalPATH)  # TODO: properly test this..
		os.environ["PKG_CONFIG_PATH"] = self.pkgConfigPath
		os.environ["PKG_CONFIG_LIBDIR"] = ""
		os.environ["COLOR"] = "ON"  # Force coloring on (for CMake primarily)
		os.environ["CLICOLOR_FORCE"] = "ON"  # Force coloring on (for CMake primarily)
	#:

	def initBuildFolders(self):
		if not self.bitnessPath.exists():
			self.logger.info(F"Creating bitdir: {self.bitnessPath}")
			self.bitnessPath.mkdir(exist_ok=True)

		if not self.fullProductDir.exists():
			self.logger.info(F"Creating product path: {self.fullProductDir}")
			self.fullProductDir.mkdir(exist_ok=True)

		if not self.fullOutputDir.exists():
			self.logger.info(F"Creating output path: {self.fullOutputDir}")
			self.fullOutputDir.mkdir(exist_ok=True)

		if not self.offtreePrefix.exists():
			self.logger.info(F"Creating bitdir: {self.offtreePrefix}")
			self.offtreePrefix.mkdir(exist_ok=True)

		# create toolchain files for meson and cmake
		self.createMesonEnvFile()
		self.createCmakeToolchainFile()

	def boolKey(self, d, k):
		if k in d:
			if d[k]:
				return True
		return False

	def reStrip(self, pat, txt):
		x = re.sub(pat, '', txt)
		return re.sub(r'[ ]+', ' ', x).strip()

	def aquireLocalPkgConfigPath(self):
		possiblePathsStr = subprocess.check_output('pkg-config --variable pc_path pkg-config', shell=True, stderr=subprocess.STDOUT).decode("utf-8").strip()
		
		if possiblePathsStr == "":
			raise Exception("Unable to determine local pkg-config path(s), pkg-config output is empty")
		
		possiblePaths = [Path(x.strip()) for x in possiblePathsStr.split(":")]

		for p in possiblePaths:
			if not p.exists():
				possiblePaths.remove(p)

		if not len(possiblePaths):
			raise Exception(F"Unable to determine local pkg-config path(s), pkg-config output is: {possiblePathsStr}")

		return ":".join(str(x) for x in possiblePaths)

	def buildMingw(self, bitness):
		gcc_bin = os.path.join(self.mingwBinpath, self.bitnessStr + "-w64-mingw32-gcc")

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
			self.logger.info("Building MinGW-w64 in folder '{0}'".format(self.mingwDir))

			# os.makedirs(self.mingwDir, exist_ok=True)

			os.unsetenv("CFLAGS")

			# self.cchdir(self.mingwDir)

			module_path = self.config["script"]["mingw_toolchain_path"].replace("/", ".").rstrip(".py")

			if not os.path.isfile(os.path.join("..", self.config["script"]["mingw_toolchain_path"])):
				self.errorExit("Specified MinGW build script path does not exist: '%s'" % (module_path))

			def toolchainBuildStatus(logMessage):
				self.logger.info(logMessage)

			mod = importlib.import_module(module_path)

			# from mingw_toolchain_script.mingw_toolchain_script import MinGW64ToolChainBuilder

			toolchainBuilder = mod.MinGW64ToolChainBuilder()

			toolchainBuilder.workDir = self.mingwDir
			if self.config["toolchain"]["mingw_commit"] is not None:
				toolchainBuilder.setMinGWcheckout(self.config["toolchain"]["mingw_commit"])
			if self.config["toolchain"]["mingw_custom_cflags"] is not None:
				toolchainBuilder.setCustomCflags(self.config["toolchain"]["mingw_custom_cflags"])
			toolchainBuilder.setDebugBuild(self.config["toolchain"]["mingw_debug_build"])
			toolchainBuilder.onStatusUpdate += toolchainBuildStatus
			toolchainBuilder.build()

			# self.cchdir("..")
		else:
			self.logger.error("It looks like the previous MinGW build failed, please delete the folder '%s' and re-run this script" % self.mingwDir)
			sys.exit(1)
	#:

	def downloadHeader(self, url):
		destination = self.targetPrefix.joinpath("include")
		fileName = os.path.basename(urlparse(url).path)

		if not os.path.isfile(os.path.join(destination, fileName)):
			fname = self.downloadFile(url)
			self.logger.debug("Moving Header File: '{0}' to '{1}'".format(fname, destination))
			shutil.move(fname, destination)
		else:
			self.logger.debug("Header File: '{0}' already downloaded".format(fileName))

	def downloadFile(self, url=None, outputFileName=None, outputPath=None, bytesMode=False):
		def fmt_size(num, suffix="B"):
				for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
					if abs(num) < 1024.0:
						return "%3.1f%s%s" % (num, unit, suffix)
					num /= 1024.0
				return "%.1f%s%s" % (num, "Yi", suffix)
		#:
		if not url:
			raise Exception("No URL specified.")

		if outputPath is None:  # Default to current dir.
			outputPath = os.getcwd()
		else:
			if not os.path.isdir(outputPath):
				raise Exception('Specified path "{0}" does not exist'.format(outputPath))

		fileName = os.path.basename(url)  # Get URL filename
		userAgent = self.userAgent

		if 'sourceforge.net' in url.lower():
			userAgent = 'wget/1.18'  # sourceforce <3 wget

		if url.lower().startswith("ftp://"):
			self.logger.info("Requesting : {0}".format(url))
			if outputFileName is not None:
				fileName = outputFileName
			fullOutputPath = os.path.join(outputPath, fileName)
			urllib.request.urlretrieve(url, fullOutputPath)
			return fullOutputPath

		if url.lower().startswith("file://"):
			url = url.replace("file://", "")
			self.logger.info("Copying : {0}".format(url))
			if outputFileName is not None:
				fileName = outputFileName
			fullOutputPath = os.path.join(outputPath, fileName)
			try:
				shutil.copyfile(url, fullOutputPath)
			except Exception as e:
				print(e)
				exit(1)
			return fullOutputPath

		req = requests.get(url, stream=True, headers={"User-Agent": userAgent})

		if req.status_code != 200:
			req.raise_for_status()

		if "content-disposition" in req.headers:
			reSponse = re.findall("filename=(.+)", req.headers["content-disposition"])
			if reSponse is None:
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

		self.logger.info("Requesting : {0} - {1}".format(url, fmt_size(size) if size is not None else "?"))

		# terms = shutil.get_terminal_size((100,100))
		# filler = 0
		# if terms[0] > 100:
		# 	filler = int(terms[0]/4)

		widgetsNoSize = [
			progressbar.FormatCustomText("Downloading: {:25.25}".format(os.path.basename(fileName))), " ",
			progressbar.AnimatedMarker(markers='|/-\\'), " ",
			progressbar.DataSize()
			# " "*filler
		]
		widgets = [
			progressbar.FormatCustomText("Downloading: {:25.25}".format(os.path.basename(fileName))), " ",
			progressbar.Percentage(), " ",
			progressbar.Bar(fill=chr(9617), marker=chr(9608), left="[", right="]"), " ",
			progressbar.DataSize(), "/", progressbar.DataSize(variable="max_value"), " |",
			progressbar.AdaptiveTransferSpeed(), " | ",
			progressbar.ETA(),
			# " "*filler
		]
		pbar = None
		if size is None:
			pbar = progressbar.ProgressBar(widgets=widgetsNoSize, maxval=progressbar.UnknownLength)
		else:
			pbar = progressbar.ProgressBar(widgets=widgets, maxval=size)

		if outputFileName is not None:
			fileName = outputFileName
		fullOutputPath = os.path.join(outputPath, fileName)

		updateSize = 0

		if isinstance(pbar.max_value, int):
			updateSize = pbar.max_value if pbar.max_value < 1024 else 1024

		if bytesMode is True:
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

	def createCmakeToolchainFile(self):
		if not os.path.isfile(self.cmakeToolchainFile):
			self.logger.info("Creating CMake Toolchain file at: '%s'" % (self.cmakeToolchainFile))
			tcFile = [
				F'set(CMAKE_SYSTEM_NAME Windows)',
				F'set(CMAKE_SYSTEM_PROCESSOR {self.bitnessStr})',
				F'set(CMAKE_SYSROOT {self.targetSubPrefix})',
				#F'set(CMAKE_STAGING_PREFIX /home/devel/stage)',
				F'set(CMAKE_RANLIB {self.shortCrossPrefixStr}ranlib)',
				F'set(CMAKE_C_COMPILER {self.shortCrossPrefixStr}gcc)',
				F'set(CMAKE_CXX_COMPILER {self.shortCrossPrefixStr}g++)',
				F'set(CMAKE_RC_COMPILER {self.shortCrossPrefixStr}windres)',
				F'set(CMAKE_FIND_ROOT_PATH {self.targetPrefix})',
				F'set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)',
				F'set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)',
				F'set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)',
				F'set(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY)',

				# for shaderc
				F'set(MINGW_COMPILER_PREFIX {self.shortCrossPrefixStr})',
				F'set(MINGW_SYSROOT {self.targetSubPrefix})'
			]
			with open(self.cmakeToolchainFile, 'w') as f:
				f.write("\n".join(tcFile))

	def createMesonEnvFile(self):
		if not os.path.isfile(self.mesonEnvFile):
			self.logger.info("Creating Meson Environment file at: '%s'" % (self.mesonEnvFile))
			meFile = (
				"[binaries]\n",
				F"c = '{self.shortCrossPrefixStr}gcc'",
				F"cpp = '{self.shortCrossPrefixStr}g++'",
				F"ld = 'bfd'", # See: https://github.com/mesonbuild/meson/issues/6431#issuecomment-572544268, no clue either why we can't just define full "ld" path, but whatever.
				# F"ld = '{self.shortCrossPrefixStr}ld'",
				F"ar = '{self.shortCrossPrefixStr}ar'",
				F"strip = '{self.shortCrossPrefixStr}strip'",
				F"windres = '{self.shortCrossPrefixStr}windres'",
				F"ranlib = '{self.shortCrossPrefixStr}ranlib'",
				"pkgconfig = 'pkg-config'",
				F"dlltool = '{self.shortCrossPrefixStr}dlltool'",
				F"gendef = '{self.mingwBinpath}/gendef'",
				"cmake = 'cmake'",
				"#needs_exe_wrapper = false",
				"#exe_wrapper = 'wine' # A command used to run generated executables.",
				"",
				"[host_machine]",
				"system = 'windows'",
				F"cpu_family = '{self.bitnessStr}'",
				F"cpu = '{self.bitnessStr}'",
				"endian = 'little'",
				"",
				"[target_machine]",
				"system = 'windows'",
				F"cpu_family = '{self.bitnessStr}'",
				F"cpu = '{self.bitnessStr}'",
				"endian = 'little'",
				"",
				"[properties]",
				"c_link_args = ['-static', '-static-libgcc']",
				"# sys_root = Directory that contains 'bin', 'lib', etc for the toolchain and system libraries",
				F"sys_root = '{self.targetSubPrefix}'"
			)
			with open(self.mesonEnvFile, 'w') as f:
				f.write("\n".join(meFile))

	# def downloadFileOld(self, link, targetName=None):
	# 	_MAX_REDIRECTS = 5
	# 	cj = http.cookiejar.CookieJar()

	# 	class RHandler(urllib.request.HTTPRedirectHandler):
	# 		def http_error_301(self, req, fp, code, msg, headers):
	# 			result = urllib.request.HTTPRedirectHandler.http_error_301(
	# 				self, req, fp, code, msg, headers)
	# 			result.status = code
	# 			return result

	# 		def http_error_302(self, req, fp, code, msg, headers):
	# 			result = urllib.request.HTTPRedirectHandler.http_error_302(
	# 				self, req, fp, code, msg, headers)
	# 			result.status = code
	# 			return result

	# 	def sizeof_fmt(num, suffix='B'):  # sizeof_fmt is courtesy of https://stackoverflow.com/a/1094933
	# 		for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
	# 			if abs(num) < 1024.0:
	# 				return "%3.1f%s%s" % (num, unit, suffix)
	# 			num /= 1024.0
	# 		return "%.1f%s%s" % (num, 'Yi', suffix)

	# 	link = urllib.parse.unquote(link)
	# 	_CHUNKSIZE = 10240

	# 	if not link.lower().startswith("https") and not link.lower().startswith("file"):
	# 		self.logger.warning("WARNING: Using non-SSL http is not advised..")  # gotta get peoples attention somehow eh?

	# 	fname = None

	# 	if targetName is None:
	# 		fname = os.path.basename(urlparse(link).path)
	# 	else:
	# 		fname = targetName

	# 	# print("Downloading {0} to {1} ".format(link, fname))

	# 	ua = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
	# 	if 'sourceforge.net' in link.lower():
	# 		ua = 'wget/1.18'  # sourceforge gives direct dls to wget agents.

	# 	f = open(fname, 'ab')
	# 	hdrs = [  # act like chrome
	# 		('Connection', 'keep-alive'),
	# 		('Pragma', 'no-cache'),
	# 		('Cache-Control', 'no-cache'),
	# 		('Upgrade-Insecure-Requests', '1'),
	# 		('User-Agent', ua),
	# 		('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),
	# 		# ('Accept-Encoding', 'gzip'),
	# 		('Accept-Language', 'en-US,en;q=0.8'),
	# 	]

	# 	opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))  # ),RHandler()

	# 	opener.addheaders = hdrs

	# 	response = None

	# 	request = urllib.request.Request(link)

	# 	try:
	# 		response = opener.open(request)

	# 		olink = link
	# 		for i in range(0, _MAX_REDIRECTS):  # i have no idea of this is something I should be doing.
	# 			if olink == response.geturl():
	# 				break
	# 			else:
	# 				print("Following redirect to: {0}".format(response.geturl()))
	# 				response = opener.open(urllib.request.Request(response.geturl()))

	# 				olink = response.geturl()

	# 	except Exception:
	# 		print("Error downloading: " + link)
	# 		traceback.print_exc()
	# 		f.close()

	# 		exit()

	# 	headers = str(response.info())
	# 	length = re.search(r'Content-Length: ([0-9]+)', headers, re.IGNORECASE)

	# 	fileSize = None
	# 	if length is None:
	# 		pass  # tbd
	# 	else:
	# 		fileSize = int(length.groups()[0])

	# 	# fileSizeDigits = int(math.log10(fileSize))+1

	# 	downloadedBytes = 0

	# 	start = time.clock()

	# 	fancyFileSize = None
	# 	if fileSize is not None:
	# 		fancyFileSize = sizeof_fmt(fileSize)
	# 		fancyFileSize = fancyFileSize.ljust(len(fancyFileSize))

	# 	isGzipped = False
	# 	if "content-encoding" in response.headers:
	# 		if response.headers["content-encoding"] == "gzip":
	# 			isGzipped = True

	# 	while True:
	# 		chunk = response.read(_CHUNKSIZE)
	# 		downloadedBytes += len(chunk)
	# 		if isGzipped:
	# 			if len(chunk):
	# 				try:
	# 					chunk = zlib.decompress(chunk, 15 + 32)
	# 				except Exception as e:
	# 					print(e)
	# 					exit()

	# 		f.write(chunk)
	# 		if fileSize is not None:
	# 			done = int(50 * downloadedBytes / fileSize)
	# 			fancySpeed = sizeof_fmt((downloadedBytes // (time.clock() - start)) / 8, "B/s").rjust(5, ' ')
	# 			fancyDownloadedBytes = sizeof_fmt(downloadedBytes).rjust(len(fancyFileSize), ' ')
	# 			print("[{0}] - {1}/{2} ({3})".format('|' * done + '-' * (50 - done), fancyDownloadedBytes, fancyFileSize, fancySpeed), end="\r")
	# 		else:
	# 			print("{0}".format(sizeof_fmt(downloadedBytes)), end="\r")

	# 		if not len(chunk):
	# 			break
	# 	print("")

	# 	response.close()

	# 	f.close()
	# 	# print("File fully downloaded to:",fname)

	# 	return os.path.basename(link)
	# #:

	# def download_file_v2(self, url=None, outputFileName=None, outputPath=None, bytes=False):
	# 	if not url:
	# 		raise Exception('No url')
	# 	if outputPath is None:
	# 		outputPath = os.getcwd()
	# 	else:
	# 		if not os.path.isdir(outputPath):
	# 			raise Exception('Path "" does not exist'.format(outputPath))
	# 	fileName = url.split('/')[-1]  # base fallback name
	# 	print("Connecting to: " + url)
	# 	req = requests.get(url, stream=True, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'})
	# 	if req.status_code != 404:
	# 		if 'content-disposition' in req.headers:
	# 			fileName = req.headers['content-disposition']
	# 		size = None
	# 		if 'Content-Length' in req.headers:
	# 			size = int(req.headers['Content-Length'])

	# 		if 'Content-Encoding' in req.headers:
	# 			if req.headers['Content-Encoding'] == "gzip":
	# 				size = None

	# 		print("Downloading: '{0}' {1}".format(url, fmt_size(size) if size!=None else "?"))
	# 		widgetsNoSize = [
	# 			progressbar.Percentage(), " ",
	# 			progressbar.Bar(fill=chr(9617), marker=chr(9608), left="[", right="]"), " ",
	# 			progressbar.DataSize(),
	# 		]
	# 		widgets = [
	# 			progressbar.Percentage(), " ",
	# 			progressbar.Bar(fill=chr(9617), marker=chr(9608), left="[", right="]"), " ",
	# 			progressbar.DataSize(), "/", progressbar.DataSize(variable="max_value"), " |",
	# 			progressbar.AdaptiveTransferSpeed(), " | ",
	# 			progressbar.ETA(),
	# 		]
	# 		pbar = None
	# 		if size is None:
	# 			pbar = progressbar.ProgressBar(widgets=widgetsNoSize,maxval=progressbar.UnknownLength)
	# 		else:
	# 			pbar = progressbar.ProgressBar(widgets=widgets,maxval=size)
	# 		if outputFileName is not None:
	# 			fileName = outputFileName
	# 		fullOutputPath = os.path.join(outputPath,fileName)

	# 		if bytes is True:
	# 			output = b''
	# 			bytesrecv = 0
	# 			pbar.start()
	# 			for buffer in req.iter_content(chunk_size=1024):
	# 				if buffer:
	# 					 output += buffer
	# 				pbar.update(bytesrecv)
	# 				bytesrecv += len(buffer)
	# 			pbar.finish()
	# 			return output
	# 		else:
	# 			with open(fullOutputPath, "wb") as file:
	# 				bytesrecv = 0
	# 				pbar.start()
	# 				for buffer in req.iter_content(chunk_size=1024):
	# 					if buffer:
	# 						file.write(buffer)
	# 						file.flush()
	# 					pbar.update(bytesrecv)
	# 					bytesrecv += len(buffer)
	# 				pbar.finish()

	# 				return fullOutputPath
	# #:

	def runProcess(self, command, ignoreErrors=False, exitOnError=True, silent=False):
		isSvn = False
		if not isinstance(command, str):
			command = " ".join(command)  # could fail I guess
		if command.lower().startswith("svn"):
			isSvn = True
		self.logger.debug("Running '{0}' in '{1}'".format(command, os.getcwd()))
		process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
		buffer = ""
		while True:
			nextline = process.stdout.readline()
			if nextline == b'' and process.poll() is not None:
				break
			buffer += nextline.decode("utf-8", "ignore")
			if isSvn:
				if not nextline.decode('utf-8').startswith('A    '):
					if self.quietMode:
						self.buildLogFile.write(nextline.decode('utf-8', 'replace'))
					elif not silent:
						sys.stdout.write(nextline.decode('utf-8', 'replace'))
						sys.stdout.flush()
			else:
				if self.quietMode:
					self.buildLogFile.write(nextline.decode('utf-8', 'replace'))
				elif not silent:
					sys.stdout.write(nextline.decode('utf-8', 'replace'))
					sys.stdout.flush()

		return_code = process.returncode
		process.communicate()[0]
		process.wait()
		if (return_code == 0):
			return buffer
		else:
			if ignoreErrors:
				return buffer
			self.logger.error("Error [{0}] running process: '{1}' in '{2}'".format(return_code, command, os.getcwd()))
			self.logger.error("You can try deleting the product/dependency folder: '{0}' and re-run the script".format(os.getcwd()))
			if self.quietMode:
				self.logger.error("Please check the raw_build.log file")
			if exitOnError:
				exit(1)

		# p = subprocess.Popen(command, stdout=subprocess.PIPE,stderr=subprocess.STDOUT, universal_newlines = True, shell = True)
		# for line in iter(p.stdout.readline, b''):
		# 	sys.stdout.write(line)
		# 	sys.stdout.flush()
		# p.close()

	def getProcessResult(self, command):
		if not isinstance(command, str):
			command = " ".join(command)  # could fail I guess
		process = subprocess.Popen(command, stdout=subprocess.PIPE, universal_newlines=True, shell=True)
		out = process.stdout.readline().rstrip("\n").rstrip("\r")
		process.stdout.close()
		return_code = process.wait()
		if (return_code == 0):
			return out
		else:
			self.logger.error("Error [%d] creating process '%s'" % (return_code, command))
			exit()

	def sanitizeFilename(self, f):
		return re.sub(r'[/\\:*?"<>|]', '', f)

	def md5(self, *args):
		msg = ''.join(args).encode("utf-8")
		m = hashlib.md5()
		m.update(msg)
		return m.hexdigest()

	def hashFile(self, fname, type="sha256"):
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

	def touch(self, f):
		Path(f).touch()

	def chmodPux(self, file):
		st = os.stat(file)
		os.chmod(file, st.st_mode | stat.S_IXUSR)  # S_IEXEC would be just +x
	#:

	def mercurialClone(self, url, virtFolderName=None, renameTo=None, desiredBranch=None, forceRebuild=False):
		if virtFolderName is None:
			virtFolderName = self.sanitizeFilename(os.path.basename(url))
			if not virtFolderName.endswith(".hg"):
				virtFolderName += ".hg"
			virtFolderName = virtFolderName.replace(".hg", "_hg")
		else:
			virtFolderName = self.sanitizeFilename(virtFolderName)

		realFolderName = virtFolderName
		if renameTo is not None:
			realFolderName = renameTo

		branchString = ""
		if desiredBranch is not None:
			branchString = " {0}".format(desiredBranch)

		# we have to do it the hard way because "hg purge" is an extension that is not on by default
		# and making users enable stuff like that is too much
		if os.path.isdir(realFolderName) and forceRebuild:
			self.logger.info("Deleting old HG clone")
			shutil.rmtree(realFolderName)

		if os.path.isdir(realFolderName):
			self.cchdir(realFolderName)
			hgVersion = subprocess.check_output('hg --debug id -i', shell=True)
			self.runProcess('hg pull -u')
			self.runProcess('hg update -C{0}'.format(" default" if desiredBranch is None else branchString))
			hgVersionNew = subprocess.check_output('hg --debug id -i', shell=True)
			if hgVersion != hgVersionNew:
				self.logger.debug("HG clone has code changes, updating")
				self.removeAlreadyFiles()
			else:
				self.logger.debug("HG clone already up to date")
			self.cchdir("..")
		else:
			self.logger.info("HG cloning '%s' to '%s'" % (url, realFolderName))
			self.runProcess('hg clone {0} {1}'.format(url, realFolderName + ".tmp"))
			if desiredBranch is not None:
				self.cchdir(realFolderName + ".tmp")
				self.logger.debug("HG updating to:{0}".format(" master" if desiredBranch is None else branchString))
				self.runProcess('hg up{0} -v'.format("" if desiredBranch is None else branchString))
				self.cchdir("..")
			self.runProcess('mv "{0}" "{1}"'.format(realFolderName + ".tmp", realFolderName))
			self.logger.info("Finished HG cloning '%s' to '%s'" % (url, realFolderName))

		return realFolderName
	#:

	def gitClone(self, url, virtFolderName=None, renameTo=None, desiredBranch=None, recursive=False, doNotUpdate=False, desiredPR=None, depth=-1):
		if virtFolderName is None:
			virtFolderName = self.sanitizeFilename(os.path.basename(url))
			if not virtFolderName.endswith(".git"):
				virtFolderName += ".git"
			virtFolderName = virtFolderName.replace(".git", "_git")
		else:
			virtFolderName = self.sanitizeFilename(virtFolderName)

		realFolderName = virtFolderName
		if renameTo is not None:
			realFolderName = renameTo

		branchString = ""
		if desiredBranch is not None:
			branchString = " {0}".format(desiredBranch)

		properBranchString = "master"
		if desiredBranch is not None:
			properBranchString = desiredBranch

		if os.path.isdir(realFolderName):
			if desiredPR is not None:
				self.logger.warning("####################")
				self.logger.info("Git repositiories with set PR will not auto-update, please delete the repo and retry to do so.")
				self.logger.warning("####################")
			elif doNotUpdate is True:
				self.logger.info("####################")
				self.logger.info("do_not_git_update is True")
				self.logger.info("####################")
			else:
				self.cchdir(realFolderName)

				self.runProcess('git remote update')

				UPSTREAM = '@{u}'  # or branchName i guess
				if desiredBranch is not None:
					UPSTREAM = properBranchString
				LOCAL = subprocess.check_output('git rev-parse @', shell=True).decode("utf-8")
				REMOTE = subprocess.check_output('git rev-parse "{0}"'.format(UPSTREAM), shell=True).decode("utf-8")
				BASE = subprocess.check_output('git merge-base @ "{0}"'.format(UPSTREAM), shell=True).decode("utf-8")

				self.runProcess('git checkout -f')
				self.runProcess('git checkout {0}'.format(properBranchString))

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
					if desiredBranch is not None:
						# bsSplit = properBranchString.split("/")
						# if len(bsSplit) == 2:
						# 	self.run_process('git pull origin {1}'.format(bsSplit[0],bsSplit[1]))
						# else:
						if 'Already up to date' in self.runProcess('git pull origin {0}'.format(properBranchString), silent=True):
							return os.getcwd()
					else:
						self.runProcess('git pull'.format(properBranchString))
					self.runProcess('git clean -ffdx')  # https://gist.github.com/nicktoumpelis/11214362
					self.runProcess('git submodule foreach --recursive git clean -ffdx')
					self.runProcess('git reset --hard')
					self.runProcess('git submodule foreach --recursive git reset --hard')
					self.runProcess('git submodule update --init --recursive')
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
			addArgs = []
			if recursive:
				addArgs.append("--recursive")

			if depth and depth >= 1:
				addArgs.append(F"--depth {depth}")
			elif depth is None or depth < 0:
				depth = 1
				addArgs.append(F"--depth 1")

			self.logger.info(F"Git {'Shallow C' if depth >= 1 else 'C'}loning '{url}' to '{os.getcwd() + '/' + realFolderName}'")
			self.runProcess('git clone {0} --progress "{1}" "{2}"'.format(" ".join(addArgs), url, realFolderName + ".tmp"))
			if desiredBranch is not None:
				self.cchdir(realFolderName + ".tmp")
				self.logger.debug("GIT Checking out:{0}".format(" master" if desiredBranch is None else branchString))
				self.runProcess('git checkout{0}'.format(" master" if desiredBranch is None else branchString))
				self.cchdir("..")
			if desiredPR is not None:
				self.cchdir(realFolderName + ".tmp")
				self.logger.info("GIT Fetching PR: {0}".format(desiredPR))
				self.runProcess('git fetch origin refs/pull/{0}/head'.format(desiredPR))
				self.cchdir("..")
			self.runProcess('mv "{0}" "{1}"'.format(realFolderName + ".tmp", realFolderName))
			self.logger.info("Finished GIT cloning '%s' to '%s'" % (url, realFolderName))

		return realFolderName
	#:

	def svnClone(self, url, dir, desiredBranch=None):  # "branch".. "clone"..
		dir = self.sanitizeFilename(dir)
		if not dir.endswith("_svn"):
			dir += "_svn"
		if not os.path.isdir(dir):
			self.logger.info("SVN checking out to %s" % (dir))
			if desiredBranch is None:
				self.runProcess('svn co "%s" "%s.tmp" --non-interactive --trust-server-cert' % (url, dir))
			else:
				self.runProcess('svn co -r "%s" "%s" "%s.tmp" --non-interactive --trust-server-cert' % (desiredBranch, url, dir))
			shutil.move('%s.tmp' % dir, dir)
		else:
			pass
		return dir
	#:

	def verifyHash(self, file, hash):
		if hash["type"] not in ["sha256", "sha512", "md5", "blake2b"]:
			raise Exception("Unsupported hash type: " + hash["type"])
		newHash = self.hashFile(file, hash["type"])
		if hash["sum"] == newHash:
			return (True, hash["sum"], newHash)
		return (False, hash["sum"], newHash)

	def downloadUnpackFile(self, packageData, packageName, folderName=None, workDir=None):
		customFolder = False
		if folderName is None:
			folderName = os.path.basename(os.path.splitext(urlparse(self.getPrimaryPackageUrl(packageData, packageName)).path)[0]).rstrip(".tar")
		else:
			customFolder = True
		folderToCheck = folderName

		if "rename_folder" in packageData and packageData["rename_folder"] != "" and packageData["rename_folder"] is not None:
			folderToCheck = packageData["rename_folder"]

		if workDir is not None:
			folderToCheck = workDir

		check_file = os.path.join(folderToCheck, "unpacked.successfully")
		if not os.path.isfile(check_file):
			dlLocation = self.getBestMirror(packageData, packageName)
			url = dlLocation["url"]
			fileName = os.path.basename(urlparse(url).path)
			self.logger.info("Downloading {0} ({1})".format(fileName, url))

			self.downloadFile(url, fileName)

			if "hashes" in dlLocation:
				if len(dlLocation["hashes"]) >= 1:
					for hash in dlLocation["hashes"]:
						self.logger.info("Comparing hashes..")
						hashReturn = self.verifyHash(fileName, hash)
						if hashReturn[0] is True:
							self.logger.info("Hashes matched: {0}...{1} (local) == {2}...{3} (remote)".format(hashReturn[1][0:5], hashReturn[1][-5:], hashReturn[2][0:5], hashReturn[2][-5:]))
						else:
							self.logger.error("File hashes didn't match: %s(local) != %s(remote)" % (hashReturn[1], hashReturn[2]))
							raise Exception("File download error: Hash mismatch")
							exit(1)

			self.logger.info("Unpacking {0}".format(fileName))

			tars = (".gz", ".bz2", ".xz", ".bz", ".tgz")  # i really need a better system for this.. but in reality, those are probably the only formats we will ever encounter.

			customFolderTarArg = ""

			if customFolder:
				customFolderTarArg = ' -C "' + folderName + '" --strip-components 1'
				os.makedirs(folderName)

			if fileName.endswith(tars):
				self.runProcess('tar -xf "{0}"{1}'.format(fileName, customFolderTarArg))
			else:
				self.runProcess('unzip "{0}"'.format(fileName))

			self.touch(os.path.join(folderName, "unpacked.successfully"))

			os.remove(fileName)

			return folderName

		else:
			self.logger.debug("{0} already downloaded".format(folderName))
			return folderName
	#:

	def checkMirrors(self, dlLocations):
		for loc in dlLocations:
			userAgent = self.userAgent
			if 'sourceforge.net' in loc["url"].lower():
				userAgent = 'wget/1.20.3'  # sourceforce allows direct downloads when using wget, so we pretend we are wget
			try:
				req = requests.request("GET", loc["url"], stream=True, allow_redirects=True, headers={"User-Agent": userAgent})
			except requests.exceptions.RequestException as e:
				self.logger.debug(e)
			else:
				if req.status_code == 200:
					return loc
				else:
					self.logger.debug(loc["url"] + " unable to reach: HTTP" + str(req.status_code))

		return dlLocations[0]  # return the first if none could be found.

	def getBestMirror(self, packageData, packageName):  # returns the first online mirror of a package, and its hash
		if "url" in packageData:
			if packageData["repo_type"] == "archive":
				self.logger.warning("Package has the old URL format, please update it.")
			return {"url": packageData["url"], "hashes": []}
		elif "download_locations" not in packageData:
			raise Exception("download_locations not specificed for package: " + packageName)
		else:
			if not len(packageData["download_locations"]) >= 1:
				raise Exception("download_locations is empty for package: " + packageName)
			if "url" not in packageData["download_locations"][0]:
				raise Exception("download_location #1 of package '%s' has no url specified" % (packageName))

			return self.checkMirrors(packageData["download_locations"])

	def getPrimaryPackageUrl(self, packageData, packageName):  # returns the URL of the first download_locations entry from a package, unlike get_best_mirror this one ignores the old url format
		if "url" in packageData:
			if packageData["repo_type"] == "archive":
				self.logger.debug("Package has the old URL format, please update it.")
			return packageData["url"]
		elif "download_locations" not in packageData:
			raise Exception("download_locations in package '%s' not specificed" % (packageName))
		else:
			if not len(packageData["download_locations"]) >= 1:
				raise Exception("download_locations is empty for package")
			if "url" not in packageData["download_locations"][0]:
				raise Exception("download_location #1 of package has no url specified")
			return packageData["download_locations"][0]["url"]  # TODO: do not assume correct format
	#:

	def getPackagePath(self, packageName, packageData, type):  # type = PRODUCT or DEPENDENCY
		outPath = os.getcwd()
		workDir = None
		renameFolder = None
		if 'rename_folder' in packageData:
			if packageData['rename_folder'] is not None:
				renameFolder = packageData['rename_folder']
		if type == "P":
			outPath = self.fullProductDir
			self.cchdir(self.fullProductDir)
		else:
			outPath = os.path.join(outPath, self.bitnessPath)
			self.cchdir(self.bitnessPath)

		if packageData["repo_type"] == "git":
			branch = self.getValueOrNone(packageData, 'branch')
			recursive = self.getValueOrNone(packageData, 'recursive_git')
			git_depth = packageData.get('depth_git', -1)
			folderName = self.getValueOrNone(packageData, 'folder_name')
			doNotUpdate = False
			if 'do_not_git_update' in packageData:
				if packageData['do_not_git_update'] is True:
					doNotUpdate = True
			workDir = self.gitClone(self.getPrimaryPackageUrl(packageData, packageName), folderName, renameFolder, branch, recursive, doNotUpdate, None, git_depth)
		if packageData["repo_type"] == "svn":
			workDir = self.svnClone(self.getPrimaryPackageUrl(packageData, packageName), packageData["folder_name"], renameFolder)
		if packageData['repo_type'] == 'mercurial':
			branch = self.getValueOrNone(packageData, 'branch')
			workDir = self.mercurialClone(self.getPrimaryPackageUrl(packageData, packageName), self.getValueOrNone(packageData, 'folder_name'), renameFolder, branch)
		if packageData["repo_type"] == "archive":
			if "folder_name" in packageData:
				workDir = self.downloadUnpackFile(packageData, packageName, packageData["folder_name"], workDir)
			else:
				workDir = self.downloadUnpackFile(packageData, packageName, None, workDir)

		if workDir is None:
			print("Unexpected error when building {0}, please report this:".format(packageName), sys.exc_info()[0])
			raise

		if 'rename_folder' in packageData:  # this should be moved inside the download functions, TODO.. but lazy
			if packageData['rename_folder'] is not None:
				if not os.path.isdir(packageData['rename_folder']):
					shutil.move(workDir, packageData['rename_folder'])
				workDir = packageData['rename_folder']
		self.cchdir("..")
		return os.path.join(outPath, workDir)

	def buildThing(self, packageName, packageData, type, forceRebuild=False, skipDepends=False):  # type = PRODUCT or DEPENDENCY # I couldn't come up with a better name :S
		# we are in workdir
		if '_already_built' in packageData:
			if packageData['_already_built'] is True:
				return
		if 'skip_deps' in packageData:
			if packageData['skip_deps'] is True:
				skipDepends = True
		if "depends_on" in packageData and skipDepends is False:  # dependception
			if len(packageData["depends_on"]) > 0:
				self.logger.info("Building dependencies of '%s'" % (packageName))
				for libraryName in packageData["depends_on"]:
					if libraryName not in self.packages["deps"]:
						raise MissingDependency("The dependency '{0}' of '{1}' does not exist in dependency config.".format(libraryName, packageName))  # sys.exc_info()[0]
					else:
						self.buildThing(libraryName, self.packages["deps"][libraryName], "DEPENDENCY")

		if 'is_dep_inheriter' in packageData:
			if packageData['is_dep_inheriter'] is True:
				if type == "PRODUCT":
					self.packages["prods"][packageName]["_already_built"] = True
				else:
					self.packages["deps"][packageName]["_already_built"] = True
				return

		if self.debugMode:
			print("### Environment variables:  ###")
			for tk in os.environ:
				print("\t" + tk + " : " + os.environ[tk])
			print("##############################")

		self.logger.info("Building {0} '{1}'".format(type.lower(), packageName))
		self.resetDefaultEnvVars()

		if 'warnings' in packageData:
			if len(packageData['warnings']) > 0:
				for w in packageData['warnings']:
					self.logger.warning(w)

		workDir = None
		renameFolder = None
		if 'rename_folder' in packageData:
			if packageData['rename_folder'] is not None:
				renameFolder = packageData['rename_folder']

		if type == "PRODUCT":
			self.cchdir(self.fullProductDir)  # descend into x86_64_products
		else:
			self.cchdir(self.bitnessPath)  # descend into x86_64

		if packageData["repo_type"] == "git":
			branch = self.getValueOrNone(packageData, 'branch')
			recursive = self.getValueOrNone(packageData, 'recursive_git')
			git_depth = packageData.get('depth_git', -1)
			folderName = self.getValueOrNone(packageData, 'folder_name')
			doNotUpdate = False
			if 'do_not_git_update' in packageData:
				if packageData['do_not_git_update'] is True:
					doNotUpdate is True
			desiredPRVal = None
			if 'desired_pr_id' in packageData:
				if packageData['desired_pr_id'] is not None:
					desiredPRVal = packageData['desired_pr_id']
			workDir = self.gitClone(self.getPrimaryPackageUrl(packageData, packageName), folderName, renameFolder, branch, recursive, doNotUpdate, desiredPRVal, git_depth)
		elif packageData["repo_type"] == "svn":
			workDir = self.svnClone(self.getPrimaryPackageUrl(packageData, packageName), packageData["folder_name"], renameFolder)
		elif packageData['repo_type'] == 'mercurial':
			branch = self.getValueOrNone(packageData, 'branch')
			workDir = self.mercurialClone(self.getPrimaryPackageUrl(packageData, packageName), self.getValueOrNone(packageData, 'folder_name'), renameFolder, branch, forceRebuild)
		elif packageData["repo_type"] == "archive":
			if "folder_name" in packageData:
				workDir = self.downloadUnpackFile(packageData, packageName, packageData["folder_name"], workDir)
			else:
				workDir = self.downloadUnpackFile(packageData, packageName, None, workDir)
		elif packageData["repo_type"] == "none":
			if "folder_name" in packageData:
				workDir = packageData["folder_name"]
				os.makedirs(workDir, exist_ok=True)
			else:
				print("Error: When using repo_type 'none' you have to set folder_name as well.")
				exit(1)

		if workDir is None:
			print("Unexpected error when building {0}, please report this:".format(packageName), sys.exc_info()[0])
			raise

		if 'rename_folder' in packageData:  # this should be moved inside the download functions, TODO.. but lazy
			if packageData['rename_folder'] is not None:
				if not os.path.isdir(packageData['rename_folder']):
					shutil.move(workDir, packageData['rename_folder'])
				workDir = packageData['rename_folder']

		if 'download_header' in packageData:
			if packageData['download_header'] is not None:
				for h in packageData['download_header']:
					self.downloadHeader(h)

		self.cchdir(workDir)  # descend into x86_64/[DEPENDENCY_OR_PRODUCT_FOLDER]
		if 'debug_downloadonly' in packageData:
			self.cchdir("..")
			exit()

		oldPath = self.getKeyOrBlankString(os.environ, "PATH")
		currentFullDir = os.getcwd()

		if not self.anyFileStartsWith('already_configured'):
			if 'run_pre_patch' in packageData:
				if packageData['run_pre_patch'] is not None:
					for cmd in packageData['run_pre_patch']:
						cmd = self.replaceVariables(cmd)
						self.logger.debug("Running pre-patch-command: '{0}'".format(cmd))
						self.runProcess(cmd)

		if forceRebuild:
			if os.path.isdir(".git"):
				self.runProcess('git clean -ffdx')  # https://gist.github.com/nicktoumpelis/11214362
				self.runProcess('git submodule foreach --recursive git clean -ffdx')
				self.runProcess('git reset --hard')
				self.runProcess('git submodule foreach --recursive git reset --hard')
				self.runProcess('git submodule update --init --recursive')

		if 'source_subfolder' in packageData:
			if packageData['source_subfolder'] is not None:
				if not os.path.isdir(packageData['source_subfolder']):
					os.makedirs(packageData['source_subfolder'], exist_ok=True)
				self.cchdir(packageData['source_subfolder'])

		if forceRebuild:
			self.removeAlreadyFiles()
			self.removeConfigPatchDoneFiles()

		if 'debug_confighelp_and_exit' in packageData:
			if packageData['debug_confighelp_and_exit'] is True:
				self.bootstrapConfigure()
				self.runProcess("./configure --help")
				exit()

		if 'cflag_addition' in packageData:
			if packageData['cflag_addition'] is not None:
				os.environ["CFLAGS"] = os.environ["CFLAGS"] + " " + packageData['cflag_addition']
				os.environ["CXXFLAGS"] = os.environ["CXXFLAGS"] + " " + packageData['cflag_addition']
				self.logger.info(F'Added to C(XX)FLAGS, they\'re are now: "{os.environ["CXXFLAGS"]}", "{os.environ["CFLAGS"]}"')

		if 'custom_cflag' in packageData:
			if packageData['custom_cflag'] is not None:
				os.environ["CFLAGS"] = packageData['custom_cflag']
				os.environ["CXXFLAGS"] = packageData['custom_cflag']
				self.logger.info(F'Set custom C(XX)FLAGS, they\'re are now: "{os.environ["CXXFLAGS"]}", "{os.environ["CFLAGS"]}"')

		if 'strip_cflags' in packageData:
			if isinstance(packageData["strip_cflags"], (list, tuple)) and len(packageData["strip_cflags"]):
				for _pattern in packageData["strip_cflags"]:
					os.environ["CFLAGS"] = self.reStrip(_pattern, os.environ["CFLAGS"])
					os.environ["CXXFLAGS"] = self.reStrip(_pattern, os.environ["CXXFLAGS"])
					self.logger.info(F'Stripped C(XX)FLAGS, they\'re are now: "{os.environ["CXXFLAGS"]}", "{os.environ["CFLAGS"]}"')

		if 'custom_path' in packageData:
			if packageData['custom_path'] is not None:
				self.logger.debug("Setting PATH to '{0}'".format(self.replaceVariables(packageData['custom_path'])))
				os.environ["PATH"] = self.replaceVariables(packageData['custom_path'])

		if 'flipped_path' in packageData:
			if packageData['flipped_path'] is True:
				bef = os.environ["PATH"]
				os.environ["PATH"] = "{0}:{1}:{2}".format(self.mingwBinpath, os.path.join(self.targetPrefix, 'bin'), self.originalPATH)  # todo properly test this..
				self.logger.debug("Flipping path to: '{0}' from '{1}'".format(bef, os.environ["PATH"]))

		if 'env_exports' in packageData:
			if packageData['env_exports'] is not None:
				for key, val in packageData['env_exports'].items():
					val = self.replaceVariables(val)
					prevEnv = ''
					if key in os.environ:
						prevEnv = os.environ[key]
					self.logger.debug("Environment variable '{0}' has been set from {1} to '{2}'".format(key, prevEnv, val))
					os.environ[key] = val

		if 'copy_over' in packageData and packageData['copy_over'] is not None:
			for f in packageData['copy_over']:
				f_formatted = self.replaceVariables(f)
				f_formatted = Path(f_formatted)
				if not f_formatted.is_file():
					self.errorExit("Copy-over file '%s' (Unformatted: '%s') does not exist." % (f_formatted, f))
				dst = os.path.join(currentFullDir, f_formatted.name)
				self.logger.info("Copying file over from '%s' to '%s'" % (f_formatted, dst))
				shutil.copyfile(f_formatted, dst)

		if 'patches' in packageData:
			if packageData['patches'] is not None:
				for p in packageData['patches']:
					self.applyPatch(p[0], p[1], False, self.getValueByIntOrNone(p, 2))

		if not self.anyFileStartsWith('already_ran_make'):

			if 'regex_replace' in packageData and packageData['regex_replace']:
				_pos = 'post_patch'
				if isinstance(packageData['regex_replace'], dict) and _pos in packageData['regex_replace']:
					for r in packageData['regex_replace'][_pos]:
						try:
							self.handleRegexReplace(r, packageName)
						except re.error as e:
							self.errorExit(e)

			if 'run_post_patch' in packageData and packageData['run_post_patch']:
					for cmd in packageData['run_post_patch']:
						ignoreFail = False
						if isinstance(cmd, tuple):
							cmd = cmd[0]
							ignoreFail = cmd[1]
						if cmd.startswith("!SWITCHDIRBACK"):
							self.cchdir(currentFullDir)
						elif cmd.startswith("!SWITCHDIR"):
							_dir = self.replaceVariables("|".join(cmd.split("|")[1:]))
							self.cchdir(_dir)
						else:
							cmd = self.replaceVariables(cmd)
							self.logger.info("Running post-patch-command: '{0}'".format(cmd))
							# self.run_process(cmd)
							self.runProcess(cmd, ignoreFail)

		conf_system = None
		build_system = None

		# conf_system_specifics = {
		# 	"gnumake_based_systems" : [ "cmake", "autoconf" ],
		# 	"ninja_based_systems" : [ "meson" ]
		# }

		if 'build_system' in packageData:  # Kinda redundant, but ill keep it for now, maybe add an alias system for this.
			if packageData['build_system'] == "ninja":
				build_system = "ninja"
			if packageData['build_system'] == "waf":
				build_system = "waf"
			if packageData['build_system'] == "rake":
				build_system = "rake"
		if 'conf_system' in packageData:
			if packageData['conf_system'] == "cmake":
				conf_system = "cmake"
				if not build_system:
					build_system = "ninja"
			elif packageData['conf_system'] == "meson":
				conf_system = "meson"
			elif packageData['conf_system'] == "waf":
				conf_system = "waf"

		conf_system = "autoconf" if not conf_system else conf_system
		build_system = "make" if not build_system else build_system

		needs_conf = True

		if 'needs_configure' in packageData:
			if packageData['needs_configure'] is False:
				needs_conf = False

		if needs_conf:
			if conf_system == "cmake":
				self.cmakeSource(packageName, packageData)
			elif conf_system == "meson":
				self.mesonSource(packageName, packageData)
			else:
				self.configureSource(packageName, packageData, conf_system)

		if 'make_subdir' in packageData:
			if packageData['make_subdir'] is not None:
				if not os.path.isdir(packageData['make_subdir']):
					os.makedirs(packageData['make_subdir'], exist_ok=True)
				self.cchdir(packageData['make_subdir'])

		if 'needs_make' in packageData:
			if packageData['needs_make'] is True:
				self.buildSource(packageName, packageData, build_system)
		else:
			self.buildSource(packageName, packageData, build_system)

		if 'needs_make_install' in packageData:
			if packageData['needs_make_install'] is True:
				self.installSource(packageName, packageData, build_system)
		else:
			self.installSource(packageName, packageData, build_system)

		if 'env_exports' in packageData:
			if packageData['env_exports'] is not None:
				for key, val in packageData['env_exports'].items():
					self.logger.debug("Environment variable '{0}' has been UNSET!".format(key, val))
					del os.environ[key]

		if 'flipped_path' in packageData:
			if packageData['flipped_path'] is True:
				_path = os.environ["PATH"]
				os.environ["PATH"] = "{0}:{1}".format(self.mingwBinpath, self.originalPATH)
				self.logger.debug("Resetting flipped path to: '{0}' from '{1}'".format(_path, os.environ["PATH"]))

		if 'source_subfolder' in packageData:
			if packageData['source_subfolder'] is not None:
				if not os.path.isdir(packageData['source_subfolder']):
					os.makedirs(packageData['source_subfolder'], exist_ok=True)
				self.cchdir(currentFullDir)

		if 'make_subdir' in packageData:
			if packageData['make_subdir'] is not None:
				self.cchdir(currentFullDir)

		self.cchdir("..")  # asecond into x86_64
		if type == "PRODUCT":
			self.packages["prods"][packageName]["_already_built"] = True
		else:
			self.packages["deps"][packageName]["_already_built"] = True

		self.logger.info("Building {0} '{1}': Done!".format(type.lower(), packageName))
		if 'debug_exitafter' in packageData:
			exit()

		if 'custom_path' in packageData:
			if packageData['custom_path'] is not None:
				self.logger.debug("Re-setting PATH to '{0}'".format(oldPath))
				os.environ["PATH"] = oldPath

		self.resetDefaultEnvVars()
		self.cchdir("..")  # asecond into workdir
	#:

	def handleRegexReplace(self, rp, packageName):
		cwd = Path(os.getcwd())
		if "in_file" not in rp:
			self.errorExit(F'The regex_replace command in the package {packageName}:\n{rp}\nMisses the in_file parameter.')
		if 0 not in rp:
			self.errorExit(F'A regex_replace command in the package {packageName}\nrequires at least the "0" key to be a RegExpression, if 1 is not defined matching lines will be removed.')

		in_files = rp["in_file"]
		if isinstance(in_files, (list, tuple)):
			in_files = (cwd.joinpath(self.replaceVariables(x)) for x in in_files)
		else:
			in_files = (cwd.joinpath(self.replaceVariables(in_files)), )

		repls = [self.replaceVariables(rp[0]), ]
		if 1 in rp:
			repls.append(self.replaceVariables(rp[1]))

		self.logger.info(F"Running regex replace commands on package: '{packageName}' [{os.getcwd()}]")

		for _current_infile in in_files:
			if "out_file" not in rp:
				out_files = (_current_infile, )
				shutil.copy(_current_infile, _current_infile.parent.joinpath(_current_infile.name + ".backup"))
			else:
				if isinstance(rp["out_file"], (list, tuple)):
					out_files = (cwd.joinpath(self.replaceVariables(x)) for x in rp["out_file"])
				else:
					out_files = (cwd.joinpath(self.replaceVariables(rp["out_file"])),)

			for _current_outfile in out_files:

				if not _current_infile.exists():
					self.logger.warning(F"[Regex-Command] In-File '{_current_infile}' does not exist in '{os.getcwd()}'")

				if _current_outfile == _current_infile:
					_backup = _current_infile.parent.joinpath(_current_infile.name + ".backup")
					if not _backup.parent.exists():
						self.logger.warning(F"[Regex-Command] Out-File parent '{_backup.parent}' does not exist.")
					shutil.copy(_current_infile, _backup)
					_tmp_file = _current_infile.parent.joinpath(_current_infile.name + ".tmp")
					shutil.move(_current_infile, _tmp_file)
					_current_infile = _tmp_file
				self.logger.info(F"[{packageName}] Running regex command on '{_current_outfile}'")

				with open(_current_infile, "r") as f, open(_current_outfile, "w") as nf:
					for line in f:
						if re.search(repls[0], line) and len(repls) > 1:
							self.logger.debug(F"RegEx replacing line")
							self.logger.debug(F"in {_current_outfile}\n{line}\nwith:")
							line = re.sub(repls[0], repls[1], line)
							self.logger.debug(F"\n{line}")
							nf.write(line)
						elif re.search(repls[0], line):
							self.logger.info(F"RegEx removing line\n{line}:")
						else:
							nf.write(line)

	def bootstrapConfigure(self):
		if not os.path.isfile("configure"):
			if os.path.isfile("bootstrap.sh"):
				self.runProcess('./bootstrap.sh')
			elif os.path.isfile("autogen.sh"):
				self.runProcess('./autogen.sh')
			elif os.path.isfile("buildconf"):
				self.runProcess('./buildconf')
			elif os.path.isfile("bootstrap"):
				self.runProcess('./bootstrap')
			elif os.path.isfile("bootstrap"):
				self.runProcess('./bootstrap')
			elif os.path.isfile("configure.ac"):
				self.runProcess('autoreconf -fiv')

	def configureSource(self, packageName, packageData, conf_system):
		touchName = "already_configured_%s" % (self.md5(packageName, self.getKeyOrBlankString(packageData, "configure_options")))

		if not os.path.isfile(touchName):

			cpuCountStr = '-j {0}'.format(self.cpuCount)

			if 'cpu_count' in packageData:
				if isinstance(packageData['cpu_count'], int) and packageData['cpu_count'] > 0:
					cpuCountStr = '-j {0}'.format(packageData['cpu_count'])
				else:
					cpuCountStr = ""

			self.removeAlreadyFiles()
			self.removeConfigPatchDoneFiles()

			doBootStrap = True
			if 'do_not_bootstrap' in packageData:
				if packageData['do_not_bootstrap'] is True:
					doBootStrap = False

			if doBootStrap:
				if conf_system == "waf":
					if not os.path.isfile("waf"):
						if os.path.isfile("bootstrap.py"):
							self.runProcess('./bootstrap.py')
				else:
					self.bootstrapConfigure()

			configOpts = ''
			if 'configure_options' in packageData:
				try:
					configOpts = self.replaceVariables(packageData["configure_options"])
				except KeyError as e:
					self.errorExit(F'Failed to parse configure line: "{packageData["configure_options"]}", the variable {e} is unvalid.')
			self.logger.info("Configuring '{0}' with: {1}".format(packageName, configOpts), extra={'type': conf_system})

			confCmd = './configure'
			if conf_system == "waf":
				confCmd = './waf --color=yes configure'
			elif 'configure_path' in packageData:
				if packageData['configure_path'] is not None:
					confCmd = packageData['configure_path']

			self.runProcess(F'{confCmd} {configOpts}')

			if 'regex_replace' in packageData and packageData['regex_replace']:
				_pos = 'post_configure'
				if isinstance(packageData['regex_replace'], dict) and _pos in packageData['regex_replace']:
					for r in packageData['regex_replace'][_pos]:
						self.handleRegexReplace(r, packageName)

			if 'run_post_configure' in packageData:
				if packageData['run_post_configure'] is not None:
					for cmd in packageData['run_post_configure']:
						cmd = self.replaceVariables(cmd)
						self.logger.info("Running post-configure-command: '{0}'".format(cmd))
						self.runProcess(cmd)

			doClean = True
			if 'clean_post_configure' in packageData:
				if packageData['clean_post_configure'] is False:
					doClean = False

			if doClean:
				mCleanCmd = 'make clean'
				if conf_system == "waf":
					mCleanCmd = './waf --color=yes clean'
				self.runProcess('{0} {1}'.format(mCleanCmd, cpuCountStr), True)

			if 'patches_post_configure' in packageData:
				if packageData['patches_post_configure'] is not None:
					for p in packageData['patches_post_configure']:
						self.applyPatch(p[0], p[1], True)

			self.touch(touchName)

	def applyPatch(self, url, type="-p1", postConf=False, folderToPatchIn=None):
		originalFolder = os.getcwd()
		if folderToPatchIn is not None:
			self.cchdir(folderToPatchIn)
			self.logger.debug("Moving to patch folder: {0}" .format(os.getcwd()))

		self.logger.debug("Applying patch '{0}' in '{1}'" .format(url, os.getcwd()))

		patchTouchName = "patch_%s.done" % (self.md5(url))

		ignoreErr = False
		exitOn = True
		ignore = ""

		if postConf:
			patchTouchName = patchTouchName + "_past_conf"
			ignore = "-N "
			ignoreErr = True
			exitOn = False

		if os.path.isfile(patchTouchName):
			self.logger.debug("Patch '{0}' already applied".format(url))
			self.cchdir(originalFolder)
			return

		pUrl = urlparse(url)
		if pUrl.scheme != '':
			fileName = os.path.basename(pUrl.path)
			self.logger.info("Downloading patch '{0}' to: {1}".format(url, fileName))
			self.downloadFile(url, fileName)
		else:
			local_patch_path = os.path.join(self.fullPatchDir, url)
			fileName = os.path.basename(Path(local_patch_path).name)
			if os.path.isfile(local_patch_path):
				copyPath = os.path.join(os.getcwd(), fileName)
				self.logger.info("Copying patch from '{0}' to '{1}'".format(local_patch_path, copyPath))
				shutil.copyfile(local_patch_path, copyPath)
			else:
				fileName = os.path.basename(urlparse(url).path)
				url = "https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches" + url
				self.downloadFile(url, fileName)

		self.logger.info("Patching source using: '{0}'".format(fileName))
		self.runProcess('patch {2}{0} < "{1}"'.format(type, fileName, ignore), ignoreErr, exitOn)

		if not postConf:
			self.removeAlreadyFiles()

		self.touch(patchTouchName)

		if folderToPatchIn is not None:
			self.cchdir(originalFolder)
	#:

	def mesonSource(self, packageName, packageData):
		touchName = "already_ran_meson_%s" % (self.md5(packageName, self.getKeyOrBlankString(packageData, "configure_options	")))

		if not os.path.isfile(touchName):
			self.removeAlreadyFiles()

			makeOpts = ''
			if 'configure_options' in packageData:
				makeOpts = self.replaceVariables(packageData["configure_options"])
			self.logger.info("Meson'ing '{0}' with: {1}".format(packageName, makeOpts))

			self.runProcess('meson {0}'.format(makeOpts))

			if 'regex_replace' in packageData and packageData['regex_replace']:
				_pos = 'post_configure'
				if isinstance(packageData['regex_replace'], dict) and _pos in packageData['regex_replace']:
					for r in packageData['regex_replace'][_pos]:
						self.handleRegexReplace(r, packageName)

			self.touch(touchName)

	def cmakeSource(self, packageName, packageData):
		touchName = "already_ran_cmake_%s" % (self.md5(packageName, self.getKeyOrBlankString(packageData, "configure_options")))

		if not os.path.isfile(touchName):
			self.removeAlreadyFiles()

			makeOpts = ''
			if 'configure_options' in packageData:
				makeOpts = self.replaceVariables(packageData["configure_options"])
			self.logger.info("C-Making '{0}' with: {1}".format(packageName, makeOpts))

			self.runProcess('cmake {0}'.format(makeOpts))

			self.runProcess("make clean", True)

			if 'regex_replace' in packageData and packageData['regex_replace']:
				_pos = 'post_configure'
				if isinstance(packageData['regex_replace'], dict) and _pos in packageData['regex_replace']:
					for r in packageData['regex_replace'][_pos]:
						self.handleRegexReplace(r, packageName)

			self.touch(touchName)

	def buildSource(self, packageName, packageData, buildSystem):
		_origDir = os.getcwd()
		touchName = "already_ran_make_%s" % (self.md5(packageName, self.getKeyOrBlankString(packageData, "build_options")))

		if not os.path.isfile(touchName):
			cpuCountStr = '-j {0}'.format(self.cpuCount)

			if 'cpu_count' in packageData:
				if isinstance(packageData['cpu_count'], int) and packageData['cpu_count'] > 0:
					cpuCountStr = '-j {0}'.format(packageData['cpu_count'])
				else:
					cpuCountStr = ""

			mkCmd = 'make'

			if buildSystem == "waf":
				mkCmd = './waf --color=yes'
			if buildSystem == "rake":
				mkCmd = 'rake'
			if buildSystem == "ninja":
				mkCmd = 'ninja'

			if buildSystem == "make":
				if os.path.isfile("configure"):
					self.runProcess(F'{mkCmd} clean {cpuCountStr}', True)

			makeOpts = ''
			if 'build_options' in packageData:
				makeOpts = self.replaceVariables(packageData["build_options"])

			if self.debugMode:
				print("### Environment variables:  ###")
				for tk in os.environ:
					print("\t" + tk + " : " + os.environ[tk])
				print("##############################")

			self.logger.info(F"Building '{packageName}' with: {makeOpts} in {os.getcwd()}", extra={'type': buildSystem})

			if 'ignore_build_fail_and_run' in packageData:
				if len(packageData['ignore_build_fail_and_run']) > 0:  # todo check if its a list too
					try:
						if buildSystem == "waf":
							mkCmd = './waf --color=yes build'
						self.runProcess(F'{mkCmd} {cpuCountStr} {makeOpts}')
					except Exception:  # todo, except specific exception
						self.logger.info("Ignoring failed make process...")
						for cmd in packageData['ignore_build_fail_and_run']:
							cmd = self.replaceVariables(cmd)
							self.logger.info(F"Running post-failed-make-command: '{cmd}'")
							self.runProcess(cmd)
			else:
				if buildSystem == "waf":
					mkCmd = './waf --color=yes build'
				self.runProcess(F'{mkCmd} {cpuCountStr} {makeOpts}')

			if 'regex_replace' in packageData and packageData['regex_replace']:
				_pos = 'post_build'
				if isinstance(packageData['regex_replace'], dict) and _pos in packageData['regex_replace']:
					for r in packageData['regex_replace'][_pos]:
						self.handleRegexReplace(r, packageName)

			if 'run_post_build' in packageData:
				if packageData['run_post_build'] is not None:
					for cmd in packageData['run_post_build']:
						if cmd.startswith("!SWITCHDIRBACK"):
							self.cchdir(_origDir)
						elif cmd.startswith("!SWITCHDIR"):
							_dir = self.replaceVariables("|".join(cmd.split("|")[1:]))
							self.cchdir(_dir)
						else:
							cmd = self.replaceVariables(cmd)
							self.logger.info("Running post-build-command: '{0}'".format(cmd))
							self.runProcess(cmd)

			self.touch(touchName)

	def installSource(self, packageName, packageData, buildSystem):
		_origDir = os.getcwd()
		touchName = "already_ran_install_%s" % (self.md5(packageName, self.getKeyOrBlankString(packageData, "install_options")))
		if not os.path.isfile(touchName):
			cpuCountStr = '-j {0}'.format(self.cpuCount)

			if 'cpu_count' in packageData:
				if isinstance(packageData['cpu_count'], int) and packageData['cpu_count'] > 0:
					cpuCountStr = '-j {0}'.format(packageData['cpu_count'])
				else:
					cpuCountStr = ""

			makeInstallOpts = ''
			if 'install_options' in packageData:
				if packageData['install_options'] is not None:
					makeInstallOpts = self.replaceVariables(packageData["install_options"])
			installTarget = "install"
			if 'install_target' in packageData:
				if packageData['install_target'] is not None:
					installTarget = packageData['install_target']

			self.logger.info("Installing '{0}' with: {1}".format(packageName, makeInstallOpts), extra={'type': buildSystem})

			mkCmd = "make"
			if buildSystem == "waf":
				mkCmd = "./waf"
			if buildSystem == "rake":
				mkCmd = "rake"
			if buildSystem == "ninja":
				mkCmd = "ninja"

			self.runProcess(F'{mkCmd} {installTarget} {makeInstallOpts} {cpuCountStr}')

			if 'regex_replace' in packageData and packageData['regex_replace']:
				_pos = 'post_install'
				if isinstance(packageData['regex_replace'], dict) and _pos in packageData['regex_replace']:
					for r in packageData['regex_replace'][_pos]:
						self.handleRegexReplace(r, packageName)

			if 'run_post_install' in packageData:
				if packageData['run_post_install'] is not None:
					for cmd in packageData['run_post_install']:
						if cmd.startswith("!SWITCHDIRBACK"):
							self.cchdir(_origDir)
						elif cmd.startswith("!SWITCHDIR"):
							_dir = self.replaceVariables("|".join(cmd.split("|")[1:]))
							self.cchdir(_dir)
						else:
							cmd = self.replaceVariables(cmd)
							self.logger.info("Running post-install-command: '{0}'".format(cmd))
							self.runProcess(cmd)

			self.touch(touchName)
	#:

	def resetDefaultEnvVars(self):
		self.logger.debug("Reset CFLAGS/CXXFLAGS to: {0}".format(self.originalCflags))
		os.environ["CFLAGS"] = self.originalCflags
		os.environ["CXXFLAGS"] = self.originalCflags
		os.environ["PKG_CONFIG_LIBDIR"] = ""
		os.environ["PATH"] = "{0}:{1}".format(self.mingwBinpath, self.originalPATH)
		os.environ["PKG_CONFIG_PATH"] = self.pkgConfigPath
	#:

	def anyFileStartsWith(self, wild):
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

	def generateCflagString(self, prefix=""):
		if "CFLAGS" not in os.environ:
			return ""
		cfs = os.environ["CFLAGS"]
		cfs = cfs.split(' ')
		if (len(cfs) == 1 and cfs[0] != "") or not len(cfs):
			return ""
		out = ''
		if len(cfs) >= 1:
			for c in cfs:
				out += prefix + c + ' '
			out.rstrip(' ')
			return out
		return ''

	def replaceToolChainVars(self, inStr):
		return inStr.format_map(self.formatDict)

	def replaceVariables(self, inStr):
		rawInStr = inStr
		varList = re.findall(r"!VAR\((?P<variable_name>[^\)\(]+)\)VAR!", inStr)  # TODO: assignment expression
		if varList:
			for varName in varList:
				if varName in self.packages["vars"]:
					variableContent = self.packages["vars"][varName]
					inStr = re.sub(rf"(!VAR\({varName}\)VAR!)", r"{0}".format(variableContent), inStr, flags=re.DOTALL)
				else:
					inStr = re.sub(rf"(!VAR\({varName}\)VAR!)", r"".format(variableContent), inStr, flags=re.DOTALL)
					self.logger.warn(F"Unknown variable has been used: '{varName}'\n in: '{rawInStr}', it has been stripped.")

		inStr = self.replaceToolChainVars(inStr)

		cmdList = re.findall(r"!CMD\((?P<full_cmd>[^\)\(]+)\)CMD!", inStr)  # TODO: assignment expression TODO: handle escaped brackets inside cmd syntax
		if cmdList:
			for cmd in cmdList:
				cmdReplacer = subprocess.check_output(cmd, shell=True).decode("utf-8").replace("\n", "").replace("\r", "").strip()
				inStr = re.sub(r"!CMD\(([^\)\(]+)\)CMD!", F"{cmdReplacer}", inStr, flags=re.DOTALL)
		return inStr
	#:

	def getValueOrNone(self, db, k):
		if k in db:
			if db[k] is None:
				return None
			else:
				return db[k]
		else:
			return None

	def getValueByIntOrNone(self, db, key):
		if key >= 0 and key < len(db):
			return db[key]
		else:
			return None

	def reReplaceInFile(self, infile, oldString, newString, outfile):
		with open(infile, 'rw') as f:
			for line in f:
				line = re.sub(oldString, newString, line)

	def getKeyOrBlankString(self, db, k):
		if k in db:
			if db[k] is None:
				return ""
			else:
				return db[k]
		else:
			return ""
	#:

	def cchdir(self, dir):
		if self.debugMode:
			print(F"Changing dir from {os.getcwd()} to {dir}")
		os.chdir(dir)


if __name__ == "__main__":
	PY_REQUIRE = (3, 6)
	if sys.version_info < PY_REQUIRE:
		sys.exit("You need at least Python %s.%s or later for this script.\n" % PY_REQUIRE)
	main = CrossCompileScript()
	main.commandLineEntrace()
