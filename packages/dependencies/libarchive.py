{
	'repo_type' : 'git',
	'url' : 'https://github.com/libarchive/libarchive.git',
    'branch': 'v3.6.2',
	'depth_git': 0,
	'conf_system' : 'cmake',
	'source_subfolder' : '_build',
	#'custom_cflag' : '-O3',
	'configure_options' : '.. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DBUILD_SHARED_LIBS=0 -DCMAKE_BUILD_TYPE=Release '
		'-DENABLE_NETTLE=ON '
		'-DENABLE_OPENSSL=OFF '
		'-DENABLE_LIBB2=ON '
		'-DENABLE_LZ4=ON '
		'-DENABLE_LZO=ON '
		'-DENABLE_LZMA=ON '
		'-DENABLE_ZSTD=ON '
		'-DENABLE_ZLIB=OFF '
		'-DZLIB_WINAPI_EXITCODE=0 '
		'-DZLIB_WINAPI_EXITCODE__TRYRUN_OUTPUT="" '
		'-DENABLE_BZip2=ON '
		'-DENABLE_LIBXML2=ON '
		'-DENABLE_EXPAT=ON '
		'-DENABLE_LibGCC=ON '
		'-DENABLE_CNG=ON '
		'-DENABLE_TAR=ON '
		'-DENABLE_TAR_SHARED=OFF '
		'-DENABLE_CPIO=ON '
		'-DENABLE_CPIO_SHARED=OFF '
		'-DENABLE_CAT=ON '
		'-DENABLE_CAT_SHARED=OFF '
		'-DENABLE_XATTR=ON '
		'-DENABLE_ACL=ON '
		'-DENABLE_ICONV=ON '
		'-DENABLE_TEST=OFF '
		'-DENABLE_COVERAGE=OFF '
		'-DLIBXML2_LIBRARIES="-lxml2 -lz -llzma -liconv -lws2_32"'
	,
	'depends_on' : [
		'bzip2', 'expat', 'zlib', 'xz', 'lzo',
	],
	'patches': [
		('libarchive/0001-libarchive-mingw-workaround.patch', '-p1', '..')
	],
	'regex_replace': {
		'post_install': [
			{
				0: r'^Libs: -L\${{libdir}} -larchive([^\n]+)?',
				1: r'Libs: -L${{libdir}} -larchive -lxml2 -llzma -lbcrypt -lbz2 -lz -liconv -lcharset -llzo2 -lws2_32\1',
				'in_file': '{pkg_config_path}/libarchive.pc'
			},
			{
				0: r'Libs.private:  [^\n]+',
				1: r'Libs.private: -lxml2 -llzma -lbcrypt -lbz2 -lz -liconv -lcharset -llzo2 -lws2_32',
				'in_file': '{pkg_config_path}/libarchive.pc'
			}
		]
	},
	'_info' : { 'version' : None, 'fancy_name' : 'libarchive' },
}