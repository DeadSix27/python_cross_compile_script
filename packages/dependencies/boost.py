{
	'repo_type' : 'archive',
	'download_locations' : [
		#UPDATECHECKS: https://sourceforge.net/projects/boost/files/boost/
		{ "url" : "https://sourceforge.net/projects/boost/files/boost/1.68.0/boost_1_68_0.tar.bz2", "hashes" : [ { "type" : "sha256", "sum" : "7f6130bc3cf65f56a618888ce9d5ea704fa10b462be126ad053e80e553d6d8b7" }, ], },
		{ "url" : "https://fossies.org/linux/misc/boost_1_68_0.tar.bz2", "hashes" : [ { "type" : "sha256", "sum" : "7f6130bc3cf65f56a618888ce9d5ea704fa10b462be126ad053e80e553d6d8b7" }, ], },
	],
	'needs_make':False,
	'needs_make_install':False,
	'needs_configure':False,
	'run_post_patch': (
		'if [ ! -f "already_configured_0" ] ; then ./bootstrap.sh mingw --prefix={target_prefix} ; fi',
		'if [ ! -f "already_configured_0" ] ; then sed -i.bak \'s/case \*       : option = -pthread ; libs = rt ;/case *      : option = -pthread ;/\' tools/build/src/tools/gcc.jam ; fi',
		'if [ ! -f "already_configured_0" ] ; then touch already_configured_0 ; fi',
		'if [ ! -f "already_ran_make_0" ] ; then echo "using gcc : mingw : {cross_prefix_bare}g++ : <rc>{cross_prefix_bare}windres <archiver>{cross_prefix_bare}ar <ranlib>{cross_prefix_bare}ranlib ;" > user-config.jam ; fi',
		'if [ ! -f "already_ran_make_0" ] ; then ./b2 toolset=gcc-mingw link=static threading=multi target-os=windows address-model=64 architecture=x86 --prefix={target_prefix} variant=release --with-system --with-filesystem --with-regex --with-date_time --with-thread --user-config=user-config.jam install ; fi',
		'if [ ! -f "already_ran_make_0" ] ; then touch already_ran_make_0 ; fi',
	),
	'_info' : { 'version' : '1.68.0', 'fancy_name' : 'Boost' },
}