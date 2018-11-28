{
	'repo_type' : 'git',
	'url' : 'https://github.com/nih-at/libzip.git',
	'configure_options': '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static',
	'patches' : [
		# ('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/libzip/0001-libzip-git-20170415-fix-static-build.patch','-p1'),
		('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/libzip/0001-Fix-building-statically-on-mingw64.patch','-p1'),

	],
	'run_post_patch' : (
		'autoreconf -fiv',
	),
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'libzip' },
}