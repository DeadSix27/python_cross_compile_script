{
	'repo_type' : 'git',
	'url' : 'https://github.com/aria2/aria2.git',
	#'env_exports' : {
	#	'LDFLAGS' : '-static',
	#	'LIBS' : '-static-libgcc -static-libstdc++ -lz -lole32',
	#},
	'configure_options':
		' --host={target_host} --prefix={output_prefix}/aria2_git.installed'
		' --without-included-gettext --disable-nls --disable-shared --enable-static' # --with-ca-bundle=ca-bundle.trust.crt
		' --without-openssl --with-libexpat --with-libz --with-libgmp --with-wintls'
		' --with-sqlite3 --with-libxml2 --without-gnutls --disable-silent-rules'
		' --with-cppunit-prefix={target_prefix} ARIA2_STATIC=yes'
	,	
	'patches' : [
		( 'aria2/aria2_timegm_workaround.patch', '-p1' ),
	],
    'regex_replace': {
        'pre_patch': [
            {
                0: r'SUBDIRS =  po lib deps src doc test',
                1: r'SUBDIRS =  po lib deps src',
                'in_file': 'Makefile.am',
            },
            {
                0: r'doc/Makefile',
                'in_file': 'configure.ac',
            },
            {
                0: r'doc/manual-src/Makefile',
                'in_file': 'configure.ac',
            },
            {
                0: r'doc/manual-src/en/Makefile',
                'in_file': 'configure.ac',
            },
            {
                0: r'doc/manual-src/en/conf.py',
                'in_file': 'configure.ac',
            },
            {
                0: r'doc/manual-src/ru/Makefile',
                'in_file': 'configure.ac',
            },
            {
                0: r'doc/manual-src/ru/conf.py',
                'in_file': 'configure.ac',
            },
            {
                0: r'doc/manual-src/pt/Makefile',
                'in_file': 'configure.ac',
            },
            {
                0: r'doc/manual-src/pt/conf.py',
                'in_file': 'configure.ac',
            },
        ],
    },

	'run_post_patch' : [
		('autoreconf -fiv', True),
		'autoreconf -fiv',
	],
	'run_post_install': [
		'{cross_prefix_bare}strip -v {output_prefix}/aria2_git.installed/bin/aria2c.exe',
	],
	'depends_on': [
		'zlib', 'libxml2', 'expat', 'gmp', 'sqlite3', 'libssh2', 'cppunit', #'gnutls', # 'c-ares', 'libsqlite3', 'openssl_1_1'
	],
	'_info' : { 'version' : None, 'fancy_name' : 'aria2' },
}