{
	'repo_type' : 'git',
	'url' : 'https://github.com/xiph/theora.git',
	'patches' : (
		('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/theora_remove_rint_1.2.0alpha1.patch', '-p1'),
	),
	'configure_options': '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static --disable-doc --disable-spec --disable-oggtest --disable-vorbistest --disable-examples',
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'theora' },
}