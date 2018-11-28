{
	'repo_type' : 'archive',
	'download_locations' : [
		#UPDATECHECKS: http://xmlsoft.org/sources/?C=M;O=D
		{ "url" : "http://xmlsoft.org/sources/libxml2-2.9.8.tar.gz", "hashes" : [ { "type" : "sha256", "sum" : "0b74e51595654f958148759cfef0993114ddccccbb6f31aee018f3558e8e2732" }, ], },
		{ "url" : "https://fossies.org/linux/www/libxml2-2.9.8.tar.gz", "hashes" : [ { "type" : "sha256", "sum" : "0b74e51595654f958148759cfef0993114ddccccbb6f31aee018f3558e8e2732" }, ], },
	],
	'folder_name' : 'libxml2-2.9.8',
	'rename_folder' : 'libxml2-2.9.8-rc1',
	'configure_options': '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static --without-python --enable-tests=no --enable-programs=no',
	# 'patches' : [ #todo remake this patch
		# ('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/libxml2/0001-libxml2-2.9.4-add_prog_test_toggle.patch', '-p1'),
	# ],
	'run_post_patch' : [
		'autoreconf -fiv',
	],
	'run_post_install' : (
		'sed -i.bak \'s/Libs: -L${{libdir}} -lxml2/Libs: -L${{libdir}} -lxml2 -lz -llzma -liconv -lws2_32/\' "{pkg_config_path}/libxml-2.0.pc"', # libarchive complaints without this.
	),
	'depends_on': [
		'xz', 'iconv'
	],
	'_info' : { 'version' : '2.9.8-rc1', 'fancy_name' : 'libxml2' },
}