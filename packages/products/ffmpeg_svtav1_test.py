{
	'repo_type' : 'git',
	'url' : 'git://git.ffmpeg.org/ffmpeg.git',
	'rename_folder' : 'ffmpeg_svtav1_test',
	'patches': [
		# ('https://raw.githubusercontent.com/OpenVisualCloud/SVT-HEVC/master/ffmpeg_plugin/0001-lavc-svt_hevc-add-libsvt-hevc-encoder-wrapper.patch', '-p1'),
		# ('https://raw.githubusercontent.com/OpenVisualCloud/SVT-HEVC/master/ffmpeg_plugin/0002-doc-Add-libsvt_hevc-encoder-docs.patch', '-p1'),
		
		# ('https://raw.githubusercontent.com/OpenVisualCloud/SVT-AV1/master/ffmpeg_plugin/0001-Add-ability-for-ffmpeg-to-run-svt-av1-with-svt-hevc.patch', '-p1'),
		('https://raw.githubusercontent.com/OpenVisualCloud/SVT-AV1/master/ffmpeg_plugin/0001-Add-ability-for-ffmpeg-to-run-svt-av1.patch', '-p1'),
		
		# ('https://raw.githubusercontent.com/OpenVisualCloud/SVT-VP9/master/ffmpeg_plugin/0001-Add-ability-for-ffmpeg-to-run-svt-vp9-with-svt-hevc-av1.patch', '-p1'),
		# ('https://raw.githubusercontent.com/OpenVisualCloud/SVT-VP9/master/ffmpeg_plugin/0001-Add-ability-for-ffmpeg-to-run-svt-vp9.patch', '-p1'),
		
		# --disable-libvpx --disable-libx265 --disable-libaom --enable-libsvthevc --enable-libsvtvp9 
		
	],
	'configure_options' : '!VAR(ffmpeg_min_config)VAR! !VAR(ffmpeg_nonfree)VAR! --disable-libaom --enable-libsvtav1 --prefix={output_prefix}/ffmpeg_svtav1_test.installed --disable-shared --enable-static',
	'depends_on' : [ 'ffmpeg_depends_min', 'ffmpeg_depends_non_free', 'svt_av1'],
	'_info' : { 'version' : None, 'fancy_name' : 'ffmpeg static with SVT-AV1' },
}