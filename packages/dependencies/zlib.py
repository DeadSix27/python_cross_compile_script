{
	'repo_type' : 'git',
	'url' : 'https://github.com/madler/zlib.git',
	'conf_system' : 'cmake',
	'source_subfolder' : '_build',
	#'custom_cflag' : '-O2',
	'configure_options' : '.. {cmake_prefix_options}'
        ' -DCMAKE_INSTALL_PREFIX={target_prefix}'
        ' -DINSTALL_PKGCONFIG_DIR="{target_prefix}/lib/pkgconfig"'
        ' -DBUILD_SHARED_LIBS=0 -DCMAKE_BUILD_TYPE=Release'
    ,
	'depends_on' : ['pkg-config', ],
	'patches' : [
		('zlib/0001-mingw-workarounds.patch', '-p1', '..'),
	],
	'_info' : { 'version' : None, 'fancy_name' : 'zlib' },
}