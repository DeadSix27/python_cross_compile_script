{
	'repo_type' : 'git',
	'url' : 'https://github.com/file/file.git',
	'branch' : 'bf8b5f2cf7ce59ae2170e7f2fb026182c4dddcdc',
	'rename_folder' : 'libfile.git',
	'patches' : [
		( 'libfile/file-win32.patch', '-p1' ),
	],
	'configure_options' : '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static --enable-fsect-man5',
	'depends_on' : [ 'mingw-libgnurx', 'libfile_local' ],
	'env_exports' : { 'TARGET_CFLAGS' : '{original_cflags}' },
	'run_post_patch' : [ 'autoreconf -fiv' ],
	'flipped_path' : True,
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'file' },
}