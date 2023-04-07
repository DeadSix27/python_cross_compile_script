{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://github.com/PCRE2Project/pcre2/releases/download/pcre2-10.42/pcre2-10.42.tar.bz2', 'hashes' : [ { 'type' : 'sha256', 'sum' : '8d36cd8cb6ea2a4c2bb358ff6411b0c788633a2a45dabbf1aeb4b701d1b5e840' }, ], },
		{ 'url' : 'https://fossies.org/linux/misc/pcre2-10.42.tar.bz2 ', 'hashes' : [ { 'type' : 'sha256', 'sum' : '8d36cd8cb6ea2a4c2bb358ff6411b0c788633a2a45dabbf1aeb4b701d1b5e840' }, ], },
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
	'_info' : { 'version' : '10.42', 'fancy_name' : 'pcre2' },
}