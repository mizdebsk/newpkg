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

%global bname     wagon
%global blevel    beta-7

# FIXME1: wagon-scm has been disabled for now due to maven-scm dependency
# FIXME2: haltOnFailure/Error has been set to false for
# wagon-http/wagon-ssh-external tests due to failures.

Name:           maven-%{bname}
Version:        1.0
Release:        0.3.b7.22%{?dist}
Epoch:          0
Summary:        Tools to manage artifacts and deployment
License:        ASL 2.0
Group:          Development/Java
URL:            http://maven.apache.org/wagon
Source0:        wagon-1.0-%{blevel}-src.tar.xz
# svn export http://svn.apache.org/repos/asf/maven/wagon/tags/wagon-1.0-beta-7/
# tar caf wagon-1.0-beta-7-src.tar.xz wagon-1.0-beta-7

Source1:        wagon-1.0-jpp-depmap.xml
#patch for 1.0 beta-6
Patch0:         wagon-http-shared-pom_xml.patch
Patch1:         disable-tck.patch

BuildArch:      noarch
BuildRequires:  jpackage-utils >= 0:1.7.2
BuildRequires:  ant >= 0:1.6
BuildRequires:  junit
BuildRequires:  maven
BuildRequires:  maven-compiler-plugin
BuildRequires:  maven-install-plugin
BuildRequires:  maven-jar-plugin
BuildRequires:  maven-javadoc-plugin
BuildRequires:  maven-project-info-reports-plugin
BuildRequires:  maven-resources-plugin
BuildRequires:  maven-site-plugin
BuildRequires:  maven-surefire-plugin
BuildRequires:  maven-surefire-provider-junit
BuildRequires:  maven-enforcer-plugin
#BuildRequires:  maven2-default-skin
BuildRequires:  plexus-maven-plugin
BuildRequires:  maven-scm-test
BuildRequires:  xerces-j2
BuildRequires:  classworlds
BuildRequires:  nekohtml
BuildRequires:  ganymed-ssh2
BuildRequires:  apache-commons-codec
BuildRequires:  apache-commons-collections
BuildRequires:  apache-commons-net
BuildRequires:  jakarta-commons-httpclient
BuildRequires:  apache-commons-logging
#BuildRequires:  jakarta-slide-webdavclient
BuildRequires:  jsch
BuildRequires:  jtidy
BuildRequires:  plexus-container-default
BuildRequires:  plexus-interactivity
BuildRequires:  plexus-utils
BuildRequires:  servletapi5
BuildRequires:  xml-commons-apis
BuildRequires:  easymock

Requires:       ganymed-ssh2
Requires:       jakarta-commons-httpclient
Requires:       apache-commons-net
#Requires:       jakarta-slide-webdavclient
Requires:       jsch
Requires:       jtidy
Requires:       plexus-interactivity
Requires:       plexus-utils
Requires:       xml-commons-apis
Requires:       nekohtml
Requires:       xerces-j2

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
Requires:       jpackage-utils

%description javadoc
Javadoc for %{name}.

%package manual
Summary:        Documents for %{name}
Group:          Development/Documentation

%description manual
Documents for %{name}.

%prep
%setup -q -n %{bname}-%{version}-%{blevel}

#FIXME: have to drop wagon-webdav-jackrabbit until jackrabbit is available
sed -i "s|<module>wagon-webdav-jackrabbit</module>|<!-- <module>wagon-webdav-jackrabbit</module> -->|" wagon-providers/pom.xml

%patch0 -b .sav
%patch1

# To wire out jetty, plexus-avalon-personality and plexus-ftpd requirement
rm -f wagon-providers/wagon-ftp/src/test/java/org/apache/maven/wagon/providers/ftp/FtpWagonTest.java
rm -f wagon-providers/wagon-http-lightweight/src/test/java/org/apache/maven/wagon/providers/http/LightweightHttpWagonTest.java
rm -f wagon-providers/wagon-http-lightweight/src/test/java/org/apache/maven/wagon/providers/http/LightweightHttpWagonGzipTest.java
rm -f wagon-providers/wagon-http/src/test/java/org/apache/maven/wagon/providers/http/HttpWagonTest.java
rm -f wagon-providers/wagon-http/src/test/java/org/apache/maven/wagon/providers/http/HttpWagonGzipTest.java
#rm -f wagon-provider-test/src/main/java/org/apache/maven/wagon/WagonTestCase.java
rm -f wagon-provider-test/src/main/java/org/apache/maven/wagon/http/HttpWagonTestCase.java

%build
mvn-rpmbuild \
        -e \
        -Dmaven.local.depmap.file=%{SOURCE1} \
        -Dmaven.test.skip=true \
        install javadoc:aggregate

%install
# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/%{name}

install -m 644 \
  wagon-provider-api/target/wagon-provider-api-%{version}-%{blevel}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/provider-api.jar
%add_to_maven_depmap org.apache.maven.wagon wagon-provider-api %{version} JPP/%{name} provider-api

install -m 644 \
  wagon-providers/wagon-file/target/wagon-file-%{version}-%{blevel}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/file.jar
%add_to_maven_depmap org.apache.maven.wagon wagon-file %{version} JPP/%{name} file

install -m 644 \
  wagon-providers/wagon-ftp/target/wagon-ftp-%{version}-%{blevel}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/ftp.jar
