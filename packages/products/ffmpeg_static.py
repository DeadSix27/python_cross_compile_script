{
	'repo_type' : 'git',
	'url' : 'git://git.ffmpeg.org/ffmpeg.git',
	'rename_folder' : 'ffmpeg_static_git',
	'configure_options' : '!VAR(ffmpeg_base_config)VAR! --enable-libbluray --prefix={product_prefix}/ffmpeg_static_git.installed --disable-shared --enable-static',
	'depends_on' : [ 'ffmpeg_depends' ],
	'_info' : { 'version' : None, 'fancy_name' : 'ffmpeg (static)' },
}