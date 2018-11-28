{
	'repo_type' : 'git',
	'branch' : '4091ea8660a4355b0379564dc901e06bdcdc8c50', #'42d9a8a34607e8b0336b4c354cd5e7e7692bfec7',
	'url' : 'https://github.com/file/file.git',
	'rename_folder' : 'libfile_local.git',
	'configure_options': '--prefix={target_prefix} --disable-shared --enable-static',
	'needs_make' : False,
	'env_exports' : { 'TARGET_CFLAGS' : '{original_cflags}' },
	'run_post_patch' : [ 'autoreconf -fiv' ],
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'libfile (bootstrap)' },
}