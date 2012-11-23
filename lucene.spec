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
Version:        3.6.0
Release:        6%{?dist}
Epoch:          0
License:        ASL 2.0
URL:            http://lucene.apache.org/
Group:          Development/Libraries
Source0:        http://www.apache.org/dist/lucene/java/%{version}/%{name}-%{version}-src.tgz
Source1:        lucene-%{version}-core-OSGi-MANIFEST.MF
Source2:        lucene-%{version}-analysis-OSGi-MANIFEST.MF
Source3:        ivy-conf.xml
#svn checkout http://svn.apache.org/repos/asf/lucene/dev/tags/lucene_solr_3_6_0/dev-tools
#tar caf dev-tools.tar.xz dev-tools/
Source4:        dev-tools.tar.xz
Patch1:         0001-Remove-bdb-packageset.patch
Patch2:         0002-Fix-version-string.patch
Patch3:         0003-Remove-classpath.patch
BuildRequires:  jpackage-utils >= 0:1.6
BuildRequires:  ant >= 0:1.6
BuildRequires:  ant-junit >= 0:1.6
BuildRequires:  junit
BuildRequires:  javacc
BuildRequires:  java-javadoc
BuildRequires:  jline
BuildRequires:  jtidy
BuildRequires:  regexp
BuildRequires:  apache-commons-digester
BuildRequires:  unzip
BuildRequires:  zip
BuildRequires:  java-devel >= 1:1.6.0
BuildRequires:  apache-commons-compress
BuildRequires:  icu4j
BuildRequires:  apache-ivy
BuildRequires:  lucene
# for tests
BuildRequires:  subversion

Provides:       lucene-core = %{epoch}:%{version}-%{release}
# previously used by eclipse but no longer needed
Obsoletes:      lucene-devel < %{epoch}:%{version}-%{release}
Obsoletes:      lucene-demo < %{epoch}:%{version}-%{release}
BuildArch:      noarch

Requires:       jpackage-utils

%description
Apache Lucene is a high-performance, full-featured text search
engine library written entirely in Java. It is a technology suitable
for nearly any application that requires full-text search, especially
cross-platform.

%package javadoc
Summary:        Javadoc for Lucene
Group:          Documentation
Requires:       jpackage-utils

%description javadoc
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

tar xfs %{SOURCE4}
pushd dev-tools
find . -name "pom.xml.template" -exec sed -i "s/@version@/%{version}/g" '{}' \;
popd

#%patch1 -p1 -b .db-javadoc
#%patch2 -p1 -b .fixmanifests
#%patch3 -p1 -b .removeclasspath

iconv --from=ISO-8859-1 --to=UTF-8 CHANGES.txt > CHANGES.txt.new

# prepare pom files (replace @version@ with real version)
find contrib -iname '*.pom.xml.template' -exec \
             sed -i "s:@version@:%{version}:g" \{\} \;

cp %{SOURCE3} .

#modify artifactIds to make it easier to map to fedora
sed -i -e "s|ant-junit|ant/ant-junit|g" test-framework/ivy.xml
sed -i -e "s|xercesImpl|xerces-j2|g" contrib/benchmark/ivy.xml
sed -i -e "s|jakarta-regexp|regexp|g" contrib/queries/ivy.xml


%build
mkdir -p docs
mkdir -p lib
export OPT_JAR_LIST="ant/ant-junit junit"
export CLASSPATH=$(build-classpath jline jtidy regexp commons-digester apache-commons-compress icu4j ivy)

ant -Divy.settings.file=ivy-conf.xml -Dbuild.sysclasspath=first \
  -Djavacc.home=%{_bindir}/javacc \
  -Djavacc.jar=%{_javadir}/javacc.jar \
  -Djavacc.jar.dir=%{_javadir} \
  -Djavadoc.link=file://%{_javadocdir}/java \
  -Dversion=%{version} \
  -Dfailonjavadocwarning=false \
  -Dmaven-tasks.uptodate=true \
  jar-lucene-core jar-test-framework docs javadocs build-contrib
        
# add missing OSGi metadata to manifests
mkdir META-INF
unzip -o build/core/lucene-core-%{version}.jar META-INF/MANIFEST.MF
cp %{SOURCE1} META-INF/MANIFEST.MF
sed -i '/^\r$/d' META-INF/MANIFEST.MF
zip -u build/core/lucene-core-%{version}.jar META-INF/MANIFEST.MF
unzip -o build/contrib/analyzers/common/lucene-analyzers-%{version}.jar META-INF/MANIFEST.MF
cp %{SOURCE2} META-INF/MANIFEST.MF
sed -i '/^\r$/d' META-INF/MANIFEST.MF
zip -u build/contrib/analyzers/common/lucene-analyzers-%{version}.jar META-INF/MANIFEST.MF

