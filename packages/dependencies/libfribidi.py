{
	'repo_type' : 'git',
	'url' : 'https://github.com/fribidi/fribidi.git',
	#'depth_git': 0,
	#'branch': '85eb863a42bcf8636d1d865625ebfc3b4eb36577', # 2020.06.19 after 85eb863a42bcf8636d1d865625ebfc3b4eb36577 fribidi builds but ffmpeg can't find it
	'conf_system' : 'meson',
	'build_system' : 'ninja',
	'source_subfolder' : 'build',
	'env_exports' : { # 2020.06.19
		'CFLAGS'   : ' -DFRIBIDI_LIB_STATIC {original_cflags}',
		'CXXFLAGS' : ' -DFRIBIDI_LIB_STATIC {original_cflags}',
		'CPPFLAGS' : ' -DFRIBIDI_LIB_STATIC {original_cflags}', # 2020.06.20 per https://github.com/fribidi/fribidi/issues/146#issuecomment-646991416
		'LDFLAGS'  : ' -DFRIBIDI_LIB_STATIC {original_cflags}',
	},
	'configure_options' :
		'--prefix={target_prefix} '
		'--libdir={target_prefix}/lib '
		'--default-library=static '
		'--buildtype=plain '
		'--backend=ninja '
		'-Ddocs=false '
		'-Dbin=false ' 
		'-Dtests=false ' # 2020.07.07 per MABS
		#'-DFRIBIDI_LIB_STATIC=true ' # 2020.06.23 comment it out
		'--buildtype=release '
		'--cross-file={meson_env_file} ./ ..'
	,
	'update_check' : { 'type' : 'git', },
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'libfribidi' },
}