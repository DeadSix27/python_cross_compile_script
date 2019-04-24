{

	# I am totally uninterested in supporting Windows, so that's not persuasive. 
	#    - Eric S. Raymond (Programmer working on GIFLIB) - 2019-03-18 (https://sourceforge.net/p/giflib/feature-requests/6/#64a5)
	'repo_type' : 'archive',
	'conf_system' : 'cmake',
	'download_locations' : [
		{ 'url' : 'https://sourceforge.net/projects/giflib/files/giflib-5.1.9.tar.bz2', 'hashes' : [ { 'type' : 'sha256', 'sum' : '292b10b86a87cb05f9dcbe1b6c7b99f3187a106132dd14f1ba79c90f561c3295' }, ], },
		{ 'url' : 'https://fossies.org/linux/misc/giflib-5.1.9.tar.bz2'				  , 'hashes' : [ { 'type' : 'sha256', 'sum' : '292b10b86a87cb05f9dcbe1b6c7b99f3187a106132dd14f1ba79c90f561c3295' }, ], },
	],
	# 'patches' : [
		# ( 'giflib/giflib-add-cmakelists.patch', '-p1', '..' ), # thanks to https://sourceforge.net/p/giflib/feature-requests/6/
	# ],
	'copy_over' : [
		'{project_root}/patches/giflib/CMakeLists.txt'
	],
	'source_subfolder' : '_build',
	'configure_options' : 
		'.. {cmake_prefix_options} -DBUILD_STATIC_LIBS=1 -DCMAKE_INSTALL_PREFIX={target_prefix}'
	,
	'update_check' : { 'url' : 'https://sourceforge.net/projects/giflib/files/', 'type' : 'sourceforge', 'regex' : r'giflib-(?P<version_num>[\d.]+)\.tar\.bz2' },
	'_info' : { 'version' : '5.1.9', 'fancy_name' : 'giflib' },
}