{
	'repo_type' : 'archive',
	'url' : 'https://downloads.sourceforge.net/project/freeglut/freeglut/3.0.0/freeglut-3.0.0.tar.gz',
	'configure_options': '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static',
	'configure_options': '. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DBUILD_SHARED_LIBS=OFF -DENABLE_STATIC_RUNTIME=ON -DFREEGLUT_GLES=OFF -DFREEGLUT_BUILD_DEMOS=OFF -DFREEGLUT_REPLACE_GLUT=ON -DFREEGLUT_BUILD_STATIC_LIBS=ON -DFREEGLUT_BUILD_SHARED_LIBS=OFF',
	'conf_system' : 'cmake',
	'_info' : { 'version' : '3.0', 'fancy_name' : 'FreeGLUT (libary?)' },
}