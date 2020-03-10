{
	'repo_type' : 'git',
	'depth_git': 1,
	'url' : 'git://git.ffmpeg.org/ffmpeg.git',
	'rename_folder' : 'libffmpeg_extra_git',
	'configure_options' : '--sysroot={target_sub_prefix} !VAR(ffmpeg_config)VAR! !VAR(ffmpeg_extra_config)VAR! !VAR(ffmpeg_nonfree)VAR! --prefix={target_prefix} --disable-sdl2 --disable-shared --enable-static --disable-doc --disable-programs',
	'depends_on' : [ 'ffmpeg_depends', 'ffmpeg_depends_extra', 'ffmpeg_depends_nonfree', ],
	'_info' : { 'version' : None, 'fancy_name' : 'FFmpeg (library, extra)' },
}