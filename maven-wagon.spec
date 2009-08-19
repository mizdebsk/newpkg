# Copyright (c) 2000-2007, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

# If you don't want to build with maven, and use straight ant instead,
# give rpmbuild option '--without maven'

%define with_maven 0
%define without_maven 1

%define bname     wagon
%define blevel    beta-2

%define bname     wagon

# FIXME1: wagon-scm has been disabled for now due to maven-scm dependency
# FIXME2: haltOnFailure/Error has been set to false for
# wagon-http/wagon-ssh-external tests due to failures.
# FIXME3: Change spec file to build with maven2
# FIXME4: Add javadoc options ant build

Name:           maven-%{bname}
Version:        1.0
Release:        0.2.b2.7%{?dist}
Epoch:          0
Summary:        Tools to manage artifacts and deployment
License:        ASL 2.0
Group:          Development/Java
URL:            http://maven.apache.org/wagon
Source0:        wagon-1.0-%{blevel}-src.tar.gz
# svn export http://svn.apache.org/repos/asf/maven/wagon/tags/wagon-1.0-beta-2/
# tar czvf wagon-1.0-beta-2-src.tar.gz wagon-1.0-beta-2

Source1:        wagon-1.0-jpp-depmap.xml
Source2:        wagon-1.0-site.xml
# The following sources (3-15) were generated by running the maven2 ant task
# inside the root directory of Source0: "mvn ant:ant"
Source3:        wagon-1.0-file-provider-build.xml
Source4:        wagon-1.0-ftp-provider-build.xml
Source5:        wagon-1.0-http-lightweight-provider-build.xml
Source6:        wagon-1.0-http-provider-build.xml
Source7:        wagon-1.0-http-shared-provider-build.xml
Source8:        wagon-1.0-provider-api-build.xml
Source9:        wagon-1.0-provider-test-build.xml
Source10:       wagon-1.0-ssh-common-provider-build.xml
Source11:       wagon-1.0-ssh-common-test-provider-build.xml
Source12:       wagon-1.0-ssh-external-provider-build.xml
Source13:       wagon-1.0-ssh-ganymed-provider-build.xml
Source14:       wagon-1.0-ssh-provider-build.xml
Source15:       wagon-1.0-webdav-provider-build.xml

Patch0:         wagon-1.0-wagon-http-lightweight-pom_xml.patch
Patch1:         wagon-1.0-wagon-http-pom_xml.patch
Patch2:         wagon-1.0-wagon-webdav-pom_xml.patch
Patch3:         wagon-1.0-WebDavWagon.patch
Patch4:         wagon-1.0-ServletServer.patch
Patch5:         wagon-1.0-pom_xml.patch
Patch6:         wagon-1.0-wagon-ftp-pom_xml.patch
Patch7:         wagon-1.0-disable-webdav.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  jpackage-utils >= 0:1.7.2
BuildRequires:  ant >= 0:1.6
BuildRequires:  junit
%if %{with_maven}
BuildRequires:  maven2 >= 0:2.0.8
BuildRequires:  maven2-plugin-compiler
BuildRequires:  maven2-plugin-install
BuildRequires:  maven2-plugin-jar
BuildRequires:  maven2-plugin-javadoc
BuildRequires:  maven2-plugin-project-info-reports
BuildRequires:  maven2-plugin-resources
BuildRequires:  maven2-plugin-site
BuildRequires:  maven2-plugin-surefire = 2.3
BuildRequires:  maven-surefire-provider-junit = 2.3
BuildRequires:  maven2-default-skin
%endif
BuildRequires:  classworlds
BuildRequires:  concurrent
BuildRequires:  ganymed-ssh2
BuildRequires:  jakarta-commons-codec
BuildRequires:  jakarta-commons-collections
BuildRequires:  jakarta-commons-net
BuildRequires:  jakarta-commons-httpclient
BuildRequires:  jakarta-commons-logging
#BuildRequires:  jakarta-slide-webdavclient
BuildRequires:  jsch
BuildRequires:  jtidy
BuildRequires:  plexus-container-default
BuildRequires:  plexus-interactivity
BuildRequires:  plexus-utils
BuildRequires:  servletapi5
BuildRequires:  xml-commons-apis

