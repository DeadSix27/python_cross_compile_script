{
	# 'debug_downloadonly': True,
	'repo_type' : 'git',
	# 'branch' : 'v0.7.94',
	'source_subfolder' : 'Project/GNU/Library',
	'rename_folder' : 'mediainfo_dll',
	'url' : 'https://github.com/MediaArea/MediaInfoLib.git',
	'configure_options' : '--host={target_host} --target={bit_name2}-{bit_name_win}-gcc --prefix={product_prefix}/mediainfo_dll.installed --enable-static --disable-shared', # --enable-static --disable-shared --enable-shared=no
	'run_post_patch' : [
		'sed -i.bak \'s/Windows.h/windows.h/\' ../../../Source/MediaInfo/Reader/Reader_File.h',
		'sed -i.bak \'s/Windows.h/windows.h/\' ../../../Source/MediaInfo/Reader/Reader_File.cpp',
	],
	'run_post_configure' : [
		'sed -i.bak \'s/ -DSIZE_T_IS_LONG//g\' Makefile',
	],
	'build_options': '{make_prefix_options}',
	'depends_on': [
		'zenlib', 'libcurl',
	],
	# 'patches' : [
		# ('libmediainfo-1-fixes.patch','-p1', '../../..'),
	# ],
	'env_exports' : { 'PKG_CONFIG' : 'pkg-config' },
	#'_info' : { 'version' : 'git (master)', 'fancy_name' : 'MediaInfoDLL' },
}