{
	'repo_type' : 'archive',
	'download_locations' : [
		#UPDATECHECKS: https://sourceforge.net/projects/modplug-xmms/files/libmodplug/
		{ 'url' : 'https://ftp.openbsd.org/pub/OpenBSD/distfiles/libmodplug-0.8.9.0.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '457ca5a6c179656d66c01505c0d95fafaead4329b9dbaa0f997d00a3508ad9de' }, ], },
		{ 'url' : 'https://sourceforge.net/projects/modplug-xmms/files/libmodplug/0.8.9.0/libmodplug-0.8.9.0.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '457ca5a6c179656d66c01505c0d95fafaead4329b9dbaa0f997d00a3508ad9de' }, ], },
	],
	'configure_options' : '--host={target_host} --prefix={target_prefix} --enable-static --disable-shared',
	'run_post_install' : [
		# unfortunately this sed isn't enough, though I think it should be [so we add --extra-libs=-lstdc++ to FFmpegs configure] https://trac.ffmpeg.org/ticket/1539
		'sed -i.bak \'s/-lmodplug.*/-lmodplug -lstdc++/\' "{pkg_config_path}/libmodplug.pc"', # huh ?? c++?
		#'sed -i.bak 's/__declspec(dllexport)//' "{target_prefix}/include/libmodplug/modplug.h"', #strip DLL import/export directives
		#'sed -i.bak 's/__declspec(dllimport)//' "{target_prefix}/include/libmodplug/modplug.h"',
	],
	'_info' : { 'version' : '0.8.9.0', 'fancy_name' : 'libmodplug' },
}