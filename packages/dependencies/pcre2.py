{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://ftp.pcre.org/pub/pcre/pcre2-10.32.tar.bz2', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'f29e89cc5de813f45786580101aaee3984a65818631d4ddbda7b32f699b87c2e' }, ], },
		{ 'url' : 'https://fossies.org/linux/misc/pcre2-10.32.tar.bz2', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'f29e89cc5de813f45786580101aaee3984a65818631d4ddbda7b32f699b87c2e' }, ], },
	],
	'conf_system' : 'cmake',
	'patches' : [
		('pcre2/0001-pcre2-iswild.patch', '-p1'),
	],
	'configure_options' : '. {cmake_prefix_options} '
		'-DCMAKE_INSTALL_PREFIX={target_prefix} -DBUILD_SHARED_LIBS=OFF -DCMAKE_BUILD_TYPE=Release -DPCRE2_BUILD_TESTS=OFF '
		'-DPCRE2_BUILD_PCRE2_8=ON -DPCRE2_BUILD_PCRE2_16=ON -DPCRE2_BUILD_PCRE2_32=ON -DPCRE2_NEWLINE=ANYCRLF '
		'-DPCRE2_SUPPORT_UNICODE=ON -DPCRE2_SUPPORT_JIT=ON'
	,
	'depends_on' : [
		'bzip2', 'zlib',
	],
	'update_check' : { 'url' : 'ftp://ftp.pcre.org/pub/pcre/', 'type' : 'ftpindex', 'regex' : r'pcre2-(?P<version_num>[\d.]+)\.tar\.bz2' },
	'_info' : { 'version' : '10.32', 'fancy_name' : 'pcre2' },
}