Requires:       ganymed-ssh2
Requires:       jakarta-commons-httpclient
Requires:       jakarta-commons-net
#Requires:       jakarta-slide-webdavclient
Requires:       jsch
Requires:       jtidy
Requires:       plexus-interactivity
Requires:       plexus-utils
Requires:       xml-commons-apis

%description
Maven Wagon is a transport abstraction that is used in Maven's
artifact and repository handling code. Currently wagon has the
following providers:
* File
* HTTP
* FTP
* SSH/SCP
* WebDAV (in progress)

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Documentation
Requires(post):   /bin/rm,/bin/ln
Requires(postun): /bin/rm

%description javadoc
Javadoc for %{name}.

%if %{with_maven}
%package manual
Summary:        Documents for %{name}
Group:          Development/Documentation

%description manual
Documents for %{name}.
%endif

%prep
%setup -q -n %{bname}-%{version}-%{blevel}
cp %{SOURCE3} wagon-providers/wagon-file/build.xml
cp %{SOURCE4} wagon-providers/wagon-ftp/build.xml
cp %{SOURCE5} wagon-providers/wagon-http-lightweight/build.xml
cp %{SOURCE6} wagon-providers/wagon-http/build.xml
cp %{SOURCE7} wagon-providers/wagon-http-shared/build.xml
cp %{SOURCE8} wagon-provider-api/build.xml
cp %{SOURCE9} wagon-provider-test/build.xml
cp %{SOURCE10} wagon-providers/wagon-ssh-common/build.xml
cp %{SOURCE11} wagon-providers/wagon-ssh-common-test/build.xml
cp %{SOURCE12} wagon-providers/wagon-ssh-external/build.xml
cp %{SOURCE13} wagon-providers/wagon-ssh-ganymed/build.xml
cp %{SOURCE14} wagon-providers/wagon-ssh/build.xml
cp %{SOURCE15} wagon-providers/wagon-webdav/build.xml

# FIXME: the following should not be necessary with a newer site-plugin
mkdir -p src/site
cp %{SOURCE2} src/site/site.xml
cp %{SOURCE2} wagon-provider-api/src/site/site.xml
cp %{SOURCE2} wagon-providers/wagon-file/src/site/site.xml
cp %{SOURCE2} wagon-providers/wagon-ftp/src/site/site.xml
mkdir -p wagon-providers/wagon-http-shared/src/site
cp %{SOURCE2} wagon-providers/wagon-http-shared/src/site/site.xml
cp %{SOURCE2} wagon-providers/wagon-http-lightweight/src/site/site.xml
cp %{SOURCE2} wagon-providers/wagon-http/src/site/site.xml
mkdir -p wagon-providers/wagon-ssh-common/src/site
cp %{SOURCE2} wagon-providers/wagon-ssh-common/src/site/site.xml
mkdir -p wagon-providers/wagon-ssh-common-test/src/site
cp %{SOURCE2} wagon-providers/wagon-ssh-common-test/src/site/site.xml
mkdir -p wagon-providers/wagon-ssh-ganymed/src/site
cp %{SOURCE2} wagon-providers/wagon-ssh-ganymed/src/site/site.xml
cp %{SOURCE2} wagon-providers/wagon-ssh-external/src/site/site.xml
cp %{SOURCE2} wagon-providers/wagon-ssh/src/site/site.xml
cp %{SOURCE2} wagon-providers/wagon-webdav/src/site/site.xml
cp %{SOURCE2} wagon-provider-test/src/site/site.xml
cp %{SOURCE2} wagon-site/src/site/site.xml


%patch0 -b .sav
%patch1 -b .sav
%patch2 -b .sav
%patch3 -b .sav
%patch4 -b .sav
%patch5 -b .sav
%patch6 -b .sav
%patch7 -b .sav

# To wire out jetty, plexus-avalon-personality and plexus-ftpd requirement
rm -f wagon-providers/wagon-ftp/src/test/java/org/apache/maven/wagon/providers/ftp/FtpWagonTest.java
rm -f wagon-providers/wagon-http-lightweight/src/test/java/org/apache/maven/wagon/providers/http/LightweightHttpWagonTest.java
rm -f wagon-providers/wagon-http-lightweight/src/test/java/org/apache/maven/wagon/providers/http/LightweightHttpWagonGzipTest.java
rm -f wagon-providers/wagon-http/src/test/java/org/apache/maven/wagon/providers/http/HttpWagonTest.java
rm -f wagon-providers/wagon-http/src/test/java/org/apache/maven/wagon/providers/http/HttpWagonGzipTest.java

