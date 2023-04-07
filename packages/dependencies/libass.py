{
	'repo_type' : 'git',
	'url' : 'https://github.com/libass/libass.git',
	'configure_options' : '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static --enable-silent-rules --enable-fontconfig',
	'env_exports' : { # 2020.06.19
		'CFLAGS'   : ' -DFRIBIDI_LIB_STATIC {original_cflags}',
		'CXXFLAGS' : ' -DFRIBIDI_LIB_STATIC {original_cflags}',
		'CPPFLAGS' : ' -DFRIBIDI_LIB_STATIC {original_cflags}', # 2020.06.20 per https://github.com/fribidi/fribidi/issues/146#issuecomment-646991416
		'LDFLAGS'  : ' -DFRIBIDI_LIB_STATIC {original_cflags}',
	},
    'run_post_install': [
		'sed -i.bak \'s/-lass -lm/-lass -lfribidi -lfreetype -lexpat -lm/\' "{pkg_config_path}/libass.pc"', #-lfontconfig # 2018.12.13
	],
	'depends_on' : [ 'expat', 'fontconfig', 'iconv', 'libfribidi'], 
	'update_check' : { 'type' : 'git', },
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'libass' },
}