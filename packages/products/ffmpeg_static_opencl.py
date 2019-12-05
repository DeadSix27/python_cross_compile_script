{
	'repo_type' : 'git',
	'url' : 'git://git.ffmpeg.org/ffmpeg.git',
	'rename_folder' : 'ffmpeg_static_opencl_git',
	'configure_options' : '!VAR(ffmpeg_min_config)VAR! --enable-libbluray --prefix={output_prefix}/ffmpeg_static_opencl_git.installed --disable-shared --enable-static --enable-opencl',
	'depends_on' : [ 'ffmpeg_depends_min', 'opencl_icd' ],
	'_info' : { 'version' : None, 'fancy_name' : 'ffmpeg (static (OpenCL))' },
}