#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ####################################################
# Copyright (C) 2018-2019 DeadSix27 (https://github.com/DeadSix27/python_cross_compile_script)
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

# pip modules
import progressbar # Please run: pip3 install progressbar2
import requests # Please run: pip3 install requests


# standard modules
import os,os.path,tarfile,io,shutil,re,subprocess,sys,hashlib,time,urllib
from multiprocessing import cpu_count
from collections import OrderedDict

_WORKDIR	     = "toolchain"
_CPU_COUNT	     = cpu_count()
_NO_CONFIG_GUESS = True # Instead of downloading config.guess we use gcc -dumpmachine, this obviously only works when gcc is installed, but we need it to be installed anyway.
_DEBUG           = False
_VERSION         = "4.3"

SOURCES = OrderedDict() # Order matters.

SOURCES['mingw-w64'] = {
	'type' : 'git',
	'url' : 'https://git.code.sf.net/p/mingw-w64/mingw-w64', # mirror: https://github.com/mirror/mingw-w64.git but that seems suprisingly out of date sometimes.
	'run_after_patches' : [
		( 'autoreconf -fiv', ),
		( 'mingw-w64-crt'  , 'autoreconf -fiv' ),
	],
	'builds' : [
		'mingw-w64-crt',
		'mingw-w64-headers',
		'mingw-w64-gendef',
		'mingw-w64-winpthreads',
		#'mingw-w64-widl', # Still won't compile, 'mingw-w64-tools/widl/src/widl.c:172:28: error: array type has incomplete element type ‘struct option’'
	]
}
SOURCES['gmp'] = {
	'type' : 'archive',
	'version'   : '6.1.2',
	'url' : 'https://ftp.gnu.org/gnu/gmp/gmp-{version}.tar.xz',
	'update_check' : { 'url' : 'https://ftp.gnu.org/gnu/gmp/', 'type' : 'httpindex', 'regex' : r'gmp-(?P<version_num>[\d.]+)\.tar\.xz' },
}
SOURCES['mpfr'] = {
	'type' : 'archive',
	'version'   : '4.0.2',
	'url' : 'https://ftp.gnu.org/gnu/mpfr/mpfr-{version}.tar.xz',
	'update_check' : { 'url' : 'https://ftp.gnu.org/gnu/mpfr/', 'type' : 'httpindex', 'regex' : r'mpfr-(?P<version_num>[\d.]+)\.tar\.xz' },
}
SOURCES['mpc'] = {
	'type' : 'archive',
	'version'   : '1.1.0',
	'url' : 'https://ftp.gnu.org/gnu/mpc/mpc-{version}.tar.gz',
	'update_check' : { 'url' : 'https://ftp.gnu.org/gnu/mpc/', 'type' : 'httpindex', 'regex' : r'mpc-(?P<version_num>[\d.]+)\.tar\.gz' },
}
SOURCES['isl'] = {
	'type' : 'archive',
	'version'   : '0.18',
	'url' : 'https://gcc.gnu.org/pub/gcc/infrastructure/isl-{version}.tar.bz2',
	'update_check' : { 'url' : 'https://gcc.gnu.org/pub/gcc/infrastructure/', 'type' : 'httpindex', 'regex' : r'isl-(?P<version_num>[\d.]+)\.tar\.bz2' },
}
SOURCES['binutils'] = {
	'type' : 'archive',
	'version'   : '2.33.1',
	# 'patches' : [
		# ( 'https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/mingw_toolchain_script/patches/0001-binutils-remove_provide_qualifiers_from_ctor_and_dtor_list.patch' , 'p1' ),
	# ],
	'url' : 'https://ftp.gnu.org/gnu/binutils/binutils-{version}.tar.bz2',
	'softlink_to_package' : [
		( 'isl'  , 'isl' ),
		( 'gmp'  , 'gmp' ),
	],
	'update_check' : { 'url' : 'https://ftp.gnu.org/gnu/binutils/', 'type' : 'httpindex', 'regex' : r'binutils-(?P<version_num>[\d.]+)\.tar\.bz2' },
}
SOURCES['gcc'] = {
	'type' : 'archive',
	'version'   : '9.2.0',
	# 'url' : 'https://gcc.gnu.org/pub/gcc/releases/gcc-{version}/gcc-{version}.tar.xz',
	'url' : 'ftp://ftp.fu-berlin.de/unix/languages/gcc/snapshots/9-20191012/gcc-9-20191012.tar.xz',
	'patches' : [
		#( 'https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/mingw_toolchain_script/patches/0001-gcc_7_1_0_weak_refs_x86_64.patch', 'p1' ),
		#( 'https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/mingw_toolchain_script/patches/0140-gcc-7-Enable-std-experimental-filesystem.patch', 'p1' ), #Unable to get this to work.
	],
	'softlink_to_package' : [
		('gmp'  , 'gmp' ),
		('mpfr' , 'mpfr'),
		('mpc'  , 'mpc' ),
		('isl'  , 'isl' ),
	],
	'builds' : [
		'gcc-1',
		'gcc-2',
	],
	'update_check' : { 'url' : 'https://gcc.gnu.org/pub/gcc/releases/', 'type' : 'httpindex', 'regex' : r'gcc-(?P<version_num>[\d.]+)' },
}


