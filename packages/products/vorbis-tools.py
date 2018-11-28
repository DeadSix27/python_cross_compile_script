{
	'repo_type' : 'git',
	'url' : 'https://github.com/xiph/vorbis-tools.git',
	'configure_options': '--host={target_host} --prefix={product_prefix}/vorbis-tools_git.installed --disable-shared --enable-static --without-libintl-prefix',
	'patches' : (
		('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/vorbis_tools_odd_locale.patch','-p1'),
	),
	'depends_on': [
		'libvorbis',
	],
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'vorbis-tools' },
}