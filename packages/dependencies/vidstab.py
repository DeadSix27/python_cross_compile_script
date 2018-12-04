{
	'repo_type' : 'git',
	'url' : 'https://github.com/georgmartius/vid.stab.git', #"Latest commit 97c6ae2  on May 29, 2015" .. master then I guess?
	'rename_folder' : 'vidstab_git',
	'conf_system' : 'cmake',
	'configure_options' : '{cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DENABLE_SHARED=OFF -DCMAKE_AR={cross_prefix_full}ar -DUSE_OMP=OFF', #fatal error: omp.h: No such file or directory
	'run_post_patch' : [
		'sed -i.bak "s/SHARED/STATIC/g" CMakeLists.txt',
	],
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'vid.stab' },
}