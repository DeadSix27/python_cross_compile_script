{
	'repo_type' : 'git',
	'url' : 'https://github.com/libarchive/libarchive.git',
	'configure_options' : '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static --disable-bsdtar --disable-bsdcat --disable-bsdcpio --without-openssl', #--without-xml2 --without-nettle
	'depends_on' : [
		'bzip2', 'expat', 'zlib', 'xz', 'lzo'
	],
	'regex_replace': {
		'post_install': [
			{
				0: r'^Libs: -L\${{libdir}} -larchive([^\n]+)?',
				1: r'Libs: -L${{libdir}} -larchive -lnettle -lxml2 -llzma -lbcrypt -lbz2 -lz -liconv -lws2_32\1',
				'in_file': '{pkg_config_path}/libarchive.pc'
			}
		]
	},
	'_info' : { 'version' : None, 'fancy_name' : 'libarchive' },
}