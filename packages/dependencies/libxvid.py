{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'http://downloads.xvid.org/downloads/xvidcore-1.3.5.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '165ba6a2a447a8375f7b06db5a3c91810181f2898166e7c8137401d7fc894cf0' }, ], },
		{ 'url' : 'https://fossies.org/linux/misc/xvidcore-1.3.5.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '165ba6a2a447a8375f7b06db5a3c91810181f2898166e7c8137401d7fc894cf0' }, ], },
	],
	'folder_name' : 'xvidcore',
	'rename_folder' : 'xvidcore-1.3.5',
	'source_subfolder' : 'build/generic',
	'configure_options' : '{autconf_prefix_options}',
	# 'cpu_count' : '1',
	'run_post_configure' : [
		'sed -i.bak "s/-mno-cygwin//" platform.inc',
	],
	'run_post_install' : [
		'rm -v {target_prefix}/lib/xvidcore.dll.a',
		'mv -v {target_prefix}/lib/xvidcore.a {target_prefix}/lib/libxvidcore.a',
	],
	# 'update_check' : { 'url' : 'https://fossies.org/search?q=folder_search&q1=xvidcore&rd=%2Ffresh%2F&sd=0&ud=%2F&ap=no&ca=no&dp=0&si=0&sn=1&ml=30&dml=3', 'type' : 'httpregex', 'regex' : r'.*\/xvidcore-(?P<version_num>[\d.]+)\.tar\.gz.*' },
	'_info' : { 'version' : '1.3.5', 'fancy_name' : 'xvidcore' },
}