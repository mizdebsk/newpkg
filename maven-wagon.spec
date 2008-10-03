# Needs to be re-enabled when spec files starts building with maven2
## If you don't want to build with maven, and use straight ant instead,
## give rpmbuild option '--without maven'
#
#%define _without_maven 1
#%define with_maven %{!?_without_maven:1}%{?_without_maven:0}
#%define without_maven %{?_without_maven:1}%{!?_without_maven:0}

%define bname     wagon

# FIXME1: wagon-scm has been disabled for now due to maven-scm dependency
# FIXME2: haltOnFailure/Error has been set to false for 
# wagon-http/wagon-ssh-external tests due to failures.
# FIXME3: Change spec file to build with maven2
# FIXME4: Add javadoc options ant build

Name:           maven-%{bname}
Version:        1.0
Release:        0.1.a5.3.4%{?dist}
Epoch:          0
Summary:        Tools to manage artifacts and deployment
License:        ASL 2.0
Group:          Development/Java
URL:            http://maven.apache.org/wagon
Source0:        wagon-1.0-alpha-5-src.tar.gz
# svn export http://svn.apache.org/repos/asf/maven/wagon/tags/wagon-1.0-alpha-5/
# tar czvf wagon-1.0-alpha-5-src.tar.gz wagon-1.0-alpha-5

# The following sources (1-17) were generated by running the maven2 ant task
# inside the root directory of Source0: "mvn ant:ant"
Source1:        wagon-1.0-alpha5-provider-api-build.xml
Source3:        wagon-1.0-alpha5-provider-test-build.xml
Source5:        wagon-1.0-alpha5-providers-file-build.xml
Source7:        wagon-1.0-alpha5-providers-ftp-build.xml
Source9:        wagon-1.0-alpha5-providers-http-build.xml
Source11:       wagon-1.0-alpha5-providers-http-lightweight-build.xml
Source13:       wagon-1.0-alpha5-providers-scm-build.xml
Source15:       wagon-1.0-alpha5-providers-ssh-build.xml
Source17:       wagon-1.0-alpha5-providers-ssh-external-build.xml

Patch0:         wagon-1.0-provider-api-index.patch
Patch1:         wagon-1.0-FtpWagon.patch
Patch2:         wagon-1.0-ScmWagon.patch
Patch3:         wagon-1.0-TraditionalUIKeyboardInteractive.patch
Patch4:         maven-wagon-AbstractSshWagon.patch

Patch5:         wagon-1.0-alpha5-provider-api-build_xml.patch
Patch6:         wagon-1.0-alpha5-providers-file-build_xml.patch
Patch7:         wagon-1.0-alpha5-providers-ftp-build_xml.patch
Patch8:         wagon-1.0-alpha5-providers-http-build_xml.patch
Patch9:         wagon-1.0-alpha5-providers-http-lightweight-build_xml.patch
Patch10:        wagon-1.0-alpha5-providers-scm-build_xml.patch
Patch11:        wagon-1.0-alpha5-providers-ssh-build_xml.patch
Patch12:        wagon-1.0-alpha5-providers-ssh-external-build_xml.patch
Patch13:        wagon-1.0-alpha5-provider-test-build_xml.patch
Patch14:	maven-wagon-jsch.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  jpackage-utils >= 0:1.6
BuildRequires:  ant
BuildRequires:  junit
BuildRequires:  classworlds
BuildRequires:  concurrent
BuildRequires:  jakarta-commons-net
BuildRequires:  jakarta-commons-codec
BuildRequires:  jakarta-commons-collections
BuildRequires:  jakarta-commons-httpclient
BuildRequires:  jakarta-commons-logging
BuildRequires:  jsch >= 0:0.1.31-2jpp.3
BuildRequires:  oro
BuildRequires:  plexus-container-default
BuildRequires:  plexus-interactivity
BuildRequires:  plexus-utils
BuildRequires:  servletapi5
BuildRequires:  jline

# Commented until wagon-scm subproject can be built.
#BuildRequires:  excalibur-avalon-framework-api
#BuildRequires:  excalibur-avalon-framework-impl
#BuildRequires:  excalibur-cornerstone-connection-api
#BuildRequires:  excalibur-cornerstone-connection-impl
#BuildRequires:  excalibur-cornerstone-sockets-api
#BuildRequires:  excalibur-cornerstone-sockets-impl
#BuildRequires:  excalibur-cornerstone-threads-api
#BuildRequires:  excalibur-cornerstone-threads-impl
#BuildRequires:  excalibur-pool-api
#BuildRequires:  excalibur-pool-impl
#BuildRequires:  excalibur-thread-api
#BuildRequires:  excalibur-thread-impl
#BuildRequires:  maven-scm
#BuildRequires:  plexus-avalon-personality
#BuildRequires:  plexus-ftpd
#BuildRequires:  plexus-jetty-httpd

