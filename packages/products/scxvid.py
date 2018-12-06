{
	'repo_type' : 'git',
	'url' : 'https://github.com/DeadSix27/SCXvid-standalone',
	'conf_system' : 'cmake',
	'source_subfolder' : 'build',
	'configure_options' : '.. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={product_prefix}/SCXvid-standalone_git.installed',
	'run_post_install' : [
		'{cross_prefix_bare}strip -v {product_prefix}/SCXvid-standalone_git.installed/bin/scxvid.exe',
	],
	'_info' : { 'version' : None, 'fancy_name' : 'SCXvid-standalone' },
}