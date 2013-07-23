%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^osgi\\(org\\.sonatype\\.sisu\\.guava\\)$

%global vertag M4

Name:           sisu
Epoch:          1
Version:        0.0.0
Release:        0.1.%{vertag}%{?dist}
Summary:        Sonatype dependency injection framework
Group:          Development/Libraries
# bundled asm is under BSD
License:        EPL and BSD
URL:            http://eclipse.org/sisu

# TODO: unbundle asm
# TODO: install EPL license file

Source0:        http://git.eclipse.org/c/%{name}/org.eclipse.%{name}.inject.git/snapshot/milestones/%{version}.M4.tar.bz2#/org.eclipse.%{name}.inject-%{version}.M4.tar.bz2
Source1:        http://git.eclipse.org/c/%{name}/org.eclipse.%{name}.plexus.git/snapshot/milestones/%{version}.M4.tar.bz2#/org.eclipse.%{name}.plexus-%{version}.M4.tar.bz2

BuildArch:      noarch

BuildRequires:  maven-local
BuildRequires:  mvn(ch.qos.logback:logback-classic)
BuildRequires:  mvn(com.google.inject.extensions:guice-assistedinject)
BuildRequires:  mvn(com.google.inject:guice)
BuildRequires:  mvn(javax.enterprise:cdi-api)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.felix:org.apache.felix.framework)
BuildRequires:  mvn(org.eclipse.tycho:tycho-maven-plugin)
BuildRequires:  mvn(org.osgi:org.osgi.core)
BuildRequires:  mvn(org.sonatype.oss:oss-parent)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)
BuildRequires:  mvn(org.jacoco:jacoco-maven-plugin)

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
BuildRequires:  osgi(org.testng)
BuildRequires:  osgi(slf4j.api)

%description
Java dependency injection framework with backward support for plexus and bean
style dependency injection.

%package        inject
Summary:        Sisu inject POM

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

# XXX: temporary hack
Provides:       mvn(org.sonatype.sisu:sisu-inject-plexus)

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

%mvn_file ":{*}" @1
%mvn_package ":*{inject,plexus}" @1
%mvn_package : __noinstall

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

sed -i '260s/<Object/<String/g' `find sisu-inject -name SisuActivator.java`

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
export TYCHO_MVN_RPMBUILD=1
export MAVEN_OPTS="-DskipTychoVersionCheck"
%mvn_build -f

%install
%mvn_install

# XXX: temporary hack
install -d -m 755 %{buildroot}%{_javadir}/%{name}
ln -sf %{_javadir}/org.eclipse.%{name}.inject.jar \
   %{buildroot}%{_javadir}/%{name}/sisu-inject-bean.jar
ln -sf %{_javadir}/org.eclipse.%{name}.plexus.jar \
   %{buildroot}%{_javadir}/%{name}/sisu-inject-plexus.jar


%files inject -f .mfiles-inject

%files plexus -f .mfiles-plexus
%{_javadir}/%{name}

%files javadoc -f .mfiles-javadoc


%changelog
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
