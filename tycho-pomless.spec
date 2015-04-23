%global commit 91b0b65808dd10d431a734f37494aefdb9d2f06e
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           tycho-pomless
Version:        0.0.1
Release:        0.1.git%{shortcommit}%{?dist}
Summary:        XXX
License:        EPL
URL:            https://github.com/jsievers/tycho-pomless
BuildArch:      noarch

Source0:        https://github.com/jsievers/tycho-pomless/archive/%{commit}/tycho-pomless-%{shortcommit}.tar.gz

BuildRequires:  maven-local
BuildRequires:  mvn(cglib:cglib)
BuildRequires:  mvn(io.takari.polyglot:polyglot-common)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.maven:maven-model)
BuildRequires:  mvn(org.apache.maven:maven-model-builder)
BuildRequires:  mvn(org.codehaus.plexus:plexus-component-metadata)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  mvn(org.eclipse.sisu:org.eclipse.sisu.inject.tests)
BuildRequires:  mvn(org.eclipse.sisu:org.eclipse.sisu.plexus)
BuildRequires:  mvn(org.eclipse.tycho:org.eclipse.osgi)

%description
XXX

%package javadoc
Summary:        API documentation for %{name}

%description javadoc
This package provides %{summary}.

%prep
%setup -q -n %{name}-%{commit}
%pom_add_dep cglib:cglib::test

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc README.md
# TODO license

%files javadoc -f .mfiles-javadoc
# TODO license

%changelog
* Thu Apr 23 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.0.1-0.1.git91b0b65
- Initial packaging
