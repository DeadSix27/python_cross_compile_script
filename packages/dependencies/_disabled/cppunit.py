{
	'repo_type' : 'git',
	'url' : 'git://anongit.freedesktop.org/git/libreoffice/cppunit',
	'configure_options':
		'--host={target_host} '
		'--prefix={target_prefix} '
		'--disable-shared '
		'--enable-static '
	,
	'patches' : [
		['https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/cppunit/Add-define-guard-for-NOMINMAX.patch','-p1']
	],
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'cppunit' },
}