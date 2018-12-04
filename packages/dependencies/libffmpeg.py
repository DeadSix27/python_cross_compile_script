{
	'repo_type' : 'git',
	'url' : 'git://git.ffmpeg.org/ffmpeg.git',
	'rename_folder' : 'libffmpeg_git',
	'configure_options' : '!VAR(ffmpeg_base_config)VAR! --prefix={target_prefix} --disable-shared --enable-static --disable-doc --disable-programs --enable-amf',
	'depends_on' : [ 'ffmpeg_depends' ],
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'FFmpeg (library)' },
}