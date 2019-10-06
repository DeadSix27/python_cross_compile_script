{
	'repo_type' : 'git',
	'recursive_git' : True,
	'build_system' : 'rake',
	'url' : 'https://gitlab.com/mbunkus/mkvtoolnix.git',
	'configure_options':
		'--host={target_host} --prefix={product_prefix}/mkvtoolnix_git.installed --disable-shared --enable-static'
		' --with-boost={target_prefix} --with-boost-system=boost_system --with-boost-filesystem=boost_filesystem --with-boost-date-time=boost_date_time --with-boost-regex=boost_regex --enable-optimization --enable-qt --enable-static-qt'
		' --with-moc={mingw_binpath2}/moc --with-uic={mingw_binpath2}/uic --with-rcc={mingw_binpath2}/rcc --with-qmake={mingw_binpath2}/qmake'
		#' QT_LIBS="-lws2_32 -lprcre"'
	,
	'build_options': '-v',
	'depends_on' : [
		'cmark', 'libfile', 'libflac', 'boost', 'gettext'
	],
	'packages': {
		'ubuntu' : [ 'xsltproc', 'docbook-utils', 'rake', 'docbook-xsl' ],
	},
	'run_post_install': (
		'{cross_prefix_bare}strip -v {product_prefix}/mkvtoolnix_git.installed/bin/mkvmerge.exe',
		# '{cross_prefix_bare}strip -v {product_prefix}/mkvtoolnix_git.installed/bin/mkvtoolnix-gui.exe',
		'{cross_prefix_bare}strip -v {product_prefix}/mkvtoolnix_git.installed/bin/mkvextract.exe',
		# '{cross_prefix_bare}strip -v {product_prefix}/mkvtoolnix_git.installed/bin/mkvinfo-gui.exe',
		'{cross_prefix_bare}strip -v {product_prefix}/mkvtoolnix_git.installed/bin/mkvpropedit.exe',
		'{cross_prefix_bare}strip -v {product_prefix}/mkvtoolnix_git.installed/bin/mkvinfo.exe',
	),
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'mkvtoolnix' },

}