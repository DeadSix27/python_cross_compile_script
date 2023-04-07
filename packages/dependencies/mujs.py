{
	'repo_type' : 'git',
	'url' : 'git://git.ghostscript.com/mujs.git',
	'needs_configure' : False,
	'build_options' : '{make_prefix_options} prefix={target_prefix} HAVE_READLINE=yes',
	'install_options' : '{make_prefix_options} prefix={target_prefix} HAVE_READLINE=yes',
	'regex_replace': {
		'post_patch': [
			{
				0: r'default\: build\/release\/mujs build\/release\/mujs\-pp',
				1: r'default: build/release/mujs build/release/mujs-pp',
				'in_file': 'Makefile'
			},
			{
				0: r'install \-m 755 build\/release\/mujs-pp \$\(DESTDIR\)\$\(bindir\)',
				1: r'install -m 755 build/release/mujs-pp.exe $(DESTDIR)$(bindir) ',
				'in_file': 'Makefile'
			},
			{
				0: r'install \-m 755 build\/release\/mujs \$\(DESTDIR\)\$\(bindir\)',
				1: r'install -m 755 build/release/mujs.exe $(DESTDIR)$(bindir) ',
				'in_file': 'Makefile'
			},
			{
				0: r'-DHAVE_READLINE -lreadline',
				1: r'',
				'in_file': 'Makefile'
			},
		],
		'post_install': [ # hardcode version because master builds use hashes and mpv checks for actual version, could probably edit the git describe command in the Makefile, but this will do.
			{
				0: r'^Version:([\n\r\s]+)?[^\n]+$',
				1: r'Version: 1.0.6',
				'in_file': '{pkg_config_path}/mujs.pc'
			},
		],
	},
	'_info' : { 'version' : None, 'fancy_name' : 'mujs' },
}