%build
%if %{with_maven}

export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL

mvn-jpp \
        -e \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        -Dmaven2.jpp.depmap.file=%{SOURCE1} \
        -Dmaven.test.failure.ignore=true \
        -Dmaven.test.skip=true \
        install javadoc:javadoc

%else

pushd wagon-provider-api
export CLASSPATH=$(build-classpath plexus/utils)
CLASSPATH=$CLASSPATH:target/classes:target/test-classes
ant -Dbuild.sysclasspath=only jar javadoc
popd

pushd wagon-provider-test
export CLASSPATH=../wagon-provider-api/target/wagon-provider-api-%{version}-%{blevel}.jar
CLASSPATH=$CLASSPATH:$(build-classpath plexus/container-default plexus/utils junit)
CLASSPATH=$CLASSPATH:target/classes:target/test-classes
ant -Dbuild.sysclasspath=only jar javadoc
popd

pushd wagon-providers/wagon-file
export CLASSPATH=../../wagon-provider-api/target/wagon-provider-api-%{version}-%{blevel}.jar
CLASSPATH=$CLASSPATH:../../wagon-provider-test/target/wagon-provider-test-%{version}-%{blevel}.jar
CLASSPATH=$CLASSPATH:$(build-classpath classworlds plexus/container-default plexus/utils)
CLASSPATH=$CLASSPATH:target/classes:target/test-classes
ant -Dbuild.sysclasspath=only jar javadoc
popd

pushd wagon-providers/wagon-ftp
export CLASSPATH=../../wagon-provider-api/target/wagon-provider-api-%{version}-%{blevel}.jar
CLASSPATH=$CLASSPATH:../../wagon-provider-test/target/wagon-provider-test-%{version}-%{blevel}.jar
CLASSPATH=$CLASSPATH:$(build-classpath classworlds concurrent commons-collections commons-net \
plexus/container-default \
plexus/utils)
CLASSPATH=$CLASSPATH:target/classes:target/test-classes
ant -Dbuild.sysclasspath=only jar javadoc
popd

pushd wagon-providers/wagon-http-shared
export CLASSPATH=../../wagon-provider-api/target/wagon-provider-api-%{version}-%{blevel}.jar
CLASSPATH=$CLASSPATH:../../wagon-provider-test/target/wagon-provider-test-%{version}-%{blevel}.jar
CLASSPATH=$CLASSPATH:$(build-classpath jtidy plexus/utils)
CLASSPATH=$CLASSPATH:target/classes:target/test-classes
ant -Dbuild.sysclasspath=only jar javadoc
popd

pushd wagon-providers/wagon-http-lightweight
export CLASSPATH=../../wagon-provider-api/target/wagon-provider-api-%{version}-%{blevel}.jar
CLASSPATH=$CLASSPATH:../../wagon-provider-test/target/wagon-provider-test-%{version}-%{blevel}.jar
CLASSPATH=$CLASSPATH:../wagon-http-shared/target/wagon-http-shared-%{version}-%{blevel}.jar
CLASSPATH=$CLASSPATH:$(build-classpath classworlds plexus/container-default plexus/utils commons-logging servletapi5)
CLASSPATH=$CLASSPATH:target/classes:target/test-classes
ant -Dbuild.sysclasspath=only jar javadoc
popd

pushd wagon-providers/wagon-http
export CLASSPATH=../../wagon-provider-api/target/wagon-provider-api-%{version}-%{blevel}.jar
CLASSPATH=$CLASSPATH:../../wagon-provider-test/target/wagon-provider-test-%{version}-%{blevel}.jar
CLASSPATH=$CLASSPATH:../wagon-http-shared/target/wagon-http-shared-%{version}-%{blevel}.jar
CLASSPATH=$CLASSPATH:$(build-classpath classworlds plexus/container-default plexus/utils commons-codec commons-httpclient commons-logging servletapi5)
CLASSPATH=$CLASSPATH:target/classes:target/test-classes
ant -Dbuild.sysclasspath=only jar javadoc
popd

pushd wagon-providers/wagon-ssh-common
export CLASSPATH=../../wagon-provider-api/target/wagon-provider-api-%{version}-%{blevel}.jar
CLASSPATH=$CLASSPATH:$(build-classpath plexus/interactivity-api plexus/utils)
CLASSPATH=$CLASSPATH:target/classes:target/test-classes
ant -Dbuild.sysclasspath=only jar javadoc
popd

