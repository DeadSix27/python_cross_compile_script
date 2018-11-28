{
	'repo_type' : 'archive',
	'download_locations' : [
		#UPDATECHECKS https://www.freedesktop.org/software/harfbuzz/release/?C=M;O=D
		{ "url" : "https://www.freedesktop.org/software/harfbuzz/release/harfbuzz-2.1.3.tar.bz2", "hashes" : [ { "type" : "sha256", "sum" : "613264460bb6814c3894e3953225c5357402915853a652d40b4230ce5faf0bee" }, ], },
		{ "url" : "https://fossies.org/linux/misc/harfbuzz-2.1.3.tar.bz2", "hashes" : [ { "type" : "sha256", "sum" : "613264460bb6814c3894e3953225c5357402915853a652d40b4230ce5faf0bee" }, ], },
	],
	'run_post_install': [
		'sed -i.bak \'s/Libs: -L${{libdir}} -lharfbuzz.*/Libs: -L${{libdir}} -lharfbuzz -lfreetype/\' "{pkg_config_path}/harfbuzz.pc"',
	],
	'folder_name' : 'harfbuzz-with-freetype',
	'rename_folder' : 'harfbuzz-with-freetype',
	'configure_options': '--host={target_host} --prefix={target_prefix} --with-freetype --with-fontconfig=no --disable-shared --with-icu=no --with-glib=no --with-gobject=no --disable-gtk-doc-html',
	'_info' : { 'version' : '2.1.3', 'fancy_name' : 'harfbuzz (with freetype2)' },
}