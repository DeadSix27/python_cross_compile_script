{
	'repo_type' : 'git',
	'url' : 'http://luajit.org/git/luajit-2.0.git',
	'needs_configure' : False,
	'custom_cflag' : '-O3', # doesn't like march's past ivybridge (yet), so we override it.
	'install_options' : 'CROSS={cross_prefix_bare} HOST_CC="gcc -m{bit_num}" TARGET_SYS=Windows BUILDMODE=static FILE_T=luajit.exe PREFIX={target_prefix}',
	'build_options': 'CROSS={cross_prefix_bare} HOST_CC="gcc -m{bit_num}" TARGET_SYS=Windows BUILDMODE=static amalg',
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'LuaJIT2' },
}