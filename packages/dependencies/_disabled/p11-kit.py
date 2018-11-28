{
	'repo_type' : 'archive',
	'needs_make_install' : False,
	'url' : 'hhttps://github.com/p11-glue/p11-kit/releases/download/0.23.9/p11-kit-0.23.9.tar.gz',
	'configure_options': '--host={target_host} --prefix={target_prefix}',
	'depends_on' : [ 'libtasn1', 'libffi' ],
	'env_exports' : {
		'LIBS' : '-liconv' # Otherwise: libcrypto.a(e_capi.o):e_capi.c:(.text+0x476d): undefined reference to `__imp_CertFreeCertificateContext'
	},
	'_info' : { 'version' : '0.23.9', 'fancy_name' : 'p11-kit' },
}