%add_to_maven_depmap org.apache.maven.wagon wagon-ftp %{version} JPP/%{name} ftp

install -m 644 \
  wagon-providers/wagon-http/target/wagon-http-%{version}-%{blevel}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/http.jar

%add_to_maven_depmap org.apache.maven.wagon wagon-http %{version} JPP/%{name} http

install -m 644 \
  wagon-providers/wagon-http-lightweight/target/wagon-http-lightweight-%{version}-%{blevel}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/http-lightweight.jar
%add_to_maven_depmap org.apache.maven.wagon wagon-http-lightweight %{version} JPP/%{name} http-lightweight

install -m 644 \
  wagon-providers/wagon-http-shared/target/wagon-http-shared-%{version}-%{blevel}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/http-shared.jar
%add_to_maven_depmap org.apache.maven.wagon wagon-http-shared %{version} JPP/%{name} http-shared

install -m 644 \
  wagon-providers/wagon-scm/target/wagon-scm-%{version}-%{blevel}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/scm.jar
%add_to_maven_depmap org.apache.maven.wagon wagon-scm %{version} JPP/%{name} scm

install -m 644 \
  wagon-providers/wagon-ssh/target/wagon-ssh-%{version}-%{blevel}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/ssh.jar
%add_to_maven_depmap org.apache.maven.wagon wagon-ssh %{version} JPP/%{name} ssh

install -m 644 \
  wagon-providers/wagon-ssh-common/target/wagon-ssh-common-%{version}-%{blevel}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/ssh-common.jar
%add_to_maven_depmap org.apache.maven.wagon wagon-ssh-common %{version} JPP/%{name} ssh-common

install -m 644 \
  wagon-providers/wagon-ssh-common-test/target/wagon-ssh-common-test-%{version}-%{blevel}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/ssh-common-test.jar
%add_to_maven_depmap org.apache.maven.wagon wagon-ssh-common-test %{version} JPP/%{name} ssh-common-test

install -m 644 \
  wagon-providers/wagon-ssh-external/target/wagon-ssh-external-%{version}-%{blevel}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/ssh-external.jar
%add_to_maven_depmap org.apache.maven.wagon wagon-ssh-external %{version} JPP/%{name} ssh-external

#Until webdav is available, map it to an empty dep
#install -m 644 \
#  wagon-providers/wagon-webdav-jackrabbit/target/wagon-webdav-jackrabbit-%{version}-%{blevel}.jar \
#  $RPM_BUILD_ROOT%{_javadir}/%{name}/web-jackrabbit-%{version}.jar
#%%add_to_maven_depmap org.apache.maven.wagon wagon-webdav-jackrabbit %{version} JPP/%{name} webdav-jackrabbit

#install -m 644 \
#  wagon-providers/wagon-webdav/target/wagon-webdav-%{version}-%{blevel}.jar \
#  $RPM_BUILD_ROOT%{_javadir}/%{name}/webdav-%{version}.jar
#%%add_to_maven_depmap org.apache.maven.wagon wagon-webdav %{version} JPP/%{name} webdav

install -m 644 \
  wagon-provider-test/target/wagon-provider-test-%{version}-%{blevel}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/provider-test.jar
%add_to_maven_depmap org.apache.maven.wagon wagon-provider-test %{version} JPP/%{name} provider-test

%add_to_maven_depmap org.apache.maven.wagon wagon %{version} JPP/%{name} wagon
%add_to_maven_depmap org.apache.maven.wagon wagon-providers %{version} JPP/%{name} providers

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
install -m 644 wagon-providers/wagon-scm/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.maven-wagon-scm.pom
install -m 644 wagon-providers/wagon-ssh-common/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.maven-wagon-ssh-common.pom
install -m 644 wagon-providers/wagon-ssh-common-test/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.maven-wagon-ssh-common-test.pom
install -m 644 wagon-providers/wagon-ssh-external/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.maven-wagon-ssh-external.pom
install -m 644 wagon-providers/wagon-ssh/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.maven-wagon-ssh.pom
#install -m 644 wagon-providers/wagon-webdav/pom.xml \
#    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.maven-wagon-webdav.pom

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# manual
install -d -m 755 $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
#install -m 644 wagon-provider-api/LICENSE.txt \
#                $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

#%if %{with_maven}
#cp -pr wagon-site/target/site/* \
#                $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
#%endif


%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(-,root,root,-)
%{_javadir}/*
%{_mavenpomdir}/*.pom
%{_mavendepmapfragdir}/*

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}

%files manual
%defattr(-,root,root,-)
%doc %{_docdir}/%{name}-%{version}

%changelog
* Tue Apr 26 2011 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-0.3.b7.22
- Install wagon-providers depmap too.

* Tue Apr 26 2011 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-0.3.b7.21
- Install wagon pom depmap.
- Use maven 3 for build.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.3.b7.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 13 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-0.2.b7.1
- Update to beta 7.
- Adapt to current guidelines.
- Fix pom names.

* Thu Sep 9 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-0.2.b6.3
- Use javadoc:aggregate.
- Drop ant build.
- Use global instead of define.

* Fri May 14 2010 Yong Yang <yyang@redhat.com> 0:1.0-0.2.b6.2
- Create patch for wagon-http-shared pom.xml

* Wed May 12 2010 Yong Yang <yyang@redhat.com> 0:1.0-0.2.b6.1
- Update to beta 6, build with with_maven 1

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
