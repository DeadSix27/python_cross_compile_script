{
	'repo_type' : 'git',
	'url' : 'https://github.com/haasn/libplacebo.git',
	'conf_system' : 'meson',
	'build_system' : 'ninja',
	'source_subfolder' : 'build',
	# 'run_post_patch' : [
	# 	'cp -nv "/usr/bin/pkg-config" "{cross_prefix_full}pkg-config"', # gotta fix this properly at some point.
	# ],

	#'warnings' : [
	#	'libplacebo for some reason can\'t detect Vulkan via pkg-config with new meson versions...',
	#	'one way to work around this (until I figure out why... or haasn does... if its even an issue on his side'
	#	'is to just install an old version by running: \'pip install meson==0.49.0 \''
	#],

	'configure_options' :
		'--prefix={target_prefix} '
		'--libdir={target_prefix}/lib '
		'--default-library=static '
		'--buildtype=plain '
		'--backend=ninja '
		'--buildtype=release '
		'-Dvulkan-registry={target_prefix}/share/vulkan/registry/vk.xml '
		'-Ddemos=false '
		'-Dvulkan=enabled '
		'--cross-file={meson_env_file} ./ ..'
	,
	'depends_on' : [ 'lcms2', 'spirv-tools', 'glslang', 'shaderc', 'vulkan_loader' ],
	'_info' : { 'version' : None, 'fancy_name' : 'libplacebo' },
}