{
	'repo_type' : 'archive',
	'url' : 'https://github.com/wxWidgets/wxWidgets/releases/download/v3.1.1/wxWidgets-3.1.1.tar.bz2',
	'configure_options':
		' --host={target_host} --build=x86_64-unknown-linux-gnu --prefix={target_sub_prefix} --disable-shared --enable-static --build='
		' --with-msw --with-opengl --disable-mslu --enable-unicode --with-regex=builtin --disable-precomp-headers'
		' --enable-graphics_ctx --enable-webview --enable-mediactrl --with-libpng=sys --with-libxpm=builtin --with-libjpeg=sys'
		' --with-libtiff=builtin --without-mac --without-dmalloc --without-wine --with-sdl --with-themes=all --disable-stl --enable-threads --enable-gui'
	,
	# 'run_post_install' : [
	# 	'cp -fv "{target_sub_prefix}/bin/wxrc-3.0" "{target_sub_prefix}/bin/wxrc"',
	# ],
	# 'patches' : [
	# 	('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/wxwidgets/0001-wxWidgets-c++11-PR2222.patch','-p1'),
	# ],
	# 'env_exports': {
	# 	'CXXFLAGS' : '-std=gnu++11',
	# 	'CXXCPP' : '{cross_prefix_bare}g++ -E -std=gnu++11',
	# },
	'_info' : { 'version' : '3.1.1', 'fancy_name' : 'wxWidgets (libary)' },
	'depends_on' : [ 'libjpeg-turbo', 'libpng', 'zlib' ],
}