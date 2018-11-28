{
	'repo_type' : 'git',
	'url' : 'https://github.com/ultravideo/kvazaar.git',
	'configure_options': '--prefix={target_prefix} --host={target_host}',
	'run_post_patch': [
		'sed -i.bak "s/KVZ_PUBLIC const kvz_api/const kvz_api/g" src/kvazaar.h',
	],
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'kvazaar' },
}