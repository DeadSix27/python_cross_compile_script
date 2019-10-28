# ### pathlib.Path extension

from __future__ import annotations

import os
import pathlib
import re
import shutil
from typing import List


class Path(pathlib.Path):
	'''### Path
	##### Path (custom extended)
	'''
	_flavour = pathlib._windows_flavour if os.name == 'nt' else pathlib._posix_flavour

	def __new__(cls, *args):
		return super(Path, cls).__new__(cls, *args)

	def __init__(self, *args):
		super().__init__()
		self.ssuffix = self.suffix.lstrip(".")
		self._some_instance_ppath_value = self.exists()

	# def ssuffix(self):
	# 	return self.suffix.lstrip(".")

	def listfiles(self, extensions=()) -> List[Path]:
		'''### listfiles
		##### listfiles

		### Args:
			`extensions` (tuple, optional): List of extensions to limit listing to, with dot prefix. Defaults to ().

		### Returns:
			List[Path]: List of Paths, matching the optionally specificed extension(s)
		'''
		lst = None
		if len(extensions) > 0:
			lst = [self.joinpath(x) for x in self._accessor.listdir(self) if self.joinpath(x).is_file() and x.endswith(extensions)]
		else:
			lst = [self.joinpath(x) for x in self._accessor.listdir(self) if self.joinpath(x).is_file()]

		def convert(text):
			return int(text) if text.isdigit() else text

		def alphanum_key(key):
			return [convert(c) for c in re.split('([0-9]+)', str(key))]

		lst = sorted(lst, key=alphanum_key)
		return lst

	def listall(self) -> List[Path]:
		lst = [self.joinpath(x) for x in self._accessor.listdir(self)]

		def convert(text):
			return int(text) if text.isdigit() else text

		def alphanum_key(key):
			return [convert(c) for c in re.split('([0-9]+)', str(key))]

		lst = sorted(lst, key=alphanum_key)
		return lst

	def listdirs(self) -> List[Path]:
		'''### listdirs
		##### Same as listfiles, except for directories only.

		### Returns:
			List[Path]: List of Path's
		'''
		return [self.joinpath(x) for x in self._accessor.listdir(self) if self.joinpath(x).is_dir()]

	def copy(self, destination: Path) -> Path:
		'''### copy
		##### Copies the Path to the specificed destination.

		### Args:
			`destination` (Path): Destination to copy to.

		### Returns:
			Path: Path of the new copy.
		'''
		shutil.copy(self, destination)
		return destination

	def change_ext(self, newExt: str) -> Path:
		'''### change_ext
		##### Changes the extension, excluding stem

		### Args:
			`newExt` (str): The new extension

		### Returns:
			Path: Newly named Path.
		'''
		return self.parent.joinpath(self.stem + newExt)

	def change_name(self, name: str) -> Path:
		'''### change_name
		##### Changes the name, including suffix

		### Args:
			`name` (str): The new name

		### Returns:
			Path: Newly named Path.
		'''
		return self.parent.joinpath(name)

	def change_stem(self, new_stem: str) -> Path:
		'''### append_stem
		##### Changes the name, ignoring the suffix.

		### Args:
			`append_str` (str): String to append.

		### Returns:
			Path: Newly named Path.
		'''
		return self.parent.joinpath(new_stem + self.suffix)

	def append_stem(self, append_str: str) -> Path:
		'''### append_stem
		##### Appends a string to the name, ignoring the suffix.

		### Args:
			`append_str` (str): String to append.

		### Returns:
			Path: Newly named Path.
		'''
		return self.parent.joinpath(self.stem + append_str + self.suffix)

	def append_name(self, append_str: str):
		'''### append_name
		##### Appends a string to the name, including the suffix.

		### Args:
			`append_str` (str): String to append.

		### Returns:
			Path: Newly named Path.
		'''
		return self.parent.joinpath(self.name + append_str)

	def rmtree(self) -> None:
		shutil.rmtree(self)

	def move(self, destination: Path) -> Path:
		'''### move
		##### Moves the Path to a newly specified Location.

		### Args:
			`destination` (Path): The destination to move the file to.

		### Returns:
			Path: The new location of the old Path
		'''
		shutil.move(self, destination)
		return destination

	def fnmatch(self, match: str) -> bool:
		cPath = self.parent
		for p in cPath.listall():
			if re.search(re.escape(match).replace("\\*", ".*"), p.name):
				return True

		return False

	def joinpath(self, *other):
		return Path(super().joinpath(*other))

# #
