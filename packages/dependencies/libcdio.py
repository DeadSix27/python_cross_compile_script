{
	'repo_type' : 'git',
	'url' : 'git://git.savannah.gnu.org/libcdio.git', # old: http://git.savannah.gnu.org/cgit/libcdio.git/snapshot/libcdio-release-0.94.tar.gz
	'configure_options': '--host={target_host} --prefix={target_prefix} --disable-cddb --enable-cpp-progs --disable-shared --enable-static', #  --enable-maintainer-mode
	'run_post_patch' : (
		'touch doc/version.texi', # took me far to long to come up with and find this workaround
		'touch src/cd-info.1 src/cd-drive.1 src/iso-read.1 src/iso-info.1 src/cd-read.1', # .....
		#'if [ ! -f "configure" ] ; then ./autogen.sh ; fi',
		#'make -C doc stamp-vti', # idk why it needs this... odd thing: https://lists.gnu.org/archive/html/libcdio-devel/2016-03/msg00007.html
	),
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'libcdio' },
}