{
	'repo_type' : 'git',
	'url' : 'https://github.com/file/file.git',
	# 'branch' : '24c9c086cd7c55b7b0a003a145b32466468e2608',
	'rename_folder' : 'libfile.git',
	'patches' : [
		( 'libfile/file-win32.patch', '-p1' ),
	],
	'configure_options' : '{autoconf_prefix_options} --enable-fsect-man5',
	'depends_on' : [ 'mingw-libgnurx' ],  # ,'libfile_local' ],
	'env_exports' : { 'TARGET_CFLAGS' : '{original_cflags}' },
	'run_post_patch' : [
		'sed -i.bak "s/#ifdef FIONREAD/#ifdef __linux__ /" src/seccomp.c',
		'sed -i.bak "s/#ifdef FIONREAD/#ifdef __linux__ /" src/compress.c',
		'autoreconf -fiv' 
	],
	'flipped_path' : True,
	'update_check' : { 'type' : 'git', },
	'_info' : { 'version' : None, 'fancy_name' : 'file' },
}