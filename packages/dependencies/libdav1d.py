{
	'repo_type' : 'git',
	'url' : 'https://code.videolan.org/videolan/dav1d.git',
	'conf_system' : 'meson',
	'build_system' : 'ninja',
	'rename_folder' : 'libdav1d_git',
	'source_subfolder' : 'build',
	'regex_replace': { #hacky but works, so who cares, for some reason libdav1d thinks we have POSIX_MEMALIGN.. maybe mingw or gcc bug, .. so we'll just force it to not define that we have it so it doesn't use it.
		'post_patch': [
			{
				0: r'cdata.set\(\'HAVE_POSIX_MEMALIGN\', 1\)',
				1: 'cdata.set(\'HAVE_ALIGNED_MALLOC\', 1)',
				'in_file': '../meson.build'
			},
			{
				0: r'cdata.set\(\'HAVE_ALIGNED_MALLOC\', 1\)',
				1: 'cdata.set(\'HAVE_ALIGNED_MALLOC\', 1)',
				'in_file': '../meson.build'
			},
		],
	},
	'configure_options' :
		'--prefix={target_prefix} '
		'--libdir={target_prefix}/lib '
		'--default-library=static '
		'--buildtype=plain '
		'--backend=ninja '
		'-Denable_tests=false '
		'-Denable_tools=false '
		'--buildtype=release '
		'--cross-file={meson_env_file} ./ ..'
  ,
	'_info' : { 'version' : None, 'fancy_name' : 'dav1d (library)' },
}