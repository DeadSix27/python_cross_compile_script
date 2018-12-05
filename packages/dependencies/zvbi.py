{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://sourceforge.net/projects/zapping/files/zvbi/0.2.35/zvbi-0.2.35.tar.bz2', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'fc883c34111a487c4a783f91b1b2bb5610d8d8e58dcba80c7ab31e67e4765318' }, ], },
		{ 'url' : 'https://download.videolan.org/contrib/zvbi/zvbi-0.2.35.tar.bz2', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'fc883c34111a487c4a783f91b1b2bb5610d8d8e58dcba80c7ab31e67e4765318' }, ], },
	],
	'env_exports' : {
		'LIBS' : '-lpng',
	},
	'configure_options' : '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static --disable-dvb --disable-bktr --disable-nls --disable-proxy --without-doxygen',
	'make_subdir' : 'src',
	'patches' : [
		('zvbi/0001-zvbi-0.2.35_win32.patch', '-p1'),
		('zvbi/0002-zvbi-0.2.35_ioctl.patch', '-p1'),
	],
	#sed -i.bak 's/-lzvbi *$/-lzvbi -lpng/' "$PKG_CONFIG_PATH/zvbi.pc"
	'run_post_build' : [
		'pwd',
		'cp -rv "../zvbi-0.2.pc" "{target_prefix}/lib/pkgconfig/zvbi-0.2.pc"',
	],
	'update_check' : { 'url' : 'https://sourceforge.net/projects/zapping/files/zvbi/', 'type' : 'sourceforge', },
	'_info' : { 'version' : '0.2.35', 'fancy_name' : 'zvbi' },
}