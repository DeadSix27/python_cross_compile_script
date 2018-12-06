{
	'repo_type' : 'git',
	'url' : 'https://github.com/libssh2/libssh2.git',
	'configure_options' :
		'--host={target_host} '
		'--prefix={target_prefix} '
		'--disable-shared '
		'--enable-static '
		'--disable-examples-build '
		# '--with-crypto=openssl'
	,
	'depends_on' : [
		'zlib', #'libressl'
	],
	'env_exports' : {
		'LIBS' : '-lcrypt32' # Otherwise: libcrypto.a(e_capi.o):e_capi.c:(.text+0x476d): undefined reference to `__imp_CertFreeCertificateContext'
	},
	'_info' : { 'version' : None, 'fancy_name' : 'libssh2' },
}