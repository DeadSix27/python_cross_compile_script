{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://ftp.gnu.org/pub/gnu/gettext/gettext-0.21.1.tar.xz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '50dbc8f39797950aa2c98e939947c527e5ac9ebd2c1b99dd7b06ba33a6767ae6' }, ], },
		{ 'url' : 'https://fossies.org/linux/misc/gettext-0.21.1.tar.xz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '50dbc8f39797950aa2c98e939947c527e5ac9ebd2c1b99dd7b06ba33a6767ae6' }, ], },
	],
	'configure_options' : '{autoconf_prefix_options} CPPFLAGS=-DLIBXML_STATIC',
    
	'regex_replace': {
		'post_patch': [
			{
				0: r'SUBDIRS = gnulib-local gettext-runtime libtextstyle gettext-tools',
				1: r'SUBDIRS = gnulib-local gettext-runtime libtextstyle',
				'in_file': 'Makefile.am'
			},
			{
				0: r'gettext-runtime libtextstyle gettext-tools',
				1: r'gettext-runtime libtextstyle',
				'in_file': 'configure.ac'
			},
		],
	},
    
	'run_post_regexreplace' : [
		'autoreconf -fiv',
	],
    
	'depends_on' : [ 'iconv' ],
	#'custom_cflag' : '-O3',
	'update_check' : { 'url' : 'https://ftp.gnu.org/pub/gnu/gettext/?C=M;O=D', 'type' : 'httpindex', 'regex' : r'gettext-(?P<version_num>[\d.]+)\.tar\.xz' },
	'_info' : { 'version' : '0.21.1', 'fancy_name' : 'gettext' },
}