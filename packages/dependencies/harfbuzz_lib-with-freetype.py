{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://www.freedesktop.org/software/harfbuzz/release/harfbuzz-2.4.0.tar.bz2', 'hashes' : [ { 'type' : 'sha256', 'sum' : '9035005903da74667d28bb181986e879e11da3d5986722759fa145cca781ead6' }, ], },
		{ 'url' : 'https://fossies.org/linux/misc/harfbuzz-2.4.0.tar.bz2', 'hashes' : [ { 'type' : 'sha256', 'sum' : '9035005903da74667d28bb181986e879e11da3d5986722759fa145cca781ead6' }, ], },
	],
	'run_post_install' : [
		'sed -i.bak \'s/Libs: -L${{libdir}} -lharfbuzz.*/Libs: -L${{libdir}} -lharfbuzz -lfreetype/\' "{pkg_config_path}/harfbuzz.pc"',
	],
	'folder_name' : 'harfbuzz-with-freetype',
	'rename_folder' : 'harfbuzz-with-freetype',
	'configure_options' : '--host={target_host} --prefix={target_prefix} --with-freetype --with-fontconfig=no --disable-shared --with-icu=no --with-glib=no --with-gobject=no --disable-gtk-doc-html',
	'update_check' : { 'url' : 'https://www.freedesktop.org/software/harfbuzz/release/?C=M;O=D', 'type' : 'httpindex', 'regex' : r'harfbuzz-(?P<version_num>[\d.]+)\.tar\.bz2' },
	'_info' : { 'version' : '2.4.0', 'fancy_name' : 'harfbuzz (with freetype2)' },
}