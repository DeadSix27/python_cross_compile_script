{
	'repo_type' : 'git',
	'url' : 'https://github.com/file/file.git',
	'branch' : '24c9c086cd7c55b7b0a003a145b32466468e2608',
	'rename_folder' : 'libfile.git',
	'patches' : [
		( 'libfile/file-win32.patch', '-p1' ),
	],
	'configure_options' : '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static --enable-fsect-man5',
	'depends_on' : [ 'mingw-libgnurx', 'libfile_local' ],
	'env_exports' : { 'TARGET_CFLAGS' : '{original_cflags}' },
	'run_post_patch' : [ 'autoreconf -fiv' ],
	'flipped_path' : True,
	'update_check' : { 'type' : 'git', },
	'_info' : { 'version' : None, 'fancy_name' : 'file' },
}