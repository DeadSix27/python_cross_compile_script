{
	'repo_type' : 'archive',
	'download_locations' : [
		#UPDATECHECKS: https://www.gnupg.org/ftp/gcrypt/gnutls/v3.6/
		{ "url" : "https://www.gnupg.org/ftp/gcrypt/gnutls/v3.6/gnutls-3.6.5.tar.xz", "hashes" : [ { "type" : "sha256", "sum" : "073eced3acef49a3883e69ffd5f0f0b5f46e2760ad86eddc6c0866df4e7abb35" }, ], },
		{ "url" : "https://fossies.org/linux/misc/gnutls-3.6.5.tar.xz", "hashes" : [ { "type" : "sha256", "sum" : "073eced3acef49a3883e69ffd5f0f0b5f46e2760ad86eddc6c0866df4e7abb35" }, ], },
	],
	'configure_options':
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
		# '--disable-guile '
		# '--disable-libdane '
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
	# 'configure_options':
		# '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static --with-included-unistring '
		# '--disable-rpath --disable-nls --disable-guile --disable-doc --disable-tests --enable-local-libopts --with-included-libtasn1 --with-libregex-libs="-lgnurx" --without-p11-kit --disable-silent-rules '
		# 'CPPFLAGS="-DWINVER=0x0501 -DAI_ADDRCONFIG=0x0400 -DIPV6_V6ONLY=27" LIBS="-lws2_32" ac_cv_prog_AR="{cross_prefix_full}ar"'
	# ,
	'run_post_install': [
		'sed -i.bak \'s/-lgnutls *$/-lgnutls -lnettle -lhogweed -lgmp -lcrypt32 -lws2_32 -liconv/\' "{pkg_config_path}/gnutls.pc"', #TODO -lintl
	],
	# 'patches' : [
		# ('https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/gnutls/0001-gnutls-3.5.11-arpainet_pkgconfig.patch', '-p1'),
		# ('https://raw.githubusercontent.com/Martchus/PKGBUILDs/master/gnutls/mingw-w64/gnutls-3.2.7-rpath.patch','-p1'),
		# ('https://raw.githubusercontent.com/Martchus/PKGBUILDs/master/gnutls/mingw-w64/gnutls-fix-external-libtasn1-detection.patch','-p1'),
	# ],
	'depends_on' : [
		'gmp',
		'libnettle',
	],
	# 'env_exports' : {
	'_info' : { 'version' : '3.6.5', 'fancy_name' : 'gnutls' },
}