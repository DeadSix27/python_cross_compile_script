{
	'repo_type' : 'git',
	'url' : 'https://github.com/libass/libass.git',
	'configure_options' : '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static --enable-silent-rules',
	# 'run_post_install' : [
	#	'sed -i.bak \'s/-lass -lm/-lass -lfribidi -lfreetype -lm/\' "{pkg_config_path}/libass.pc"', #-lfontconfig
	# ],
	'depends_on' : [ 'fontconfig', 'freetype', 'iconv', 'libfribidi'],
	'_info' : { 'version' : None, 'fancy_name' : 'libass' },
}