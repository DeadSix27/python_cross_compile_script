{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://download.savannah.gnu.org/releases/freetype/freetype-2.13.0.tar.xz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '5ee23abd047636c24b2d43c6625dcafc66661d1aca64dec9e0d05df29592624c' }, ], },
		{ 'url' : 'https://sourceforge.net/projects/freetype/files/freetype2/2.13.0/freetype-2.13.0.tar.xz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '5ee23abd047636c24b2d43c6625dcafc66661d1aca64dec9e0d05df29592624c' }, ], },
		{ 'url' : 'https://fossies.org/linux/misc/freetype-2.13.0.tar.xz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '5ee23abd047636c24b2d43c6625dcafc66661d1aca64dec9e0d05df29592624c' }, ], },
	],
	#'custom_cflag' : '-O3',
	'folder_name' : 'freetype-with-harfbuzz',
	'rename_folder' : 'freetype-with-harfbuzz',
	'configure_options' : '{autoconf_prefix_options} --build=x86_64-linux-gnu --with-zlib={target_prefix} --with-zlib --without-png --with-harfbuzz=yes',
	'run_post_install' : [
		'sed -i.bak \'s/Libs: -L${{libdir}} -lfreetype.*/Libs: -L${{libdir}} -lfreetype -lbz2 -lharfbuzz/\' "{pkg_config_path}/freetype2.pc"',
	],
	'update_check' : { 'url' : 'https://sourceforge.net/projects/freetype/files/freetype2/', 'type' : 'sourceforge', },
	'_info' : { 'version' : '2.13.0', 'fancy_name' : 'freetype2' },
}