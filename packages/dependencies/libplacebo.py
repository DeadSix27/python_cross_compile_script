{
	'repo_type' : 'git',
	'url' : 'https://github.com/haasn/libplacebo.git',
	'conf_system' : 'meson',
	'build_system' : 'ninja',
	'source_subfolder' : 'build',
	'run_post_patch' : [
		'cp -nv "/usr/bin/pkg-config" "{cross_prefix_full}pkg-config"', # gotta fix this properly at some point.
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
	'depends_on' : [ 'lcms2', 'shaderc', 'vulkan_loader' ],
	'_info' : { 'version' : None, 'fancy_name' : 'libplacebo' },
}