{
	'repo_type' : 'git',
	'url' : 'https://github.com/fribidi/fribidi.git',
	'depth_git': 0,
	'conf_system' : 'meson',
	'branch': 'f9e8e71a6fbf4a4619481284c9f484d10e559995',
	'build_system' : 'ninja',
	'source_subfolder' : 'build',
	'configure_options' :
		'--prefix={target_prefix} '
		'--libdir={target_prefix}/lib '
		'--default-library=static '
		'--buildtype=plain '
		'--backend=ninja '
		'-Ddocs=false '
		'--buildtype=release '
		'--cross-file={meson_env_file} ./ ..'
	,
	'_info' : { 'version' : None, 'fancy_name' : 'libfribidi' },
}