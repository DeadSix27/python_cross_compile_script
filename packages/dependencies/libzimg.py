{
	'repo_type' : 'git',
	'url' : 'https://github.com/sekrit-twc/zimg.git',
	'depth_git': 1,
	'run_post_patch' : [
        "rm -vrf graphengine/",
        "git submodule update --recursive --remote"
    ],
	#'branch' : 'd0f9cdebd34b0cb032f79357660bd0f6f23069ee', # '3aae2066e5b8df328866ba7e8636d8901f42e8e7',
	'configure_options' : '{autoconf_prefix_options}',
	'_info' : { 'version' : None, 'fancy_name' : 'zimg' },
}