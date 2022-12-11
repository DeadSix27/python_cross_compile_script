{
	'repo_type' : 'git',
	'url' : 'https://github.com/OpenVisualCloud/SVT-AV1.git',
	'conf_system' : 'cmake',
	'source_subfolder' : '_build',
	#'custom_cflag' : '-D_FORTIFY_SOURCE=0',
	'configure_options' : '.. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DBUILD_SHARED_LIBS=OFF -DCPPAN_BUILD=OFF -DCMAKE_BUILD_TYPE=Release',
	'run_post_patch' : [
		'sed -i.bak \'s/#include <Windows.h>/#include <windows.h>/\' ../Source/App/EncApp/EbAppMain.c',
		'sed -i.bak \'s/#include <Windows.h>/#include <windows.h>/\' ../Source/Lib/Common/Codec/EbThreads.h',
		'sed -i.bak \'s/-D_FORTIFY_SOURCE=2/-D_FORTIFY_SOURCE=0/\' ../CMakeLists.txt',
		'sed -i.bak \'s/-D_FORTIFY_SOURCE=2/-D_FORTIFY_SOURCE=0/\' ../gstreamer-plugin/CMakeLists.txt',
	],
	'_info' : { 'version' : None, 'fancy_name' : 'SVT-AV1' },
}