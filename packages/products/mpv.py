{
	'repo_type' : 'git',
	'url' : 'https://github.com/mpv-player/mpv.git',
	'build_system' : 'waf',
	'conf_system' : 'waf',
	'env_exports' : {
		'DEST_OS' : 'win32',
		'TARGET'  : '{target_host}',
		'PKG_CONFIG' : 'pkg-config',
		'LDFLAGS': '-Wl,-Bdynamic -lvulkan-1' # See near 'regex_replace'
	},
	'configure_options' :
		'--enable-libmpv-shared '
		'--enable-static-build '
		'--prefix={product_prefix}/mpv_git.installed '
		'--enable-sdl2 '
		'--enable-rubberband '
		'--enable-lcms2 '
		'--enable-dvdnav '
		'--enable-libbluray '
		'--enable-cdda '
		'--enable-libass '
		'--enable-lua '
		'--enable-vapoursynth '
		'--enable-uchardet '
		'--disable-xv '
		'--disable-pulse '
		'--enable-vulkan '
		'--enable-libplacebo '
		'--disable-alsa '
		'--disable-jack '
		'--disable-x11 '
		'--disable-wayland '
		'--disable-wayland-protocols '
		'--disable-wayland-scanner '
		'--enable-libarchive '
		'--enable-javascript '
		'--disable-manpage-build '
		'--enable-pdf-build '
		'TARGET={target_host} '
		'DEST_OS=win32 '
	,
	'depends_on' : [
		'libffmpeg',
		'python3_libs',
		'vapoursynth_libs',
		'sdl2',
		'luajit',
		'librubberband',
		'lcms2',
		'libdvdnav',
		'libbluray',
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
	'packages' : {
		'arch' : [ 'rst2pdf' ],
	},
	# Dirty hack, so far I've found no way to get -Wl,-Bdynamic into the .pc file or mpv itself without the use of LDFLAGS...
	'regex_replace': {
		'post_patch': [
			{
				0: r'Libs: -L\${{libdir}} -lvulkan',
				1: r'Libs: -L${{libdir}}',
				'in_file': '{pkg_config_path}/vulkan.pc'
			},
		],
		'post_install': [
			{
				0: r'Libs: -L\${{libdir}}',
				1: r'Libs: -L${{libdir}} -lvulkan',
				'in_file': '{pkg_config_path}/vulkan.pc'
			}
		]
	},
	'run_post_install' : (
		'{cross_prefix_bare}strip -v {product_prefix}/mpv_git.installed/bin/mpv.com',
		'{cross_prefix_bare}strip -v {product_prefix}/mpv_git.installed/bin/mpv.exe',
		'{cross_prefix_bare}strip -v {product_prefix}/mpv_git.installed/bin/mpv-1.dll',
	),
	'_info' : { 'version' : None, 'fancy_name' : 'mpv' },
}
