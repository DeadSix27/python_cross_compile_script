{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://downloads.xvid.com/downloads/xvidcore-1.3.6.tar.bz2', 'hashes' : [ { 'type' : 'sha256', 'sum' : '5e6b58b13c247fe7a9faf9b95517cc52bc4b59a44b630cab20aae0c7f654f77e' }, ], },
		{ 'url' : 'https://fossies.org/linux/misc/xvidcore-1.3.6.tar.bz2', 'hashes' : [ { 'type' : 'sha256', 'sum' : '5e6b58b13c247fe7a9faf9b95517cc52bc4b59a44b630cab20aae0c7f654f77e' }, ], },
	],
	'folder_name' : 'xvidcore',
	'rename_folder' : 'xvidcore-1.3.6',
	'source_subfolder' : 'build/generic',
	'configure_options' : '--host={target_host} --prefix={target_prefix}',
	# 'run_post_configure' : [
	# 	'sed -i.bak "s/-mno-cygwin//" platform.inc',
	# ],
	'run_post_install' : [
		'rm -v {target_prefix}/lib/xvidcore.dll.a',
		'mv -v {target_prefix}/lib/xvidcore.a {target_prefix}/lib/libxvidcore.a',
	],
	# last i checked their website (xvid one) had some shitty DDoS protection or w/e, which needs shitty JS to verify, so no way to parse the site.
	# and fossies site changes a lot, maybe if i feel like it ill re-add the check
	# 'update_check' : { 'url' : 'https://fossies.org/search?q=folder_search&q1=xvidcore&rd=%2Ffresh%2F&sd=0&ud=%2F&ap=no&ca=no&dp=0&si=0&sn=1&ml=30&dml=3', 'type' : 'httpregex', 'regex' : r'.*\/xvidcore-(?P<version_num>[\d.]+)\.tar\.gz.*' },
	'_info' : { 'version' : '1.3.6', 'fancy_name' : 'xvidcore' },
}