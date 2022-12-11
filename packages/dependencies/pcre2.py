{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://github.com/PCRE2Project/pcre2/releases/download/pcre2-10.40/pcre2-10.40.tar.bz2', 'hashes' : [ { 'type' : 'sha256', 'sum' : '14e4b83c4783933dc17e964318e6324f7cae1bc75d8f3c79bc6969f00c159d68' }, ], },
		{ 'url' : 'https://fossies.org/linux/misc/pcre2-10.40.tar.bz2 ', 'hashes' : [ { 'type' : 'sha256', 'sum' : '14e4b83c4783933dc17e964318e6324f7cae1bc75d8f3c79bc6969f00c159d68' }, ], },
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
	'update_check' : { 'url' : 'https://github.com/PCRE2Project/pcre2/releases', 'type' : 'githubreleases', 'name_or_tag' : 'name' },
	'_info' : { 'version' : '10.40', 'fancy_name' : 'pcre2' },
}