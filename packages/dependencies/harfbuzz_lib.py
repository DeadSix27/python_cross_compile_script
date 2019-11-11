{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://www.freedesktop.org/software/harfbuzz/release/harfbuzz-2.6.4.tar.xz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '9413b8d96132d699687ef914ebb8c50440efc87b3f775d25856d7ec347c03c12' }, ], },
		{ 'url' : 'https://fossies.org/linux/misc/harfbuzz-2.6.4.tar.xz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '9413b8d96132d699687ef914ebb8c50440efc87b3f775d25856d7ec347c03c12' }, ], },
	],
	'configure_options' : '--host={target_host} --prefix={target_prefix} --without-freetype --with-fontconfig=no --disable-shared --with-icu=no --with-glib=no --with-gobject=no --disable-gtk-doc-html', #--with-graphite2 --with-cairo --with-icu --with-gobject
	'update_check' : { 'url' : 'https://www.freedesktop.org/software/harfbuzz/release/?C=M;O=D', 'type' : 'httpindex', 'regex' : r'harfbuzz-(?P<version_num>[\d.]+)\.tar\.bz2' },
	'_info' : { 'version' : '2.6.4', 'fancy_name' : 'harfbuzz' },
}