BUILDS = OrderedDict()

BUILDS['binutils'] = {
	'lineConfig' :
		'configure '
		' --prefix="{prefix}"'
		' --build="{host}"'
		' --disable-shared'
		' --enable-static'
		' --with-sysroot={prefix}'
		' --target="{target}"'
		' --disable-multilib'
		' --disable-nls'
		#' --disable-win32-registry'
		#' --without-included-gettext'
		' --enable-plugins'
		' --enable-threads'
		' --enable-lto'
	,
}
BUILDS['mingw-w64-headers'] = {
	'lineConfig' :
		'mingw-w64-headers/configure'
		' --build="{host}"'
		' --host="{target}"'
		' --prefix="{prefix}"'
		' --enable-secure-api'
		' --enable-idl'
		' --enable-sdk=all'
		' --enable-idl'
		#' --with-default-win32-winnt=0x600'
	,
	'softLinks' : [
		( '{prefix}', './{target}', './mingw' ),
		( '{prefix}/{target}', '../include', './include' ),
	],
	'lineInstall' : 'install-strip',
}
BUILDS['gcc-1'] = {
	'lineConfig' :
		'configure '
		' --build="{host}"'
		' --prefix="{prefix}"'
		' --target="{target}"'
		' --disable-shared'
		' --enable-static'
		' --disable-multilib'
		' --disable-win32-registry'
		' --enable-languages=c,c++'
		' --disable-nls'
		' --enable-libstdcxx-time=yes'
		' --enable-threads=posix'
		' --enable-fully-dynamic-string'
		#' --without-included-gettext'
		' --enable-lto'
	,
	'lineMake'	: 'all-gcc',
	'lineInstall' : 'install-strip-gcc',
}
BUILDS['mingw-w64-crt'] = {
	'lineConfig' :
		'mingw-w64-crt/configure'
		' --build="{host}"'
		' --host="{target}"'
		' --prefix="{prefix}"'
		' --target="{target}"'
		' --with-sysroot={prefix}'
	,
	'customCommands' : [
		( '{prefix}', 'mv "./{target}/lib/"* "./lib/"', True ),
		( '{prefix}', 'rm -fr "./{target}/lib"', True ),
		( '{prefix}/{target}', 'ln -s "../lib" "./lib"', True ),
	],
	'lineInstall' : 'install-strip',
}

BUILDS['mingw-w64-winpthreads'] = {
	'lineConfig' :
		'mingw-w64-libraries/winpthreads/configure'
		' --build="{host}"'
		' --host="{target}"'
		' --disable-shared'
		' --enable-static'
		' --prefix="{prefix}"'
	,
	'lineInstall' : 'install-strip',
	'cpu_count' : 1,
}

BUILDS['gcc-2'] = {
	'lineConfig' : 'dummy',
	'noConfigure' : True,
	'lineInstall' : 'install-strip',

}
BUILDS['mingw-w64-gendef'] = {
	'lineConfig' :
		'mingw-w64-tools/gendef/configure'
		' --build="{host}"'
		' --prefix="{prefix}"'
		' --target="{target}"'
	,
	'lineInstall' : 'install-strip',
	'customCommands' : [
		( '{prefix}', 'cp -f "./bin/gendef" "./bin/{target}-gendef"' ),
	],
}
# BUILDS['mingw-w64-widl'] = { # See line 49
# 	'lineConfig' :
# 		'mingw-w64-tools/widl/configure'
# 		' --build="{host}"'
# 		' --prefix="{prefix}"'
# 		' --target="{target}"'
# 	,
# }

