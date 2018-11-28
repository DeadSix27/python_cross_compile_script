{
	'repo_type' : 'git',
	'url' : 'git://sourceware.org/git/binutils-gdb.git',
	'configure_options': '--host={target_host} --enable-static --enable-lto --prefix={product_prefix}/gdb_git.installed',
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'GDB' },
}