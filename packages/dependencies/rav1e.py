#type: ignore
{
	'repo_type' : 'git',
	'url' : 'https://github.com/xiph/rav1e',
	'depth_git': 1,
	'needs_configure' : False,
	'needs_make_install' : False,
	'build_system' : 'rust',
    'cpu_count': '',
	'build_options' : 
        'cinstall -v '
        # '--manifest-path ./dolby_vision/Cargo.toml '
        '--prefix {target_prefix} '
        '--library-type staticlib '
        '--crt-static '
        '--target {rust_target} '
        '--release '
    ,
	'env_exports' : {
		"CC": "gcc",
		"CXX": "g++",
		"PKG_CONFIG_LIBDIR": "",
		"PKG_CONFIG_PATH": "",
		"TARGET_CC": "{cross_prefix_bare}gcc",
		"TARGET_LD": "{cross_prefix_bare}ld",
		"TARGET_CXX": "{cross_prefix_bare}g++",
		"CROSS_COMPILE": "1",
	},
	'_info' : { 'version' : None, 'fancy_name' : 'rav1e' },
}