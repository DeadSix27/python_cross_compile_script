{
	'repo_type' : 'git',
	'url' : 'https://github.com/google/angle.git',
	'folder_name' : 'angle_headers_git',
	'needs_make':False,
	'needs_make_install':False,
	'needs_configure':False,
	'run_post_patch': [
		'if [ ! -f "already_done" ] ; then cp -rv "include/EGL" "{target_prefix}/include/" ; fi',
		'if [ ! -f "already_done" ] ; then cp -rv "include/KHR" "{target_prefix}/include/" ; fi',
		'if [ ! -f "already_done" ] ; then touch already_done ; fi',
	],
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'ANGLE headers' },
}