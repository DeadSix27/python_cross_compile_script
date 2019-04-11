{
	'repo_type' : 'git',
	'url' : 'git://git.ghostscript.com/mujs.git',
	# 'branch' : '3430d9a06d6f8a3696e2bbdca7681937e60ca7a9',
	'needs_configure' : False,
	'build_options' : '{make_prefix_options} prefix={target_prefix} HAVE_READLINE=no',
	'install_options' : '{make_prefix_options} prefix={target_prefix} HAVE_READLINE=no',
	'run_post_patch' : [
		'sed -i.bak \'s/install -m 755 $(OUT)\/mujs $(DESTDIR)$(bindir)/install -m 755 $(OUT)\/mujs.exe $(DESTDIR)$(bindir)/g\' Makefile',
	],
	'_info' : { 'version' : None, 'fancy_name' : 'mujs' },
}