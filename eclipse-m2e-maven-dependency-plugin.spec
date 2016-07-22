%global commit 38c09f1ee625369f5ebc7a57f5b2a63e9034f9a4
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           eclipse-m2e-maven-dependency-plugin
Version:        0.0.4
Release:        0.1.git%{shortcommit}%{?dist}
Summary:        M2E maven-dependency-plugin connector
License:        EPL
URL:            https://github.com/ianbrandt/m2e-maven-dependency-plugin
BuildArch:      noarch

Source0:        https://github.com/ianbrandt/m2e-maven-dependency-plugin/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz

BuildRequires:  maven-local
BuildRequires:  mvn(org.eclipse.tycho:target-platform-configuration)
BuildRequires:  mvn(org.eclipse.tycho:tycho-maven-plugin)
BuildRequires:  mvn(org.sonatype.forge:forge-parent:pom:)
BuildRequires:  osgi(org.eclipse.core.resources)
BuildRequires:  osgi(org.eclipse.core.runtime)
BuildRequires:  osgi(org.eclipse.m2e.jdt)
BuildRequires:  osgi(org.eclipse.m2e.core)
BuildRequires:  osgi(org.eclipse.m2e.maven.runtime)

Enhances:       eclipse-m2e-core

%description
This package provides maven-dependency-plugin connector for Eclipse M2E.

%prep
%setup -q -n m2e-maven-dependency-plugin-%{commit}

# Tests are skipped because of missing dependencies:
# osgi(org.eclipse.m2e.tests.common)
%pom_disable_module tests
%pom_disable_module site

%build
%mvn_build -j

%install
%mvn_install

%files -f .mfiles
%license feature/license.html

%changelog
* Fri Jul 22 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.0.4-0.1.git38c09f1
- Initial packaging
