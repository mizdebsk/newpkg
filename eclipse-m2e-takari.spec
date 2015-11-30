%global commit 780a6e9a2cd3fbedc950ecad9e7d04fa423db2a1
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           eclipse-m2e-takari
Version:        0.1.0
Release:        0.1.git%{shortcommit}%{?dist}
Summary:        M2E Takari connector
License:        EPL
URL:            https://github.com/takari/io.takari.m2e.lifecycle
BuildArch:      noarch

Source0:        https://github.com/takari/io.takari.m2e.lifecycle/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz

BuildRequires:  maven-local
BuildRequires:  mvn(io.takari:incrementalbuild-workspace)
BuildRequires:  mvn(io.takari.tycho:tycho-support:pom:)
BuildRequires:  osgi(com.google.guava)
BuildRequires:  osgi(io.takari.incrementalbuild.workspace)
BuildRequires:  osgi(org.eclipse.core.filesystem)
BuildRequires:  osgi(org.eclipse.core.resources)
BuildRequires:  osgi(org.eclipse.core.runtime)
BuildRequires:  osgi(org.eclipse.m2e.core)
BuildRequires:  osgi(org.eclipse.m2e.jdt)
BuildRequires:  osgi(org.eclipse.m2e.maven.runtime)
BuildRequires:  osgi(org.eclipse.osgi)
BuildRequires:  osgi(slf4j.api)

Enhances:       eclipse-m2e-core

%description
This package provides Takari connector for Eclipse M2E.

%prep
%setup -q -n io.takari.m2e.lifecycle-%{commit}
find -name \*.jar -type f -delete

# Disable user tracking (oficially known as "usage statistics collection")
sed -i /io.takari.stats/d io.takari.m2e.lifecycle.feature/feature.xml

# Tests are skipped because of missing dependencies:
# osgi(org.eclipse.m2e.tests.common)
%pom_disable_module io.takari.m2e.lifecycle.test

# SLF4J in Fedora uses a different BSN
sed -i s/org.slf4j.api/slf4j.api/ $(find -name *.MF)

%build
%mvn_build -j

%install
%mvn_install

%files -f .mfiles
%license io.takari.m2e.lifecycle.feature/license.html

%changelog
* Mon Nov 30 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.1.0-0.1.git780a6e9
- Initial packaging
