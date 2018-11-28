{
	'repo_type' : 'git',
	'rename_folder' : 'sox_git',
	'url' : 'git://git.code.sf.net/p/sox/code',
	'configure_options': '--host={target_host} --prefix={product_prefix}/sox_git.installed --disable-shared --enable-static --without-gsm',
	'run_post_patch' : (
		'autoreconf -fiv',
		'if [ -f "{target_prefix}/lib/libgsm.a" ] ; then mv {target_prefix}/lib/libgsm.a {target_prefix}/lib/libgsm.a.disabled ; fi',
		'if [ -d "{target_prefix}/include/gsm" ] ; then mv {target_prefix}/include/gsm {target_prefix}/include/gsm.disabled ; fi',
	),
	'run_post_install' : (
		'if [ -f "{target_prefix}/lib/libgsm.a.disabled" ] ; then mv {target_prefix}/lib/libgsm.a.disabled {target_prefix}/lib/libgsm.a ; fi',
		'if [ -d "{target_prefix}/include/gsm.disabled" ] ; then mv {target_prefix}/include/gsm.disabled {target_prefix}/include/gsm ; fi',
	),
	'depends_on': [
		'libvorbis','gettext',
	],
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'SoX' },
}