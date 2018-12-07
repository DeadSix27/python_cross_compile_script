#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os,re,sys,pprint,shutil
from pathlib import Path

PACKAGES_DIR = "../packages"
		
def errorExit(msg):
	print(msg)
	sys.exit(1)

def isPathDisabled(path):
	for part in path.parts:
		if part.lower().startswith("_disabled"):
			return True
	return False

depsFolder = Path(os.path.join(PACKAGES_DIR,"dependencies"))
prodFolder = Path(os.path.join(PACKAGES_DIR,"products"))

if not os.path.isdir(PACKAGES_DIR):
	errorExit("Packages folder '%s' does not exist." % (packages_folder))
if not os.path.isdir(depsFolder):
	errorExit("Packages folder '%s' does not exist." % (depsFolder))
if not os.path.isdir(prodFolder):
	errorExit("Packages folder '%s' does not exist." % (depsFolder))
	
things = { "merged_deps.py" : depsFolder, "merged_prods.py" : prodFolder, }

for mergefile_name in things:
	mergedFileTmp = ""
	print("Merging packages of " + str(things[mergefile_name]) + " to " + mergefile_name )
	for path, subdirs, files in os.walk(things[mergefile_name]):
		for name in files:
			p = Path(os.path.join(path, name))
			if p.suffix == ".py" :
				if not isPathDisabled(p):
					with p.open("r",encoding="utf-8") as f:
						mergedFileTmp += "########START:[" + name + "]\n" + f.read() + "\n########END:[" + name + "]\n"

	with open(mergefile_name, "w", encoding="utf-8") as f:
		f.write(mergedFileTmp)
print("Done")