pushd wagon-providers/wagon-ssh-common-test
export CLASSPATH=../../wagon-provider-api/target/wagon-provider-api-%{version}-%{blevel}.jar
CLASSPATH=$CLASSPATH:../wagon-ssh-common/target/wagon-ssh-common-%{version}-%{blevel}.jar
CLASSPATH=$CLASSPATH:$(build-classpath junit plexus/container-default plexus/utils)
CLASSPATH=$CLASSPATH:target/classes:target/test-classes
ant -Dbuild.sysclasspath=only jar javadoc
popd

pushd wagon-providers/wagon-ssh-external
export CLASSPATH=../../wagon-provider-api/target/wagon-provider-api-%{version}-%{blevel}.jar
CLASSPATH=$CLASSPATH:../../wagon-provider-test/target/wagon-provider-test-%{version}-%{blevel}.jar
CLASSPATH=$CLASSPATH:../wagon-ssh-common/target/wagon-ssh-common-%{version}-%{blevel}.jar
CLASSPATH=$CLASSPATH:../wagon-ssh-common-test/target/wagon-ssh-common-test-%{version}-%{blevel}.jar
CLASSPATH=$CLASSPATH:$(build-classpath classworlds plexus/container-default plexus/utils)
CLASSPATH=$CLASSPATH:target/classes:target/test-classes
ant -Dbuild.sysclasspath=only jar javadoc
popd

pushd wagon-providers/wagon-ssh-ganymed
export CLASSPATH=../../wagon-provider-api/target/wagon-provider-api-%{version}-%{blevel}.jar
CLASSPATH=$CLASSPATH:../../wagon-provider-test/target/wagon-provider-test-%{version}-%{blevel}.jar
CLASSPATH=$CLASSPATH:../wagon-ssh-common/target/wagon-ssh-common-%{version}-%{blevel}.jar
CLASSPATH=$CLASSPATH:../wagon-ssh-common-test/target/wagon-ssh-common-test-%{version}-%{blevel}.jar
CLASSPATH=$CLASSPATH:$(build-classpath classworlds ganymed-ssh2 plexus/container-default plexus/interactivity-api plexus/utils)
CLASSPATH=$CLASSPATH:target/classes:target/test-classes
ant -Dbuild.sysclasspath=only jar javadoc
popd

pushd wagon-providers/wagon-ssh
export CLASSPATH=../../wagon-provider-api/target/wagon-provider-api-%{version}-%{blevel}.jar
CLASSPATH=$CLASSPATH:../../wagon-provider-test/target/wagon-provider-test-%{version}-%{blevel}.jar
CLASSPATH=$CLASSPATH:../wagon-ssh-common/target/wagon-ssh-common-%{version}-%{blevel}.jar
CLASSPATH=$CLASSPATH:../wagon-ssh-common-test/target/wagon-ssh-common-test-%{version}-%{blevel}.jar
CLASSPATH=$CLASSPATH:$(build-classpath classworlds jsch plexus/container-default plexus/interactivity-api plexus/utils)
CLASSPATH=$CLASSPATH:target/classes:target/test-classes
ant -Dbuild.sysclasspath=only jar javadoc
popd

## FIXME: webdav disabled until jakarta-slide-webdav and it-could-webdav are in Fedora

#pushd wagon-providers/wagon-webdav
#export CLASSPATH=../../wagon-provider-api/target/wagon-provider-api-%{version}-%{blevel}.jar
#CLASSPATH=$CLASSPATH:../../wagon-provider-test/target/wagon-provider-test-%{version}-%{blevel}.jar
#CLASSPATH=$CLASSPATH:$(build-classpath classworlds commons-codec commons-httpclient commons-logging it-could-webdav jetty5/jetty5 plexus/container-default plexus/utils slide/slide-webdavclient-webdavlib servletapi5)
#CLASSPATH=$CLASSPATH:target/classes:target/test-classes
#ant -Dbuild.sysclasspath=only jar javadoc
#popd
%endif

%install
rm -rf $RPM_BUILD_ROOT
# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/%{name}
install -m 644 \
  wagon-provider-api/target/wagon-provider-api-%{version}-%{blevel}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/provider-api-%{version}.jar
