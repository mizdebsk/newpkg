# Copyright (c) 2000-2005, JPackage Project
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

Summary:        High-performance, full-featured text search engine
Name:           lucene
Version:        2.4.1
Release:        7%{?dist}
Epoch:          0
License:        ASL 2.0
URL:            http://lucene.apache.org/
Group:          Development/Libraries
Source0:        http://archive.apache.org/dist/lucene/java/%{name}-%{version}-src.tar.gz
Source1:        lucene-1.9-OSGi-MANIFEST.MF
Source2:        lucene-1.9-analysis-OSGi-MANIFEST.MF
Patch1:         lucene-2.4.1-db-javadoc.patch
Patch2:         %{name}-2.4.1-fixmanifests.patch
Patch4:         lucli-remove-classpath.patch
BuildRequires:  jpackage-utils >= 0:1.6
BuildRequires:  ant >= 0:1.6
BuildRequires:  ant-junit >= 0:1.6
#BuildRequires:  berkeleydb
#BuildRequires:  berkeleydb-native >= 0:4.3.29
BuildRequires:  junit
BuildRequires:  javacc
BuildRequires:  java-javadoc
BuildRequires:  jline
BuildRequires:  jtidy
BuildRequires:  regexp
BuildRequires:  apache-commons-digester
BuildRequires:  unzip
BuildRequires:  java-devel >= 1:1.6.0
Provides:       lucene-core = %{epoch}:%{version}-%{release}
# previously used by eclipse but no longer needed
Obsoletes:      lucene-devel < %{version}
BuildArch:      noarch
Requires:       jpackage-utils

%description
Jakarta Lucene is a high-performance, full-featured text search engine
written entirely in Java. It is a technology suitable for nearly any
application that requires full-text search, especially cross-platform.

%package javadoc
Summary:        Javadoc for Lucene
Group:          Documentation
Requires:       jpackage-utils

%description javadoc
%{summary}.

%package demo
Summary:        Lucene demonstration library
Group:          Development/Libraries
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description demo
%{summary}.

%package contrib
Summary:        Lucene contributed extensions
Group:          Development/Libraries
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description contrib
%{summary}.

%prep
%setup -q -n %{name}-%{version}
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;

%patch1 -p1 -b .db-javadoc
%patch2 -p1 -b .fixmanifests
%patch4

iconv --from=ISO-8859-1 --to=UTF-8 CHANGES.txt > CHANGES.txt.new 

%build
mkdir -p docs
mkdir -p lib
export OPT_JAR_LIST="ant/ant-junit junit"
export CLASSPATH=$(build-classpath jline jtidy regexp commons-digester)
#pushd contrib/db/bdb/lib
#ln -sf $(build-classpath berkeleydb-native) .
#popd
#pushd contrib/db/bdb-je/lib
#ln -sf $(build-classpath berkeleydb) .
#popd
rm -r contrib/db

#FIXME: Tests freeze randomly. Turning on debug messages shows warnings like:

# [junit] GC Warning: Repeated allocation of very large block (appr. size 512000):
# [junit]   May lead to memory leak and poor performance.

# See: http://koji.fedoraproject.org/koji/getfile?taskID=169839&name=build.log
# for an example

ant -Dbuild.sysclasspath=first \
  -Djavacc.home=%{_bindir}/javacc \
  -Djavacc.jar=%{_javadir}/javacc.jar \
  -Djavacc.jar.dir=%{_javadir} \
  -Djavadoc.link=%{_javadocdir}/java \
  -Dversion=%{version} \
  package
#  package test generate-test-reports

# add missing OSGi metadata to manifests
mkdir META-INF
unzip -o build/lucene-core-%{version}.jar META-INF/MANIFEST.MF
cat %{SOURCE1} >> META-INF/MANIFEST.MF
sed -i '/^\r$/d' META-INF/MANIFEST.MF
zip -u build/lucene-core-%{version}.jar META-INF/MANIFEST.MF
unzip -o build/contrib/analyzers/lucene-analyzers-%{version}.jar META-INF/MANIFEST.MF
cat %{SOURCE2} >> META-INF/MANIFEST.MF
sed -i '/^\r$/d' META-INF/MANIFEST.MF
zip -u build/contrib/analyzers/lucene-analyzers-%{version}.jar META-INF/MANIFEST.MF

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d -m 0755 $RPM_BUILD_ROOT%{_javadir}
install -m 0644 build/%{name}-core-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
install -m 0644 build/%{name}-demos-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-demos-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# contrib jars
install -d -m 0755 $RPM_BUILD_ROOT%{_javadir}/%{name}-contrib
for c in analyzers ant highlighter lucli memory misc queries similarity snowball spellchecker surround swing wordnet xml-query-parser; do
    install -m 0644 build/contrib/$c/%{name}-${c}-%{version}.jar \
        $RPM_BUILD_ROOT%{_javadir}/%{name}-contrib
