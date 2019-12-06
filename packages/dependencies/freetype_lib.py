{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://download.savannah.gnu.org/releases/freetype/freetype-2.10.1.tar.xz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '16dbfa488a21fe827dc27eaf708f42f7aa3bb997d745d31a19781628c36ba26f' }, ], },
		{ 'url' : 'https://sourceforge.net/projects/freetype/files/freetype2/2.10.1/freetype-2.10.1.tar.xz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '16dbfa488a21fe827dc27eaf708f42f7aa3bb997d745d31a19781628c36ba26f' }, ], },
		{ 'url' : 'https://fossies.org/linux/misc/freetype-2.10.1.tar.xz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '16dbfa488a21fe827dc27eaf708f42f7aa3bb997d745d31a19781628c36ba26f' }, ], },
	],
	'configure_options' : '{autoconf_prefix_options} --build=x86_64-linux-gnu --with-zlib={target_prefix} --without-png --with-harfbuzz=no', # TODO get rid of hardcoded build variable
	'update_check' : { 'url' : 'https://sourceforge.net/projects/freetype/files/freetype2/', 'type' : 'sourceforge', },
	'_info' : { 'version' : '2.10.1', 'fancy_name' : 'freetype2' },
}