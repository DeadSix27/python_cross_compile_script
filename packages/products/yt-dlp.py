{
	'repo_type' : 'git',
	'url' : 'https://github.com/yt-dlp/yt-dlp',
	'install_options' : 'yt-dlp DESTDIR="{output_prefix}/yt-dlp_git.installed"',
	'run_post_install' : [
		'if [ -f "{output_prefix}/yt-dlp_git.installed/bin/yt-dlp" ] ; then mv "{output_prefix}/yt-dlp_git.installed/bin/yt-dlp" "{output_prefix}/yt-dlp_git.installed/bin/yt-dlp.py" ; fi',
	],
	'build_options' : 'yt-dlp',
	'needs_configure' : False,
	'_info' : { 'version' : None, 'fancy_name' : 'yt-dlp' },
}