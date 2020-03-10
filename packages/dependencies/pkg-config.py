{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://pkg-config.freedesktop.org/releases/pkg-config-0.29.2.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '6fc69c01688c9458a57eb9a1664c9aba372ccda420a02bf4429fe610e7e7d591' }, ], },
		{ 'url' : 'https://fossies.org/linux/misc/pkg-config-0.29.2.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '6fc69c01688c9458a57eb9a1664c9aba372ccda420a02bf4429fe610e7e7d591' }, ], },
	],
	'env_exports' : { 'PKG_CONFIG_PATH' : '{local_pkg_config_path}', 'PATH' : '{local_path}' },
	'build_options' : 'V=1',
	'configure_options' : '--prefix={target_sub_prefix} --disable-shared --enable-static',
	'update_check' : { 'url' : 'https://pkg-config.freedesktop.org/releases/?C=M;O=D', 'type' : 'httpindex', 'regex' : r'pkg-config-(?P<version_num>[\d.]+)\.tar\.gz' },
	'_info' : { 'version' : '0.29.2', 'fancy_name' : 'pkg-config' },
}