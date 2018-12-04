{
	'repo_type' : 'git',
	'url' : 'git://git.ffmpeg.org/ffmpeg.git',
	'rename_folder' : 'ffmpeg_static_non_free',
	'configure_options' : '!VAR(ffmpeg_base_config)VAR! --enable-libbluray --prefix={product_prefix}/ffmpeg_static_non_free.installed --disable-shared --enable-static --enable-nonfree --enable-libfdk-aac --enable-decklink',
	'depends_on' : [ 'ffmpeg_depends', 'decklink_headers', 'fdk_aac' ],
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'ffmpeg NonFree (static)' },
}