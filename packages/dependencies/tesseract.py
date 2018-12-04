{
	'repo_type' : 'git',
	'url' : 'https://github.com/tesseract-ocr/tesseract.git',
	'conf_system' : 'cmake',
	'source_subfolder' : '_build',
	'configure_options' : '.. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DBUILD_SHARED_LIBS=0 -DBUILD_TRAINING_TOOLS=0 -DBUILD_TESTS=0 -DSTATIC=1 -DLIBRARY_TYPE=STATIC -DCMAKE_BUILD_TYPE=Release',
	'depends_on' : [ 'leptonica' ],
	'run_post_patch' : [
		'sed -i.bak \'s/set(LIB_Ws2_32 Ws2_32)/set(LIB_Ws2_32 ws2_32)/\' ../CMakeLists.txt',
	],
	'run_post_install' : [
		'sed -i.bak \'s/set(LIB_Ws2_32 Ws2_32)/set(LIB_Ws2_32 ws2_32)/\' ../CMakeLists.txt',
		'sed -i.bak \'s/Libs: -L${{libdir}} -ltesseract40*$/Requires.private: lept\\nLibs: -L${{libdir}} -ltesseract40 -lstdc++ -lws2_32/\' "{pkg_config_path}/tesseract.pc"',
	],
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'tesseract' },
}