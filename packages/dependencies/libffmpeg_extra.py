#type: ignore
{
	'repo_type' : 'git',
	'depth_git': 0,
	'url' : 'git://git.ffmpeg.org/ffmpeg.git',
	'rename_folder' : 'libffmpeg_extra_git',
	'configure_options' : '--sysroot={target_sub_prefix} !VAR(ffmpeg_config)VAR! !VAR(ffmpeg_extra_config)VAR! !VAR(ffmpeg_nonfree)VAR! --prefix={target_prefix} --disable-sdl2 --disable-shared --enable-static --disable-doc --disable-programs  --disable-doc --disable-htmlpages --disable-manpages --disable-podpages --disable-txtpages',
	'depends_on' : [ 'ffmpeg_depends_min', 'ffmpeg_depends_extra', 'ffmpeg_depends_nonfree', ],
    
    # 'do_not_git_update': True,
	# 'regex_replace': {
	# 	'post_install': [
	# 		{
	# 			0: r'-lOpenCL',
	# 			1: r'-l:libOpenCL.dll.a',
	# 			'in_file': '{pkg_config_path}/libavfilter.pc',
	# 		},
	# 		{
	# 			0: r'-lOpenCL',
	# 			1: r'-l:libOpenCL.dll.a',
	# 			'in_file': '{pkg_config_path}/libavutil.pc',
	# 		},
	# 	]
	# },
    'env_exports' : {
        'OPENAL_LIBS' : '-lOpenAL32 -lstdc++ -lwinmm -lole32',
	},
	'_info' : { 'version' : None, 'fancy_name' : 'FFmpeg (library, extra)' },
}