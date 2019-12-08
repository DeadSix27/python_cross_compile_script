{
	'repo_type' : 'git',
	'url' : 'https://code.videolan.org/videolan/dav1d.git',
	'conf_system' : 'meson',
	'build_system' : 'ninja',
	'source_subfolder' : 'build',
	'configure_options' : ''
		'--prefix={output_prefix}/dav1d.installed  '
		'--libdir={output_prefix}/dav1d.installed/lib '
		'--default-library=static '
		'--buildtype=plain '
		'--backend=ninja '
		'--buildtype=release '
		'--cross-file={meson_env_file} ./ ..'
	,
	'_info' : { 'version' : None, 'fancy_name' : 'dav1d' },
}