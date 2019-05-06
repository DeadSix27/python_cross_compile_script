{
	'repo_type' : 'git',
	'url' : 'https://github.com/harfbuzz/harfbuzz',
	'branch' : '0d5fd168f8e3c1202358a82161a28e407149b1b4',
	'configure_options' : '--host={target_host} --prefix={target_prefix} --without-freetype --with-fontconfig=no --disable-shared --with-icu=no --with-glib=no --with-gobject=no --disable-gtk-doc-html', #--with-graphite2 --with-cairo --with-icu --with-gobject
	'update_check' : { 'url' : 'https://www.freedesktop.org/software/harfbuzz/release/?C=M;O=D', 'type' : 'httpindex', 'regex' : r'harfbuzz-(?P<version_num>[\d.]+)\.tar\.bz2' },
	'_info' : { 'version' : '2.4.0', 'fancy_name' : 'harfbuzz' },
}