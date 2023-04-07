#type: ignore
{
	'repo_type' : 'git',
	'url' : 'https://github.com/haasn/libplacebo.git',
    # 'url': 'https://code.videolan.org/philipl/libplacebo',
	'recursive_git' : True,
    # 'branch' : 'video',
    'depth_git': 0,
	'conf_system' : 'meson',
	'build_system' : 'ninja',
	'source_subfolder' : 'build',
	'run_post_patch' : [
		# 'cp -nv "/usr/bin/pkg-config" "{cross_prefix_full}pkg-config"', # gotta fix this properly at some point.
		# '!SWITCHDIR|../',
        # 'git submodule update --init',
        # '!SWITCHDIR|3rdparty',
		# 'rm -rfv Vulkan-Headers',
		# 'ln -snfv {inTreePrefix}/Vulkan-Headers_git/ Vulkan-Headers',
        # 'pwd',
        # '!SWITCHDIR|../',
        # '!SWITCHDIR|build',
	],
    # 'branch': '61a9f2bf69a85ef20bdf0464c04caad1f7d65169',
	#'warnings' : [
	#	'libplacebo for some reason can\'t detect Vulkan via pkg-config with new meson versions...',
	#	'one way to work around this (until I figure out why... or haasn does... if its even an issue on his side'
	#	'is to just install an old version by running: \'pip install meson==0.49.0 \''
	#],
	'regex_replace': {
		'post_install': [
			{
				0: r'^(Libs: )(.*)$',
				1: r'\1\2 -lstdc++',
				'in_file': '{pkg_config_path}/libplacebo.pc'
			},
		],
	},
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
		'-Dd3d11=enabled '
		'-Dopengl=enabled '
        '-Dglslang=enabled '
		'--cross-file={meson_env_file} ./ ..'
	,
	'depends_on' : [ 'lcms2', 'libdovi', 'libepoxy', 'spirv-tools', 'glslang', 'shaderc', 'vulkan_loader' ],
	'_info' : { 'version' : None, 'fancy_name' : 'libplacebo' },
}