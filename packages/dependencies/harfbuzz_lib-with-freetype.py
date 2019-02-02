{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://www.freedesktop.org/software/harfbuzz/release/harfbuzz-2.3.1.tar.bz2', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'f205699d5b91374008d6f8e36c59e419ae2d9a7bb8c5d9f34041b9a5abcae468' }, ], },
		{ 'url' : 'https://fossies.org/linux/misc/harfbuzz-2.3.1.tar.bz2', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'f205699d5b91374008d6f8e36c59e419ae2d9a7bb8c5d9f34041b9a5abcae468' }, ], },
	],
	'run_post_install' : [
		'sed -i.bak \'s/Libs: -L${{libdir}} -lharfbuzz.*/Libs: -L${{libdir}} -lharfbuzz -lfreetype/\' "{pkg_config_path}/harfbuzz.pc"',
	],
	'folder_name' : 'harfbuzz-with-freetype',
	'rename_folder' : 'harfbuzz-with-freetype',
	'configure_options' : '--host={target_host} --prefix={target_prefix} --with-freetype --with-fontconfig=no --disable-shared --with-icu=no --with-glib=no --with-gobject=no --disable-gtk-doc-html',
	'update_check' : { 'url' : 'https://www.freedesktop.org/software/harfbuzz/release/?C=M;O=D', 'type' : 'httpindex', 'regex' : r'harfbuzz-(?P<version_num>[\d.]+)\.tar\.bz2' },
	'_info' : { 'version' : '2.3.1', 'fancy_name' : 'harfbuzz (with freetype2)' },
}