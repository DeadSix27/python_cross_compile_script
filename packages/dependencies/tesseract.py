{
	'repo_type' : 'git',
	'url' : 'https://github.com/tesseract-ocr/tesseract.git',
	'conf_system' : 'cmake',
	'source_subfolder' : '_build',
	'configure_options' : '.. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DBUILD_SHARED_LIBS=0 -DBUILD_TRAINING_TOOLS=0 -DSW_BUILD=0 -DBUILD_TESTS=0 -DSTATIC=1 -DHAVE_LIBARCHIVE=0 -DLIBRARY_TYPE=STATIC -DCMAKE_BUILD_TYPE=Release',
	'depends_on' : [ 'leptonica', 'libxml2' ],
	'run_post_patch' : [
		'sed -i.bak \'s/set(LIB_Ws2_32 Ws2_32)/set(LIB_Ws2_32 ws2_32)/\' ../CMakeLists.txt',
		'sed -i.bak \'s/find_package(LibArchive)/#find_package(LibArchive)/\' ../CMakeLists.txt',
	],
	'env_exports' : {
		'LDFLAGS' :
			'-L/home/vm/python_cross_compile_script/workdir/toolchain/x86_64-w64-mingw32/x86_64-w64-mingw32/lib',
		'LDLIBS' :
			'-lnettle -lxml2 -lz -liconv -lws2_32 -lbcrypt -lbz2 -llzma',
	},
	'custom_cflag' : '-O3',
	'patches' : [
		('tesseract/lzma_workaround.diff', '-p1', '..'),
	],
	'regex_replace': {
		'post_install': [
			{
				0: r'^(?:[\s]+)?Libs:(?:[\s]+)?-L\${{libdir}}(?:[\s]+)?(-ltesseract[0-9]{{2}})(?:[^\n]+)?$',
				1: r'Requires: lept\nRequires.private: lept\nLibs: -L${{libdir}} \1 -lstdc++ -lws2_32',
				'in_file': '{pkg_config_path}/tesseract.pc'
			}
		]
	},
	# 'run_post_install' : [
		# 'sed -i.bak \'s/set(LIB_Ws2_32 Ws2_32)/set(LIB_Ws2_32 ws2_32)/\' ../CMakeLists.txt',
	# ],
	'_info' : { 'version' : None, 'fancy_name' : 'tesseract' },
}