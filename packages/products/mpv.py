{
	'repo_type' : 'git',
	'url' : 'https://github.com/mpv-player/mpv.git',
	'build_system' : 'waf',
	'conf_system' : 'waf',
	'env_exports' : {
		'DEST_OS' : 'win32',
		'TARGET'  : '{target_host}',
		'PKG_CONFIG' : 'pkg-config',
		'LDFLAGS': '-Wl,-Bdynamic -lvulkan-1 -fstack-protector-strong' # See near 'regex_replace'
	},
	'configure_options' :
		'--enable-libmpv-shared '
		'--enable-static-build '
		'--prefix={output_prefix}/mpv_git.installed '
		# '--enable-sdl2 '
		'--enable-rubberband '
		'--enable-lcms2 '
		# '--enable-openal '
		'--enable-dvdnav '
		'--enable-libbluray '
		'--enable-cdda '
		#'--enable-egl-angle-lib ' # not maintained anymore apparently, crashes for me anyway.
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
		#'openal',
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
			{
				0: r'Libs: -L\${{libdir}} -lvulkan',
				1: r'Libs: -L${{libdir}}',
				'in_file': '{pkg_config_path}/vulkan.pc',
				'out_file': '{pkg_config_path}/vulkan.pc'
			},
			{
				0: r' --dirty', # dirty.
				1: r'',
				'in_file': 'version.sh',
			},
		],
		'post_install': [
			{
				0: r'Libs: -L\${{libdir}}',
				1: r'Libs: -L${{libdir}} -lvulkan',
				'in_file': '{pkg_config_path}/vulkan.pc',
				'out_file': '{pkg_config_path}/vulkan.pc'
			}
		]
	},
	'patches': [
		('mpv/0001-resolve-naming-collision-with-xavs2.patch', '-p1'),
	],
	'run_post_install' : (
		'{cross_prefix_bare}strip -v {output_prefix}/mpv_git.installed/bin/mpv.com',
		'{cross_prefix_bare}strip -v {output_prefix}/mpv_git.installed/bin/mpv.exe',
		'{cross_prefix_bare}strip -v {output_prefix}/mpv_git.installed/bin/mpv-1.dll',
	),
	'_info' : { 'version' : None, 'fancy_name' : 'mpv' },
}
