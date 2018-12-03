{
	'repo_type' : 'git',
	'branch' : 'bf8b5f2cf7ce59ae2170e7f2fb026182c4dddcdc',
	'url' : 'https://github.com/file/file.git',
	'rename_folder' : 'libfile_local.git',
	'configure_options' : '--prefix={target_prefix} --disable-shared --enable-static',
	'needs_make' : False,
	'env_exports' : { 'TARGET_CFLAGS' : '{original_cflags}' },
	'run_post_patch' : [ 'autoreconf -fiv' ],
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'libfile (bootstrap)' },
}