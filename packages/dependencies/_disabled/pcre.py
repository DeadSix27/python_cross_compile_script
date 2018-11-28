{
	'repo_type' : 'archive',
	'url' : 'https://ftp.pcre.org/pub/pcre/pcre-8.41.tar.gz',
	'configure_options' : '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static --enable-unicode-properties --enable-jit --enable-pcre16 --enable-pcre32 --enable-pcregrep-libz --enable-pcregrep-libbz2',
	'depends_on' : [
		'bzip2',
	],
	'_info' : { 'version' : '8.41', 'fancy_name' : 'pcre' },
}