{
	'repo_type' : 'git',
	'url' : 'https://github.com/DeadSix27/waifu2x-converter-cpp',
	'needs_make_install' : False,
	'conf_system' : 'cmake',
	'source_subfolder' : 'out',
	# 'depends_on' : [ 'opencl_icd' ],
	'configure_options' : '.. {cmake_prefix_options} -DFORCE_AMD=ON -DCMAKE_INSTALL_PREFIX={product_prefix}/w2x.installed',
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'waifu2x-converter-cpp' },
}