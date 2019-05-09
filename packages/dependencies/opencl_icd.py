{
	'repo_type' : 'git',
	'url' : 'https://github.com/KhronosGroup/OpenCL-ICD-Loader.git',
	'needs_make_install' :False,
	'conf_system' : 'cmake',
	'configure_options' : '. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DBUILD_SHARED_LIBS=ON',
	'depends_on' : [ 'opencl_headers' ],	
	'run_post_build' : [
		'if [ ! -f "already_ran_make_install" ] ; then cp -vf "libOpenCL.dll.a" "{target_prefix}/lib/libOpenCL.dll.a" ; fi',
		'if [ ! -f "already_ran_make_install" ] ; then touch already_ran_make_install ; fi',
	],
	'patches' : [
		('opencl/0001-OpenCL-git-prefix.patch','-p1'),
		('opencl/0002-OpenCL-git-header.patch','-p1'),
	],
	'_info' : { 'version' : None, 'fancy_name' : 'OpenCL ICD' },
}