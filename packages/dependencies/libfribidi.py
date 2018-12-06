{
	#https://raw.githubusercontent.com/rdp/ffmpeg-windows-build-helpers/master/patches/fribidi.diff
	'repo_type' : 'git',
	'do_not_bootstrap' : True,
	'patches' : [
		( 'fribidi/0001-mingwcompat-remove-doc-tests.patch', '-p1' ),
	],
	'run_post_patch' : [
		'autoreconf -fiv',
	],
	#'branch' : 'c8fb314d9cab3e4803054eb9829373f014684dc0', # 'b534ab2642f694c3106d5bc8d0a8beae60bf60d3',
	'url' : 'https://github.com/fribidi/fribidi.git',
	'configure_options' : '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static --disable-docs',
	'_info' : { 'version' : None, 'fancy_name' : 'libfribidi' },
}