{
	'repo_type' : 'git',
	'depth_git': 0,
	'url' : 'https://git.savannah.gnu.org/git/readline.git',
	'branch': 'readline-8.2',
	'patches': [
		# ('https://aur.archlinux.org/cgit/aur.git/plain/fix_signal.diff?h=mingw-w64-readline', '-p1'),
		('readline.patch','-p1'),
	],
	'configure_options': '{autoconf_prefix_options} --enable-multibyte --without-purify --with-curses',
	'_info' : { 'version' : None, 'fancy_name' : 'cppunit' },
}