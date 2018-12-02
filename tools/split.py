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

depsFolder = Path("_deps_split")
prodFolder = Path("_prods_split")

merged_deps  = Path("merged_deps.py" )
merged_prods = Path("merged_prods.py")

if not os.path.isfile(merged_deps):
	errorExit("Merged depends file does not exist")
if not os.path.isfile(merged_prods):
	errorExit("Merged products file does not exist")
	
if not os.path.isdir(depsFolder):
	os.makedirs(depsFolder)
else:
	print("Clearing old split folder:" + str(depsFolder))
	shutil.rmtree(depsFolder)
	os.makedirs(depsFolder)
	
if not os.path.isdir(prodFolder):
	os.makedirs(prodFolder)
else:
	print("Clearing old split folder:" + str(prodFolder))
	shutil.rmtree(prodFolder)
	os.makedirs(prodFolder)
	
things = { "merged_deps.py" : depsFolder, "merged_prods.py" : prodFolder, }

for mergefile_name in things:
	mergedFile = None
	enableWrite = False
	curFile = None
	
	print("Splitting " +mergefile_name+ " into seperate files in " + str(things[mergefile_name]))
		
	with open(mergefile_name, "r", encoding="utf-8") as f:
		mergedFile = f.read().split("\n")
	
	fileBuffer = ""
	
	for line in mergedFile:
		startR = re.search("^########START:\[(.+)\]$",line)
		endR = re.search("^########END:\[(.+)\]$",line)
		if endR != None:
			enableWrite = False
			curFile.write(fileBuffer.rstrip("\n"))
			curFile.close()
			
		if enableWrite:
			fileBuffer+=line+"\n"
			
		if startR != None:
			enableWrite = True
			fileBuffer = ""
			curFile = open(os.path.join(things[mergefile_name],startR.groups()[0]) ,"w",encoding="utf-8")
print("Done")