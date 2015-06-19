Name:           sisu-mojos
Version:        0.3.1
Release:        2%{?dist}
Summary:        Sisu plugin for Apache Maven
License:        EPL
URL:            http://www.eclipse.org/sisu
BuildArch:      noarch

Source0:        http://git.eclipse.org/c/sisu/org.eclipse.sisu.mojos.git/snapshot/releases/%{version}.tar.bz2#/%{name}-%{version}.tar.bz2

BuildRequires:  maven-local
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:  mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildRequires:  mvn(org.apache.maven.shared:maven-common-artifact-filters)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  mvn(org.eclipse.sisu:org.eclipse.sisu.inject)
BuildRequires:  mvn(org.slf4j:slf4j-nop)
BuildRequires:  mvn(org.sonatype.oss:oss-parent:pom:)

Obsoletes:      sisu-maven-plugin < 1:0.1

%description
The Sisu Plugin for Maven provides mojos to generate
META-INF/sisu/javax.inject.Named index files for the Sisu container.

%package javadoc
Summary:        API documentation for %{name}

%description javadoc
This package contains %{summary}.

%prep
%setup -q -c
mv releases/%{version}/* .
# Animal Sniffer is not useful in Fedora
%pom_remove_plugin :animal-sniffer-maven-plugin
%mvn_alias : org.sonatype.plugins:

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%dir %{_javadir}/%{name}
%doc LICENSE.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt

%changelog
* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 18 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.3.1-1
- Update to upstream version 0.3.1

* Mon Mar 30 2015 Michael Simacek <msimacek@redhat.com> - 0.1.0-4
- Fix parent POM BR

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Nov 14 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.1.0-2
- Obsolete sisu-maven-plugin

* Wed Nov 13 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.1.0-1
- Update to upstream version 0.1.0

* Mon Sep 23 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.0.0-0.1.M5
- Initial packaging.
- Fix unowned directory
