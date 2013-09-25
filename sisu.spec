%global vertag M5

Name:           sisu
Epoch:          1
Version:        0.0.0
Release:        0.5.%{vertag}%{?dist}
Summary:        Eclipse dependency injection framework
# bundled asm is under BSD
# See also: https://fedorahosted.org/fpc/ticket/346
License:        EPL and BSD
URL:            http://eclipse.org/sisu

# TODO: unbundle asm

Source0:        http://git.eclipse.org/c/%{name}/org.eclipse.%{name}.inject.git/snapshot/milestones/%{version}.%{vertag}.tar.bz2#/org.eclipse.%{name}.inject-%{version}.%{vertag}.tar.bz2
Source1:        http://git.eclipse.org/c/%{name}/org.eclipse.%{name}.plexus.git/snapshot/milestones/%{version}.%{vertag}.tar.bz2#/org.eclipse.%{name}.plexus-%{version}.%{vertag}.tar.bz2
Patch0:         0001-Fix-OSGi-compatibility.patch
# Incompatible version of Plexus Classworlds (upstreamable)
Patch1:         0002-Fix-compatibility-with-Plexus-Classworlds-2.5.patch

BuildArch:      noarch

BuildRequires:  maven-local
BuildRequires:  mvn(com.google.guava:guava)
BuildRequires:  mvn(com.google.inject:guice)
BuildRequires:  mvn(javax.enterprise:cdi-api)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)
BuildRequires:  mvn(org.codehaus.plexus:plexus-classworlds)
BuildRequires:  mvn(org.codehaus.plexus:plexus-component-annotations)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  mvn(org.eclipse.sisu:org.eclipse.sisu.inject)
BuildRequires:  mvn(org.eclipse.sisu:sisu-inject)
BuildRequires:  mvn(org.eclipse.sisu:sisu-plexus)
BuildRequires:  mvn(org.eclipse.tycho:target-platform-configuration)
BuildRequires:  mvn(org.eclipse.tycho:tycho-maven-plugin)
BuildRequires:  mvn(org.eclipse.tycho:tycho-source-plugin)
BuildRequires:  mvn(org.slf4j:slf4j-api)
BuildRequires:  mvn(org.sonatype.oss:oss-parent)
BuildRequires:  mvn(org.sonatype.sisu:sisu-guice::no_aop:)

BuildRequires:  osgi(aopalliance)
BuildRequires:  osgi(com.google.guava)
BuildRequires:  osgi(javax.el)
BuildRequires:  osgi(javax.enterprise.cdi-api)
BuildRequires:  osgi(javax.inject)
BuildRequires:  osgi(javax.servlet)
BuildRequires:  osgi(javax.xml.rpc)
BuildRequires:  osgi(org.apache.geronimo.specs.geronimo-annotation_1.1_spec)
BuildRequires:  osgi(org.apache.geronimo.specs.geronimo-ejb_3.1_spec)
BuildRequires:  osgi(org.codehaus.plexus.classworlds)
BuildRequires:  osgi(org.codehaus.plexus.component-annotations)
BuildRequires:  osgi(org.codehaus.plexus.utils)
BuildRequires:  osgi(org.eclipse.jdt.apt.core)
BuildRequires:  osgi(org.eclipse.osgi)
BuildRequires:  osgi(org.hamcrest.core)
BuildRequires:  osgi(org.junit)
BuildRequires:  osgi(org.sonatype.sisu.guice)
BuildRequires:  osgi(slf4j.api)


%description
Java dependency injection framework with backward support for plexus and bean
style dependency injection.

%package        inject
Summary:        Sisu inject POM
Requires:       mvn(javax.enterprise:cdi-api)
Requires:       mvn(com.google.inject:guice)

