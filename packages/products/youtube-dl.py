{
	'repo_type' : 'git',
	'url' : 'https://github.com/rg3/youtube-dl.git',
	'install_options' : 'youtube-dl PREFIX="{output_prefix}/youtube-dl_git.installed"',
	'run_post_patch' : [
		'sed -i.bak \'s/pandoc.*/touch youtube-dl.1/g\' Makefile', # "disables" doc, the pandoc requirement is so annoyingly big..
	],
	'run_post_install' : [
		'if [ -f "{output_prefix}/youtube-dl_git.installed/bin/youtube-dl" ] ; then mv "{output_prefix}/youtube-dl_git.installed/bin/youtube-dl" "{output_prefix}/youtube-dl_git.installed/bin/youtube-dl.py" ; fi',
	],
	'build_options' : 'youtube-dl',
	'patches' : [
		( 'https://github.com/DeadSix27/youtube-dl/commit/4a386648cf85511d9eb283ba488858b6a5dc2444.patch', '-p1' ),
	],
	'needs_configure' : False,
	'_info' : { 'version' : None, 'fancy_name' : 'youtube-dl' },
}