%description
Maven Wagon is a transport abstraction that is used in Maven's 
artifact and repository handling code. Currently wagon has the 
following providers:
* File
* HTTP
* FTP
* SSH/SCP
* WebDAV (in progress)

# Needs to be re-enabled when spec files starts building with maven2
#%package javadoc
#Summary:        Javadoc for %{name}
#Group:          Development/Documentation
#
#%description javadoc
#Javadoc for %{name}.
#
#%if %{with_maven}
#%package manual
#Summary:        Documents for %{name}
#Group:          Development/Documentation

#%description manual
#Documents for %{name}.
#%endif

%prep
%setup -q -n %{bname}-%{version}-alpha-5
cp %{SOURCE1} wagon-provider-api/build.xml
cp %{SOURCE3} wagon-provider-test/build.xml
cp %{SOURCE5} wagon-providers/wagon-file/build.xml
cp %{SOURCE7} wagon-providers/wagon-ftp/build.xml
cp %{SOURCE9} wagon-providers/wagon-http/build.xml
cp %{SOURCE11} wagon-providers/wagon-http-lightweight/build.xml
cp %{SOURCE13} wagon-providers/wagon-scm/build.xml
cp %{SOURCE15} wagon-providers/wagon-ssh/build.xml
cp %{SOURCE17} wagon-providers/wagon-ssh-external/build.xml

%patch0 -b .sav
%patch1 -b .sav
%patch2 -b .sav
%patch3 -b .sav
%patch4 -b .sav

%patch5 -b .sav
%patch6 -b .sav
%patch7 -b .sav
%patch8 -b .sav
%patch9 -b .sav
%patch10 -b .sav
%patch11 -b .sav
%patch12 -b .sav
%patch13 -b .sav
%patch14 -b .sav

%build
pushd wagon-provider-api
export MAVEN_REPOSITORY=$PWD/.m2/respository
mkdir -p $MAVEN_REPOSITORY
build-jar-repository -s -p $MAVEN_REPOSITORY plexus/utils
ant -Dmaven.mode.offline=true -Dmaven.repo.local=$MAVEN_REPOSITORY jar #javadoc
popd

pushd wagon-provider-test
export MAVEN_REPOSITORY=$PWD/.m2/respository
mkdir -p $MAVEN_REPOSITORY
cp ../wagon-provider-api/target/wagon-provider-api*.jar $MAVEN_REPOSITORY
build-jar-repository -s -p $MAVEN_REPOSITORY plexus/container-default plexus/utils junit
ant -Dmaven.mode.offline=true -Dmaven.repo.local=$MAVEN_REPOSITORY jar #javadoc
popd

pushd wagon-providers/wagon-file
export MAVEN_REPOSITORY=$PWD/.m2/respository
mkdir -p $MAVEN_REPOSITORY
cp ../../wagon-provider-api/target/wagon-provider-api*.jar $MAVEN_REPOSITORY
cp ../../wagon-provider-test/target/wagon-provider-test*.jar $MAVEN_REPOSITORY
build-jar-repository -s -p $MAVEN_REPOSITORY plexus/container-default plexus/utils classworlds
ant  -Dmaven.mode.offline=true -Dmaven.repo.local=$MAVEN_REPOSITORY jar #javadoc
popd

pushd wagon-providers/wagon-http-lightweight
export MAVEN_REPOSITORY=$PWD/.m2/respository
mkdir -p $MAVEN_REPOSITORY
cp ../../wagon-provider-api/target/wagon-provider-api*.jar $MAVEN_REPOSITORY
cp ../../wagon-provider-test/target/wagon-provider-test*.jar $MAVEN_REPOSITORY
# We don't ship Jetty
# so we removed 'jetty4' and 'plexus/jetty-httpd' from the list below
build-jar-repository -s -p $MAVEN_REPOSITORY plexus/container-default plexus/utils classworlds servletapi5

# Since we don't ship jetty, we also need to remove tests that need it
rm -f src/test/java/org/apache/maven/wagon/providers/http/LightweightHttpWagonTest.java

ant -Dmaven.mode.offline=true -Dmaven.repo.local=$MAVEN_REPOSITORY jar #javadoc
popd

