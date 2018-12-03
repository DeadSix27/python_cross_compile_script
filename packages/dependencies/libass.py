{
	'repo_type' : 'git',
	'url' : 'https://github.com/libass/libass.git',
	# 'patches' : [
		# ( 'https://github.com/libass/libass/pull/298.patch' , '-p1' ), # Use FriBiDi 1.x API when available # for testing.
	# ],
	'configure_options': '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static --enable-silent-rules',
	'run_post_install': (
		'sed -i.bak \'s/-lass -lm/-lass -lfribidi -lfreetype -lexpat -lm/\' "{pkg_config_path}/libass.pc"', #-lfontconfig
	),
	'depends_on' : [ 'fontconfig', 'harfbuzz', 'libfribidi', 'freetype', 'iconv', ],
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'libass' },
}