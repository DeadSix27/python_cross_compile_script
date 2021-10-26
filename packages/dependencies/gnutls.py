{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://www.gnupg.org/ftp/gcrypt/gnutls/v3.6/gnutls-3.6.16.tar.xz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '1b79b381ac283d8b054368b335c408fedcb9b7144e0c07f531e3537d4328f3b3' }, ], },
		{ 'url' : 'https://fossies.org/linux/misc/gnutls-3.6.16.tar.xz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '1b79b381ac283d8b054368b335c408fedcb9b7144e0c07f531e3537d4328f3b3' }, ], },
	],
	'configure_options' :
		'--host={target_host} --prefix={target_prefix} --disable-shared --enable-static '
		'--disable-srp-authentication '
		'--disable-non-suiteb-curves '
		'--enable-cxx '
		'--enable-nls '
		'--disable-rpath '
		'--disable-gtk-doc '
		'--disable-guile '
		'--disable-doc '
		'--enable-local-libopts '
		'--disable-tools '
		'--disable-tests '
		'--with-zlib '
		'--with-included-libtasn1 '
		'--with-included-unistring '
		'--with-default-trust-store-file '
		'--with-default-blacklist-file '
		'--without-tpm '
		'--without-p11-kit'
	,
	'regex_replace': {
		'post_install': [
			{
				0: r'^(Libs: -L\${{libdir}} -lgnutls)([\n\r\s]+)?$',
				1: r'\1 -lnettle -lhogweed -lgmp -lcrypt32 -lws2_32 -lintl -liconv\2', # iconv is required by gettext, but gettext has no .pc file, so...
				'in_file': '{pkg_config_path}/gnutls.pc'
			},
		],
	},
	# 'patches' : [
		#('gnutls/rename-inet_pton_for_srt.diff', '-p1'),
		# ('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/gnutls/0001-gnutls-3.5.11-arpainet_pkgconfig.patch', '-p1'),
		# ('https://raw.githubusercontent.com/Martchus/PKGBUILDs/master/gnutls/mingw-w64/gnutls-3.2.7-rpath.patch','-p1'),
		# ('https://raw.githubusercontent.com/Martchus/PKGBUILDs/master/gnutls/mingw-w64/gnutls-fix-external-libtasn1-detection.patch','-p1'),
	# ],
	'depends_on' : [
		'gettext',
		'iconv',
		'libnettle',
		'zlib',
	],
	'update_check' : { 'url' : 'ftp://ftp.gnutls.org/gcrypt/gnutls/v3.6', 'type' : 'ftpindex', 'regex' : r'gnutls-(?P<version_num>[\d.]+)\.tar\.xz' },
	'_info' : { 'version' : '3.6.16', 'fancy_name' : 'gnutls' },
}