{
	'repo_type' : 'git',
	'url' : 'https://github.com/rossy/crossc.git',
	'cpu_count' : '1',
	'recursive_git' : True,
	'needs_configure' : False,
	'build_options' : '{make_prefix_options} static',
	'install_options' : '{make_prefix_options} prefix={target_prefix} install-static',
	'run_post_patch' : [
		'git submodule update --remote --recursive',
		'rm -vf {target_prefix}/lib/pkgconfig/crossc.pc',
	],
	'run_post_install' : [
		"rm -vf {target_prefix}/lib/libcrossc.dll.a", # we only want static, somehow this still gets installed tho.
	],
	'_info' : { 'version' : None, 'fancy_name' : 'crossc' },
}