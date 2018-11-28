{
	'repo_type' : 'git',
	'url' : 'git://git.ffmpeg.org/ffmpeg.git',
	'rename_folder' : 'ffmpeg_shared_git',
	'configure_options': '!VAR(ffmpeg_base_config)VAR! --prefix={product_prefix}/ffmpeg_shared_git.installed --enable-shared --disable-static --disable-libbluray --disable-libgme',
	'depends_on': [ 'ffmpeg_depends' ],
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'ffmpeg (shared)' },
}