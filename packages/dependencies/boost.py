{
	'repo_type' : 'archive',
	'download_locations' : [
		{ 'url' : 'https://dl.bintray.com/boostorg/release/1.71.0/source/boost_1_71_0.tar.bz2', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'd73a8da01e8bf8c7eda40b4c84915071a8c8a0df4a6734537ddde4a8580524ee' }, ], },
		{ 'url' : 'https://fossies.org/linux/misc/boost_1.71.0.tar.bz2', 'hashes' : [ { 'type' : 'sha256', 'sum' : 'd73a8da01e8bf8c7eda40b4c84915071a8c8a0df4a6734537ddde4a8580524ee' }, ], },
	],
	'needs_make' :False,
	'needs_make_install' :False,
	'needs_configure' :False,
	'run_post_patch' : [
		'if [ ! -f "already_configured_0" ] ; then ./bootstrap.sh mingw --prefix={target_prefix} ; fi',
		'if [ ! -f "already_configured_0" ] ; then sed -i.bak \'s/case \*       : option = -pthread ; libs = rt ;/case *      : option = -pthread ;/\' tools/build/src/tools/gcc.jam ; fi',
		'if [ ! -f "already_configured_0" ] ; then touch already_configured_0 ; fi',
		'if [ ! -f "already_ran_make_0" ] ; then echo "using gcc : mingw : {cross_prefix_bare}g++ : <rc>{cross_prefix_bare}windres <archiver>{cross_prefix_bare}ar <ranlib>{cross_prefix_bare}ranlib ;" > user-config.jam ; fi',
		'if [ ! -f "already_ran_make_0" ] ; then ./b2 toolset=gcc-mingw link=static threading=multi target-os=windows address-model=64 architecture=x86 --prefix={target_prefix} variant=release --with-system --with-filesystem --with-regex --with-date_time --with-thread --user-config=user-config.jam install ; fi',
		'if [ ! -f "already_ran_make_0" ] ; then touch already_ran_make_0 ; fi',
	],
	'update_check' : { 'url' : 'https://sourceforge.net/projects/boost/files/boost/', 'type' : 'sourceforge', 'regex' : r'(?P<version_num>[\d.]+)\.beta\.(?P<rc_num>[0-9])', },
	'_info' : { 'version' : '1.71.0', 'fancy_name' : 'Boost' },
}