{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://ftp.gnu.org/pub/gnu/gettext/gettext-0.19.8.1.tar.xz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '105556dbc5c3fbbc2aa0edb46d22d055748b6f5c7cd7a8d99f8e7eb84e938be4' }, ], },
		{ 'url' : 'https://fossies.org/linux/misc/gettext-0.19.8.1.tar.xz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '105556dbc5c3fbbc2aa0edb46d22d055748b6f5c7cd7a8d99f8e7eb84e938be4' }, ], },
	],
	'configure_options' : '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static --enable-threads=posix --without-libexpat-prefix --without-libxml2-prefix CPPFLAGS=-DLIBXML_STATIC',
	'depends_on' : [ 'iconv' ],
	'update_check' : { 'url' : 'https://ftp.gnu.org/pub/gnu/gettext/?C=M;O=D', 'type' : 'httpindex', 'regex' : r'gettext-(?P<version_num>[\d.]+)\.tar\.xz' },
	'_info' : { 'version' : '0.19.8.1', 'fancy_name' : 'gettext' },
}