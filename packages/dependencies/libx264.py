{
	'repo_type' : 'git',
	'url' : 'https://git.videolan.org/git/x264.git',
	'rename_folder' : 'libx264_git',
	'configure_options' : '--host={target_host} --enable-static --cross-prefix={cross_prefix_bare} --prefix={target_prefix} --enable-strip --disable-lavf --disable-cli',
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'x264 (library)' },
}