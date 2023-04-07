{
	'repo_type' : 'git',
	'url' : 'https://github.com/xz-mirror/xz.git',
	# 'branch': '6468f7e41a8e9c611e4ba8d34e2175c5dacdbeb4',
	'depth_git': 0,
	#'url' : 'http://git.tukaani.org/xz.git',
	'custom_cflag' : '-O2',
	'configure_options' : '{autoconf_prefix_options} --disable-xz --disable-xzdec --disable-lzmadec --disable-lzmainfo --disable-doc',
	'_info' : { 'version' : None, 'fancy_name' : 'xz' },
}