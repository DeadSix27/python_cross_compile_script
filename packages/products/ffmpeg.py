{
	'repo_type' : 'git',
	'url' : 'git://git.ffmpeg.org/ffmpeg.git',
	'rename_folder' : 'ffmpeg_git',
	'configure_options' : '!VAR(ffmpeg_min_config)VAR! !VAR(ffmpeg_extra_config)VAR! !VAR(ffmpeg_nonfree)VAR! --prefix={output_prefix}/ffmpeg_git.installed --enable-sdl --disable-shared --enable-static',
	'depends_on' : [ 'ffmpeg_depends_min', 'ffmpeg_depends_extra', 'ffmpeg_depends_nonfree', 'sdl2'],
	'_info' : { 'version' : None, 'fancy_name' : 'ffmpeg (static)' },
}