%add_to_maven_depmap org.apache.maven.wagon wagon-provider-api %{version} JPP/%{name} provider-api
install -m 644 \
  wagon-providers/wagon-file/target/wagon-file-%{version}-%{blevel}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/file-%{version}.jar
%add_to_maven_depmap org.apache.maven.wagon wagon-file %{version} JPP/%{name} file
install -m 644 \
  wagon-providers/wagon-ftp/target/wagon-ftp-%{version}-%{blevel}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/ftp-%{version}.jar
%add_to_maven_depmap org.apache.maven.wagon wagon-ftp %{version} JPP/%{name} ftp
install -m 644 \
  wagon-providers/wagon-http-lightweight/target/wagon-http-lightweight-%{version}-%{blevel}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/http-lightweight-%{version}.jar
%add_to_maven_depmap org.apache.maven.wagon wagon-http-lightweight %{version} JPP/%{name} http-lightweight
install -m 644 \
  wagon-providers/wagon-http-shared/target/wagon-http-shared-%{version}-%{blevel}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/http-shared-%{version}.jar
%add_to_maven_depmap org.apache.maven.wagon wagon-http-shared %{version} JPP/%{name} http-shared
install -m 644 \
  wagon-providers/wagon-http/target/wagon-http-%{version}-%{blevel}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/http-%{version}.jar

%add_to_maven_depmap org.apache.maven.wagon wagon-http %{version} JPP/%{name} http
install -m 644 \
  wagon-providers/wagon-ssh-common/target/wagon-ssh-common-%{version}-%{blevel}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/ssh-common-%{version}.jar
%add_to_maven_depmap org.apache.maven.wagon wagon-ssh-common %{version} JPP/%{name} ssh-common
install -m 644 \
  wagon-providers/wagon-ssh-common-test/target/wagon-ssh-common-test-%{version}-%{blevel}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/ssh-common-test-%{version}.jar
%add_to_maven_depmap org.apache.maven.wagon wagon-ssh-common-test %{version} JPP/%{name} ssh-common-test
install -m 644 \
  wagon-providers/wagon-ssh-external/target/wagon-ssh-external-%{version}-%{blevel}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/ssh-external-%{version}.jar
%add_to_maven_depmap org.apache.maven.wagon wagon-ssh-external %{version} JPP/%{name} ssh-external
install -m 644 \
  wagon-providers/wagon-ssh-ganymed/target/wagon-ssh-ganymed-%{version}-%{blevel}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/ssh-ganymed-%{version}.jar
%add_to_maven_depmap org.apache.maven.wagon wagon-ssh-ganymed %{version} JPP/%{name} ssh-ganymed
install -m 644 \
  wagon-providers/wagon-ssh/target/wagon-ssh-%{version}-%{blevel}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/ssh-%{version}.jar
%add_to_maven_depmap org.apache.maven.wagon wagon-ssh %{version} JPP/%{name} ssh
#install -m 644 \
#  wagon-providers/wagon-webdav/target/wagon-webdav-%{version}-%{blevel}.jar \
#  $RPM_BUILD_ROOT%{_javadir}/%{name}/webdav-%{version}.jar
#%%add_to_maven_depmap org.apache.maven.wagon wagon-webdav %{version} JPP/%{name} webdav

# Until webdav is available, map it to an empty dep
%add_to_maven_depmap org.apache.maven.wagon wagon-webdav %{version} JPP/maven2 empty-dep

install -m 644 \
  wagon-provider-test/target/wagon-provider-test-%{version}-%{blevel}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/provider-test-%{version}.jar
%add_to_maven_depmap org.apache.maven.wagon wagon-provider-test %{version} JPP/%{name} provider-test

(cd $RPM_BUILD_ROOT%{_javadir}/%{name} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)

