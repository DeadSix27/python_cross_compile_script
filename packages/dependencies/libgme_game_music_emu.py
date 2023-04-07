#type: ignore
{
	'repo_type' : 'git',
	'depth_git': 0,
	'url' : 'https://bitbucket.org/mpyne/game-music-emu.git',
	# 'branch' : '97527b20a40e6a8ddc272e0c503fea254a0b8eb2',
	'conf_system' : 'cmake',
	'configure_options' : '. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DBUILD_SHARED_LIBS=OFF -DENABLE_UBSAN=OFF',
    'regex_replace': {
		'post_patch': [
			{
				0: r'add_subdirectory\(player EXCLUDE_FROM_ALL\)',
				'in_file': 'CMakeLists.txt'
			},
			{
				0: r'add_subdirectory\(demo EXCLUDE_FROM_ALL\)',
				'in_file': 'CMakeLists.txt'
			}
			
		],

	},
	'_info' : { 'version' : None, 'fancy_name' : 'game-music-emu' },
}