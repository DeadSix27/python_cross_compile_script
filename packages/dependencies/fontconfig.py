{
	'repo_type' : 'git',
	'do_not_bootstrap' : True,
	'cpu_count' : '1', # I had strange build issues with multiple threads..
	'branch' : '65c7427c019c1cb7c621e6be87fb298564d45f51',
	'url' : 'https://gitlab.freedesktop.org/fontconfig/fontconfig.git',
	'folder_name' : 'fontconfig_git',
	'configure_options': '--host={target_host} --prefix={target_prefix} --enable-libxml2 --disable-shared --enable-static --disable-docs --disable-silent-rules',
	'patches' : [
		('fontconfig/0001-fontconfig-remove-tests.patch', '-p1' ),
		('fontconfig/fontconfig-git-utimes.patch', '-p1' ),
		# ['https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/fontconfig/fontconfig-0001-fix-missing-bracket.patch', '-p1' ],
	],
	'run_post_patch': [
		'autoreconf -fiv',
	],
	'run_post_install': (
		'sed -i.bak \'s/-L${{libdir}} -lfontconfig[^l]*$/-L${{libdir}} -lfontconfig -lfreetype -lharfbuzz -lxml2 -liconv -lintl/\' "{pkg_config_path}/fontconfig.pc"',
	),
	'depends_on' : [
		'iconv','libxml2','freetype',
	],
	'packages': {
		'arch' : [ 'gperf' ],
	},
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'fontconfig' },
}