{
	'repo_type' : 'git',
	'url' : 'https://github.com/commonmark/cmark.git',
	'conf_system' : 'cmake',
	'source_subfolder': '_build',
	'configure_options': '.. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DCMARK_STATIC=ON -DCMARK_SHARED=OFF -DCMARK_TESTS=OFF', #CMARK_STATIC_DEFINE
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'cmark' },
}