mv build/contrib/analyzers/common build/contrib/analyzers/analyzers
mv dev-tools/maven/lucene/contrib/analyzers/common dev-tools/maven/lucene/contrib/analyzers/analyzers

%install

# jars
install -d -m 0755 $RPM_BUILD_ROOT%{_javadir}
install -d -m 0755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -m 0644 build/core/%{name}-core-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
install -m 0644 dev-tools/maven/lucene/core/pom.xml.template \
           $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP-lucene-core.pom
ln -sf %{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-core.jar
%add_maven_depmap JPP-lucene-core.pom %{name}-core.jar

# contrib jars
install -d -m 0755 $RPM_BUILD_ROOT%{_javadir}/%{name}-contrib
for c in benchmark demo facet grouping highlighter \
         icu instantiated join memory misc pruning queries queryparser remote \
         spatial spellchecker xml-query-parser; do
    install -m 0644 build/contrib/$c/%{name}-${c}-%{version}.jar \
        $RPM_BUILD_ROOT%{_javadir}/%{name}-contrib/%{name}-${c}.jar

    install -m 0644 dev-tools/maven/lucene/contrib/$c/pom.xml.template \
               $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP.lucene-contrib-lucene-$c.pom
    %add_maven_depmap JPP.lucene-contrib-lucene-$c.pom %{name}-contrib/%{name}-${c}.jar
done

# contrib analyzers
for c in analyzers kuromoji phonetic smartcn stempel; do
    install -m 0644 build/contrib/analyzers/$c/%{name}-${c}-%{version}.jar \
        $RPM_BUILD_ROOT%{_javadir}/%{name}-contrib/%{name}-${c}.jar

    install -m 0644 dev-tools/maven/lucene/contrib/analyzers/$c/pom.xml.template \
               $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP.lucene-contrib-lucene-$c.pom
    %add_maven_depmap JPP.lucene-contrib-lucene-$c.pom %{name}-contrib/%{name}-${c}.jar
done

# main poms
install -m 0644 dev-tools/maven/lucene/contrib/pom.xml.template \
       $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP-lucene-contrib.pom
%add_maven_depmap JPP-lucene-contrib.pom
install -m 0644 dev-tools/maven/lucene/pom.xml.template \
       $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP-lucene-parent.pom
%add_maven_depmap JPP-lucene-parent.pom
install -m 0644 dev-tools/maven/pom.xml.template \
       $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP-lucene-solr-grandparent.pom
%add_maven_depmap JPP-lucene-solr-grandparent.pom

# javadoc
install -d -m 0755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr build/docs/api/* \
  $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%files
%doc CHANGES.txt LICENSE.txt README.txt NOTICE.txt
%{_mavenpomdir}/JPP*pom
%{_mavendepmapfragdir}/%{name}
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-core.jar

%files javadoc
%doc LICENSE.txt
%{_javadocdir}/%{name}

%files contrib
%{_javadir}/%{name}-contrib
%doc contrib/CHANGES.txt

%changelog
* Fri Nov 23 2012 Severin Gehwolf <sgehwolf@redhat.com> 0:3.6.0-6
- Fix OSGi medatada. In particular:
- Missing import javax.management (lucene-core)
- Missing import javax.xml.parsers and org.xml.sax.helpers
  (lucene-analysis)
- BundleVersion updated to 3.6.0 (lucene-core & lucene-analysis)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:3.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 5 2012 Alexander Kurtakov <akurtako@redhat.com> 0:3.6.0-4
- Properly install analyzers.

* Wed Jul 4 2012 Alexander Kurtakov <akurtako@redhat.com> 0:3.6.0-3
- Really fix manifests.

* Wed Jul 4 2012 Alexander Kurtakov <akurtako@redhat.com> 0:3.6.0-2
- Remove duplicated manifest entries.

* Tue Jul 3 2012 Alexander Kurtakov <akurtako@redhat.com> 0:3.6.0-1
- Update to upstream 3.6.0.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.9.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Sep 12 2011 Alexander Kurtakov <akurtako@redhat.com> 0:2.9.4-7
- Fix duplicate Manifes-version warnings.

* Mon Jun 27 2011 Alexander Kurtakov <akurtako@redhat.com> 0:2.9.4-6
- BR zip - fixes FTBFS.

* Tue May 3 2011 Alexander Kurtakov <akurtako@redhat.com> 0:2.9.4-5
- Update OSGi manifests.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.9.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb  8 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.9.4-3
- Fix empty lucene-analyzers (rhbz#675950)

* Wed Feb  2 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.9.4-2
- Add maven metadata (rhbz#566775)

* Mon Jan 31 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.9.4-1
- Update to latest 2.x version (3.x is not API compatible)
- Add new modules
- Enable tests again
- Versionless jars & javadocs

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
