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
_VERSION = "1.1"

class Colors: # improperly named ansi colors.
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

_CPU_COUNT = cpu_count()
_MINGW_SCRIPT_URL = "https://raw.githubusercontent.com/DeadSix27/modular_cross_compile_script/master/mingw-build-script.sh"
_LOGFORMAT = '[%(asctime)s][%(levelname)s] %(message)s' + Colors.RESET
_LOG_DATEFORMAT = '%H:%M:%S'
_QUIET = False #not recommended, but sure looks nice...
_WORKDIR = "workdir"
_MINGW_DIR = "xcompilers"
_BITNESS = ( 64, )
_DOWNLOADER = "wget" # wget or curl
git_get_latest = True # to be implemented in a better way

PRODUCTS = { # e.g mpv, ffmpeg
	'ffmpeg' : {
		'repo_type' : 'git', # git, svn, archive
		'branch' : '0.13.6', # git branch/tag or svn whatever -r stood for
		'url' : 'https://git.ffmpeg.org/ffmpeg.git',
		'folder_name': None, # Required for SVN repos, weird git onee and borked direct file downloads I guess. 
		'configure_options': '--host={compile_target} --prefix={compile_prefix} --disable-shared --enable-static',
		'depends_on' : ( "zlib", "bzlib2", 'liblzma', 'libzimg' ) # order them correctly, if one needs yet another dep. you put that one first.
	}
}
DEPENDS = { # e.g flac, libpng
	'libdlfcn' : {
		'repo_type' : 'git',
		'branch' : '0.13.6',
		'url' : 'https://github.com/dlfcn-win32/dlfcn-win32.git',
		'folder_name': None,
		'configure_options': '--cross-prefix={cross_prefix} --prefix={compile_prefix} --disable-shared --enable-static',
	},
	'bzlib2' : { # simple name for the library
		'repo_type' : 'archive', # git, svn, archive
		'branch' : None, # git/svn branch/tag [Optional, set None or remove]
		'url' : 'https://fossies.org/linux/misc/bzip2-1.0.6.tar.gz', # https,http,file:// (ftp not yet supported, I think)
		'folder_name': None, # [Optional, set None or remove]
		'patches' : ( # ordered list of patches, first one will be applied first..
			('https://raw.githubusercontent.com/rdp/ffmpeg-windows-build-helpers/master/patches/bzip2_cross_compile.diff', "p0"),
		),
		'configure_options': '--static --prefix={compile_prefix}',
		'make_options': '{make_prefix_options} libbz2.a bzip2 bzip2recover', # self.makePrefixOptions
	},
	'zlib' : {
		'repo_type' : 'archive',
		'url' : 'https://sourceforge.net/projects/libpng/files/zlib/1.2.11/zlib-1.2.11.tar.gz',
		'folder_name': None,
		'configure_options': '--static --prefix={compile_prefix}',
		'make_options': '{make_prefix_options} ARFLAGS=rcs', # self.makePrefixOptions
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
		self.targetBitness     = _BITNESS
		self.originalPATH      = os.environ["PATH"]
		
		#init some stuff.
		self.compileTarget     = None
		self.compilePrefix     = None
		self.mingwBinpath      = None
		self.crossPrefix       = None
		self.makePrefixOptions = None
		self.bitnessDir        = None
		self.winBitnessDir     = None
		
		#main starting point
		for b in self.targetBitness:		
		
			if not os.path.isdir(_WORKDIR):
				self.logger.info("Creating workdir: %s" % (_WORKDIR))
				os.makedirs(_WORKDIR, exist_ok=True)
			os.chdir(_WORKDIR)
		
			self.bitnessDir        = "x86_64" if b is 64 else "i686"
			self.winBitnessDir     = "win64" if b is 64 else "win32"
			self.compileTarget     = "{0}-w64-mingw32".format ( self.bitnessDir )
			self.compilePrefix     = "{0}/{1}/mingw-w64-{2}/{3}".format( self.fullWorkDir, _MINGW_DIR, self.bitnessDir, self.compileTarget )
			self.mingwBinpath      = "{0}/{1}/mingw-w64-{2}/bin".format( self.fullWorkDir, _MINGW_DIR, self.bitnessDir )
			self.crossPrefix       = "{0}/{1}-w64-mingw32-".format( self.mingwBinpath, self.bitnessDir )
			self.makePrefixOptions = "CC={0}gcc AR={0}ar PREFIX={1} RANLIB={0}ranlib LD={0}ld STRIP={0}strip CXX={0}g++".format( self.crossPrefix, self.compilePrefix )
			
			self.build_mingw(b)
			self.initProcess(b) # the passing is actually unessesary but looks better. 
		
			os.chdir("..")
		
	#:

	def initProcess(self,bitness):
		
		os.environ["PATH"]           = "{0}:{1}".format ( self.mingwBinpath, self.originalPATH )
		os.environ["KG_CONFIG_PATH"] = "{0}/lib/pkgconfig".format( self.compileTarget )
		
		if not os.path.isdir(self.bitnessDir):
			self.logger.info("Creating bitdir: {0}".format( self.bitnessDir ))
			os.makedirs(self.bitnessDir, exist_ok=True)
			
		os.chdir(self.bitnessDir)

		for p, pi in PRODUCTS.items():
			self.build_product(p,pi)
			
		os.chdir("..")
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
		mingw_script_options = "--clean-build --disable-shared --default-configure  --pthreads-w32-ver=2-9-1 --cpu-count={0} --mingw-w64-ver=git --gcc-ver=6.3.0 --enable-gendef --verbose".format ( _CPU_COUNT )
		self.chmodpux(mingw_script_file)
		try:
			self.run_process( [ "./" + mingw_script_file, mingw_script_options, "--build-type={0}".format( self.winBitnessDir ) ], False, False )
		except Exception as e:
			self.logger.error("Previous MinGW build may have failed, delete the compiler folder named '{0}' and try again".format( _MINGW_DIR ))
			exit(1)
	#:
	
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
			print("WARNING: Using non-SSL http is not advised.")
		
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
				('Accept-Encoding'           , 'gzip*;q=1.0,deflate*;q=0.0,sdch*;q=0.0'),
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
					chunk = zlib.decompress(chunk, 16+zlib.MAX_WBITS)
					
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
					sys.stdout.write(nextline.decode('utf-8'))
					sys.stdout.flush()
			else:
				sys.stdout.write(nextline.decode('utf-8'))
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
				exit(return_code)
		
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
			self.logger.info("git checkout'ing $desired_branch")
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
			
			if fileName.endswith(".tar.gz"):
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
		workDir = None
		self.logger.info("Building library '%s'" % (name))
		if data["repo_type"] == "git":
			workDir = self.git_clone(data["url"])
		if data["repo_type"] == "svn":
			workDir = self.svn_clone(data["url"],data["folder_name"])
		if data["repo_type"] == "archive":
			workDir = self.download_unpack_file(data["url"])
		if workDir == None:
			print("Unexpected error when building {0}, please report this:".format(name), sys.exc_info()[0])
			raise
		os.chdir(workDir)
		
		if 'patches' in data:
			if data['patches'] != None:
				for p in data['patches']:
					self.apply_patch(p[0],p[1])
			exit()
		
		self.configure_source(name,data)
		
		self.make_source(name,data)
		
		self.make_install_source(name,data)
		
		os.chdir("..")
		
	def build_product(self,name,data):
	
		if "depends_on" in data:
			if len(data["depends_on"])>0:
				self.logger.info("Building dependencies of '%s'" % (name))
				for libraryName in data["depends_on"]:
					if libraryName not in DEPENDS:
						raise MissingDependency("The dependency '{0}' of '{1}' does not exist in dependency config.".format( libraryName, name)) #sys.exc_info()[0]
					else:
						self.build_depend(libraryName,DEPENDS[libraryName])
					
		exit()
	
		workDir = None
		self.logger.info("Building project '%s'" % (name))
		if data["repo_type"] == "git":
			workDir = self.git_clone(data["url"])
		if data["repo_type"] == "svn":
			workDir = self.svn_clone(data["url"],data["folder_name"])
		if workDir == None:
			print("Unexpected error, please report this:", sys.exc_info()[0])
			raise
		
		os.chdir(workDir)
		
		self.configure_source(name,data)
		
		self.make_source(name,data)
		
		self.make_install_source(name,data)
		
		os.chdir("..")
		
	def configure_source(self,name,data):
		touch_name = "already_configured_%s" % (self.md5(name,self.getKeyOrBlankString(data,"configure_options")))
		if not os.path.isfile(touch_name):
			self.removeAlreadyFiles()
			if not os.path.isfile("configure"):
				if os.path.isfile("bootstrap.sh"):
					self.run_process('./bootstrap.sh')
				if os.path.isfile("autogen.sh"):
					self.run_process('./autogen.sh')
					
			configOpts = ''
			if 'configure_options' in data:
				configOpts = data["configure_options"].format( 
					cross_prefix   = self.crossPrefix,
					compile_target = self.compileTarget,
					compile_prefix = self.compilePrefix,
					)
			print("writing: " + touch_name)
			self.touch(touch_name)
			self.logger.info("Configuring '{0}' with: {1}".format( name, configOpts ))
			
			self.run_process('./configure %s' % configOpts)
			self.run_process('make clean -j {0}'.format( _CPU_COUNT ),True)
			
	def apply_patch(self,url,type = "-p1"): #p1 for github, p0 for idk
		fileName = os.path.basename(urlparse(url).path)
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
			
	def make_source(self,name,data):
		touch_name = "already_ran_make_%s" % (self.md5(name,self.getKeyOrBlankString(data,"make_options")))
		if not os.path.isfile(touch_name):
			if os.path.isfile("configure"):
				self.run_process('make clean -j {0}'.format( _CPU_COUNT ),True)

			makeOpts = ''
			if 'make_options' in data:
				makeOpts = data["make_options"].format( 
					make_prefix_options = self.makePrefixOptions,
					cross_prefix        = self.crossPrefix,
					compile_target      = self.compileTarget,
					compile_prefix      = self.compilePrefix,
					)
				
			self.logger.info("Making '{0}' with: {1}".format( name, makeOpts ))
			
			self.run_process('make -j {0} {1}'.format( _CPU_COUNT, makeOpts ))
			
			self.touch(touch_name)
	#:
			
	def make_install_source(self,name,data):
		touch_name = "already_ran_make_install_%s" % (self.md5(name,self.getKeyOrBlankString(data,"install_options")))
		if not os.path.isfile(touch_name):
		
			makeInstallOpts  = ''
			if 'install_options' in data:
				makeInstallOpts = data["install_options"].format( 
					make_prefix_options = self.makePrefixOptions,
					cross_prefix        = self.crossPrefix,
					compile_target      = self.compileTarget,
					compile_prefix      = self.compilePrefix,
					)
				
				
			self.logger.info("Make installing '{0}' with: {1}".format( name, makeInstallOpts ))
			
			self.run_process('make -j {0} install {1}'.format( _CPU_COUNT, makeInstallOpts ))
			
			self.touch(touch_name)
	#:
	def removeAlreadyFiles(self):
		for af in glob.glob("./already_*"):
			os.remove(af)
		
	def getKeyOrBlankString(self,db,k):
		if k in db:
			if k == None:
				return ""
			else:
				return k
		else:
			return ""
		
if __name__ == "__main__":
	main = CrossCompileScript()