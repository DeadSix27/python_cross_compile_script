{
	'repo_type' : 'git',
	'url' : 'https://github.com/mpv-player/mpv.git',
	'build_system' : 'waf',
	'conf_system' : 'waf',
	'env_exports' : {
		'DEST_OS' : 'win32',
		'TARGET'  : '{target_host}',
		'PKG_CONFIG' : 'pkg-config',
		# 'LDFLAGS': '-fstack-protector-strong' # See near 'regex_replace' #-Wl,-Bdynamic -lvulkan-1 -Wl,-Bdynamic -lOpenCL
	},
	'configure_options' :
		'--enable-libmpv-shared '
		'--enable-static-build '
		'--prefix={output_prefix}/mpv_git.installed '
		'--disable-sdl2 '
		'--enable-rubberband '
		'--enable-lcms2 '
		'--enable-openal '
		'--enable-dvdnav '
		'--enable-libbluray '
		'--enable-cdda '
		# '--enable-egl-angle-lib ' # not maintained anymore apparently, crashes for me anyway.
		'--enable-lua '
		'--enable-vapoursynth '
		'--enable-uchardet '
		'--enable-vulkan '
		'--enable-libplacebo '
		'--enable-libarchive '
		'--enable-javascript '
		'--disable-manpage-build '
		'--disable-pdf-build '
		'TARGET={target_host} '
		'DEST_OS=win32 '
	,
	'depends_on' : [
		'libffmpeg',
		'zlib',
		'iconv',
		'python3_libs',
		'vapoursynth_libs',
		# 'sdl2',
		'luajit',
		'rubberband',
		'lcms2',
		'libdvdnav',
		'libbluray',
		'openal',
		'libass',
		'libcdio-paranoia',
		'libjpeg-turbo',
		'uchardet',
		'libarchive',
		'mujs',
		'shaderc',
		'vulkan_loader',
		'libplacebo'
	],
	# Dirty hack, so far I've found no way to get -Wl,-Bdynamic into the .pc file or mpv itself without the use of LDFLAGS...
	'regex_replace': {
		'post_patch': [
			# {
			# 	0: r'Libs: -L\${{libdir}} -lvulkan-1',
			# 	1: r'Libs: -L${{libdir}}',
			# 	'in_file': '{pkg_config_path}/vulkan.pc',
			# 	'out_file': '{pkg_config_path}/vulkan.pc'
			# },
			{
				0: r' --dirty', # dirty.
				1: r'',
				'in_file': 'version.sh',
			},
			{
				0: r'bool encoder_encode',
				1: r'bool mpv_encoder_encode',
				'in_file': 'common/encode_lavc.c',
			},
			{
				0: r'bool encoder_encode',
				1: r'bool mpv_encoder_encode',
				'in_file': 'common/encode_lavc.h',
			},
			{
				0: r'encoder_encode',
				1: r'mpv_encoder_encode',
				'in_file': 'video/out/vo_lavc.c',
			},
			{
				0: r'encoder_encode',
				1: r'mpv_encoder_encode',
				'in_file': 'audio/out/ao_lavc.c',
			},
		],
		'post_install': [
			# {
			# 	0: r'Libs: -L\${{libdir}}',
			# 	1: r'Libs: -L${{libdir}} -lvulkan-1',
			# 	'in_file': '{pkg_config_path}/vulkan.pc',
			# 	'out_file': '{pkg_config_path}/vulkan.pc'
			# },
			# {
			# 	0: r'Libs: -L\${{libdir}}',
			# 	1: r'Libs: -L${{libdir}} -lvulkan-1',
			# 	'in_file': '{pkg_config_path}/vulkan.pc',
			# 	'out_file': '{pkg_config_path}/vulkan.pc'
			# }
		]
	},
	'patches': [
		# ('mpv/0001-resolve-naming-collision-with-xavs2.patch', '-p1'),
		# ('https://github.com/mpv-player/mpv/pull/9360.patch', '-p1'), #player: add --auto-window-resize option
		('https://github.com/mpv-player/mpv/pull/10065.patch', '-p1'), #player: add --auto-window-resize option redux #10065 
		('https://github.com/mpv-player/mpv/pull/9274.patch', '-p1'), #vo_tct: rewrite using the newer vo api, generalize and optimize code
		('https://github.com/mpv-player/mpv/pull/9348.patch', '-p1'), #w32_common: fix bad window style for no-border window
		# ('https://github.com/mpv-player/mpv/pull/9667.patch', '-p1'), #ao_wasapi: Use ks.h public abi instead of ksuuid.h
		('https://github.com/mpv-player/mpv/pull/9765.patch', '-p1'), #w32_common: fixes minimized window being focused on launch
		('https://github.com/mpv-player/mpv/pull/9792.patch', '-p1'), #hwdec/d3d11va: Fix a possible memory leak
	],
	'run_post_install' : (
		'{cross_prefix_bare}strip -v {output_prefix}/mpv_git.installed/bin/mpv.com',
		'{cross_prefix_bare}strip -v {output_prefix}/mpv_git.installed/bin/mpv.exe',
		'{cross_prefix_bare}strip -v {output_prefix}/mpv_git.installed/bin/mpv-2.dll',
	),
	'_info' : { 'version' : None, 'fancy_name' : 'mpv' },
}
