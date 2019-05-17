{
	'repo_type' : 'git',
	'url' : 'https://github.com/cisco/openh264.git',
	'conf_system' : 'meson',
	'build_system' : 'ninja',
	'source_subfolder' : '_build',
	'patches' : [
		( 'openh264/0001-openh264-static-only.patch', '-p1', ".." ),
	],
	'configure_options' :
		'--prefix={target_prefix} '
		'--libdir={target_prefix}/lib '
		'--default-library=static '
		'--buildtype=plain '
		'--backend=ninja '
		'--buildtype=release '
		'--cross-file={meson_env_file} ./ ..'
	,
	'_info' : { 'version' : None, 'fancy_name' : 'openh264' },
}