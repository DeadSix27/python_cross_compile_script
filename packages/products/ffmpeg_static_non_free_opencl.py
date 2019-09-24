{
	'repo_type' : 'git',
	'url' : 'git://git.ffmpeg.org/ffmpeg.git',
	'rename_folder' : 'ffmpeg_static_non_free_opencl',
	'patches': [
		('https://raw.githubusercontent.com/OpenVisualCloud/SVT-HEVC/master/ffmpeg_plugin/0001-lavc-svt_hevc-add-libsvt-hevc-encoder-wrapper.patch', '-p1'),
		# ('https://raw.githubusercontent.com/OpenVisualCloud/SVT-HEVC/master/ffmpeg_plugin/0002-doc-Add-libsvt_hevc-encoder-docs.patch', '-p1'),
		
		('https://raw.githubusercontent.com/OpenVisualCloud/SVT-AV1/master/ffmpeg_plugin/0001-Add-ability-for-ffmpeg-to-run-svt-av1-with-svt-hevc.patch', '-p1'),
		# ('https://raw.githubusercontent.com/OpenVisualCloud/SVT-AV1/master/ffmpeg_plugin/0001-Add-ability-for-ffmpeg-to-run-svt-av1.patch', '-p1'),
		
		('https://raw.githubusercontent.com/OpenVisualCloud/SVT-VP9/master/ffmpeg_plugin/0001-Add-ability-for-ffmpeg-to-run-svt-vp9-with-svt-hevc-av1.patch', '-p1'),
		# ('https://raw.githubusercontent.com/OpenVisualCloud/SVT-VP9/master/ffmpeg_plugin/0001-Add-ability-for-ffmpeg-to-run-svt-vp9.patch', '-p1'),
		
	],
	'configure_options' : '!VAR(ffmpeg_base_config)VAR! --enable-libsvthevc --enable-libsvtvp9 --enable-libsvtav1 --enable-libbluray --prefix={product_prefix}/ffmpeg_static_non_free_opencl.installed --disable-shared --enable-static --enable-opencl --enable-nonfree --enable-libfdk-aac --enable-decklink',
	'depends_on' : [ 'ffmpeg_depends', 'decklink_headers', 'fdk_aac', 'opencl_icd', 'svt_av1', 'svt_av1', 'svt_vp9'],
	'_info' : { 'version' : None, 'fancy_name' : 'ffmpeg NonFree (static (OpenCL))' },
}