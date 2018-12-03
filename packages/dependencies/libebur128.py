{
	'repo_type' : 'git',
	'url' : 'https://github.com/jiixyj/libebur128.git',
	'configure_options' : '. {cmake_prefix_options} -DENABLE_INTERNAL_QUEUE_H:BOOL=ON -DCMAKE_AR={cross_prefix_full}ar', #not sure why it cries about AR
	'conf_system' : 'cmake',
	'run_post_patch' : [
		'sed -i.bak \'s/ SHARED / STATIC /\' ebur128/CMakeLists.txt',
	],
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'libebur128' },
}