Obsoletes:      %{name}                   < %{epoch}:%{version}-%{release}
Obsoletes:      %{name}-bean              < %{epoch}:%{version}-%{release}
Obsoletes:      %{name}-bean-binders      < %{epoch}:%{version}-%{release}
Obsoletes:      %{name}-bean-containers   < %{epoch}:%{version}-%{release}
Obsoletes:      %{name}-bean-converters   < %{epoch}:%{version}-%{release}
Obsoletes:      %{name}-bean-inject       < %{epoch}:%{version}-%{release}
Obsoletes:      %{name}-bean-locators     < %{epoch}:%{version}-%{release}
Obsoletes:      %{name}-bean-reflect      < %{epoch}:%{version}-%{release}
Obsoletes:      %{name}-bean-scanners     < %{epoch}:%{version}-%{release}
Obsoletes:      %{name}-containers        < %{epoch}:%{version}-%{release}
Obsoletes:      %{name}-inject-bean       < %{epoch}:%{version}-%{release}
Obsoletes:      %{name}-inject-plexus     < %{epoch}:%{version}-%{release}
Obsoletes:      %{name}-osgi-registry     < %{epoch}:%{version}-%{release}
Obsoletes:      %{name}-parent            < %{epoch}:%{version}-%{release}
Obsoletes:      %{name}-plexus-binders    < %{epoch}:%{version}-%{release}
Obsoletes:      %{name}-plexus-converters < %{epoch}:%{version}-%{release}
Obsoletes:      %{name}-plexus-lifecycles < %{epoch}:%{version}-%{release}
Obsoletes:      %{name}-plexus-locators   < %{epoch}:%{version}-%{release}
Obsoletes:      %{name}-plexus-metadata   < %{epoch}:%{version}-%{release}
Obsoletes:      %{name}-plexus-scanners   < %{epoch}:%{version}-%{release}
Obsoletes:      %{name}-plexus-shim       < %{epoch}:%{version}-%{release}
Obsoletes:      %{name}-registries        < %{epoch}:%{version}-%{release}
Obsoletes:      %{name}-spi-registry      < %{epoch}:%{version}-%{release}

%description    inject
This package contains %{summary}.

%package        plexus
Summary:        Sisu Plexus POM
Requires:       mvn(javax.enterprise:cdi-api)
Requires:       mvn(com.google.guava:guava)
Requires:       mvn(org.sonatype.sisu:sisu-guice::no_aop:)
Requires:       mvn(org.eclipse.sisu:org.eclipse.sisu.inject)
Requires:       mvn(org.codehaus.plexus:plexus-component-annotations)
Requires:       mvn(org.codehaus.plexus:plexus-classworlds)
Requires:       mvn(org.codehaus.plexus:plexus-utils)

%description    plexus
This package contains %{summary}.

%package        javadoc
Summary:        API documentation for Sisu

%description    javadoc
This package contains %{summary}.