BUILDS['gmp'] = {
	'dummy' : True,
}
BUILDS['mpfr'] = {
	'dummy' : True,
}
BUILDS['mpc'] = {
	'dummy' : True,
}
BUILDS['isl'] = {
	'dummy' : True,
}

class Event:
	def __init__(self):
		self.handlers = set()

	def any(self):
		if len(self.handlers) > 0:
			return True
		else:
			return False

	def handle(self, handler):
		self.handlers.add(handler)
		return self

	def unhandle(self, handler):
		try:
			self.handlers.remove(handler)
		except:
			raise ValueError("Handler is not handling this event, so cannot unhandle it.")
		return self

	def fire(self, *args, **kargs):
		for handler in self.handlers:
			handler(*args, **kargs)

	def getHandlerCount(self):
		return len(self.handlers)

	__iadd__ = handle
	__isub__ = unhandle
	__call__ = fire
	__len__  = getHandlerCount

class MinGW64ToolChainBuilder:

	def __init__(self):
		sys.dont_write_bytecode = True # Avoid __pycache__ folder, never liked that solution.
		self.pathOrig = os.environ["PATH"]
		self.workDir = _WORKDIR
		self.nativeHost = ""
		self.cwd = os.getcwd()
		self.debugBuild = False
		self.customCflags = None
		self.targetHost = "x86_64-w64-mingw32"
		self.targetPrefix = os.path.join(self.cwd,self.workDir,self.targetHost)
		self.targetPrefixBin = os.path.join(self.targetPrefix,"bin")
		self.quietMode = False
		self.sourceDir  = os.path.join(self.cwd,self.workDir,"src")
		self.buildDir  = os.path.join(self.cwd,self.workDir,"bld")
		self.logFile = None
		self.onStatusUpdate = Event()
		
		self.log("Running Python3 MinGW Build Script v" + _VERSION)

	#:
	def log(self,msg,type = None):
		if self.onStatusUpdate.any():
			if type == "debug":
				if _DEBUG == True:
					self.onStatusUpdate("[TOOLCHAIN] " + msg)
			else:
				self.onStatusUpdate("[TOOLCHAIN] " + msg)
		else:
			print(msg)

	def extractFile(self,filename):
		def on_progress(filename, position, total_size, pb):
			pass
		def get_file_progress_file_object_class(on_progress,pb):
			class FileProgressFileObject(tarfile.ExFileObject):
				def read(self, size, *args):
				  on_progress(self.name, self.position, self.size, pb)
				  return tarfile.ExFileObject.read(self, size, *args)
			return FileProgressFileObject

		class ProgressFileObject(io.FileIO):
			def __init__(self, path, pb, *args, **kwargs):
				self.pb = pb
				self._total_size = os.path.getsize(path)
				io.FileIO.__init__(self, path, *args, **kwargs)

			def read(self, size):
				self.pb.update(self.tell())
				return io.FileIO.read(self, size)
		#:
		terms = shutil.get_terminal_size((100,100))
		# filler = 0
		# if terms[0] > 100:
		# 	filler = int(terms[0]/4)
		widgets = [
			progressbar.FormatCustomText("Extracting : {:25.25}".format(os.path.basename(filename)))," ",
			progressbar.Percentage(), " ",
			progressbar.Bar(fill=chr(9617), marker=chr(9608), left="[", right="]"), " ",
			progressbar.DataSize(), "/", progressbar.DataSize(variable="max_value"),
			# " "*filler,
		]

		pbar = progressbar.ProgressBar(widgets=widgets,maxval=os.path.getsize(filename))
		pbar.start()
		tarfile.TarFile.fileobject = get_file_progress_file_object_class(on_progress,pbar)
		tar = tarfile.open(fileobj=ProgressFileObject(filename,pbar), mode="r:*")
		outputPath = os.path.commonprefix(tar.getnames())
		if os.path.isfile(outputPath):
			return outputPath
			tar.close()
			pbar.finish()
		else:
			tar.extractall()
			tar.close()
			pbar.finish()
			return outputPath
	#:
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
		userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0"

		if 'sourceforge.net' in url.lower():
			userAgent = 'wget/1.18' # sourceforce <3 wget

		if url.lower().startswith("ftp://"):
			self.log("Requesting : {0}".format(url))
			if outputFileName != None:
				fileName = outputFileName
			fullOutputPath = os.path.join(outputPath,fileName)
			urllib.request.urlretrieve(url, fullOutputPath)
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

		self.log("Requesting : {0} - {1}".format(url, fmt_size(size) if size!=None else "?" ))

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
				if not nextline.decode('utf-8').startswith('A	'):
					if self.quietMode == True:
						self.logFile.write(nextline.decode('utf-8','replace'))
					else:
						sys.stdout.write(nextline.decode('utf-8','replace'))
						sys.stdout.flush()
			else:
				if self.quietMode == True:
					self.logFile.write(nextline.decode('utf-8','replace'))
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
			self.log("Error [{0}] running process: '{1}' in '{2}'".format(return_code,command,os.getcwd()))
			self.log("You can try deleting the product/dependency folder: '{0}' and re-run the script".format(os.getcwd()))
			if exitOnError:
				exit(1)
	#:
	def gitClone(self,url,virtFolderName=None,renameTo=None,desiredBranch=None,recursive=False,shallow=False):
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

			LOCAL	= subprocess.check_output('git rev-parse @',shell=True).decode("utf-8")
			REMOTE   = subprocess.check_output('git rev-parse "{0}"'.format(UPSTREAM),shell=True).decode("utf-8")
			BASE	 = subprocess.check_output('git merge-base @ "{0}"'.format(UPSTREAM),shell=True).decode("utf-8")

			self.run_process('git checkout -f')
			self.run_process('git checkout {0}'.format(properBranchString))

			if LOCAL == BASE:
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
			self.cchdir("..")
		else:
			self.run_process('git clone{0}{1} --progress "{2}" "{3}"'.format
				(
					" --recursive" if recursive == True else "",
					" --depth 1" if shallow == True else "",
					url,
					realFolderName + ".tmp" )
				)
			if desiredBranch != None:
				self.cchdir(realFolderName + ".tmp")
				self.run_process('git checkout{0}'.format(" master" if desiredBranch == None else branchString))
				self.cchdir("..")
			self.run_process('mv "{0}" "{1}"'.format(realFolderName + ".tmp", realFolderName))

		return realFolderName
	#:
	def getConfigGuess(self):
		if _NO_CONFIG_GUESS == True:
			return subprocess.check_output("gcc -dumpmachine", shell=True).decode("utf-8").strip()
		else:
			return subprocess.check_output("wget -qO - 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD' | sh", shell=True).decode("utf-8").strip()
	#:
	def cchdir(self,dir):
		if _DEBUG:
			self.log("Changing dir from {0} to {1}".format(os.getcwd(),dir))
		os.chdir(dir)
	#:
	def createWorkDirs(self):
		if not os.path.isdir(self.workDir):
			os.makedirs(self.workDir)

		if not os.path.isdir(self.sourceDir):
			os.makedirs(self.sourceDir)

		if not os.path.isdir(self.buildDir):
			os.makedirs(self.buildDir)
	#:
	def applyPatch(self,url,p):
		patchBn = os.path.basename(url)
		return subprocess.check_output("wget '{0}' && git apply -v {1}".format(url,patchBn), shell=True, stderr=subprocess.STDOUT).decode("utf-8")
	#:
	def sanitize_filename(self,f):
		return re.sub(r'[/\\:*?"<>|]', '', f)
	#:
	def splitext(self,path):
		for ext in ['.tar.gz', '.tar.bz2', '.tar.xz']:
			if path.endswith(ext):
				return path[:-len(ext)], path[-len(ext):]
		return os.path.splitext(path)

	def downloadSources(self):
		origDir = os.getcwd()
		self.cchdir(self.sourceDir)
		baseDir = os.getcwd()

		for pn, p in SOURCES.items():
			pUrl = ""
			fileName = ""
			productPath = ""
			shallowClone = False
			if "type" in p:
				if p["type"] == "git":
					pUrl = p["url"]
					branch = None
					if "checkout" in p:
						branch = p["checkout"]
					if "git_shallow" in p:
						if p["git_shallow"] == True:
							shallowClone = True
					self.log("Cloning git repo '%s' from '%s'" % (pn,pUrl))
					productPath = self.gitClone(pUrl,desiredBranch=branch,shallow=shallowClone)

				elif p["type"] == "archive":
					pUrl = p["url"].format(version=p["version"])
					fileName = os.path.basename(pUrl)
					folderName = self.splitext(fileName)[0]
					if not os.path.isfile(fileName) and not os.path.isdir(folderName):
						self.log("Downloading sources for: %s" % pn)
						self.download_file(pUrl)
						self.log("Extracting sources for: %s" % pn)
						productPath = self.extractFile(fileName)
						os.unlink(fileName)
					else:
						productPath = folderName
				else:
					raise Exception("Missing type")

			if "patches" in p and len(p["patches"]) >= 1:
				
				self.cchdir(productPath)
				
				for patchTuple in p['patches']:
					patchBn = os.path.basename(patchTuple[0])
					self.log( "Patching " + str(pn) + " with: " + str(patchTuple[0]) )
					if not os.path.isfile(os.path.basename(patchTuple[0])):
						result = self.applyPatch(patchTuple[0],patchTuple[1])
						if _DEBUG:
							self.log(result)
						self.logFile.write(result)
				
				self.cchdir(baseDir)
				
			if 'run_after_patches' in p and len(p['run_after_patches']) >= 1:
				
				self.cchdir(productPath)
				
				for cmd in p['run_after_patches']:
					pathBefore = os.getcwd()
					if len(cmd) > 1:
						self.cchdir(cmd[0])
						os.system(cmd[1])
						self.cchdir(pathBefore)
					else:
						os.system(cmd[0])
						
						
				self.cchdir(baseDir)
				
			if "softlink_to_package" in p:
				self.cchdir(productPath)
				for sl in p["softlink_to_package"]:
					if not os.path.isdir(sl[1]):
						try:
							os.symlink(SOURCES[sl[0]]["sourceFolder"],sl[1])
						except Exception as e:
							self.log(str(e) + " ["+SOURCES[sl[0]]["sourceFolder"] + " -> " + sl[1] + " in: " + productPath + "]")
							exit()
				self.cchdir(baseDir)			
			SOURCES[pn]["sourceFolder"] = os.path.join( self.sourceDir, productPath )
			SOURCES[pn]["buildFolder"]  = os.path.join( self.buildDir,  productPath )
			if "builds" in p:
				for b in p["builds"]:
					if b in BUILDS:
						BUILDS[b]["sourceFolder"] = os.path.join( self.sourceDir, productPath )
						BUILDS[b]["buildFolder"]  = os.path.join( self.buildDir,  productPath )
			else:
				if pn in BUILDS:
					BUILDS[pn]["sourceFolder"] = os.path.join( self.sourceDir, productPath )
					BUILDS[pn]["buildFolder"]  = os.path.join( self.buildDir,  productPath )
		
		self.cchdir(origDir)
	#:
	def getSafePath(self,b,name):
		if "sourceFolder" in b[name]:
			return b[name]["sourceFolder"]
		else:
			return None
	def dictGetSafeString(self,d,k,default = ""):
		if k in d:
			return d[k]
		else:
			return default

	def md5(self,str):
		return hashlib.md5(str.encode("utf-8")).hexdigest()

	def createAlreadyFile(self,fname, data):
		with open(fname, 'w+') as f:
			f.write(data)

	def buildSources(self):
	
		def formatProgVars(inpFormat):
			return inpFormat.format(
				prefix=self.targetPrefix,
				target=self.targetHost,
				host=self.nativeHost,
				mpfr_path=self.getSafePath(BUILDS,"mpfr"),
				isl_path=self.getSafePath(BUILDS,"isl"),
				mpc_path=self.getSafePath(BUILDS,"mpc"),
				gmp_path=self.getSafePath(BUILDS,"gmp"),
			)
		os.environ["PATH"] = "{0}:{1}".format(self.targetPrefixBin,self.pathOrig)
		
		origDir = os.getcwd()
		self.cchdir(self.sourceDir)
		baseDir = os.getcwd()

		for pn, p in BUILDS.items():
			if "dummy" in p:
				continue
			if "sourceFolder" not in p:
				raise Exception("Source for %s is missing" % pn)
				exit()
			baseFolder = os.getcwd()
			pSourceFolder = p["sourceFolder"]
			pBuildFolder  = p["buildFolder"]
			if not os.path.isdir(pBuildFolder):
				os.makedirs(pBuildFolder)

			self.cchdir(pBuildFolder)

			confOpts = formatProgVars(p["lineConfig"])

			confOptsHash = "already_built_" + pn + "_" + self.md5(confOpts)
			cpuCount = _CPU_COUNT
			if "cpu_count" in p:
				cpuCount = p["cpu_count"]
			
			if self.customCflags != None:
				if _DEBUG:
					self.log("Setting custom C(XX)FLAGS to: " + self.customCflags)
				os.environ["CFLAGS"] = self.customCflags
				os.environ["CXXFLAGS"] = self.customCflags
			else:
				if self.debugBuild:
					if _DEBUG:
						self.log("Setting C(XX)FLAGS to: -ggdb -O0")
					os.environ["CFLAGS"] = "-ggdb -O0"
					os.environ["CXXFLAGS"] = "-ggdb -O0"
				else:
					if _DEBUG:
						self.log("Setting C(XX)FLAGS to: -O3")
					os.environ["CFLAGS"] = "-O3"
					os.environ["CXXFLAGS"] = "-O3"
				
			if not os.path.isfile(confOptsHash):
				self.log("Building: %s" % pn)
				noConfig = False
				if "noConfigure" in p:
					if p["noConfigure"] == True:
						noConfig = True
				if not noConfig:
					self.log("Configuring '%s' with: <%s/%s> in <%s>" % (pn,pSourceFolder, confOpts, os.getcwd()))
					self.run_process("%s/%s" % (pSourceFolder.rstrip("/"), confOpts))#configure

				if "debug_exit_after_config" in p:
					if p["debug_exit_after_config"] == True:
						exit()

				noMake = False
				if "noMake" in p:
					if p["noMake"] == True:
						noMake = True
				if not noMake:
					makeOpt = self.dictGetSafeString(p,"lineMake")
					self.log("Making '%s' with: <%s> in <%s>" % (pn,"make %s -j%d V=1" % (makeOpt,cpuCount), os.getcwd()))
					self.run_process("make %s -j%d V=1" % (makeOpt,cpuCount))

				if "debug_exit_after_make" in p:
					if p["debug_exit_after_make"] == True:
						exit()
				noInstall = False
				if "noInstall" in p:
					if p["noInstall"] == True:
						noInstall = True
				if not noInstall:
					isntOpt = self.dictGetSafeString(p,"lineInstall", "install")
					self.log("Installing '%s' with: <%s> in <%s>" % (pn,"make %s -j%d V=1" % (isntOpt,cpuCount), os.getcwd()))
					self.run_process("make %s -j%d V=1" % (isntOpt,cpuCount))

				if "softLinks" in p:
					for sl in p["softLinks"]:
						pathBefore = os.getcwd()
						linkContainerPath = formatProgVars(sl[0])
						linkTarget		= formatProgVars(sl[1])
						linkName		  = formatProgVars(sl[2])
						self.cchdir(linkContainerPath)
						if not os.path.isdir(linkName):
							os.symlink(linkTarget,linkName)
						self.cchdir(pathBefore)
				#:
				if "customCommands" in p:
					for cc in p["customCommands"]:
						pathBefore = os.getcwd()
						pathFormatted = formatProgVars(cc[0])
						self.cchdir(pathFormatted)
						cmd = formatProgVars(cc[1])
						self.log("Running customCommands: '{0}'".format( cmd ))
						ignoreFail = False
						if len(cc) >= 3:
							if cc[2] == True:
								ignoreFail = True
						self.run_process(cmd, ignoreErrors=ignoreFail)
						self.cchdir(pathBefore)
				#:

				self.createAlreadyFile(confOptsHash,confOpts)
				
			else:
				self.log("ALREADY BUILT: " + pn)
			#:
			if "debug_exit_after_install" in p:
				if p["debug_exit_after_install"] == True:
					exit()
				#:
			#:
			self.cchdir(baseFolder)
		#:
		self.cchdir(origDir)
	#:
	def setCustomCflags(self,flags):
		self.customCflags = flags
		self.log("MinGW custom C(XX)FLAGS: " + self.customCflags)
		
	def setMinGWcheckout(self,hash):
		if hash != "":
			SOURCES['mingw-w64']['checkout'] = hash
			self.log("Set MinGW checkout to: " + hash)
			
	def setDebugBuild(self,switch):
		self.debugBuild = switch
		self.log("MinGW debug build: " + ("On" if self.debugBuild == True else "Off"))
	#:
	def build(self):
		self.nativeHost = self.getConfigGuess()
		self.createWorkDirs()
		self.logFile = open(os.path.join(self.cwd,self.workDir,"build.log"),"w")
		self.downloadSources()
		self.buildSources()
		
		self.log("Deleting {}/{}".format(os.getcwd(), self.sourceDir))
		shutil.rmtree(self.sourceDir)
		self.log("Deleting {}/{}".format(os.getcwd(), self.buildDir))
		shutil.rmtree(self.buildDir)
		
		self.logFile.close()
		self.log("DONE!")
	#:

if __name__ == "__main__":
   test = MinGW64ToolChainBuilder()
   test.build()
