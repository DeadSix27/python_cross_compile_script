#type: ignore
{
	'repo_type' : 'git',
	'url' : 'https://github.com/quietvoid/dovi_tool.git',
	'depth_git': 1,
	'branch': "main",
	'needs_configure' : False,
	'needs_make_install' : False,
	'build_system' : 'rust',
    'cpu_count': '',
	'build_options' : 
        'cinstall '
        '--manifest-path ./dolby_vision/Cargo.toml '
        '--prefix {target_prefix} '
        '--target x86_64-pc-windows-gnu '
        '--release '
        '--library-type staticlib'
    ,
	'_info' : { 'version' : None, 'fancy_name' : 'libdovi' },
}