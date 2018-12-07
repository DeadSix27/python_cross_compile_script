#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os,re,sys,pprint,shutil,ast,traceback,json
from pathlib import Path
from urllib.parse import urlparse
import requests
from colorama import init
from colorama import Fore, Back, Style
init()
from bs4 import BeautifulSoup
from distutils.version import LooseVersion, StrictVersion
import ftplib

import libs.htmllistparse as htmllistparse # https://github.com/gumblex/htmllisting-parser

PACKAGES_DIR = "../packages"
BUILD_DIRS = [
  "../workdir/x86_64/",
  "../workdir/x86_64_products/",
]

HEADERS = {
	'User-Agent' 	  : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
	'Accept-Language' : 'en,en-US;',
	'Accept' 		  : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
}

# SOURCEFORGE_APIKEY = None

# if not os.path.isfile("sourceforge.apikey"):
	# errorExit("Missing sourceforge.apikey file, create it and write your api key inside of it")
# else:
	# SOURCEFORGE_APIKEY = open("sourceforge.apikey","r").read()
	# print("Loaded sourceforge api key: " + SOURCEFORGE_APIKEY)

def loadPackages(packages_folder):
		def bool_key(d,k):
			if k in d:
				if d[k]:
					return True
			return False
		
		def isPathDisabled(path):
			for part in path.parts:
				if part.lower().startswith("_disabled"):
					return True
			return False
		
		depsFolder = Path(os.path.join(packages_folder,"dependencies"))
		prodFolder = Path(os.path.join(packages_folder,"products"))
		varsPath   = Path(os.path.join(packages_folder,"variables.py"))
	
		if not os.path.isdir(packages_folder):
			errorExit("Packages folder '%s' does not exist." % (packages_folder))
		if not os.path.isdir(depsFolder): #TODO simplify code
			errorExit("Packages folder '%s' does not exist." % (depsFolder))
		if not os.path.isfile(varsPath):
			errorExit("Variables file '%s' does not exist." % (varsPath))
			
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
			errorExit("There's no packages in the folder '%s'." % (depsFolder))
				
		if len(tmpPkglist["prods"]) < 1:
			errorExit("There's no packages in the folder '%s'." % (prodFolder))
		
		with open(varsPath,"r",encoding="utf-8") as f:
			try:
				o = ast.literal_eval(f.read()) # was gonna use .json instead of eval on py files, but I like having multiline strings and comments.. so.
				if not isinstance(o, dict):
					errorExit("Variables file is misformatted")					
				packages["vars"] = o
			except SyntaxError:
				errorExit("Loading variables.py failed:\n\n" + traceback.format_exc())
			
		for d in tmpPkglist["deps"]:
			with open(d,"r",encoding="utf-8") as f:
				p = Path(d)
				package_name = p.stem.lower()
				try:
					o = ast.literal_eval(f.read())
					if not isinstance(o, dict):
						errorExit("Package file '%s' is misformatted" % (p.name))
						
					if "_info" not in o and not bool_key(o,"is_dep_inheriter"):
						print("Package '%s.py' is missing '_info' tag." % (package_name))
					
					if bool_key(o,"_disabled"):
						pass
					else:
						packages["deps"][package_name] = o
						
				except SyntaxError as e:
					errorExit("Loading '%s.py' failed:\n\n%s" % ( package_name,traceback.format_exc() ))
		
		for d in tmpPkglist["prods"]:
			with open(d,"r",encoding="utf-8") as f:
				p = Path(d)
				package_name = p.stem.lower()
				try:
					o = ast.literal_eval(f.read())
					if not isinstance(o, dict):
						errorExit("Package file '%s' is misformatted" % (p.name))
						
					if "_info" not in o and not bool_key(o,"is_dep_inheriter"):
						print("Package '%s.py' is missing '_info' tag." % (package_name))
						
					if bool_key(o,"_disabled"):
						pass
					else:
						packages["prods"][package_name] = o
						
				except SyntaxError as e:
					errorExit("Loading '%s.py' failed:\n\n%s" % ( package_name,traceback.format_exc() ))
		
		print("Loaded %d packages" % (len(packages["prods"])+len(packages["deps"])) )
		return packages
		
