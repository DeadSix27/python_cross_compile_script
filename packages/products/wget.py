{
	'repo_type' : 'git',
	'url' : 'https://git.savannah.gnu.org/git/wget.git',
	# 'branch' : 'tags/v1.19.1',
	'rename_folder' : 'wget_git',
	'recursive_git' : True,
	'configure_options' : '--target={bit_name2}-{bit_name_win}-gcc --host={target_host} --build=x86_64-linux-gnu --with-ssl=openssl --enable-nls --enable-dependency-tracking --with-metalink --prefix={output_prefix}/wget_git.installed --exec-prefix={output_prefix}/wget_git.installed',
	'cflag_addition' : ' -DIN6_ARE_ADDR_EQUAL=IN6_ADDR_EQUAL', #-DGNUTLS_INTERNAL_BUILD
	'patches' : [
		( 'wget/0001-remove-RAND_screen-which-doesn-t-exist-on-mingw.patch', '-p1' ),
		( 'wget/0001-wget-look-for-ca-bundle.trust.crt-in-exe-path-by-def.patch', '-p1' ),
		( 'wget/wget.timegm.patch', '-p1' ),
	],
	'run_post_install' : [
		'if [ -f "/etc/ssl/certs/ca-certificates.crt" ] ; then cp -v /etc/ssl/certs/ca-certificates.crt "{output_prefix}/wget_git.installed/bin/ca-bundle.trust.crt" ; fi',
	],
	'depends_on' : [
		'zlib', 'libressl', 'libpsl',
	],
	'_info' : { 'version' : None, 'fancy_name' : 'wget' },
}