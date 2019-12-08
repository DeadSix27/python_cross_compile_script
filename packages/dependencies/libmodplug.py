{
	'repo_type' : 'git',
	'url': 'https://github.com/Konstanty/libmodplug.git',
	'conf_system' : 'cmake',
	'configure_options' : '.. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix}',
	'source_subfolder': '_build',
	'patches': [
		('modplug/0001-modplug-mingw-workaround.patch', '-p1', '..'), # to avoid setting -DLIBMODPLUG_STATIC
	],
	'regex_replace': {
		'post_patch': [
			{
				# Will they ever realise that WIN32 is True on MinGW as well where we need pkg-config files and so on?
				# Use MSVC or a combination of MINGW/WINDOWS/WIN32
				0: r'if \(NOT WIN32\)',
				1: r'if (NOT MSVC)',
				'in_file': '../CMakeLists.txt'
			},
		],
	},
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'libmodplug' },
}