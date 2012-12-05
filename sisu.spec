%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^osgi\\(org\\.sonatype\\.sisu\\.guava\\)$

Name:           sisu
Version:        2.3.0
Release:        3%{?dist}
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
BuildRequires:  xmvn

BuildRequires:  aopalliance
BuildRequires:  atinject
BuildRequires:  cdi-api
BuildRequires:  felix-framework
BuildRequires:  google-guice
BuildRequires:  junit
BuildRequires:  plexus-classworlds
BuildRequires:  plexus-containers-component-annotations
BuildRequires:  plexus-utils
BuildRequires:  sisu
BuildRequires:  testng
BuildRequires:  weld-parent

Requires:       java
Requires:       jpackage-utils
Requires:       aopalliance
Requires:       atinject
Requires:       cdi-api
Requires:       felix-framework
Requires:       google-guice
Requires:       junit
Requires:       plexus-classworlds
Requires:       plexus-containers-component-annotations
Requires:       plexus-utils
Requires:       sisu
Requires:       testng

%description
Java dependency injection framework with backward support for plexus and bean
style dependency injection.

%package        javadoc
Summary:        API documentation for %{name}
Group:          Documentation
Requires:       jpackage-utils

%description    javadoc
%{summary}.

%prep
%setup -q

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
%mvn_build -f

%install
%mvn_install

%files -f .mfiles
%doc LICENSE-ASL.txt LICENSE-EPL.txt
%dir %{_javadir}/%{name}

%files javadoc -f .mfiles-javadoc
%doc LICENSE-ASL.txt LICENSE-EPL.txt


%changelog
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


