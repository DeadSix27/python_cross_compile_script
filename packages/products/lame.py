{
	# 'debug_downloadonly': True,
	'repo_type' : 'archive',
	'download_locations' : [
		#UPDATECHECKS: https://sourceforge.net/projects/lame/files/lame/
		{ 'url' : 'https://sourceforge.net/projects/lame/files/lame/3.100/lame-3.100.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'ddfe36cab873794038ae2c1210557ad34857a4b6bdc515785d1da9e175b1da1e' }, ], },
		{ 'url' : 'https://fossies.org/linux/misc/lame-3.100.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'ddfe36cab873794038ae2c1210557ad34857a4b6bdc515785d1da9e175b1da1e' }, ], },
	],
	'patches' : [
		('lame/0007-revert-posix-code.patch','-p1'), # borrowing their file since lame will fix this shortly anyway, its already fixed on svn
	],
	'depends_on' : ['iconv'],
	'configure_options' : '--host={target_host} --without-libiconv-prefix --prefix={product_prefix}/lame-3.100.installed --disable-shared --enable-static --enable-nasm',
	'_info' : { 'version' : '3.10', 'fancy_name' : 'LAME3' },
}