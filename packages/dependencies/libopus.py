{
	'repo_type' : 'git',
	'url' : 'https://github.com/xiph/opus.git',
	'custom_cflag' : '-O3 -D_FORTIFY_SOURCE=0',
	'conf_system' : 'cmake',
	'source_subfolder' : '_build',
	'configure_options' : '.. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={product_prefix}/opus_git.installed -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=0 -DBUILD_TESTING=0 -DOPUS_CUSTOM_MODES=1 -DOPUS_BUILD_PROGRAMS=0 -DOPUS_INSTALL_PKG_CONFIG_MODULE=1',
	# 'patches' : [
		# ('opus/opus_git_strip_declspec.patch', '-p1'),
	# ],
	'run_post_install' : [
		'sed -i.bak \'s/Libs: -L${{libdir}} -lopus.*/Libs: -L${{libdir}} -lopus -lssp/\' "{pkg_config_path}/opus.pc"', # ???, keep checking whether this is needed, apparently it is for now.
	],
	'_info' : { 'version' : None, 'fancy_name' : 'opus' },
}