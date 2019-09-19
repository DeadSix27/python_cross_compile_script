{
	'repo_type' : 'git',
	'url' : 'https://github.com/xiph/opus.git',
	'patches' : [
		("opus/opus_git_strip_declspec.patch", '-p1'),
	],
	'custom_cflag' : '-O3 -D_FORTIFY_SOURCE=0',
	'run_post_install' : [
		'sed -i.bak \'s/Libs: -L${{libdir}} -lopus.*/Libs: -L${{libdir}} -lopus -lssp/\' "{pkg_config_path}/opus.pc"', # ???, keep checking whether this is needed, apparently it is for now.
	],
	'configure_options' : '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static --disable-silent-rules',
	'_info' : { 'version' : None, 'fancy_name' : 'opus' },
}