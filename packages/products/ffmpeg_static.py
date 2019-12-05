{
	'repo_type' : 'git',
	'url' : 'git://git.ffmpeg.org/ffmpeg.git',
	'rename_folder' : 'ffmpeg_static_git',
	'configure_options' : '!VAR(ffmpeg_min_config)VAR! --prefix={output_prefix}/ffmpeg_static_git.installed --disable-shared --enable-static',
	'depends_on' : [ 'ffmpeg_depends_min' ],
	'_info' : { 'version' : None, 'fancy_name' : 'ffmpeg (static)' },
}