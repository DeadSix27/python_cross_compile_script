{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://ftp.gnu.org/pub/gnu/libiconv/libiconv-1.16.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'e6a1b1b589654277ee790cce3734f07876ac4ccfaecbee8afa0b649cf529cc04' }, ], },
		{ 'url' : 'https://fossies.org/linux/misc/libiconv-1.16.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'e6a1b1b589654277ee790cce3734f07876ac4ccfaecbee8afa0b649cf529cc04' }, ], },
	],
	# CFLAGS=-O2
	'configure_options' : '{autoconf_prefix_options} --disable-nls --enable-extra-encodings',
	'update_check' : { 'url' : 'https://ftp.gnu.org/pub/gnu/libiconv/?C=M;O=D', 'type' : 'httpindex', 'regex' : r'libiconv-(?P<version_num>[\d.]+)\.tar\.gz' },
	'_info' : { 'version' : '1.16', 'fancy_name' : 'libiconv' },
}