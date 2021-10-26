{
	'repo_type' : 'mercurial',
	'url' : 'http://hg.videolan.org/x265/',
	'rename_folder' : 'libx265_hg_multibit',
	'source_subfolder' : '_build',
	'configure_options' :
		'../source {cmake_prefix_options} '
		'-DCMAKE_AR={cross_prefix_full}ar '
		'-DENABLE_ASSEMBLY=ON '
		'-DENABLE_SHARED=OFF '
		'-DENABLE_CLI:BOOL=OFF '
		'-DEXTRA_LIB="x265_main10.a;x265_main12.a" '
		'-DEXTRA_LINK_FLAGS="-L{offtree_prefix}/libx265_10bit/lib;-L{offtree_prefix}/libx265_12bit/lib" '
		'-DLINKED_10BIT=ON '
		'-DLINKED_12BIT=ON '
		'-DCMAKE_INSTALL_PREFIX={target_prefix}'
	,
	'conf_system' : 'cmake',
	'run_post_build' : [
		'mv -fv libx265.a libx265_main.a',
		'cp -fv {offtree_prefix}/libx265_10bit/lib/libx265_main10.a libx265_main10.a',
		'cp -fv {offtree_prefix}/libx265_12bit/lib/libx265_main12.a libx265_main12.a',
		"\"{cross_prefix_full}ar\" -M <<EOF\nCREATE libx265.a\nADDLIB libx265_main.a\nADDLIB libx265_main10.a\nADDLIB libx265_main12.a\nSAVE\nEND\nEOF",
	],
	'run_post_install' : [
		'sed -i.bak \'s|-lmingwex||g\' "{pkg_config_path}/x265.pc"',
	],
	'depends_on' : [ 'libxml2', 'libx265_multibit_10', 'libx265_multibit_12' ],
	'_info' : { 'version' : None, 'fancy_name' : 'x265 (multibit library 12/10/8)' },
}