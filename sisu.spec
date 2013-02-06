%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^osgi\\(org\\.sonatype\\.sisu\\.guava\\)$

Name:           sisu
Version:        2.3.0
Release:        6%{?dist}
Summary:        Sonatype dependency injection framework
Group:          Development/Libraries
License:        ASL 2.0 and EPL and MIT
URL:            http://github.com/sonatype/sisu

# git clone git://github.com/sonatype/%{name}
# git archive --prefix=%{name}-%{version}/ --format=tar %{name}-%{version} | xz >%{name}-%{version}.tar.xz
Source0:        %{name}-%{version}.tar.xz

BuildArch:      noarch

BuildRequires:  java-devel
BuildRequires:  jpackage-utils
BuildRequires:  maven-local >= 0.11.1

BuildRequires:  animal-sniffer
BuildRequires:  aopalliance
BuildRequires:  atinject
BuildRequires:  cdi-api
BuildRequires:  felix-framework
BuildRequires:  geronimo-specs
BuildRequires:  google-guice
BuildRequires:  junit
BuildRequires:  plexus-classworlds
BuildRequires:  plexus-containers-component-annotations
BuildRequires:  plexus-utils
BuildRequires:  geronimo-parent-poms
BuildRequires:  sisu
BuildRequires:  testng
BuildRequires:  weld-parent

Requires:       %{name}-bean              = %{version}-%{release}
Requires:       %{name}-bean-binders      = %{version}-%{release}
Requires:       %{name}-bean-containers   = %{version}-%{release}
Requires:       %{name}-bean-converters   = %{version}-%{release}
Requires:       %{name}-bean-inject       = %{version}-%{release}
Requires:       %{name}-bean-locators     = %{version}-%{release}
Requires:       %{name}-bean-reflect      = %{version}-%{release}
Requires:       %{name}-bean-scanners     = %{version}-%{release}
Requires:       %{name}-containers        = %{version}-%{release}
Requires:       %{name}-inject            = %{version}-%{release}
Requires:       %{name}-inject-bean       = %{version}-%{release}
Requires:       %{name}-inject-plexus     = %{version}-%{release}
Requires:       %{name}-osgi-registry     = %{version}-%{release}
Requires:       %{name}-parent            = %{version}-%{release}
Requires:       %{name}-plexus            = %{version}-%{release}
Requires:       %{name}-plexus-binders    = %{version}-%{release}
Requires:       %{name}-plexus-converters = %{version}-%{release}
Requires:       %{name}-plexus-lifecycles = %{version}-%{release}
Requires:       %{name}-plexus-locators   = %{version}-%{release}
Requires:       %{name}-plexus-metadata   = %{version}-%{release}
Requires:       %{name}-plexus-scanners   = %{version}-%{release}
Requires:       %{name}-plexus-shim       = %{version}-%{release}
Requires:       %{name}-registries        = %{version}-%{release}
Requires:       %{name}-spi-registry      = %{version}-%{release}

%description
Java dependency injection framework with backward support for plexus and bean
style dependency injection.

%package        parent
Summary:        Sisu parent POM

%description    parent
This package contains %{summary}.

%package        containers
Summary:        Sisu containers POM

%description    containers
This package contains %{summary}.

%package        bean
Summary:        Sisu bean POM

%description    bean
This package contains %{summary}.

%package        plexus
Summary:        Sisu Plexus POM

%description    plexus
This package contains %{summary}.

%package        registries
Summary:        Sisu registries POM

%description    registries
This package contains %{summary}.

%package        inject
Summary:        Sisu inject POM

%description    inject
This package contains %{summary}.

%package        bean-binders
Summary:        Guice Bean Binders module for Sisu

%description    bean-binders
This package contains %{summary}.

%package        bean-containers
Summary:        Guice Bean Containers module for Sisu

%description    bean-containers
This package contains %{summary}.

%package        bean-converters
Summary:        Guice Bean Converters module for Sisu

%description    bean-converters
This package contains %{summary}.

%package        bean-inject
Summary:        Guice Bean Inject module for Sisu

%description    bean-inject
This package contains %{summary}.

%package        bean-locators
Summary:        Guice Bean Locators module for Sisu

%description    bean-locators
This package contains %{summary}.

%package        bean-reflect
Summary:        Guice Bean Reflect module for Sisu

%description    bean-reflect
This package contains %{summary}.

%package        bean-scanners
Summary:        Guice Bean Scanners module for Sisu

%description    bean-scanners
This package contains %{summary}.

%package        plexus-binders
Summary:        Guice Plexus Binders module for Sisu

%description    plexus-binders
This package contains %{summary}.

%package        plexus-converters
Summary:        Guice Plexus Converters module for Sisu

%description    plexus-converters
This package contains %{summary}.

%package        plexus-lifecycles
Summary:        Guice Plexus Lifecycles module for Sisu

%description    plexus-lifecycles
This package contains %{summary}.