# commented until wagon-scm can be built
#pushd wagon-providers/wagon-scm
#%if %{with_maven}
#maven \
#        -Dmaven.repo.remote=file:/usr/share/maven-1.0/repository \
#        -Dmaven.home.local=$MAVEN_HOME_LOCAL \
#        jar:install javadoc
#%else
#mkdir -p target/lib
#cp ../../wagon-provider-api/target/wagon-provider-api*.jar target/lib
#cp ../../wagon-provider-test/target/wagon-provider-test*.jar target/lib
#build-jar-repository -s -p target/lib plexus/container-default plexus/utils classworlds \
#maven-scm/api \
#maven-scm/test \
#maven-scm/manager-plexus \
#maven-scm/provider-cvs \
#maven-scm/provider-svn \

#ant jar javadoc
#%endif
#popd

pushd wagon-providers/wagon-ssh-external
export MAVEN_REPOSITORY=$PWD/.m2/respository
mkdir -p $MAVEN_REPOSITORY
cp ../../wagon-provider-api/target/wagon-provider-api*.jar $MAVEN_REPOSITORY
cp ../../wagon-provider-test/target/wagon-provider-test*.jar $MAVEN_REPOSITORY
build-jar-repository -s -p $MAVEN_REPOSITORY plexus/container-default plexus/utils classworlds
export ANT_OPTS="-Dtest.host=$(hostname)"
ant -Dmaven.mode.offline=true -Dmaven.repo.local=$MAVEN_REPOSITORY -Dtest.host=$(hostname) jar #javadoc
popd

pushd wagon-providers/wagon-ssh
export MAVEN_REPOSITORY=$PWD/.m2/respository
mkdir -p $MAVEN_REPOSITORY
cp ../../wagon-provider-api/target/wagon-provider-api*.jar $MAVEN_REPOSITORY
cp ../../wagon-provider-test/target/wagon-provider-test*.jar $MAVEN_REPOSITORY
build-jar-repository -s -p $MAVEN_REPOSITORY plexus/container-default plexus/utils classworlds \
plexus/interactivity-api plexus/interactivity-jline jsch jline
ant -Dmaven.mode.offline=true -Dmaven.repo.local=$MAVEN_REPOSITORY -Dtest.host=$(hostname) jar #javadoc
popd

pushd wagon-providers/wagon-http
export MAVEN_REPOSITORY=$PWD/.m2/respository
mkdir -p $MAVEN_REPOSITORY
cp ../../wagon-provider-api/target/wagon-provider-api*.jar $MAVEN_REPOSITORY
cp ../../wagon-provider-test/target/wagon-provider-test*.jar $MAVEN_REPOSITORY
# We don't ship Jetty
# so we removed 'jetty4' and 'plexus/jetty-httpd' from the list below
build-jar-repository -s -p $MAVEN_REPOSITORY plexus/container-default plexus/utils classworlds \
commons-httpclient commons-logging servletapi5

# Since we don't ship jetty, we also need to remove tests that need it
rm -f src/test/java/org/apache/maven/wagon/providers/http/HttpWagonTest.java

ant -Dmaven.mode.offline=true -Dmaven.repo.local=$MAVEN_REPOSITORY jar #javadoc
popd

pushd wagon-providers/wagon-ftp
export MAVEN_REPOSITORY=$PWD/.m2/respository
mkdir -p $MAVEN_REPOSITORY
cp ../../wagon-provider-api/target/wagon-provider-api*.jar $MAVEN_REPOSITORY
cp ../../wagon-provider-test/target/wagon-provider-test*.jar $MAVEN_REPOSITORY
# FIXME we don't ship plexus ftpd
# After we get Excalibur, it would be nice to ship it also
# and add plexus/ftpd back into the list below

build-jar-repository -s -p $MAVEN_REPOSITORY plexus/container-default plexus/utils classworlds \
concurrent \
commons-collections commons-net \
oro
ant -Dmaven.mode.offline=true -Dmaven.repo.local=$MAVEN_REPOSITORY jar #javadoc
popd

%install
rm -rf $RPM_BUILD_ROOT
# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/%{name}
install -m 644 wagon-provider-api/target/wagon-provider-api-1.0-alpha-5.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/provider-api-%{version}.jar
install -m 644 wagon-providers/wagon-file/target/wagon-file-1.0-alpha-5.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/file-%{version}.jar
install -m 644 wagon-providers/wagon-ftp/target/wagon-ftp-1.0-alpha-5.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/ftp-%{version}.jar
install -m 644 wagon-providers/wagon-http-lightweight/target/wagon-http-lightweight-1.0-alpha-5.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/http-lightweight-%{version}.jar
install -m 644 wagon-providers/wagon-http/target/wagon-http-1.0-alpha-5.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/http-%{version}.jar

