#{
#	 # '_already_built' : True,
#	# 'warnings' : [
#		# 'Qt5 building CAN fail sometimes with multiple threads.. so if this failed try re-running it',
#		# 'For more information see: https://bugreports.qt.io/browse/QTBUG-53393',
#		# '(You could add 'cpu_count' : '1', to the config of QT5 if the slower speed is acceptable for you)',
#		# '---------------',
#		# 'Build needs around 40G, install around 10-15Gb.',
#		# 'Make sure you have at least 60GB free when building,',
#		# 'you can delete the entire source folder of qt after install to free space up again,',
#		# 'then just uncomment the "'_already_built' : True," line in the qt5 block, so building will be skipped each time.'
#	# ],
#	'env_exports' : {
#		# 'CFLAGS'   : '-DDBUS_STATIC_BUILD -DJAS_DLL=0',
#		#'CXXFLAGS' : '-DGRAPHITE2_STATIC',
#		'PKG_CONFIG' : '{cross_prefix_full}pkg-config',
#		# 'PKG_CONFIG_SYSROOT_DIR' : '/',
#		# 'PKG_CONFIG_LIBDIR' : '{target_prefix}/lib/pkgconfig',
#		'CROSS_COMPILE' : '{cross_prefix_bare}',
#		'CROSS_target_prefix' : '{target_sub_prefix}',
#		#'OPENSSL_LIBS' : '!CMD({cross_prefix_full}pkg-config --libs-only-l openssl)CMD!',
#	},
#	# 'cpu_count' : '1',
#	# 'clean_post_configure' : False,
#	'repo_type' : 'archive',
#	'url': 'https://download.qt.io/official_releases/qt/6.4/6.4.2/single/qt-everywhere-src-6.4.2.tar.xz',
#	'configure_options' :
#		'-prefix {target_sub_prefix} '
#		'-static '
#		'-release '
#		'-opensource '
#		'-confirm-license '
#		'-platform win32-g++ '
#		'-developer-build '
#		# '-c++11 '
#		'-icu '
#		'-opengl desktop '
#		'-openssl '
#		'-plugin-sql-odbc '
#		'-nomake tests '
#		'-cmake-generator ninja'
#		'-no-guess-compiler '
#		# ' -no-iconv'
#		# ' -no-sqlite'
#		# ' -skip qtconnectivity'
#		# ' -skip qtserialbus'
#		# ' -skip qtactiveqt'
#		# ' -skip qtdeclarative'
#		# ' -skip qttools'
#		# ' -release'
#		# ' -accessibility'
#		# ' -opengl desktop'
#		# ' -no-openssl'
#		#' -xplatform win32-g++'
#		# ' -xplatform mingw-w64-g++'
#		# ' -optimized-qmake'
#		# ' -verbose'
#		# ' -opensource'
#		# ' -confirm-license'
#		# ' -force-pkg-config'
#		# ' -force-debug-info'
#		# ' -system-zlib'
#		# ' -system-libpng'
#		# ' -system-libjpeg'
#		#' -system-sqlite'
#		#' -system-freetype'
#		# ' -system-harfbuzz'
#		# ' -no-direct2d'
#		# ' -system-pcre'
#		# ' -no-fontconfig'
#		#' -sql-mysql'
#		#' -sql-psql'
#		#' -sql-sqlite'
#		#' -dbus-linked'
#		# ' -no-glib'
#		# ' -no-icu'
#		#' -iconv'
#		# ' -nomake examples'
#		# ' -make tools'
#		# ' -hostprefix {target_sub_prefix}'
#		# ' -hostdatadir {target_sub_prefix}/lib/qt'
#		# ' -hostbindir {target_sub_prefix}/bin'
#		# ' -bindir {target_sub_prefix}/bin'
#		# ' -archdatadir {target_sub_prefix}/lib/qt'
#		# ' -datadir {target_sub_prefix}/share/qt'
#		# ' -docdir {target_sub_prefix}/share/doc/qt'
#		# ' -examplesdir {target_sub_prefix}/share/qt/examples'
#		# ' -headerdir {target_sub_prefix}/include/qt'
#		# ' -libdir {target_sub_prefix}/lib'
#		# ' -plugindir {target_sub_prefix}/lib/qt/plugins'
#		# ' -sysconfdir {target_sub_prefix}/etc'
#		# ' -translationdir {target_sub_prefix}/share/qt/translations'
#		# ' -device-option CROSS_COMPILE={cross_prefix_bare}'
#		# ' -device-option CROSS_target_prefix={target_sub_prefix}'
#		# ' -device-option CROSS_COMPILE_CFLAGS=-fpch-preprocess'
#		# ' -device-option CUSTOM_LIB_DIR={target_sub_prefix}/lib'
#		# ' -device-option CUSTOM_INC_DIR={target_sub_prefix}/include'
#	,
#	'depends_on' : [ 'libwebp', 'freetype', 'libpng', 'libjpeg-turbo', 'pcre2',],# 'd-bus', ],
#
#	'patches' : [
#	],
#	'_info' : { 'version' : '6', 'fancy_name' : 'QT6' },
#}


{
	'repo_type' : 'archive',
	'url': 'https://download.qt.io/official_releases/qt/6.4/6.4.2/submodules/qtbase-everywhere-src-6.4.2.tar.xz',
	'conf_system' : 'cmake',
	'source_subfolder' : '_build',
	# 'clean_post_configure' : False,
	'configure_options' : 
		'.. {cmake_prefix_options} '
		# '-DQT_BUILD_TOOLS_WHEN_CROSS_COMPILING=ON '
		# '-DQT_HOST_PATH={target_prefix}/qt6 '
		'-DQt6HostInfo_DIR=/usr/lib/cmake/Qt6HostInfo/ '
		'-DQt6CoreTools_DIR=/usr/lib/cmake/Qt6CoreTools/ '
		'-DQt6WidgetsTools_DIR=/usr/lib/cmake/Qt6WidgetsTools/ '
		'-DQt6GuiTools_DIR=/usr/lib/cmake/Qt6GuiTools/ '
		'-DQt6DBusTools_DIR=/usr/lib/cmake/Qt6DBusTools/ '
		# '-DQt6WidgetsTools_DIR=/usr/lib/cmake/Qt6WidgetsTools/ '
		# '-DQt6WidgetsTools_DIR=/usr/lib/cmake/Qt6WidgetsTools/ '
		'-DCMAKE_INSTALL_PREFIX={target_prefix} '
		'-DQT_BUILD_EXAMPLES=OFF '
		'-DQT_BUILD_TESTS=OFF '
	,
	'patches': [
		# ('196f295.diff', '-p1', '..'),
	],
	'_info' : { 'version' : None, 'fancy_name' : 'qt6' },

}