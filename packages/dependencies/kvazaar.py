{
	'repo_type' : 'git',
	'url' : 'https://github.com/ultravideo/kvazaar.git',
	'configure_options' : '{autoconf_prefix_options}',
	'run_post_patch' : [
		'sed -i.bak "s/KVZ_PUBLIC const kvz_api/const kvz_api/g" src/kvazaar.h',
	],
	'_info' : { 'version' : None, 'fancy_name' : 'kvazaar' },
}