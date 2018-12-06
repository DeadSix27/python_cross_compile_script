{
	'repo_type' : 'git',
	'url' : 'https://chromium.googlesource.com/webm/libvpx',
	'rename_folder' : 'vpx_git',
	'configure_options' :
		'--target={bit_name2}-{bit_name_win}-gcc '
		'--prefix={product_prefix}/vpx_git.installed '
		'--disable-shared --enable-static --enable-webm-io --enable-vp9 '
		'--enable-vp8 --enable-runtime-cpu-detect '
		'--enable-vp9-highbitdepth --enable-vp9-postproc --enable-coefficient-range-checking '
		'--enable-error-concealment --enable-better-hw-compatibility '
		'--enable-multi-res-encoding --enable-vp9-temporal-denoising '
		'--enable-tools --disable-docs --enable-examples --disable-install-docs --disable-unit-tests --disable-decode-perf-tests --disable-encode-perf-tests --disable-avx512 --as=nasm' #--as=yasm'
	,
	'env_exports' : {
		'CROSS' : '{cross_prefix_bare}',
	},
	'custom_cflag' : '-fno-asynchronous-unwind-tables',
	'patches' : [
		( 'vpx/vpx_160_semaphore.patch', '-p1' ),
	],
	'_info' : { 'version' : None, 'fancy_name' : 'vpx' },
}