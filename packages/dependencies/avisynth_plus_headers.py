{
	'repo_type' : 'git',			
	'url' : 'https://github.com/AviSynth/AviSynthPlus',
	'source_subfolder' : '_build',
	'patches' : [
		( 'avisynthplus/fix-version.patch', '-p1', '..' ),
	],
	'conf_system' : 'cmake',
	'configure_options' : '.. {cmake_prefix_options} -DCMAKE_INSTALL_PREFIX={target_prefix} -DHEADERS_ONLY:bool=on ',
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'Avisynth+ (Headers only)' },
}