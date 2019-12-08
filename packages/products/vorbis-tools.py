{
	'repo_type' : 'git',
	'url' : 'https://github.com/xiph/vorbis-tools.git',
	'configure_options' : '--host={target_host} --prefix={output_prefix}/vorbis-tools_git.installed --disable-shared --enable-static --without-libintl-prefix',
	'patches' : [
		('vorbis-tools/vorbis_tools_odd_locale.patch','-p1'),
	],
	'depends_on' : [
		'libvorbis',
	],
	'_info' : { 'version' : None, 'fancy_name' : 'vorbis-tools' },
}