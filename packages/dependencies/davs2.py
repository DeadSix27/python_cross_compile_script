{
	'repo_type' : 'git',
	'url' : 'https://github.com/pkuvcl/davs2.git',
	'source_subfolder' : 'build/linux',
	'configure_options' : '{autconf_prefix_options} --cross-prefix={cross_prefix_bare} --disable-cli --disable-win32thread',
	'install_target' : 'install-lib-static',
	'_info' : { 'version' : None, 'fancy_name' : 'davs2' },
}