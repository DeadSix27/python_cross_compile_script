{
	'repo_type' : 'git',
	'url' : 'git://git.ffmpeg.org/ffmpeg.git',
	'rename_folder' : 'libffmpeg_git',
	'configure_options' : '!VAR(ffmpeg_base_config)VAR! !VAR(ffmpeg_nonfree)VAR! --enable-libbluray --prefix={target_prefix} --disable-shared --enable-static --disable-doc --disable-programs',
	'depends_on' : [ 'ffmpeg_depends', 'ffmpeg_depends_nonfree', ],
	'run_post_install' : [
		'sed -i.bak \'s/-luser32 -ldl/-luser32 -lpsapi -ldl/\' "{pkg_config_path}/libavcodec.pc"',
		'sed -i.bak \'s/-lbz2 -ldl/-lbz2 -lpsapi -ldl/\' "{pkg_config_path}/libavfilter.pc"',
		'sed -i.bak \'s/-lws2_32 -ldl/-lws2_32 -lpsapi -ldl/\' "{pkg_config_path}/libavformat.pc"',
		'sed -i.bak \'s/-lbcrypt -ldl/-lbcrypt -lpsapi -ldl/\' "{pkg_config_path}/libavutil.pc"',
		'sed -i.bak \'s/-luuid -static-libgcc -ldl/-luuid -static-libgcc -lpsapi -ldl/\' "{pkg_config_path}/libavdevice.pc"',
	],
	'_info' : { 'version' : None, 'fancy_name' : 'FFmpeg (library)' },
}