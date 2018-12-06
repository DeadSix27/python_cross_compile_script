{
	'repo_type' : 'git',
	'recursive_git' : True,
	'url' : 'https://git.videolan.org/git/libbluray.git',
	'configure_options' : '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static --disable-examples --disable-doxygen-doc --disable-bdjava-jar --enable-udf', #--without-libxml2 --without-fontconfig .. optional.. I guess
	'patches' : [
		('libbluray/libbluray_git_remove_strtok_s.patch', '-p1'),
	],
	'run_post_install' : [
		'sed -i.bak \'s/-lbluray.*$/-lbluray -lfreetype -lexpat -lz -lbz2 -lxml2 -lws2_32 -lgdi32 -liconv/\' "{pkg_config_path}/libbluray.pc"', # fix undefined reference to `xmlStrEqual' and co
	],
	'depends_on' : [
		'freetype', 'libcdio-paranoia'
	],
	'_info' : { 'version' : None, 'fancy_name' : 'libbluray' },
}