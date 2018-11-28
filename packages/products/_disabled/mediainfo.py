{
	'repo_type' : 'git',
	'branch' : 'v0.7.94',
	'custom_cflag' : '',
	'recursive_git' : True,
	'url' : 'https://github.com/MediaArea/MediaInfo.git',
	'source_subfolder' : 'Project/GNU/CLI',
	'rename_folder' : 'mediainfo_git',
	'configure_options': '--host={target_host} --prefix={product_prefix}/mediainfo_git.installed --disable-shared --disable-static-libs',
	'depends_on': [
		'libmediainfo',
	],
	'run_post_configure' : [
		'sed -i.bak \'s/ -DSIZE_T_IS_LONG//g\' Makefile',
	],
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'MediaInfo' },
	'_disabled' : True,
}