{
	'repo_type' : 'git',
	'url' : 'https://github.com/xiph/vorbis.git',
	'configure_options' : '{autoconf_prefix_options}',
	'run_post_install' : [
		'sed -i.bak \'s/Libs: -L${{libdir}} -lvorbisenc/Libs: -L${{libdir}} -lvorbisenc -lvorbis -logg/\' "{pkg_config_path}/vorbisenc.pc"', # dunno why ffmpeg doesnt work with Requires.private
		'sed -i.bak \'s/Libs: -L${{libdir}} -lvorbis/Libs: -L${{libdir}} -lvorbis -logg/\' "{pkg_config_path}/vorbis.pc"', # dunno why ffmpeg doesnt work with Requires.private
	],
	'depends_on': ['libogg'],
	'_info' : { 'version' : None, 'fancy_name' : 'vorbis' },
}