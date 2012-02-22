#!/bin/sh

VERSION=1.9.0
SRCDIR=mockito-${VERSION}

hg clone https://code.google.com/p/mockito/ ${SRCDIR}
cd $SRCDIR
hg update ${VERSION}
rm -rf `find -name *.jar` build.gradle cglib-and-asm conf doc gradle gradlew gradlew.bat
dos2unix `find -name *.java`
cd ..

tar -cvJf mockito-${VERSION}.tar.xz ${SRCDIR}