# poms
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms
install -m 644 pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.maven-wagon-wagon.pom
install -m 644 wagon-provider-api/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.maven-wagon-provider-api.pom
install -m 644 wagon-provider-test/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.maven-wagon-provider-test.pom
install -m 644 wagon-providers/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.maven-wagon-providers.pom
install -m 644 wagon-providers/wagon-file/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.maven-wagon-file.pom
install -m 644 wagon-providers/wagon-ftp/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.maven-wagon-ftp.pom
install -m 644 wagon-providers/wagon-http-shared/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.maven-wagon-http-shared.pom
install -m 644 wagon-providers/wagon-http-lightweight/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.maven-wagon-http-lightweight.pom
install -m 644 wagon-providers/wagon-http/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.maven-wagon-http.pom
install -m 644 wagon-providers/wagon-ssh-common/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.maven-wagon-ssh-common.pom
install -m 644 wagon-providers/wagon-ssh-common-test/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.maven-wagon-ssh-common-test.pom
install -m 644 wagon-providers/wagon-ssh-external/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.maven-wagon-ssh-external.pom
install -m 644 wagon-providers/wagon-ssh-ganymed/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.maven-wagon-ssh-ganymed.pom
install -m 644 wagon-providers/wagon-ssh/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.maven-wagon-ssh.pom
#install -m 644 wagon-providers/wagon-webdav/pom.xml \
#    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.maven-wagon-webdav.pom

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}

install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/provider-api

ls -lR wagon-provider-api/target/

cp -pr wagon-provider-api/target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/provider-api

install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/file
cp -pr wagon-providers/wagon-file/target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/file

install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/ftp
cp -pr wagon-providers/wagon-ftp/target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/ftp

install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/http-lightweight
cp -pr wagon-providers/wagon-http-lightweight/target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/http-lightweight

install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/http-shared
cp -pr wagon-providers/wagon-http-shared/target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/http-shared

install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/http
cp -pr wagon-providers/wagon-http/target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/http

install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/ssh-common
cp -pr wagon-providers/wagon-ssh-common/target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/ssh-common

install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/ssh-common-test
cp -pr wagon-providers/wagon-ssh-common-test/target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/ssh-common-test

install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/ssh-external
cp -pr wagon-providers/wagon-ssh-external/target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/ssh-external

install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/ssh-ganymed
cp -pr wagon-providers/wagon-ssh-ganymed/target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/ssh-ganymed

install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/ssh
cp -pr wagon-providers/wagon-ssh/target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/ssh

##install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/webdav
##cp -pr wagon-providers/wagon-webdav/target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/ssh

install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/provider-test
cp -pr wagon-provider-test/target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/provider-test

ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# manual
install -d -m 755 $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
install -m 644 wagon-provider-api/LICENSE.txt \
                $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

#%if %{with_maven}
#cp -pr wagon-site/target/site/* \
#                $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
#%endif


%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(-,root,root,-)
%{_javadir}/*
%doc %{_docdir}/%{name}-%{version}/LICENSE.txt
%{_datadir}/maven2/poms/*.pom
%{_mavendepmapfragdir}

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

%if %{with_maven}
%files manual
%defattr(-,root,root,-)
%doc %{_docdir}/%{name}-%{version}
%endif

%changelog
* Wed Aug 19 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-0.2.b2.7
- Remove gcj parts.

* Wed Aug 19 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-0.2.b2.6
- Update to beta2 - sync with jpackage.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.3.a5.3.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.2.a5.3.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec  1 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 0:1.0-0.1.a5.3.5
- include missing dir below _docdir

* Fri Oct 03 2008 Matt Wringe <mwringe@redhat.com> - 0:1.0-0.1.a5.3.4
- added patch to make it compatible with the newer version of jsch

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.0-0.1.a5.3.3
- drop repotag
- fix license tag

* Sat Apr 05 2008 Matt Wringe <mwringe@redhat.com> - 0:1.0-0.1.a5.3jpp.2
- Rebuild with new version of jsch

* Tue Mar 13 2007 Matt Wringe <mwringe@redhat.com> - 0:1.0-0.1.a5.3jpp.1
- Merge in the changes neeeded to build without jetty
- Fix rpmlint issues
- Generate new *-build.xml files from pom.xml files as origins of
  *-project files is unknown.
- Remove maven1 project.xml files from sources
- Comment out various section requiring maven or javadocs
  (to be re-enabled at a future time). Note that the ant:ant task
  for maven2 does not currently generate javadocs.

* Tue Apr 04 2006 Ralph Apel <r.apel@r-apel.de> - 0:1.0-0.a5.3jpp
- Require j-c-codec, to build with j-c-httpclient = 3.0

* Thu Dec 22 2005 Deepak Bhole <dbhole@redhat.com> - 0:1.0-0.a5.2jpp
- Commented out potentially superfluous dependencies.
- Disabled wagon-scm

* Mon Nov 07 2005 Ralph Apel <r.apel at r-apel.de> - 0:1.0-0.a5.1jpp
- First JPackage build
