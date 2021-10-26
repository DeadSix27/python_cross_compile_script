{
	'repo_type' : 'git',
	'do_not_bootstrap' : True,
	'url' : 'https://gitlab.freedesktop.org/fontconfig/fontconfig.git',
	'branch': 'main',
	'folder_name' : 'fontconfig_git',
	'configure_options' : '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static --enable-libxml2 --disable-docs --disable-silent-rules --with-expat',
	'patches' : [
		('fontconfig/0001-fontconfig-remove-tests.patch', '-p1' ),
		# ('fontconfig/fontconfig-git-utimes.patch', '-p1' ),
		# ('fontconfig/fontconfig-0001-fix-missing-bracket.patch', '-p1' ),
	],
	'run_post_patch' : [
		'autoreconf -fiv',
	],
	# 'run_post_install' : [
	# 	'sed -i.bak \'s/-L${{libdir}} -lfontconfig[^l]*$/-L${{libdir}} -lfontconfig -lfreetype -lharfbuzz -lxml2 -liconv -lintl/\' "{pkg_config_path}/fontconfig.pc"',
	# ],

	'regex_replace': {
		'post_install': [
			{
				0: r'Requires:  freetype2',
				1: r'Requires: harfbuzz libxml-2.0 freetype2',
				'in_file': '{pkg_config_path}/fontconfig.pc'
			},
			{
				0: r'Libs: -L\${{libdir}} -lfontconfig',
				1: r'Libs: -L${{libdir}} -lfontconfig -liconv -lintl ',
				'in_file': '{pkg_config_path}/fontconfig.pc'
			}
		]
	},

	'depends_on' : [
		'expat', 'iconv', 'libxml2', 'freetype', 'json-c',
	],
	# 'update_check' : { 'type' : 'git', },
	'_info' : { 'version' : None, 'fancy_name' : 'fontconfig' },
}