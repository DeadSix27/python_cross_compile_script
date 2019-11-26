{
	'repo_type' : 'git',
	'url' : 'https://github.com/libarchive/libarchive.git',
	'configure_options' : '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static --disable-bsdtar --disable-bsdcat --disable-bsdcpio --without-openssl', #--without-xml2 --without-nettle
	'depends_on' : [
		'bzip2', 'expat', 'zlib', 'xz', 'lzo'
	],
	'run_post_install' : [
		'sed -i.bak \'s/Libs: -L${{libdir}} -larchive/Libs: -L${{libdir}} -larchive -llzma -lbcrypt -lz/\' "{pkg_config_path}/libarchive.pc"', # libarchive complaints without this.
	],
	'_info' : { 'version' : None, 'fancy_name' : 'libarchive' },
}