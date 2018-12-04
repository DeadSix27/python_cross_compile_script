{
	'repo_type' : 'archive',
	'download_locations' : [
		#UPDATECHECKS: https://ftp.pcre.org/pub/pcre/
		{ 'url' : 'https://ftp.pcre.org/pub/pcre/pcre2-10.32.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '9ca9be72e1a04f22be308323caa8c06ebd0c51efe99ee11278186cafbc4fe3af' }, ], },
		{ 'url' : 'https://fossies.org/linux/misc/pcre2-10.32.tar.bz2', 'hashes' : [ { 'type' : 'sha256', 'sum' : '9ca9be72e1a04f22be308323caa8c06ebd0c51efe99ee11278186cafbc4fe3af' }, ], },
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
	'_info' : { 'version' : '10.32', 'fancy_name' : 'pcre2' },
}