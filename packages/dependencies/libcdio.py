{
	'repo_type' : 'git',
	'url' : 'https://git.savannah.gnu.org/git/libcdio.git',
	'configure_options' : '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static --disable-cddb --enable-cpp-progs', #  --enable-maintainer-mode
	'run_post_patch' : [
		'touch doc/version.texi', # took me far to long to come up with and find this workaround
		'touch src/cd-info.1 src/cd-drive.1 src/iso-read.1 src/iso-info.1 src/cd-read.1', # .....
		#'if [ ! -f "configure" ] ; then ./autogen.sh ; fi',
		#'make -C doc stamp-vti', # idk why it needs this... odd thing: https://lists.gnu.org/archive/html/libcdio-devel/2016-03/msg00007.html
	],
	'_info' : { 'version' : None, 'fancy_name' : 'libcdio' },
}