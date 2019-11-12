{
	'repo_type' : 'git',
	'url' : 'https://github.com/xiph/opus.git',
	'custom_cflag' : '-O3 -D_FORTIFY_SOURCE=0',
	'conf_system' : 'cmake',
	'source_subfolder' : '_build',
	'needs_make_install' : False,
	'run_post_build' : [
		'if [ ! -f "already_ran_make_install" ] ; then mkdir -pv "{product_prefix}/opus_git.installed/bin" ; fi',
		'if [ ! -f "already_ran_make_install" ] ; then pwd ; fi',
		'if [ ! -f "already_ran_make_install" ] ; then cp -vf "opus_demo.exe" "{product_prefix}/opus_git.installed/bin/opus.exe" ; fi',
		'if [ ! -f "already_ran_make_install" ] ; then touch already_ran_make_install ; fi',
	],
	'configure_options' : '.. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={product_prefix}/opus_git.installed -DCMAKE_BUILD_TYPE=Release -DOPUS_STACK_PROTECTOR=0 -DBUILD_SHARED_LIBS=0 -DBUILD_TESTING=0 -DOPUS_CUSTOM_MODES=1 -DOPUS_BUILD_PROGRAMS=1 -DOPUS_INSTALL_PKG_CONFIG_MODULE=0 -DOPUS_INSTALL_CMAKE_CONFIG_MODULE=0',
	'_info' : { 'version' : None, 'fancy_name' : 'opus' },
}