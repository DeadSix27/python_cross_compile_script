{
	'repo_type' : 'archive',
	'download_locations' : [
		#UPDATECHECKS https://www.freedesktop.org/software/harfbuzz/release/?C=M;O=D
		{ "url" : "https://www.freedesktop.org/software/harfbuzz/release/harfbuzz-2.2.0.tar.bz2", "hashes" : [ { "type" : "sha256", "sum" : "49b8d984d2e9a0157ffaf880d4bdeda4207aff6431d85303df77a0d4" }, ], },
		{ "url" : "https://fossies.org/linux/misc/harfbuzz-2.2.0.tar.bz2", "hashes" : [ { "type" : "sha256", "sum" : "49b8d984d2e9a0157ffaf880d4bdeda4207aff6431d85303df77a0d4" }, ], },
	],
	'run_post_install': [
		'sed -i.bak \'s/Libs: -L${{libdir}} -lharfbuzz.*/Libs: -L${{libdir}} -lharfbuzz -lfreetype/\' "{pkg_config_path}/harfbuzz.pc"',
	],
	'folder_name' : 'harfbuzz-with-freetype',
	'rename_folder' : 'harfbuzz-with-freetype',
	'configure_options': '--host={target_host} --prefix={target_prefix} --with-freetype --with-fontconfig=no --disable-shared --with-icu=no --with-glib=no --with-gobject=no --disable-gtk-doc-html',
	'_info' : { 'version' : '2.2.0', 'fancy_name' : 'harfbuzz (with freetype2)' },
}