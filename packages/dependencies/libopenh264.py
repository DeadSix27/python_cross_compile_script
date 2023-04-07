{
	'repo_type' : 'git',
	'url' : 'https://github.com/cisco/openh264.git',
	'patches' : [
		('openh264/0001-remove-fma3-call.patch','-p1'),
	],
	#'custom_cflag' : '-O3',
	'needs_configure' : False,
	'build_options' : '{make_prefix_options} OS=mingw_nt ARCH={bit_name} ASM=yasm',
	'install_options' : '{make_prefix_options} OS=mingw_nt',
	'install_target' : 'install-static',
	'_info' : { 'version' : None, 'fancy_name' : 'openh264' },
}