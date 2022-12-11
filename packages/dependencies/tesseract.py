{
	'repo_type' : 'git',
	'url' : 'https://github.com/tesseract-ocr/tesseract.git',
	'conf_system' : 'cmake',
	'branch': 'main',
	'source_subfolder' : '_build',
	'configure_options' : '.. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DBUILD_SHARED_LIBS=0 -DBUILD_TRAINING_TOOLS=0 -DSW_BUILD=0 -DBUILD_TRAINING_TOOLS=0 -DBUILD_TESTS=0 -DSTATIC=1 -DHAVE_LIBARCHIVE=1 -DLIBRARY_TYPE=STATIC -DCMAKE_BUILD_TYPE=Release',
	'regex_replace': {
		'post_patch': [
			{
				0: 
					r'    if\(LibArchive_FOUND\)\n'
				,
				1:
					r'    set(LibArchive_LIBRARIES "!CMD(pkg-config libarchive --libs-only-l)CMD!")\n'
					r'    message(STATUS "LibArchive Libs: ${{LibArchive_LIBRARIES}}")\n'
    				r'    if(LibArchive_FOUND)\n'
				,
				'in_file': '../CMakeLists.txt'
			},
			{
				0: r'set\(LIB_Ws2_32 Ws2_32\)',
				1: r'set(LIB_Ws2_32 ws2_32)',
				'in_file': '../CMakeLists.txt'
			},
			{
				0: r'add_executable\(tesseract src/tesseract.cpp\)',
				'in_file': '../CMakeLists.txt'
			},
			{
				0: r'install\(TARGETS tesseract DESTINATION bin\)',
				'in_file': '../CMakeLists.txt'
			},
			{
				0: r'target_link_libraries\(tesseract libtesseract\)',
				'in_file': '../CMakeLists.txt'
			},
			{
				0: r'if\(HAVE_TIFFIO_H AND WIN32\)',
				1: r'if(FALSE)',
				'in_file': '../CMakeLists.txt'
			}
			
		],
		'post_install': [
			{
				0: r'^(?:[\s]+)?Libs:(?:[\s]+)?-L\${{libdir}}(?:[\s]+)?(-ltesseract[0-9]{{2}})(?:[^\n]+)?$',
				1: r'Requires: lept libarchive\nRequires.private: lept libarchive\nLibs: -L${{libdir}} \1 -lstdc++ -lws2_32',
				'in_file': '{pkg_config_path}/tesseract.pc'
			}
		]
	},
	'depends_on' : [ 'leptonica', 'libxml2', 'zlib', 'libarchive', 'libtiff'],
	'_info' : { 'version' : None, 'fancy_name' : 'tesseract' },
}