{
	'repo_type' : 'git',
	'url' : 'git://git.ghostscript.com/mujs.git',
	# 'branch' : '3430d9a06d6f8a3696e2bbdca7681937e60ca7a9',
	'needs_configure' : False,
	'build_options' : '{make_prefix_options} prefix={target_prefix} HAVE_READLINE=no',
	'install_options' : '{make_prefix_options} prefix={target_prefix} HAVE_READLINE=no',
	'patches' : [
		# ['https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/mujs/mujs-0001-fix-building-with-mingw.patch', '-p1'],
		('mujs/mujs-0002-fix-install-with-mingw.patch', '-p1'),
	],
	'_info' : { 'version' : None, 'fancy_name' : 'mujs' },
}