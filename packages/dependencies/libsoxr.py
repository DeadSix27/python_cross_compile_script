{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://download.videolan.org/contrib/soxr/soxr-0.1.3-Source.tar.xz', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'b111c15fdc8c029989330ff559184198c161100a59312f5dc19ddeb9b5a15889' }, ], },
		{ 'url' : 'https://sourceforge.net/projects/soxr/files/soxr-0.1.3-Source.tar.xz', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'b111c15fdc8c029989330ff559184198c161100a59312f5dc19ddeb9b5a15889' }, ], },
	],
	'conf_system' : 'cmake',
	'configure_options' : '. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DCMAKE_BUILD_TYPE=Release -DWITH_LSR_BINDINGS:bool=ON -DBUILD_LSR_TESTS:bool=OFF -DBUILD_EXAMPLES:bool=OFF -DBUILD_SHARED_LIBS:bool=off -DBUILD_TESTS:BOOL=OFF -DCMAKE_AR={cross_prefix_full}ar', #not sure why it cries about AR
	'update_check_url' : { 'url' : 'https://sourceforge.net/projects/soxr/files/', 'type' : 'sourceforge', },
	'_info' : { 'version' : '0.1.3', 'fancy_name' : 'soxr' },
}