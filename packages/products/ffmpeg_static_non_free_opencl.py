{
	'repo_type' : 'git',
	'url' : 'git://git.ffmpeg.org/ffmpeg.git',
	'rename_folder' : 'ffmpeg_static_non_free_opencl',
	'configure_options' : '!VAR(ffmpeg_base_config)VAR! !VAR(ffmpeg_nonfree)VAR! --enable-libbluray --enable-opencl --prefix={product_prefix}/ffmpeg_static_non_free_opencl.installed --disable-shared --enable-static',
	'depends_on' : [ 'ffmpeg_depends', 'decklink_headers', 'fdk_aac', 'opencl_icd' ],
	'_info' : { 'version' : None, 'fancy_name' : 'ffmpeg NonFree (static (OpenCL))' },
}