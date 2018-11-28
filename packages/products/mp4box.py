{
	'repo_type' : 'git',
	'url' : 'https://github.com/gpac/gpac.git',
	'rename_folder' : 'mp4box_git',
	'do_not_bootstrap' : True,
	'run_post_patch' : [
		'sed -i.bak \'s/has_dvb4linux="yes"/has_dvb4linux="no"/g\' configure',
		'sed -i.bak \'s/targetos=`uname -s`/targetos=MINGW64/g\' configure',
		'sed -i.bak \'s/extralibs="-lm"/extralibs=""/g\' configure',
		'sed -i.bak \'s/SHFLAGS=-shared/SHFLAGS=/g\' configure',
		'sed -i.bak \'s/extralibs="$extralibs -lws2_32 -lwinmm -limagehlp"/extralibs="$extralibs -lws2_32 -lwinmm -lz"/g\' configure',
	],
	'configure_options': '--host={target_host} --target-os={bit_name3} --prefix={product_prefix}/mp4box_git.installed --static-modules --cross-prefix={cross_prefix_bare} --static-mp4box --enable-static-bin --disable-oss-audio --disable-x11 --disable-docs --sdl-cfg={cross_prefix_full}sdl2-config --disable-shared --enable-static',
	'depends_on': [
		 'sdl2', 'libffmpeg',
	],
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'mp4box' },
}