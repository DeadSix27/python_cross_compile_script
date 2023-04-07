# type: ignore
{
	'repo_type' : 'git',
	'url' : 'https://github.com/mpv-player/mpv.git',
    # 'url' :'https://github.com/philipl/mpv.git',
    # 'branch': 'vulkan-interop',
	'conf_system' : 'meson',
	'depth_git': 0,
	'build_system' : 'ninja',
    'do_not_git_update': True,
	# 'source_subfolder' : 'build',
	'env_exports' : {
		'DEST_OS' : 'win32',
        # 'CFLAGS'  : '-DHAVE_VK_EXT_DESCRIPTOR_BUFFER -DHAVE_VULKAN_INTEROP',
		'TARGET'  : '{target_host}',
		'PKG_CONFIG' : 'pkg-config',
		'LDFLAGS': '-fstack-protector-strong',
	},
	'run_post_configure' : [
		'!SWITCHDIR|build',
	],

	'configure_options' :
		'--prefix={output_prefix}/mpv_git.installed '
		'--default-library=both '
		'--backend=ninja '
		'--buildtype=minsize '
		'-Dcdda=enabled '
        # '-Ddvbin=enabled '
        '-Ddvdnav=enabled '
        '-Diconv=enabled '
        '-Djavascript=enabled '
        '-Dlcms2=enabled '
        '-Dlibarchive=enabled '
        '-Dlibavdevice=enabled '
        '-Dlibbluray=enabled '
        '-Dlua=enabled '
        '-Drubberband=enabled '
        '-Dsdl2=enabled '
        '-Dsdl2-gamepad=enabled '
        '-Dsdl2-audio=enabled '
        '-Dvapoursynth=enabled '
        '-Dlibplacebo-next=enabled '
        '-Dmanpage-build=disabled '
        '-Dhtml-build=enabled '
        '-Dpdf-build=enabled '
        '-Dzimg=enabled '
        '-Dzlib=enabled '
        '-Dopenal=enabled '
        '-Dcaca=enabled '
        '-Ddirect3d=enabled '
        # '-Degl-angle-win32=enabled '
        '-Dlibrary-prefix=\'\' '
        '-Dgl-dxinterop=enabled '
        '-Dgl-win32=enabled '
        '-Dlibmpv=true '
		'-Doptimization=3 '
		
		'--cross-file={meson_env_file} ./ build/'
	,
	'depends_on' : [
		'libffmpeg_extra',
		'zlib',
		'iconv',
		'python3_libs',
		'vapoursynth_libs',
		'sdl2',
		'luajit',
		# 'rubberband',
		'lcms2',
		'libdvdnav',
		'openal',
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
	'regex_replace': {
		'post_patch': [
			{
				0: r'\"--dirty\"', # dirty.
				1: r'',
				'in_file': 'version.py',
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
	},
	'patches': [
		( 'mpv/ádd-lib-prefix.patch', '-p1'),
        # ('https://github.com/mpv-player/mpv/pull/9975.patch', '-p1'),
        # ( 'https://github.com/mpv-player/mpv/pull/11494.patch', '-p1'),
		{ 'file': 'mpv/0001-change-icons.patch', 'cmd': 'git apply '},
        # ('https://github.com/mpv-player/mpv/pull/11495.patch', '-p1'),
	],
	'run_post_install' : (
		'{cross_prefix_bare}strip -v {output_prefix}/mpv_git.installed/bin/mpv.com',
		'{cross_prefix_bare}strip -v {output_prefix}/mpv_git.installed/bin/mpv.exe',
		'{cross_prefix_bare}strip -v {output_prefix}/mpv_git.installed/bin/mpv-2.dll',
	),
	'_info' : { 'version' : None, 'fancy_name' : 'mpv' },
}
