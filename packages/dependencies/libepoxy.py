{
	'repo_type' : 'git',
	'url' : 'https://github.com/anholt/libepoxy.git',
	'conf_system' : 'meson',
	'build_system' : 'ninja',
	'source_subfolder' : 'build',
	'configure_options' :
		'--prefix={target_prefix} '
		'--libdir={target_prefix}/lib '
		'--default-library=static '
		'--buildtype=plain '
		'--backend=ninja '
		'--buildtype=release '
        '-Dtests=false '
        '-Ddocs=false '
		'--cross-file={meson_env_file} ./ ..'
	,
	'patches' : [
		# ( 'https://github.com/anholt/libepoxy/pull/265.patch', '-p1', '..' ),
		( 'https://github.com/anholt/libepoxy/pull/266.patch', '-p1', '..' ),
	],
	'_info' : { 'version' : None, 'fancy_name' : 'libepoxy' },
}