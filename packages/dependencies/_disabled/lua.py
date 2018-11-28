{
	'repo_type' : 'archive',
	'url' : 'https://www.lua.org/ftp/lua-5.3.4.tar.gz',
	'needs_configure' : False,
	'build_options': 'CC={cross_prefix_bare}gcc PREFIX={target_prefix} RANLIB={cross_prefix_bare}ranlib LD={cross_prefix_bare}ld STRIP={cross_prefix_bare}strip CXX={cross_prefix_bare}g++ AR="{cross_prefix_bare}ar rcu" mingw', # LUA_A=lua53.dll LUA_T=lua.exe LUAC_T=luac.exe
	'install_options' : 'TO_BIN="lua.exe luac.exe lua53.dll" TO_LIB="liblua.a" INSTALL_TOP="{target_prefix}"', #TO_LIB="liblua.a liblua.dll.a"
	'install_target' : 'install',
	'packages': {
		'ubuntu' : [ 'lua5.2' ],
	},
	'_info' : { 'version' : '5.3.4', 'fancy_name' : 'lua' },
}