# commented until wabon-scm can be built
#install -m 644 wagon-providers/wagon-scm/target/wagon-scm-1.0-alpha-5.jar \
#  $RPM_BUILD_ROOT%{_javadir}/%{name}/scm-%{version}.jar

install -m 644 wagon-providers/wagon-ssh-external/target/wagon-ssh-external-1.0-alpha-5.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/ssh-external-%{version}.jar
install -m 644 wagon-providers/wagon-ssh/target/wagon-ssh-1.0-alpha-5.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/ssh-%{version}.jar
install -m 644 wagon-provider-test/target/wagon-provider-test-1.0-alpha-5.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/provider-test-%{version}.jar

(cd $RPM_BUILD_ROOT%{_javadir}/%{name} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)

install -d -m 755 $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
install -m 644 wagon-provider-api/LICENSE.txt $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

# Needs to be re-enabled when spec files starts building with maven2
## javadoc
#install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
#
#install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/provider-api
#cp -pr wagon-provider-api/target/docs/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/provider-api
#rm -rf wagon-provider-api/target/docs/apidocs
#
#install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/file
#cp -pr wagon-providers/wagon-file/target/docs/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/file
#rm -rf wagon-providers/wagon-file/target/docs/apidocs
#
#install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/ftp
#cp -pr wagon-providers/wagon-ftp/target/docs/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/ftp
#rm -rf wagon-providers/wagon-ftp/target/docs/apidocs
#
#install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/http-lightweight
#cp -pr wagon-providers/wagon-http-lightweight/target/docs/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/http-lightweight
#rm -rf wagon-providers/wagon-http-lightweight/target/docs/apidocs
#
#install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/http
#cp -pr wagon-providers/wagon-http/target/docs/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/http
#rm -rf wagon-providers/wagon-http/target/docs/apidocs
#
## commented until wagon-scm can be build
##install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/scm
##cp -pr wagon-providers/wagon-scm/target/docs/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/scm
##rm -rf wagon-providers/wagon-scm/target/docs/apidocs
#
#install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/ssh-external
#cp -pr wagon-providers/wagon-ssh-external/target/docs/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/ssh-external
#rm -rf wagon-providers/wagon-ssh-external/target/docs/apidocs
#
#install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/ssh
#cp -pr wagon-providers/wagon-ssh/target/docs/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/ssh
#rm -rf wagon-providers/wagon-ssh/target/docs/apidocs
#
#install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/provider-test
#cp -pr wagon-provider-test/target/docs/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/provider-test
#rm -rf wagon-provider-test/target/docs/apidocs
#
#ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} 
#
# manual
#install -d -m 755 $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
#install -m 644 wagon-provider-api/LICENSE.txt \
#                $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
#%if %{with_maven}
#install -d -m 755 $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/provider-api
#cp -pr wagon-provider-api/target/docs/* \
#                $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/provider-api
#
## commented until wagon-scm can be built
##install -d -m 755 $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/file
##cp -pr wagon-providers/wagon-file/target/docs/* \
##               $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/file
#
#install -d -m 755 $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/ftp
#cp -pr wagon-providers/wagon-ftp/target/docs/* \
#                $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/ftp
#install -d -m 755 $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/http
#cp -pr wagon-providers/wagon-http/target/docs/* \
#                $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/http
#
## commented until wagon-scm can be built
##install -d -m 755 $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/http-lightweight
##cp -pr wagon-providers/wagon-http-lightweight/target/docs/* \
##               $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/http-lightweight
##install -d -m 755 $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/scm
##cp -pr wagon-providers/wagon-scm/target/docs/* \
##               $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/scm
#
#install -d -m 755 $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/ssh
#cp -pr wagon-providers/wagon-ssh/target/docs/* \
#                $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/ssh
#
## commented until wagon-scm can be built
##install -d -m 755 $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/ssh-external
##cp -pr wagon-providers/wagon-ssh-external/target/docs/* \
##               $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/ssh-external
#%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_javadir}/*
%doc %{_docdir}/%{name}-%{version}/LICENSE.txt

# Needs to be re-enabled when spec files starts building with maven2
#%files javadoc
#%defattr(-,root,root,-)
#%doc %{_javadocdir}/*

# Needs to be re-enabled when spec files starts building with maven2
#%if %{with_maven}
#%files manual
#%defattr(-,root,root,-)
#%doc %{_docdir}/%{name}-%{version}
#%endif

%changelog
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