%prep
%setup -q -c -T
tar xf %{SOURCE0} && mv milestones/* sisu-inject && rmdir milestones
tar xf %{SOURCE1} && mv milestones/* sisu-plexus && rmdir milestones

%patch0 -p1
%patch1 -p1

%mvn_file ":{*}" @1
%mvn_package ":*{inject,plexus}" @1
%mvn_package : __noinstall

%pom_disable_module org.eclipse.sisu.inject.tests sisu-inject
%pom_disable_module org.eclipse.sisu.plexus.tests sisu-plexus

for target in \
    sisu-inject/org.eclipse.sisu.inject/build.target \
    sisu-plexus/org.eclipse.sisu.plexus/build.target
do
    sed -i '/<unit/s|version="[^"]*"||' $target
    sed -i '/<repository/s|location="[^"]*"|location="file:'"$PWD"'/.m2/p2/repo"|' $target
    sed -i '/<unit id="plexus-deps"/s|.*|<unit id="org.codehaus.plexus.classworlds"/><unit id="org.codehaus.plexus.component-annotations"/><unit id="org.codehaus.plexus.utils"/>|' $target
    sed -i '/<unit id="org.aopalliance"/s|.*|<unit id="aopalliance"/>|' $target
    sed -i '/<unit id="cdi.api"/s|.*|<unit id="javax.enterprise.cdi-api"/>|' $target
    sed -i '/<unit id="javax.annotation"/s|.*|<unit id="org.apache.geronimo.specs.geronimo-annotation_1.1_spec"/>|' $target
    sed -i '/<unit id="javax.ejb"/s|.*|<unit id="org.apache.geronimo.specs.geronimo-ejb_3.1_spec"/>|' $target
    sed -i '/<unit id="com.google.inject"/s|.*|<unit id="org.sonatype.sisu.guice"/>|' $target
    sed -i '/<unit id="org.slf4j.api"/s|.*|<unit id="slf4j.api"/>|' $target
done

for pom in \
    sisu-inject/org.eclipse.sisu.inject \
    sisu-inject/org.eclipse.sisu.inject.extender \
    sisu-plexus/org.eclipse.sisu.plexus
do
    %pom_remove_plugin :animal-sniffer-maven-plugin $pom
done

# missing dep org.eclipse.tycho.extras:tycho-sourceref-jgit
%pom_xpath_remove "pom:plugin[pom:artifactId[text()='tycho-packaging-plugin']]/pom:dependencies" sisu-inject
%pom_xpath_remove "pom:plugin[pom:artifactId[text()='tycho-packaging-plugin']]/pom:configuration/pom:sourceReferences" sisu-inject
%pom_xpath_remove "pom:plugin[pom:artifactId[text()='tycho-packaging-plugin']]/pom:dependencies" sisu-plexus
%pom_xpath_remove "pom:plugin[pom:artifactId[text()='tycho-packaging-plugin']]/pom:configuration/pom:sourceReferences" sisu-plexus


cat <<EOF >pom.xml
<project>
  <modelVersion>4.0.0</modelVersion>
  <groupId>org.fedoraproject.maven</groupId>
  <artifactId>aggregator-project</artifactId>
  <version>dummy</version>
  <packaging>pom</packaging>
  <modules>
    <module>sisu-inject</module>
    <module>sisu-plexus</module>
  </modules>
</project>
EOF

%build
# Tycho inject dependencies with system scope.  Disable installation
# of effective POMs until Mvn can handle system-scoped deps.
%mvn_build -f -i
for mod in inject plexus; do
    %mvn_artifact sisu-${mod}/pom.xml
    %mvn_artifact sisu-${mod}/org.eclipse.sisu.${mod}/pom.xml sisu-${mod}/org.eclipse.sisu.${mod}/target/org.eclipse.sisu.${mod}-%{version}.%{vertag}.jar

    # inject pom.properties file
    mkdir -p META-INF/maven/org.eclipse.sisu/org/eclipse/sisu/${mod}/
    cat > META-INF/maven/org.eclipse.sisu/org/eclipse/sisu/${mod}/pom.properties << EOF
version=%{version}
groupId=org.eclipse.sisu
artifactId=org.eclipse.sisu.${mod}
EOF
    zip -u sisu-${mod}/org.eclipse.sisu.${mod}/target/org.eclipse.sisu.${mod}-%{version}.%{vertag}.jar \
      META-INF/maven/org.eclipse.sisu/org/eclipse/sisu/${mod}/pom.properties
done

%install
%mvn_install


%files inject -f .mfiles-inject
%doc sisu-inject/LICENSE.txt

%files plexus -f .mfiles-plexus
%doc sisu-inject/LICENSE.txt

%files javadoc -f .mfiles-javadoc
%doc sisu-inject/LICENSE.txt


%changelog
* Wed Sep 25 2013 Michal Srb <msrb@redhat.com> - 1:0.0.0-0.5.M5
- Update to upstream version 0.0.0.M5
- Install EPL license file
- Inject pom.properties
- Regenerate BR
- Add R

* Fri Sep 20 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:0.0.0-0.4.M4
- Update to XMvn 1.0.0

* Tue Aug 13 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:0.0.0-0.3.M4
- Obsolete sisu main package, resolves: rhbz#996288

* Tue Jul 23 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:0.0.0-0.2.M4
- Remove unneeded provides and compat symlinks

* Mon Jul 22 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:0.0.0-0.1.M4
- Update to upstream version 0.0.0.M4

* Wed Mar 27 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.3.0-8
- Remove unneeded animal-sniffer BuildRequires
- Add forge-parent to BuildRequires to ensure it's present

* Thu Mar 14 2013 Michal Srb <msrb@redhat.com> - 2.3.0-7
- sisu-inject-bean: add dependency on asm
- Fix dependencies on javax.inject and javax.enterprise.inject
- Remove bundled JARs and .class files from tarball

* Thu Feb  7 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.0-6
- Add ASM dependency only to a single module, not all of them
- Disable animal-sniffer plugin
- Don't generate auto-requires for optional dependencies

* Wed Feb 06 2013 Tomas Radej <tradej@redhat.com> - 2.3.0-5
- Added BR on animal-sniffer

* Tue Feb 05 2013 Tomas Radej <tradej@redhat.com> - 2.3.0-4
- Split into subpackages
- Build with new macros
- Unbundled objectweb-asm

* Wed Dec  5 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.0-3
- Fix OSGi __requires_exclude

* Wed Dec  5 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.0-2
- Disable OSGi auto-requires: org.sonatype.sisu.guava

* Mon Dec  3 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.0-1
- Update to upstream version 2.3.0

* Tue Jul 24 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.3-6
- Convert patches to POM macros

* Mon Jul 23 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.3-5
- Fix license tag

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Aug 19 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.3-2
- Add backward compatible package path for lifecycles
- Remove temporary BRs/Rs

* Thu Jun 23 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.3-1
- Update to latest upstream 2.2.3 (#683795)
- Add forge-parent to Requires
- Rework spec to be more simple, update patches

* Tue Mar  1 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.1.1-2
- Add atinject into poms as dependency

* Mon Feb 28 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.1.1-1
- Update to 2.1.1
- Update patch
- Disable guice-eclipse for now

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.4.3.2-1
- Update to latest upstream version
- Versionless jars & javadocs

* Mon Oct 18 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.4.2-2
- Add felix-framework BR

* Thu Oct 14 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.4.2-1
- Initial version of the package
