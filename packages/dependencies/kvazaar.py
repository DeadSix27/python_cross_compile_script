{
	'repo_type' : 'git',
	'url' : 'https://github.com/ultravideo/kvazaar.git',
	'configure_options' : '{autoconf_prefix_options}',
	#'custom_cflag' : '-O3',
	'patches' : [
		( 'kvazaar/0001-mingw-workaround.patch', '-p1' ),
	],
	'_info' : { 'version' : None, 'fancy_name' : 'kvazaar' },
}