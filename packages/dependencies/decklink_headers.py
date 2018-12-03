{
	'repo_type' : 'none',
	'folder_name' : 'decklink_headers',
	'run_post_patch' : [
		'if [ ! -f "already_done" ] ; then wget https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/additional_headers/DeckLinkAPI.h ; fi',
		'if [ ! -f "already_done" ] ; then wget https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/additional_headers/DeckLinkAPI_i.c ; fi',
		'if [ ! -f "already_done" ] ; then wget https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/additional_headers/DeckLinkAPIVersion.h ; fi',
		'if [ ! -f "already_done" ] ; then cp -fv "DeckLinkAPI.h" "{target_prefix}/include/DeckLinkAPI.h" ; fi',
		'if [ ! -f "already_done" ] ; then cp -fv "DeckLinkAPI_i.c" "{target_prefix}/include/DeckLinkAPI_i.c" ; fi',
		'if [ ! -f "already_done" ] ; then cp -fv "DeckLinkAPIVersion.h" "{target_prefix}/include/DeckLinkAPIVersion.h" ; fi',
		'if [ ! -f "already_done" ] ; then touch  "already_done" ; fi',
	],
	'needs_make' : False,
	'needs_make_install' : False,
	'needs_configure' : False,
	'_info' : { 'version' : '10.11.2', 'fancy_name' : 'Decklink SDK Headers' },
}