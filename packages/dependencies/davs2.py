{
	'repo_type' : 'git',
	'url' : 'https://github.com/pkuvcl/davs2.git',
	'source_subfolder' : 'build/linux',
	'configure_options' : '--prefix={target_prefix} --host={target_host} --cross-prefix={cross_prefix_bare} --disable-cli --disable-win32thread',
	'install_target' : 'install-lib-static',
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'davs2' },
}