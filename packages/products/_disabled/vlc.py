{
	'repo_type' : 'git',
	'url' : 'https://github.com/videolan/vlc.git', # https://git.videolan.org/git/vlc.git is slow..
	'configure_options':
		'--host={target_host} --prefix={product_prefix}/vlc_git.installed --disable-lua --enable-qt --disable-ncurses --disable-dbus --disable-sdl --disable-telx --enable-nls LIBS="-lbcrypt -lbz2"'
	,
	'depends_on' : [
		'lua', 'a52dec',
	],
	# 'patches' : [
		# ('https://raw.githubusercontent.com/Alexpux/MINGW-packages/master/mingw-w64-vlc-git/0002-MinGW-w64-lfind-s-_NumOfElements-is-an-unsigned-int.patch','-p1'),
		# ('https://raw.githubusercontent.com/Alexpux/MINGW-packages/master/mingw-w64-vlc-git/0003-MinGW-w64-don-t-pass-static-to-pkg-config-if-SYS-min.patch','-p1'),
		# ('https://raw.githubusercontent.com/Alexpux/MINGW-packages/master/mingw-w64-vlc-git/0004-Revert-Win32-prefer-the-static-libraries-when-creati.patch','-p1'),
	# ],
	'env_exports' : {
		'LIBS' : '-lbcrypt -lbz2', # add the missing bcrypt Link, is windows SSL api, could use gcrypt or w/e idk what that lib is, i'd probably rather use openssl_1_1
	},
	# 'download_header' : [
	# 	'https://raw.githubusercontent.com/gongminmin/UniversalDXSDK/master/Include/dxgi1_3.h',
	# 	'https://raw.githubusercontent.com/gongminmin/UniversalDXSDK/master/Include/dxgi1_4.h',
	# 	'https://raw.githubusercontent.com/gongminmin/UniversalDXSDK/master/Include/dxgi1_5.h',
	# 	'https://raw.githubusercontent.com/gongminmin/UniversalDXSDK/master/Include/dxgi1_6.h',
	# ],
	'_info' : { 'version' : 'git (master)', 'fancy_name' : 'VLC (git)' },
	'_disabled' : True,
}