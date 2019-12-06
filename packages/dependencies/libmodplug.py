{
	'repo_type' : 'git',
	'url': 'https://github.com/Konstanty/libmodplug.git',
	'conf_system' : 'cmake',
	'configure_options' : '.. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix}',
	'source_subfolder': '_build',
	'patches': [
		('modplug/0001-modplug-mingw-workaround.patch', '-p1', '..'), # to avoid setting -DLIBMODPLUG_STATIC
	],
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'libmodplug' },
}