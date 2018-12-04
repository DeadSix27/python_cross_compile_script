{
	'repo_type' : 'git',
	'url' : 'https://github.com/DeadSix27/Baka-MPlayer',
	'rename_folder' : 'mpv_gui_qt5_git',
	'configure_options' :
		'CONFIG+=embed_translations lupdate="{target_sub_prefix}/bin/lupdate" lrelease="{target_sub_prefix}/bin/lrelease" PKG_CONFIG={cross_prefix_full}pkg-config INSTALL_ROOT={product_prefix}/mpv_gui_qt5_git.installed'
		' LIBS+=-L{target_sub_prefix}/lib INCLUDEPATH+=-I{target_sub_prefix}/include'
	,
	'run_post_patch' : [
		'cp -nv "/usr/bin/pkg-config" "{cross_prefix_full}pkg-config"'
	],
	'install_options' : 'INSTALL_ROOT={product_prefix}/mpv_gui_qt5_git.installed',
	'env_exports' : {
		'QTROOT' : '{target_sub_prefix}/bin',
		'QMAKE' : '{target_sub_prefix}/bin/qmake',
		'PKG_CONFIG' : '{cross_prefix_full}pkg-config'
	},
	'depends_on' : [
		'qt5',
		'libmpv',
		'libzip'
	],
}