class Parsers:
	def __init__(self,url,verex):
		self.url = url
		self.verex = verex
		# self.api_key = SOURCEFORGE_APIKEY
		
	def sourceforge(self):	
		soup = BeautifulSoup(requests.get(self.url,headers=HEADERS).content,features="html5lib")
		
		allFolderTrs = soup.find_all("tr",attrs={"class": "folder ", "title" : re.compile(r".*")})
		
		allFileTrs = soup.find_all("tr",attrs={"class": "file ", "title" : re.compile(r".*")})
			
		newest = "0.0.0"
		
		for tr in allFolderTrs+allFileTrs:
			v = tr["title"]
			
			if self.verex != None:
				m = re.search(self.verex,v)
				if m!= None:
					g = m.groupdict()
					if "version_num" not in g:
						errorExit("You have to name a regex group version_num")
					v = g["version_num"]
					if "rc_num" in g:
						v = v + "." + g["rc_num"]
				else:
					v=""
			
			if v != "":
				if re.match("^(?P<version_num>(?:[\dx]{1,3}\.){0,3}[\dx]{1,3})$",v):
					if LooseVersion(v) > LooseVersion(newest):
						newest = v
		return newest
		
		
	def httpindex(self):
		cwd, listing = htmllistparse.fetch_listing(self.url, timeout=30)
		newest = "0.0.0"
		for entry in listing:
			v = entry.name
			if self.verex != None:
				m = re.search(self.verex,v)
				if m!= None:
					g = m.groupdict()
					if "version_num" not in g:
						errorExit("You have to name a regex group version_num")
					v = g["version_num"]
					if "rc_num" in g:
						v = v + "." + g["rc_num"]
				else:
					v = ""
			
			if v != "":
				if re.match("^(?P<version_num>(?:[\dx]{1,3}\.){0,3}[\dx]{1,3})$",v):
					if LooseVersion(v) > LooseVersion(newest):
						newest = v
		return newest
		
	def githubreleases(self,githubType = "name"):
		m = re.search('http?s:\/\/github.com\/(.+\/.+\/releases)',self.url)
		if m == None:
			errorExit("Improper github release URL: '%s' (Example: https://github.com/exampleGroup/exampleProject/releases)" % (self.url))
		
		releaseApiUrl = 'https://api.github.com/repos/%s' % (m.groups()[0])
		
		jString = requests.get(releaseApiUrl,headers=HEADERS).content#.decode("utf-8")
		
		releases = json.loads(jString)
		
		newest = "0.0.0"
		
		for r in releases:
			v = r[githubType]
			if self.verex != None:
				m = re.search(self.verex,v)
				if m!= None:
					g = m.groupdict()
					if "version_num" not in g:
						errorExit("You have to name a regex group version_num")
					v = g["version_num"]
					if "rc_num" in g:
						v = v + "." + g["rc_num"]
				else:
					v = ""
			
			if v != "":
				if re.match("^(?P<version_num>(?:[\dx]{1,3}\.){0,3}[\dx]{1,3})$",v):
					if LooseVersion(v) > LooseVersion(newest):
						newest = v
		return newest
		
		
	def httpregex(self):
		r = requests.get(self.url,headers=HEADERS)
		
		html = r.content.decode("utf-8")
		
		m = re.findall(self.verex,html)
		newest = "0.0.0"
		for v in m:
			if v != "":
				if re.match("^(?P<version_num>(?:[\dx]{1,3}\.){0,3}[\dx]{1,3})$",v):
					if LooseVersion(v) > LooseVersion(newest):
						newest = v
		return newest
		
		
	def ftp(self):
		pUrl = urlparse(self.url)
		ftp = ftplib.FTP(pUrl.netloc)
		ftp.login()
		ftp.cwd(pUrl.path) 
		files = []

		try:
			files = ftp.nlst()
		except ftplib.error_perm as resp:
			if str(resp) == "550 No files found":
				errorExit("FTP 550: No files in this directory")
			else:
				errorExit("Failed to parse version of " + url + "\n\n" + traceback.format_exc())
				
		newest = "0.0.0"

		for v in files:
			if self.verex != None:
				m = re.search(self.verex,v)
				if m!= None:
					g = m.groupdict()
					if "version_num" not in g:
						errorExit("You have to name a regex group version_num")
					v = g["version_num"]
					if "rc_num" in g:
						v = v + "." + g["rc_num"]
				else:
					v = ""
			
			if v != "":
				if re.match("^(?P<version_num>(?:[\dx]{1,3}\.){0,3}[\dx]{1,3})$",v):
					if LooseVersion(v) > LooseVersion(newest):
						newest = v
		return newest

