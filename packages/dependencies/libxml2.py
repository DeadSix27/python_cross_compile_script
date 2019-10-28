{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'http://xmlsoft.org/sources/libxml2-2.9.10-rc1.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '913d85bf02ab22f07c76805522e013b7dfda7585dfe5addc465440880ef8cae5' }, ], },
		{ 'url' : 'https://fossies.org/linux/www/libxml2-2.9.10-rc1.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '913d85bf02ab22f07c76805522e013b7dfda7585dfe5addc465440880ef8cae5' }, ], },
	],
	'folder_name' : 'libxml2-2.9.10',
	'rename_folder' : 'libxml2-2.9.10-rc1',
	'configure_options' : '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static --without-python --enable-tests=no --enable-programs=no',
	# 'patches' : [ #todo remake this patch
		# ('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/libxml2/0001-libxml2-2.9.4-add_prog_test_toggle.patch', '-p1'),
	# ],
	'run_post_patch' : [
		'autoreconf -fiv',
	],
	'run_post_install' : [
		'sed -i.bak \'s/Libs: -L${{libdir}} -lxml2/Libs: -L${{libdir}} -lxml2 -lz -llzma -liconv -lws2_32/\' "{pkg_config_path}/libxml-2.0.pc"', # libarchive complaints without this.
	],
	'depends_on' : [
		'xz', 'iconv'
	],
	'update_check' : { 'url' : 'http://xmlsoft.org/sources/?C=M;O=D', 'type' : 'httpindex', 'regex' : r'libxml2-(?P<version_num>[\d.]+)-rc(?P<rc_num>[0-9]).tar.gz' },
	'_info' : { 'version' : '2.9.9.2', 'fancy_name' : 'libxml2' },
}