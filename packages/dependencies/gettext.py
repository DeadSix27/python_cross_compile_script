{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://ftp.gnu.org/pub/gnu/gettext/gettext-0.21.tar.xz', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'd20fcbb537e02dcf1383197ba05bd0734ef7bf5db06bdb241eb69b7d16b73192' }, ], },
		{ 'url' : 'https://fossies.org/linux/misc/gettext-0.21.tar.xz', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'd20fcbb537e02dcf1383197ba05bd0734ef7bf5db06bdb241eb69b7d16b73192' }, ], },
	],
	'configure_options' : '{autoconf_prefix_options} --enable-threads=posix --without-libexpat-prefix --without-libxml2-prefix CPPFLAGS=-DLIBXML_STATIC',
	'depends_on' : [ 'iconv' ],
	'update_check' : { 'url' : 'https://ftp.gnu.org/pub/gnu/gettext/?C=M;O=D', 'type' : 'httpindex', 'regex' : r'gettext-(?P<version_num>[\d.]+)\.tar\.xz' },
	'_info' : { 'version' : '0.21', 'fancy_name' : 'gettext' },
}