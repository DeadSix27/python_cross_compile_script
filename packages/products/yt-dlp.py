{
	'repo_type' : 'git',
	'url' : 'https://github.com/yt-dlp/yt-dlp',
	'install_options' : 'yt-dlp DESTDIR="{output_prefix}/yt-dlp_git.installed"',
	'build_options' : 'yt-dlp',
	'run_post_build' : [
		'mkdir -pv "{output_prefix}/yt-dlp_git.installed/bin"',
		'cp -v yt-dlp "{output_prefix}/yt-dlp_git.installed/bin"',
	],
	'needs_configure' : False,
	'needs_make_install' : False,
	'_info' : { 'version' : None, 'fancy_name' : 'yt-dlp' },
}