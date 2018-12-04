{
	'repo_type' : 'git',
	'url' : 'https://github.com/pkuvcl/xavs2.git',
	'source_subfolder' : 'build/linux',
	'configure_options' : '--prefix={target_prefix} --host={target_host} --cross-prefix={cross_prefix_bare} --disable-cli',
	'install_target' : 'install-lib-static',
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'xavs2' },
}