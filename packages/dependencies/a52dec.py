{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'http://liba52.sourceforge.net/files/a52dec-0.7.4.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'a21d724ab3b3933330194353687df82c475b5dfb997513eef4c25de6c865ec33' }, ], },
		{ 'url' : 'https://gstreamer.freedesktop.org/src/mirror/a52dec-0.7.4.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'a21d724ab3b3933330194353687df82c475b5dfb997513eef4c25de6c865ec33' }, ], },
	],
	'configure_options' : '{autconf_prefix_options} CFLAGS=-std=gnu89',
	'run_post_patch' : [
		'rm configure',
	],
	'build_options' : 'bin_PROGRAMS= sbin_PROGRAMS= noinst_PROGRAMS=',
	'install_options' : 'bin_PROGRAMS= sbin_PROGRAMS= noinst_PROGRAMS=',
	'update_check' : { 'url' : 'http://liba52.sourceforge.net/', 'type' : 'httpregex', 'regex' : r'<a href="files\/a52dec-(?P<version_num>[\d.]+)\.tar\.gz">released<\/a>' },
	'_info' : { 'version' : '0.7.4', 'fancy_name' : 'a52dec' },
}