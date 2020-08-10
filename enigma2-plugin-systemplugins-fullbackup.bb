DESCRIPTION = "full backup and manual flashing image"
HOMEPAGE = "https://github.com/aouamed/fullbackup"
LICENSE = "PD"
LIC_FILES_CHKSUM = "file://README;md5=f521231b9317995c51bdc211746b2802"
SRC_URI = "git://github.com/aouamed/fullbackup.git"
S = "${WORKDIR}/git"

inherit gitpkgv
SRCREV = "${AUTOREV}"
PV = "1+git${SRCPV}"
PKGV = "1+git${GITPKGV}"
SRCREV = "${AUTOREV}"

inherit distutils-openplugins

RDEPENDS_${PN} = " \
	mtd-utils-ubifs \
	mtd-utils \
	util-linux-mkfs \
	kernel-module-jffs2 \
	util-linux-sfdisk \
	kernel \
	bzip2 \
	"
