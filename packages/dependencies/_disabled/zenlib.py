{
	'repo_type' : 'git',
	# 'branch' : 'v0.4.35',
	'source_subfolder' : 'Project/GNU/Library',
	'url' : 'https://github.com/MediaArea/ZenLib.git',
	'configure_options' : '--host={target_host} --prefix={target_prefix} --enable-static --disable-shared --enable-shared=no',
	'run_post_configure' : [
		'sed -i.bak 's/ -DSIZE_T_IS_LONG//g' Makefile',
	],
	# 'patches' : (
		# ('fcurl_gitibzen-1-fixes.patch', '-p1','../../..'),
	# ),
	# 'run_post_patch' : [
		# 'sed -i.bak '/#include <windows.h>/ a\#include <time.h>' ../../../Source/ZenLib/Ztring.cpp',
	# ],
	'_info' : { 'version' : 'git (v4.35)', 'fancy_name' : 'zenlib' },
}