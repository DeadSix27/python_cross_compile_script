{
	'repo_type' : 'svn',
	'folder_name' : 'libfilezilla_svn',
	'url' : 'https://svn.filezilla-project.org/svn/libfilezilla/trunk',
	'configure_options': '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static',
	'run_post_patch' : [
		'autoreconf -fiv',
	],
	'env_exports' : {
		'CXXFLAGS' : '-O0',
	},
	'_info' : { 'version' : 'svn (master)', 'fancy_name' : 'FileZilla (libary)' },
}