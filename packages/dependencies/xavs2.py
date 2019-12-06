{
	'repo_type' : 'git',
	'url' : 'https://github.com/pkuvcl/xavs2.git',
	'source_subfolder' : 'build/linux',
	'configure_options' : '{autoconf_prefix_options} --cross-prefix={cross_prefix_bare} --disable-cli',
	'install_target' : 'install-lib-static',
	'_info' : { 'version' : None, 'fancy_name' : 'xavs2' },
}