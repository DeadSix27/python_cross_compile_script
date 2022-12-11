{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://download.savannah.gnu.org/releases/freetype/freetype-2.12.1.tar.xz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '4766f20157cc4cf0cd292f80bf917f92d1c439b243ac3018debf6b9140c41a7f' }, ], },
		{ 'url' : 'https://sourceforge.net/projects/freetype/files/freetype2/2.12.1/freetype-2.12.1.tar.xz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '4766f20157cc4cf0cd292f80bf917f92d1c439b243ac3018debf6b9140c41a7f' }, ], },
		{ 'url' : 'https://fossies.org/linux/misc/freetype-2.12.1.tar.xz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '4766f20157cc4cf0cd292f80bf917f92d1c439b243ac3018debf6b9140c41a7f' }, ], },
	],
	#'custom_cflag' : '-O3',
	'configure_options' : '{autoconf_prefix_options} --build=x86_64-linux-gnu --with-zlib={target_prefix} --with-zlib --without-png --with-harfbuzz=no', # TODO get rid of hardcoded build variable
	'update_check' : { 'url' : 'https://sourceforge.net/projects/freetype/files/freetype2/', 'type' : 'sourceforge', },
	'_info' : { 'version' : '2.12.1', 'fancy_name' : 'freetype2' },
}