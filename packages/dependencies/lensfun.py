
#type:ignore
{
	'repo_type' : 'git',
	'url' : 'https://github.com/lensfun/lensfun',
    'do_not_git_update': True,
	'conf_system' : 'cmake',
	'source_subfolder' : '_build',
	'run_post_patch' : [
		'sed -i.bak \'s/GLIB2_INCLUDE_DIRS/GLIB2_STATIC_INCLUDE_DIRS/\' "../CMakeLists.txt"',
		'sed -i.bak \'s/GLIB2_LIBRARIES/GLIB2_STATIC_LIBRARIES/\' "../CMakeLists.txt"',
		'sed -i.bak \'s/Libs: -L${{libdir}} -llensfun.*/Libs: -L${{libdir}} -llensfun -lstdc++/\' "../libs/lensfun/lensfun.pc.cmake"',
	],
    'patches':[
		('lensfun/0001-fix-mingw-building.patch', '-p1', '..'),
	],
	'configure_options' : '.. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DCMAKE_INSTALL_DATAROOTDIR={target_prefix}/share -DBUILD_DOC=0 -DBUILD_STATIC=1 -DBUILD_SHARED_LIBS=0 -DBUILD_TESTS=0 -DBUILD_LENSTOOL=0',
	'depends_on': [ 'libpng','glib2' ],
	'_info' : { 'version' : None, 'fancy_name' : 'lensfun (library)' },
}