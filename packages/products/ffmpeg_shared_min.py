{
	'repo_type' : 'git',
	'url' : 'git://git.ffmpeg.org/ffmpeg.git',
	'rename_folder' : 'ffmpeg_shared_git',
	'configure_options' : '!VAR(ffmpeg_min_config)VAR! !VAR(ffmpeg_nonfree)VAR! --prefix={output_prefix}/ffmpeg_shared_min_git.installed --enable-shared --disable-static --disable-libbluray --disable-libgme',
	'depends_on' : [ 'ffmpeg_depends_min', 'ffmpeg_depends_nonfree' ],
	'_info' : { 'version' : None, 'fancy_name' : 'ffmpeg (shared, min)' },
}