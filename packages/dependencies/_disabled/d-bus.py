{
	'repo_type' : 'archive',
	'download_locations' : [
		{ "url" : "https://dbus.freedesktop.org/releases/dbus/dbus-1.13.4.tar.gz", "hashes" : [ { "type" : "sha256", "sum" : "8a8f0b986ac6214da9707da521bea9f49f09610083c71fdc8eddf8b4c54f384b" }, ], },
		{ "url" : "https://fossies.org/linux/misc/dbus-1.13.4.tar.gz", "hashes" : [ { "type" : "sha256", "sum" : "8a8f0b986ac6214da9707da521bea9f49f09610083c71fdc8eddf8b4c54f384b" }, ], },
	],
	'configure_options' : '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static --with-xml=expat --disable-systemd --disable-tests --disable-Werror --disable-asserts --disable-verbose-mode --disable-xml-docs --disable-doxygen-docs --disable-ducktype-docs',
	'_info' : { 'version' : '1.13.4', 'fancy_name' : 'D-bus (Library)' },
}