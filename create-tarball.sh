#!/bin/bash

VERSION=`grep Version: *spec | sed -e 's/Version:\s*\(.*\)/\1/'`
echo $VERSION

NAME="takari-archiver"

rm -rf ${NAME}-${VERSION}.tar.gz ${NAME}-${NAME}-${VERSION} ${NAME}-${VERSION}
wget https://github.com/takari/${NAME}/archive/${NAME}-${VERSION}.tar.gz
tar xf ${NAME}-${VERSION}.tar.gz
rm -f ${NAME}-${VERSION}.tar.gz
mv ${NAME}-${NAME}-${VERSION} ${NAME}-${VERSION}
rm -rf ${NAME}-${VERSION}/src/test/
wget -O ${NAME}-${VERSION}/epl-v10.html http://www.eclipse.org/legal/epl-v10.html
tar caf ${NAME}-${VERSION}-clean.tar.xz ${NAME}-${VERSION}
