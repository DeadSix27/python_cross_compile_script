# type: ignore
{
	'repo_type' : 'git',
	'rename_folder' : 'spirv-tools',
	'url' : 'https://github.com/KhronosGroup/SPIRV-Tools.git',
    'patches': [
		('https://github.com/DeadSix27/SPIRV-Tools/commit/6ef89a00fbccb833f6ba3c86c169845019ef36b0.patch', '-p1'),
	],
	'depth_git': 0,
	'branch':'main', 
	# 'branch':'v2023.1', 
	'needs_make' : False,
	'needs_make_install' : False,
	'needs_configure' : False,
	'recursive_git' : True,
	'update_check' : { 'type' : 'git', },
	'_info' : { 'version' : None, 'fancy_name' : 'SPIRV Tools' },
}