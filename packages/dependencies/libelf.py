{
	'repo_type' : 'archive',
	'cpu_count' : '1',
	'download_locations' : [ # the homepage: http://www.mr511.de/software/english.html seems to be dead.
		{ 'url' : 'https://fossies.org/linux/misc/old/libelf-0.8.13.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '591a9b4ec81c1f2042a97aa60564e0cb79d041c52faa7416acb38bc95bd2c76d' }, ], },
		{ 'url' : 'https://ftp.osuosl.org/pub/blfs/conglomeration/libelf/libelf-0.8.13.tar.gz', 'hashes' : [ { 'type' : 'sha256', 'sum' : '591a9b4ec81c1f2042a97aa60564e0cb79d041c52faa7416acb38bc95bd2c76d' }, ], },
	],
	'configure_options' : '--host={target_host} --prefix={target_prefix} --target={bit_name2}-{bit_name_win}-gcc',
	
	'run_post_install' : [
		"echo '--- sys_elf.h	2019-03-31 15:25:39.746139300 +0200\n+++ sys_elf.h	2019-03-31 15:29:18.102775000 +0200\n@@ -66,15 +66,7 @@\n /*\n  * Ok, now get the correct instance of elf.h...\n  */\n-#ifdef __LIBELF_HEADER_ELF_H\n-# include __LIBELF_HEADER_ELF_H\n-#else /* __LIBELF_HEADER_ELF_H */\n-# if __LIBELF_INTERNAL__\n-#  include <elf_repl.h>\n-# else /* __LIBELF_INTERNAL__ */\n-#  include <libelf/elf_repl.h>\n-# endif /* __LIBELF_INTERNAL__ */\n-#endif /* __LIBELF_HEADER_ELF_H */\n+#include <elf_repl.h>\n \n /*\n  * On some systems, <elf.h> is severely broken.  Try to fix it.\n' > {target_prefix}/include/libelf/elf.patch",
		'!SWITCHDIR|{target_prefix}/include/libelf/',
		'patch -p0 < elf.patch',
		'!SWITCHDIRBACK',
	],
	
	'_info' : { 'version' : "0.8.13", 'fancy_name' : 'speex' },
}