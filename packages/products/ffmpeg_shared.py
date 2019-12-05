{
	'repo_type' : 'git',
	'url' : 'git://git.ffmpeg.org/ffmpeg.git',
	'rename_folder' : 'ffmpeg_shared_git',
	'configure_options' : '!VAR(ffmpeg_min_config)VAR! --prefix={output_prefix}/ffmpeg_shared_git.installed --enable-shared --disable-static --disable-libbluray --disable-libgme',
	'depends_on' : [ 'ffmpeg_depends_min' ],
	'_info' : { 'version' : None, 'fancy_name' : 'ffmpeg (shared)' },
}