%package        plexus-locators
Summary:        Guice Plexus Locators module for Sisu

%description    plexus-locators
This package contains %{summary}.

%package        plexus-metadata
Summary:        Guice Plexus Metadata module for Sisu

%description    plexus-metadata
This package contains %{summary}.

%package        plexus-scanners
Summary:        Guice Plexus Scanners module for Sisu

%description    plexus-scanners
This package contains %{summary}.

%package        plexus-shim
Summary:        Guice Plexus Shim module for Sisu

%description    plexus-shim
This package contains %{summary}.

%package        inject-bean
Summary:        Bean Inject bundle for Sisu

%description    inject-bean
This package contains %{summary}.

%package        inject-plexus
Summary:        Plexus Inject bundle for Sisu

%description    inject-plexus
This package contains %{summary}.

%package        osgi-registry
Summary:        OSGi registry for Sisu

%description    osgi-registry
This package contains %{summary}.

%package        spi-registry
Summary:        SPI registry for Sisu

%description    spi-registry
This package contains %{summary}.

%package        javadoc
Summary:        API documentation for Sisu
Group:          Documentation

%description    javadoc
This package contains %{summary}.

%prep
%setup -q

# Remove bundled objectweb-asm library
rm -rf ./sisu-inject/containers/guice-bean/guice-bean-scanners/src/main/java/org/sonatype/guice/bean/scanners/asm
%pom_add_dep asm:asm

# Fix namespace of imported asm classes
sed -i 's/org.sonatype.guice.bean.scanners.asm/org.objectweb.asm/g' \
    sisu-inject/containers/guice-plexus/guice-plexus-scanners/src/{main,test}/java/org/sonatype/guice/plexus/scanners/*.java \
    sisu-inject/containers/guice-bean/guice-bean-scanners/src/{main,test}/java/org/sonatype/guice/bean/scanners/*.java \

# Fix plexus bundling
sed -i -e '/provide these APIs as a convenience/,+2d' \
    sisu-inject/containers/guice-bean/sisu-inject-bean/pom.xml
%pom_add_dep javax.inject:javax.inject sisu-inject/containers/guice-plexus/sisu-inject-plexus

# add backward compatible location
cp sisu-inject/containers/guice-plexus/guice-plexus-lifecycles/src/main/java/org/sonatype/guice/plexus/lifecycles/*java \
   sisu-inject/containers/guice-plexus/guice-plexus-lifecycles/src/main/java/org/codehaus/plexus/
sed -i 's/org.sonatype.guice.plexus.lifecycles/org.codehaus.plexus/' \
       sisu-inject/containers/guice-plexus/guice-plexus-lifecycles/src/main/java/org/codehaus/plexus/*java

# Dependency not available
%pom_disable_module sisu-eclipse-registry sisu-inject/registries

%pom_remove_plugin :maven-surefire-plugin sisu-inject/containers/guice-bean/guice-bean-containers
%pom_remove_plugin :maven-clean-plugin sisu-inject/containers/guice-plexus/guice-plexus-binders
%pom_remove_plugin :maven-dependency-plugin sisu-inject/containers/guice-plexus/guice-plexus-binders

%build
%mvn_package ":{sisu,guice}-{*}" @2
%mvn_build -s -f

%install
%mvn_install

%files
%doc LICENSE-ASL.txt LICENSE-EPL.txt
%dir %{_javadir}/%{name}

%files parent            -f .mfiles-parent
%files containers        -f .mfiles-containers
%files bean              -f .mfiles-bean
%files plexus            -f .mfiles-plexus
%files registries        -f .mfiles-registries
%files inject            -f .mfiles-inject
%files bean-binders      -f .mfiles-bean-binders
%files bean-containers   -f .mfiles-bean-containers
%files bean-converters   -f .mfiles-bean-converters
%files bean-inject       -f .mfiles-bean-inject
%files bean-locators     -f .mfiles-bean-locators
%files bean-reflect      -f .mfiles-bean-reflect
%files bean-scanners     -f .mfiles-bean-scanners
%files plexus-binders    -f .mfiles-plexus-binders
%files plexus-converters -f .mfiles-plexus-converters
%files plexus-lifecycles -f .mfiles-plexus-lifecycles
%files plexus-locators   -f .mfiles-plexus-locators
%files plexus-metadata   -f .mfiles-plexus-metadata
%files plexus-scanners   -f .mfiles-plexus-scanners
%files plexus-shim       -f .mfiles-plexus-shim
%files inject-bean       -f .mfiles-inject-bean
%files inject-plexus     -f .mfiles-inject-plexus
%files osgi-registry     -f .mfiles-osgi-registry
%files spi-registry      -f .mfiles-spi-registry

%files javadoc -f .mfiles-javadoc
%doc LICENSE-ASL.txt LICENSE-EPL.txt


%changelog
* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.3.0-6
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

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
