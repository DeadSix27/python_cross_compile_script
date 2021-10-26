{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://download.savannah.gnu.org/releases/freetype/freetype-2.11.0.tar.xz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '8bee39bd3968c4804b70614a0a3ad597299ad0e824bc8aad5ce8aaf48067bde7' }, ], },
		{ 'url' : 'https://sourceforge.net/projects/freetype/files/freetype2/2.11.0/freetype-2.11.0.tar.xz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '8bee39bd3968c4804b70614a0a3ad597299ad0e824bc8aad5ce8aaf48067bde7' }, ], },
		{ 'url' : 'https://fossies.org/linux/misc/freetype-2.11.0.tar.xz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '8bee39bd3968c4804b70614a0a3ad597299ad0e824bc8aad5ce8aaf48067bde7' }, ], },
	],
	'folder_name' : 'freetype-with-harfbuzz',
	'rename_folder' : 'freetype-with-harfbuzz',
	'configure_options' : '{autoconf_prefix_options} --build=x86_64-linux-gnu --with-zlib={target_prefix} --without-png --with-harfbuzz=yes',
	'run_post_install' : [
		'sed -i.bak \'s/Libs: -L${{libdir}} -lfreetype.*/Libs: -L${{libdir}} -lfreetype -lbz2 -lharfbuzz/\' "{pkg_config_path}/freetype2.pc"',
	],
	'update_check' : { 'url' : 'https://sourceforge.net/projects/freetype/files/freetype2/', 'type' : 'sourceforge', },
	'_info' : { 'version' : '2.11.0', 'fancy_name' : 'freetype2' },
}