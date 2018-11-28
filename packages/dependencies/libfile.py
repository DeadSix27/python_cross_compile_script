{
	'repo_type' : 'git',
	'url' : 'https://github.com/file/file.git',
	'branch' : '4091ea8660a4355b0379564dc901e06bdcdc8c50', #'42d9a8a34607e8b0336b4c354cd5e7e7692bfec7',
	'rename_folder' : 'libfile.git',
	'patches' : [
		( 'https://raw.githubusercontent.com/DeadSix27/python_cross_compile_script/master/patches/file-win32.patch', '-p1' ),
	],
	'configure_options': '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static --enable-fsect-man5',
	'depends_on' : [ 'mingw-libgnurx', 'libfile_local' ],
	'env_exports' : { 'TARGET_CFLAGS' : '{original_cflags}' },
	'run_post_patch' : [ 'autoreconf -fiv' ],
	'flipped_path' : True,
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'file' },
}