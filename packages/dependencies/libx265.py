{
	'repo_type' : 'mercurial',
	'url' : 'https://bitbucket.org/multicoreware/x265',
	'rename_folder' : 'libx265_hg',
	'configure_options' : '. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DENABLE_ASSEMBLY=ON -DENABLE_CLI:BOOL=OFF -DENABLE_SHARED=OFF -DCMAKE_AR={cross_prefix_full}ar -DLIBXML_STATIC=ON -DGLIB_STATIC_COMPILATION=ON', # no cli, as this is just for the library.
	'conf_system' : 'cmake',
	'source_subfolder' : 'source',
	'depends_on' : [ 'libxml2' ],
	'run_post_install' : [
		'sed -i.bak \'s|-lmingwex||g\' "{pkg_config_path}/x265.pc"',
	],
	'_info' : { 'version' : None, 'fancy_name' : 'x265 (library)' },
}