def errorExit(msg):
	print(msg)
	sys.exit(1)
	
def getGitClonePathFromPkg(pkg):
	clonePath = None
	if "folder_name" in pkg:
		clonePath = pkg["folder_name"]
	if "rename_folder" in pkg:
		clonePath = pkg["rename_folder"]
	if not "rename_folder" in pkg and not "folder_name" in pkg:
		pUrl = urlparse(pkg["url"])
		clonePath = os.path.basename(pUrl.path).replace(".","_")
		if not clonePath.endswith("_git"):
			clonePath = clonePath + "_git"
		
	dirs = []
		
	for dir in BUILD_DIRS:
		mDir = os.path.join(dir,clonePath)
		dirs.append(mDir)
		if os.path.isdir(mDir):
			return mDir
			
	# print("Debug: None of those exist: " + ", ".join(dirs))
			
	return None
	
def run(cmd):
	return os.popen(cmd).read()
	
def getCommitsDiff(pkg):
	curCommit = pkg["branch"]
	
	origDir = os.getcwd()

	clonePath = getGitClonePathFromPkg(pkg)
	
	if clonePath != None:
		os.chdir(clonePath)	
		cmts = [c.split(";;") for c in run("git log --pretty=format:\"%H;;%an;;%s\" {0}..master".format(curCommit)).split("\n") if c != ""]
		os.chdir(origDir)
		return cmts
	return None

def geLatestVersion(versionEl):
	url = versionEl["url"]	
	verex = None
	ghtype = None
	if "regex" in versionEl:
		verex = versionEl["regex"]
	if "name_or_tag" in versionEl:
		ghtype = versionEl["name_or_tag"]
	pUrl = urlparse(url)
	if pUrl.scheme == '':
		errorExit("Update check URL '%s' is invalid." % (url))
		
	try:
		pType = versionEl["type"]
		parser = Parsers(url,verex)
		if pType == "sourceforge":
			return parser.sourceforge()
		elif pType == "httpindex":
			return parser.httpindex()
		elif pType == "ftpindex":
			return parser.ftp()
		elif pType == "httpregex":
			return parser.httpregex()
		elif pType == "githubreleases":
			return parser.githubreleases(ghtype)
		else:
			errorExit("Unknown parser: %s " % (pType))
	except Exception as e:
		errorExit("Failed to parse version of " + url + "\n\n" + traceback.format_exc())

specificPkgs = None

if len(sys.argv) > 1:
	if sys.argv[1].lower().startswith("-h") or sys.argv[1].lower().startswith("--h"):
		print("Syntax:\ncheck_versions.py (<package*>,<package*>,....) (E.g: check_versions.py libxml)\nRun it without any arguments to check every supported package.")
		sys.exit(0)
	specificPkgs = sys.argv[1:]

pkgs = loadPackages(PACKAGES_DIR)


for name, d in pkgs["deps"].items():
	if specificPkgs != None:
		if not any(word in name for word in specificPkgs):
			continue
	if "update_check" in d:
	
		versionEl = d["update_check"]
		vType = versionEl["type"]
		
		
		if vType == "git":
			if "branch" not in d:
				# print("Package is has update check, but isn't set to a commit, ignore.")
				continue
			di = getCommitsDiff(d)
			
			if di != None:
				numCmts = len(di)
				
				if numCmts > 0:
					print(Style.DIM + Fore.YELLOW + "%s is %d commits behind!" % (name.rjust(30),numCmts) + Style.RESET_ALL)
				else:
					print(Style.BRIGHT +            "%s is up to date." % (name.rjust(30)) + Style.RESET_ALL)
			
		else:
			
			ourVer = d["_info"]["version"]
			
			latestVer = geLatestVersion(versionEl)
			
			if LooseVersion(ourVer) < LooseVersion(latestVer):
				print(Fore.GREEN + "%s has an update! [Local: %s Remote: %s]" % (name.rjust(30),ourVer.center(10) ,latestVer.center(10) ) + Style.RESET_ALL)
			else:
				print(Style.BRIGHT + "%s is up to date. [Local: %s Remote: %s]" % (name.rjust(30),ourVer.center(10) ,latestVer.center(10) ) + Style.RESET_ALL)
