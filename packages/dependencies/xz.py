{
	'repo_type' : 'git',
	'url' : 'https://github.com/xz-mirror/xz.git',
	#'url' : 'http://git.tukaani.org/xz.git',
	'configure_options' : '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static --disable-xz --disable-xzdec --disable-lzmadec --disable-lzmainfo --disable-doc',
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'xz' },
}