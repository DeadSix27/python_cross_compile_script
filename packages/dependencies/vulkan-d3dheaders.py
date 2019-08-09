{
	'repo_type' : 'none',
	'folder_name' : 'vulkan_d3dheaders',
	'run_post_patch' : [
		'if [ ! -f "already_done" ] ; then wget https://going.full.moe/d3dukmdt.h ; fi',
		'if [ ! -f "already_done" ] ; then wget https://going.full.moe/d3dkmthk.h ; fi',
		'if [ ! -f "already_done" ] ; then cp -fv "d3dkmthk.h" "{target_prefix}/include/d3dkmthk.h" ; fi',
		'if [ ! -f "already_done" ] ; then cp -fv "d3dukmdt.h" "{target_prefix}/include/d3dukmdt.h" ; fi',
		'if [ ! -f "already_done" ] ; then touch  "already_done" ; fi',
	],
	'needs_make' : False,
	'needs_make_install' : False,
	'needs_configure' : False,
	'_info' : { 'version' : '1.0', 'fancy_name' : 'Modified D3D headers from the Wine package to satisfy vulkan-icd compilation' },
}