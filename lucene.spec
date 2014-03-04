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

%bcond_with test

Summary:        High-performance, full-featured text search engine
Name:           lucene
Version:        4.7.0
Release:        1%{?dist}
Epoch:          0
License:        ASL 2.0
URL:            http://lucene.apache.org/
Source0:        http://www.apache.org/dist/lucene/java/%{version}/%{name}-%{version}-src.tgz
Source1:        lucene-%{version}-core-OSGi-MANIFEST.MF
Source2:        lucene-%{version}-analysis-OSGi-MANIFEST.MF

Patch0:         0001-disable-ivy-settings.patch
# upstream randomizedtesting bundles it's deps
Patch3:         0001-fix-randomizedtesting-deps.patch
# dependencies on non-maven artifacts (tar.gz files)
Patch4:         0001-disable-mecab.patch

BuildRequires:  git
BuildRequires:  simple-xml
BuildRequires:  jpackage-utils
BuildRequires:  ant
BuildRequires:  regexp
BuildRequires:  apache-commons-compress
BuildRequires:  ivy-local
BuildRequires:  icu4j
BuildRequires:  httpcomponents-client
BuildRequires:  jetty
BuildRequires:  morfologik-stemming
BuildRequires:  uimaj
BuildRequires:  uima-addons
BuildRequires:  spatial4j
BuildRequires:  nekohtml
BuildRequires:  xerces-j2
BuildRequires:  groovy
BuildRequires:  mvn(javax.servlet:servlet-api)
BuildRequires:  mvn(org.antlr:antlr-runtime)

# test deps
BuildRequires:  junit
BuildRequires:  randomizedtesting-junit4-ant
BuildRequires:  randomizedtesting-runner

Provides:       lucene-core = %{epoch}:%{version}-%{release}
# previously used by eclipse but no longer needed
Obsoletes:      lucene-devel < %{epoch}:%{version}-%{release}
Obsoletes:      lucene-demo < %{epoch}:%{version}-%{release}
# previously distributed separately, but merged into main package
Provides:       lucene-contrib = %{version}-%{release}
Obsoletes:      lucene-contrib < %{version}-%{release}

BuildArch:      noarch

BuildRequires:  maven-local

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

%prep
%autosetup -S git -n %{name}-%{version}

# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;

sed -i 's|groovy-all|groovy|' common-build.xml

# incorrect artifact type
sed -i 's/type="orbit"//' replicator/ivy.xml

# interferes with XMvn local resolution
rm ivy-settings.xml

# ivy.xml files don't specify revision, which makes them invalid and would
# crash %%mvn_artifact
find . -name 'ivy.xml' -exec sed -i 's/<info/<info revision="%{version}"/' {} \;

# failing due to old version of nekohtml
rm benchmark/src/test/org/apache/lucene/benchmark/byTask/feeds/TestHtmlParser.java

# old API
rm -r replicator/src/test/*
rm -r spatial/src/test/*

%build
ant jar javadocs \
  %if %{with test}
  test \
  %endif
  -Divy.mode=local \
  -Dversion=%{version} \
  -Djavadoc.link=file://%{_javadocdir}/java \
  -Dfailonjavadocwarning=false

# add missing OSGi metadata to manifests
mkdir META-INF
unzip -o build/core/lucene-core-%{version}.jar META-INF/MANIFEST.MF
cat %{SOURCE1} >> META-INF/MANIFEST.MF
sed -i '/^\r$/d' META-INF/MANIFEST.MF
zip -u build/core/lucene-core-%{version}.jar META-INF/MANIFEST.MF

unzip -o build/analysis/common/lucene-analyzers-common-%{version}.jar META-INF/MANIFEST.MF
cat %{SOURCE2} >> META-INF/MANIFEST.MF
sed -i '/^\r$/d' META-INF/MANIFEST.MF
zip -u build/analysis/common/lucene-analyzers-common-%{version}.jar META-INF/MANIFEST.MF

%install
for module in core benchmark classification codecs demo expressions facet    \
grouping highlighter join memory misc queries queryparser replicator sandbox \
spatial   suggest test-framework; do
    %mvn_artifact "${module}/ivy.xml" "build/${module}/%{name}-${module}-%{version}.jar"
done

%mvn_file :core %{name}/%{name}-core %{name}

for analyzer in common icu kuromoji morfologik phonetic smartcn stempel uima; do
    %mvn_artifact "analysis/${analyzer}/ivy.xml" "build/analysis/${analyzer}/%{name}-analyzers-${analyzer}-%{version}.jar"
done

# suggest provides spellchecker
%mvn_alias :suggest :%{name}-spellchecker

# artifacts on maven central have name prepended to artifactId
%mvn_alias ':{*}' ':%{name}-@1'

# compatibility with existing packages
%mvn_alias ':analyzers-{*}' ':%{name}-@1'
%mvn_alias :analyzers-common :%{name}-analyzers

sed -i "/rawPom/{p;s//effectivePom/g}" .xmvn-reactor

%mvn_install -J build/docs

%files -f .mfiles
%doc CHANGES.txt LICENSE.txt README.txt NOTICE.txt MIGRATE.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt

%changelog
* Tue Mar 04 2014 Michael Simacek <msimacek@redhat.com> - 0:4.7.0-1
- Update to upstream version 4.7.0

* Mon Feb 10 2014 Michael Simacek <msimacek@redhat.com> - 0:4.6.1-1
- Update to upstream version 4.6.1
- Use XMvn to resolve ivy artifacts and for installation
- Remove contrib subpackage (was merged into main package)

* Wed Nov 06 2013 Severin Gehwolf <sgehwolf@redhat.com> 0:3.6.2-4
- Remove unneeded BR jline. Resolves RHBZ#1023015.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:3.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 1 2013 Krzysztof Daniel <kdaniel@redhat.com> 0:3.6.2-2
- 830762: lucene ships POMs with uninitialized version properties

* Tue Feb 26 2013 Severin Gehwolf <sgehwolf@redhat.com> 0:3.6.2-1
- Update to upstream release 3.6.2
- Fix build errors related to icu4j v50 incompatibility.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:3.6.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Dec 5 2012 Severin Gehwolf <sgehwolf@redhat.com> 0:3.6.0-11
- Remove patches which weren't applied (rpmlint warnings).

* Mon Dec 3 2012 Severin Gehwolf <sgehwolf@redhat.com> 0:3.6.0-10
- Upload new tarball for dev-tools as checksum could not be
  reproduced with given commands listed in comment.

* Tue Nov 27 2012 Severin Gehwolf <sgehwolf@redhat.com> 0:3.6.0-9
- Always install grand-parent pom as well.

* Tue Nov 27 2012 Severin Gehwolf <sgehwolf@redhat.com> 0:3.6.0-8
- Always install lucene-parent pom.

* Mon Nov 26 2012 Severin Gehwolf <sgehwolf@redhat.com> 0:3.6.0-7
- Only build lucene-contrib for Fedora.
- This removes BR on icu4j on rhel.

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
