#type: ignore
{
	'ffmpeg_config' : # the base for all ffmpeg configurations.
		'--arch={bit_name2} '
		'--target-os=mingw32 '
		'--cross-prefix={cross_prefix_bare} '
		'--pkg-config=pkg-config '
		'--pkg-config-flags=--static '
		'--disable-w32threads '
		'--enable-cross-compile '
		'--target-exec=wine '
		'--enable-runtime-cpudetect '
		'--enable-gpl '
		'--enable-version3 '
		'--extra-version=xcompile '

		# Misc.
		'--enable-pic '
		'--enable-bzlib '
		'--enable-zlib '
		'--enable-lzma '
		# '--enable-gcrypt '
		'--enable-fontconfig '
		'--enable-libfontconfig '
		'--enable-libfreetype '
		'--enable-libfribidi '
		'--enable-libbluray '
		'--enable-libcdio '
		'--enable-avisynth '
		'--enable-vapoursynth ' #maybe works?
		'--enable-librtmp '
		'--enable-libcaca '
		'--enable-iconv '
		'--enable-libxml2 '
		# '--enable-gmp '
        '--enable-openssl '
        '--enable-libtls '
		# '--enable-gnutls ' # nongpl: openssl,libtls(libressl)
		'--enable-vulkan '
		'--enable-libshaderc '
        '--enable-libplacebo '

		# Video/Picture Libs
		'--enable-libzimg '
		'--enable-libx264 '
		'--enable-libopenh264 '
		'--enable-libx265 '
		'--enable-libkvazaar '
		'--enable-libvpx '
		'--enable-libdav1d '
		'--enable-libaom '
        '--enable-libsvtav1 '
        '--enable-librav1e '
		'--enable-libxvid '
		'--enable-gray '

		# Audio Libs
		'--enable-libopus '
		'--enable-libmp3lame '
		'--enable-libvorbis '
		'--enable-libtheora '
		'--enable-libspeex '
		'--enable-libsoxr '
		'--enable-librubberband '
        '--enable-openal '

		# Subtitle/OCR Libs:
		'--enable-libass '
		'--enable-libtesseract '
		'--enable-liblensfun '

		# Image libs
		'--enable-libwebp '
        '--enable-libopenjpeg '
        '--enable-libjxl '

		# HW Decoders
		'--enable-ffnvcodec '
		'--enable-cuvid '
		'--enable-opengl '
		'--disable-opencl '
		'--enable-d3d11va '
		'--enable-nvenc '
		'--enable-nvdec '
		'--enable-dxva2 '
		'--enable-cuda-nvcc '
		'--enable-libmfx '
		'--enable-amf '
        '--extra-cflags="-DAL_LIBTYPE_STATIC -DMODPLUG_STATIC" '
	,

	'ffmpeg_nonfree': '--enable-nonfree --enable-libfdk-aac --enable-decklink', # --enable-cuda-sdk # nonfree stuff

	'ffmpeg_extra_config' :
		'--enable-libtwolame '
		'--enable-libzvbi '
		'--enable-libgsm '
		'--enable-libopencore-amrnb '
		'--enable-libopencore-amrwb '
		'--enable-libvo-amrwbenc '
		'--enable-libsnappy '
		'--enable-frei0r '
		'--enable-filter=frei0r '
		'--enable-libsrt '
		'--enable-libbs2b '
		# '--enable-libwavpack '
		'--enable-libilbc '
		'--enable-libgme '
		#'--enable-libflite ' #todo fix this shit
		'--enable-sdl '
		'--enable-libdavs2 '
		'--enable-libxavs '
		'--enable-libxavs2 '
		'--enable-libopenmpt '
		'--enable-libmysofa '
		'--enable-libvidstab '
		'--enable-libmodplug '
		# '--disable-schannel '
		#'--disable-gcrypt '
		#'--enable-ladspa '
		# '--enable-libcodec2 ' # Requires https://github.com/traviscross/freeswitch/tree/master/libs/libcodec2, too lazy to split that off.
		# '--enable-libvmaf '
		# '--extra-libs="-lpsapi" '
		# '--extra-libs="-liconv" ' # -lschannel #-lsecurity -lz -lcrypt32 -lintl -liconv -lpng -loleaut32 -lstdc++ -lspeexdsp -lpsapi
		# '--extra-cflags="-DLIBTWOLAME_STATIC" '
		# '--extra-cflags="-DMODPLUG_STATIC" '
	,
}
