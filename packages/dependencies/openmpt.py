#type:ignore
{
	'repo_type' : 'git',
	'url' : 'https://github.com/OpenMPT/openmpt.git',
	# 'source_subfolder' : '_build',
	'needs_configure' : False,
	'build_options' : 'PREFIX=/xc/workdir/toolchain/x86_64-w64-mingw32/x86_64-w64-mingw32 CONFIG=mingw-w64 OPTIMIZE=vectorize OPENMPT123=0 VERBOSE=1 TEST=0 SHARED_LIB=0 SHARED_SONAME=0 DYNLINK=0 STATIC_LIB=1 EXAMPLES=0 MODERN=1',
	'install_options' : 'PREFIX=/xc/workdir/toolchain/x86_64-w64-mingw32/x86_64-w64-mingw32 CONFIG=mingw-w64 OPTIMIZE=vectorize OPENMPT123=0 VERBOSE=1 TEST=0 SHARED_LIB=0 SHARED_SONAME=0 DYNLINK=0 STATIC_LIB=1 EXAMPLES=0 MODERN=1 PREFIX={target_prefix}',
	# 'configure_path' : '../build/autotools/configure',
	# 'run_post_patch' : [
		# '!SWITCHDIR|../build/autotools',
		# 'autoreconf -fiv',
		# '!SWITCHDIR|../../_build',
	# ],
	# 'configure_options' : '--prefix={target_prefix} --host={target_host}',

	# 'run_post_patch' : [
	# 	'cp -fv {cross_prefix_full}ld {mingw_binpath}/ld',
	# ],
	# 'run_post_install' : [
	# 	'rm -v {mingw_binpath}/ld',
	# ],
	'env_exports' : {
		"CC": "x86_64-w64-mingw32-gcc",
		"AR": "x86_64-w64-mingw32-ar",
		"RANLIB": "x86_64-w64-mingw32-ranlib",
		"LD": "x86_64-w64-mingw32-ld",
		"STRIP": "x86_64-w64-mingw32-strip",
		"CXX": "x86_64-w64-mingw32-g++",
        # "LDFLAGS": "-Wl,-fuse-ld=x86_64-w64-mingw32-ld",
	},
	'_info' : { 'version' : None, 'fancy_name' : 'openmpt' },
}