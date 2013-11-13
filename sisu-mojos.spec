%global vertag M5

Name:           sisu-mojos
Version:        0.0.0
Release:        0.1.%{vertag}%{?dist}
Summary:        Sisu plugin for Apache Maven
License:        EPL
URL:            http://www.eclipse.org/sisu
BuildArch:      noarch

Source0:        http://git.eclipse.org/c/sisu/org.eclipse.sisu.mojos.git/snapshot/milestones/0.0.0.M5.tar.bz2#/%{name}-%{version}.%{vertag}.tar.bz2

BuildRequires:  maven-local
BuildRequires:  mvn(com.google.guava:guava)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  mvn(org.apache.maven.shared:maven-common-artifact-filters)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  mvn(org.eclipse.sisu:org.eclipse.sisu.inject)
BuildRequires:  mvn(org.slf4j:slf4j-api)
BuildRequires:  mvn(org.slf4j:slf4j-nop)
BuildRequires:  mvn(org.sonatype.oss:oss-parent)
BuildRequires:  mvn(org.sonatype.sisu:sisu-guice)

%description
The Sisu Plugin for Maven provides mojos to generate
META-INF/sisu/javax.inject.Named index files for the Sisu container.

%package javadoc
Summary:        API documentation for %{name}

%description javadoc
This package contains %{summary}.

%prep
%setup -q -c
mv milestones/%{version}.%{vertag}/* .
# Animal Sniffer is not useful in Fedora
%pom_remove_plugin :animal-sniffer-maven-plugin

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc LICENSE.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt

%changelog
* Mon Sep 23 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.0.0-0.1.M5
- Initial packaging.
