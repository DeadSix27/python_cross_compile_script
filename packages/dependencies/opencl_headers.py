{
	'repo_type' : 'git',
	'url' : 'https://github.com/KhronosGroup/OpenCL-Headers.git',
	'run_post_patch' : [
		'if [ ! -f "already_ran_make_install" ] ; then if [ ! -d "{target_prefix}/include/CL" ] ; then mkdir "{target_prefix}/include/CL" ; fi ; fi',
		'if [ ! -f "already_ran_make_install" ] ; then cp -rfv CL/*.h "{target_prefix}/include/CL/" ; fi',
		'if [ ! -f "already_ran_make_install" ] ; then touch already_ran_make_install ; fi',
	],
	'branch': 'main',
	'needs_make' : False,
	'needs_make_install' : False,
	'needs_configure' : False,
	'_info' : { 'version' : None, 'fancy_name' : 'OpenCL Headers' },
}