{
	'repo_type' : 'archive',
	# 'patches' : [
		# ('https://raw.githubusercontent.com/Alexpux/MINGW-packages/master/mingw-w64-icu/0012-libprefix.mingw.patch','-p1')
	# ],
	'url' : 'http://download.icu-project.org/files/icu4c/60.2/icu4c-60_2-src.tgz',
	'rename_folder': 'icu_60_1',
	'folder_name' : 'icu',
	'source_subfolder' : 'source',
	'configure_options': ' --host={target_host} --target={target_host} --prefix={target_prefix} --disable-shared --enable-static --with-cross-build=/xc/gcct/icu_native/source --with-data-packaging=library',
	'depends_on' : [ 'zlib', ],
	'_info' : { 'version' : '60_2', 'fancy_name' : 'icu' },
}