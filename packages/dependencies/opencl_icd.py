{
	'repo_type' : 'git',
	'url' : 'https://github.com/KhronosGroup/OpenCL-ICD-Loader.git',
	# 'needs_make_install' : False,
	'source_subfolder': '_build',
	'conf_system' : 'cmake',
	'branch': 'main',
	'configure_options' : '.. {cmake_prefix_options} -DOPENCL_ICD_LOADER_HEADERS_DIR={target_prefix}/include -DCMAKE_INSTALL_PREFIX={target_prefix} -DBUILD_SHARED_LIBS=ON -DCMAKE_STATIC_LIBRARY_PREFIX="" ',
	#-DBUILD_SHARED_LIBS=ON
	# -DOPENCL_ICD_LOADER_REQUIRE_WDK=OFF
	'depends_on' : [ 'opencl_headers' ],	
	# 'run_post_build' : [
	# 	'if [ ! -f "already_ran_make_install" ] ; then cp -vf "libOpenCL.dll.a" "{target_prefix}/lib/libOpenCL.dll.a" ; fi',
	# 	'if [ ! -f "already_ran_make_install" ] ; then touch already_ran_make_install ; fi',
	# ],
	'patches' : [
		# ('opencl/0001-OpenCL-git-prefix.patch', '-p1', '..'),
		# ('opencl/0002-OpenCL-git-header.patch', '-p1', '..'),
		# ('opencl/0001-win32_crosscompile_fixes.patch', '-p1', '..'),
		# ('opencl/1.patch', '-p1', '..'),
	],
	'_info' : { 'version' : None, 'fancy_name' : 'OpenCL ICD' },
}