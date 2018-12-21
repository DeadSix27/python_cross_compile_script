{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://www.freedesktop.org/software/harfbuzz/release/harfbuzz-2.3.0.tar.bz2', 'hashes' : [ { 'type' : 'sha256', 'sum' : '3b314db655a41d19481e18312465fa25fca6f63382217f08062f126059f96764' }, ], },
		{ 'url' : 'https://fossies.org/linux/misc/harfbuzz-2.3.0.tar.bz2', 'hashes' : [ { 'type' : 'sha256', 'sum' : '3b314db655a41d19481e18312465fa25fca6f63382217f08062f126059f96764' }, ], },
	],
	'run_post_install' : [
		'sed -i.bak \'s/Libs: -L${{libdir}} -lharfbuzz.*/Libs: -L${{libdir}} -lharfbuzz -lfreetype/\' "{pkg_config_path}/harfbuzz.pc"',
	],
	'folder_name' : 'harfbuzz-with-freetype',
	'rename_folder' : 'harfbuzz-with-freetype',
	'configure_options' : '--host={target_host} --prefix={target_prefix} --with-freetype --with-fontconfig=no --disable-shared --with-icu=no --with-glib=no --with-gobject=no --disable-gtk-doc-html',
	'update_check' : { 'url' : 'https://www.freedesktop.org/software/harfbuzz/release/?C=M;O=D', 'type' : 'httpindex', 'regex' : r'harfbuzz-(?P<version_num>[\d.]+)\.tar\.bz2' },
	'_info' : { 'version' : '2.3.0', 'fancy_name' : 'harfbuzz (with freetype2)' },
}