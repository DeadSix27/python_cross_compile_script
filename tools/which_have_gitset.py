#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# noqa: E121

import ast
import ftplib
import json
import os
import re
import subprocess
import sys
from telnetlib import EC
import traceback
from pathlib import Path
from urllib.parse import urlparse

import pprint

import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style, init

import libs.htmllistparse as htmllistparse  # https://github.com/gumblex/htmllisting-parser

init()


PACKAGES_DIR = "../packages"
BUILD_DIRS = [
	"../workdir/x86_64/",
	"../workdir/x86_64_products/",
]

HEADERS = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
	'Accept-Language': 'en,en-US;',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

CWD = Path.cwd()

SOURCEFORGE_APIKEY = None

# if not os.path.isfile("sourceforge.apikey"):
# 	errorExit("Missing sourceforge.apikey file, create it and write your api key inside of it")
# else:
# 	SOURCEFORGE_APIKEY = open("sourceforge.apikey","r").read()
# 	print("Loaded sourceforge api key: " + SOURCEFORGE_APIKEY)


def loadPackages(packages_folder):
		def bool_key(d, k):
			if k in d:
				if d[k]:
					return True
			return False

		def isPathDisabled(path):
			for part in path.parts:
				if part.lower().startswith("_disabled"):
					return True
			return False

		depsFolder = Path(os.path.join(packages_folder, "dependencies"))
		prodFolder = Path(os.path.join(packages_folder, "products"))
		varsPath = Path(os.path.join(packages_folder, "variables.py"))

		if not os.path.isdir(packages_folder):
			errorExit("Packages folder '%s' does not exist." % (packages_folder))
		if not os.path.isdir(depsFolder):
			errorExit("Packages folder '%s' does not exist." % (depsFolder))
		if not os.path.isfile(varsPath):
			errorExit("Variables file '%s' does not exist." % (varsPath))

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

		if len(tmpPkglist["deps"]) < 1:
			errorExit("There's no packages in the folder '%s'." % (depsFolder))

		if len(tmpPkglist["prods"]) < 1:
			errorExit("There's no packages in the folder '%s'." % (prodFolder))

		with open(varsPath, "r", encoding="utf-8") as f:
			try:
				o = ast.literal_eval(f.read())
				if not isinstance(o, dict):
					errorExit("Variables file is misformatted")
				packages["vars"] = o
			except SyntaxError:
				errorExit("Loading variables.py failed:\n\n" + traceback.format_exc())

		for d in tmpPkglist["deps"]:
			with open(d, "r", encoding="utf-8") as f:
				p = Path(d)
				package_name = p.stem.lower()
				try:
					o = ast.literal_eval(f.read())
					if not isinstance(o, dict):
						errorExit("Package file '%s' is misformatted" % (p.name))

					if "_info" not in o and not bool_key(o, "is_dep_inheriter"):
						print("Package '%s.py' is missing '_info' tag." % (package_name))

					if bool_key(o, "_disabled"):
						pass
					else:
						packages["deps"][package_name] = o

				except SyntaxError:
					errorExit("Loading '%s.py' failed:\n\n%s" % (package_name, traceback.format_exc()))

		for d in tmpPkglist["prods"]:
			with open(d, "r", encoding="utf-8") as f:
				p = Path(d)
				package_name = p.stem.lower()
				try:
					o = ast.literal_eval(f.read())
					if not isinstance(o, dict):
						errorExit("Package file '%s' is misformatted" % (p.name))

					if "_info" not in o and not bool_key(o, "is_dep_inheriter"):
						print("Package '%s.py' is missing '_info' tag." % (package_name))

					if bool_key(o, "_disabled"):
						pass
					else:
						packages["prods"][package_name] = o

				except SyntaxError:
					errorExit("Loading '%s.py' failed:\n\n%s" % (package_name, traceback.format_exc()))

		print("Loaded %d packages" % (len(packages["prods"]) + len(packages["deps"])))
		return packages


pkgs = loadPackages(PACKAGES_DIR)

for a, b in pkgs["deps"].items():
    if "branch" in b and b["branch"] not in ("main", "default", "master"):
        pprint.pprint([a, b["branch"]])