{
	'repo_type' : 'git',
	'url' : 'https://github.com/cacalabs/libcaca.git',
	'run_post_configure' : [
		'sed -i.bak "s/int vsnprintf/int vnsprintf_disabled/" "caca/string.c"',
		'sed -i.bak "s/int vsnprintf/int vnsprintf_disabled/" "caca/figfont.c"',
		'sed -i.bak "s/__declspec(dllexport)//g" cxx/caca++.h',
		'sed -i.bak "s/__declspec(dllexport)//g" caca/caca.h',
		'sed -i.bak "s/__declspec(dllexport)//g" caca/caca0.h',
		'sed -i.bak "s/__declspec(dllimport)//g" caca/caca.h',
		'sed -i.bak "s/__declspec(dllimport)//g" caca/caca0.h',
	],
	'run_post_install' : [
		"sed -i.bak 's/-lcaca *$/-lcaca -lz/' \"{pkg_config_path}/caca.pc\"",
	],
	'configure_options' : '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static --libdir={target_prefix}/lib --disable-cxx --disable-csharp --disable-java --disable-python --disable-ruby --disable-imlib2 --disable-doc --disable-examples',
	'_info' : { 'version' : None, 'fancy_name' : 'libcaca' },
}