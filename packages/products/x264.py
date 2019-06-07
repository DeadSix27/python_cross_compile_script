{
	'repo_type' : 'git',
	'url' : 'https://code.videolan.org/videolan/x264.git',
	'configure_options' : '--host={target_host} --enable-static --cross-prefix={cross_prefix_bare} --prefix={product_prefix}/x264_git.installed --enable-strip --bit-depth=all',
	'env_exports' : {
		'PKGCONFIG' : 'pkg-config',
	},
	'depends_on' : [
		'libffmpeg',
	],
	'_info' : { 'version' : None, 'fancy_name' : 'x264' },
}