done
(cd $RPM_BUILD_ROOT%{_javadir}/%{name}-contrib && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# javadoc
install -d -m 0755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr build/docs/api/* \
  $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# webapp
install -d -m 0755 $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
install -m 0644 build/%{name}web.war \
  $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc CHANGES.txt LICENSE.txt README.txt
%{_javadir}/%{name}-%{version}.jar
%{_javadir}/%{name}.jar
%{_datadir}/%{name}-%{version}

%files javadoc
%defattr(-,root,root,-)
%doc LICENSE.txt
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

%files contrib
%defattr(-,root,root,-)
%{_javadir}/%{name}-contrib
%doc contrib/CHANGES.txt

%files demo
%defattr(-,root,root,-)
%{_javadir}/%{name}-demos-%{version}.jar
%{_javadir}/%{name}-demos.jar

%changelog
* Wed Oct 13 2010 Alexander Kurtakov <akurtako@redhat.com> 0:2.4.1-7
- BR java 1.6.0.

* Wed Oct 13 2010 Alexander Kurtakov <akurtako@redhat.com> 0:2.4.1-6
- Fix merge review comments (rhbz#226110).

* Fri Oct 01 2010 Caolán McNamara <caolanm@redhat.com> 0:2.4.1-5
- remove empty lines from MANIFEST.MF

* Fri Oct 01 2010 Caolán McNamara <caolanm@redhat.com> 0:2.4.1-4
- Resolves: rhbz#615609 custom MANIFEST.MF in lucene drops
  "Specification-Version"

* Mon Jun 7 2010 Alexander Kurtakov <akurtako@redhat.com> 0:2.4.1-3
- Fix build.
- FIx various rpmlint warnings.

* Fri Mar 5 2010 Alexander Kurtakov <akurtako@redhat.com> 0:2.4.1-2
- Drop gcj_support.

* Tue Dec  1 2009 Orion Poplawski <orion@cora.nwra.com> - 0:2.4.1-1
- Update to 2.4.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.3.1-5.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Apr 30 2009 Deepak Bhole <dbhole@redhat.com> - 0:2.3.1-4.5
- rhbz #465344: Fix Implementation-Version and remove Class-Path from manifest

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.3.1-4.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jul 14 2008 Andrew Overholt <overholt@redhat.com> 0:2.3.1-3.4
- Update OSGi manifest data for Eclipse SDK 3.4

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:2.3.1-3.2
- drop repotag

* Thu May 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:2.3.1-3jpp.1
- fix license tag

* Mon May 19 2008 Lubomir Rintel <lkundrak@v3.sk> - 0:2.3.1-3jpp.0
- Correct gcj-compat dependencies, so that this builds on RHEL
- Use --without gcj to disable gcj aot compilation

* Mon May 5 2008 Lubomir Rintel <lkundrak@v3.sk> - 0:2.3.1-2jpp.0
- Unbreak build by repacing the version patch with and -Dversion

* Mon May 5 2008 Lubomir Rintel <lkundrak@v3.sk> - 0:2.3.1-1jpp.0
- 2.3.1, bugfixes only

* Tue Feb 19 2008 Lubomir Kundrak <lkundrak@redhat.com> - 0:2.3.0-1jpp.0
- 2.3.0 (#228141)

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:1.9.1-2jpp.5
- Autorebuild for GCC 4.3

* Fri Sep 21 2007 Deepak Bhole <dbhole@redhat.com> 1.9.1-1jpp.5
- Disable tests due to random hangs (see FIXME comment above ant call)

* Thu Sep 20 2007 Deepak Bhole <dbhole@redhat.com> 0:1.9.1-1jpp.4
- Rebuild for ppc32 execmem issue and new build-id

* Thu Aug 02 2007 Ben Konrath <bkonrath@redhat.com> 0:1.9.1-1jpp.3
- Cleanup packaging of OSGi manifests.

* Tue Jul 31 2007 Ben Konrath <bkonrath@redhat.com> 0:1.9.1-1jpp.2
- Use OSGi manifests from eclipse 3.3.0 instead of merged manifests.
- Resolves: #250221.

* Tue Jul 17 2007 Ben Konrath <bkonrath@redhat.com> 0:1.9.1-1jpp.1
- Disable db sub-package.
- Disable generating test report.
- Add OSGi manifest.
- Obsolete lucene-devel.

* Wed Mar 29 2006 Ralph Apel <r.apel@r-apel.de> 0:1.9.1-1jpp
- Upgrade to 1.9.1

* Tue Apr 26 2005 Ville Skyttä <scop at jpackage.org> - 0:1.4.3-2jpp
- Add unversioned javadoc dir symlink.
- Crosslink with local JDK javadocs.
- Convert specfile to UTF-8.
- Fix URLs.

* Mon Jan 10 2005 Kaj J. Niemi <kajtzu@fi.basen.net> 0:1.4.3
- 1.4.3

* Mon Aug 23 2004 Fernando Nasser <fnasser at redhat.com> - 0:1.3-3jpp
- Rebuild with Ant 1.6.2

* Tue Jun 01 2004 Randy Watler <rwatler at finali.com> - 0:1.3-2jpp
- Upgrade to Ant 1.6.X

* Wed Jan 21 2004 David Walluck <david@anti-microsoft.org> 0:1.3-1jpp
- 1.3

* Wed Mar 26 2003 Ville Skyttä <scop at jpackage.org> - 0:1.2-2jpp
- Rebuilt for JPackage 1.5.

* Thu Mar  6 2003 Ville Skyttä <scop at jpackage.org> - 1.2-1jpp
- First JPackage release.
