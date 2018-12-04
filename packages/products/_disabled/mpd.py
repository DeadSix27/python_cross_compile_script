{
	'repo_type' : 'git',
	'url' : 'https://github.com/MaxKellermann/MPD.git',
	'configure_options' : '--host={target_host} --prefix={target_prefix} --disable-shared --enable-static --disable-wavpack --disable-gme --disable-bzip2 --disable-cdio-paranoia --disable-sqlite --enable-silent-rules --disable-icu LDFLAGS="-static" LIBS="-static-libgcc -static-libstdc++ -lz -lole32"',
	'env_exports' : {
		'LDFLAGS' : '-static',
		'LIBS' : '-static-libgcc -static-libstdc++ -lz -lole32',
		'CXXFLAGS' : '-O2 -g',
	},
	'_disabled' : True,
}