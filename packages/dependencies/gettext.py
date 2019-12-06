{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://ftp.gnu.org/pub/gnu/gettext/gettext-0.20.1.tar.xz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '53f02fbbec9e798b0faaf7c73272f83608e835c6288dd58be6c9bb54624a3800' }, ], },
		{ 'url' : 'https://fossies.org/linux/misc/gettext-0.20.1.tar.xz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '53f02fbbec9e798b0faaf7c73272f83608e835c6288dd58be6c9bb54624a3800' }, ], },
	],
	'configure_options' : '{autoconf_prefix_options} --enable-threads=posix --without-libexpat-prefix --without-libxml2-prefix CPPFLAGS=-DLIBXML_STATIC',
	'depends_on' : [ 'iconv' ],
	'update_check' : { 'url' : 'https://ftp.gnu.org/pub/gnu/gettext/?C=M;O=D', 'type' : 'httpindex', 'regex' : r'gettext-(?P<version_num>[\d.]+)\.tar\.xz' },
	'_info' : { 'version' : '0.20.1', 'fancy_name' : 'gettext' },
}