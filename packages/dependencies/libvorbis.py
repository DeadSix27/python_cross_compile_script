{
	'repo_type' : 'git',
	'url' : 'https://github.com/xiph/vorbis.git',
	'conf_system' : 'cmake',
	'source_subfolder' : '_build',
	# 'patches' : [
		# ('https://github.com/xiph/vorbis/pull/62.patch', '-p1', '..'), # temporary; I submitted that patch, I assume it'll get merged soon.
	# ],
	'configure_options' : '.. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DBUILD_SHARED_LIBS=0 -DCMAKE_BUILD_TYPE=Release',
	'regex_replace': {
		'post_install': [
			# {
			# 	0: r'Libs: -L${{libdir}} -lvorbisenc[^\n]+',
			# 	1: r'Libs: -L${{libdir}} -lvorbisenc -lvorbis -logg',
			# 	'in_file': '{pkg_config_path}/vorbisenc.pc'
			# },
			# {
			# 	0: r'Libs: -L${{libdir}} -lvorbis[^\n]+',
			# 	1: r'Libs: -L${{libdir}} -lvorbis -logg',
			# 	'in_file': '{pkg_config_path}/vorbis.pc'
			# }
			{
				0: r'Requires\.private:',
				1: r'Requires:',
				'in_file': '{pkg_config_path}/vorbisenc.pc'
			},
			{
				0: r'Requires\.private:',
				1: r'Requires:',
				'in_file': '{pkg_config_path}/vorbis.pc'
			},
		]
	},
	'depends_on': ['libogg',],
	'_info' : { 'version' : None, 'fancy_name' : 'vorbis' },
}