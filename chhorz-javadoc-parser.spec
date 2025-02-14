Name:           chhorz-javadoc-parser
Version:        0.3.1
Release:        1%{?dist}
Summary:        Javadoc comment parser library
License:        Apache-2.0
URL:            https://github.com/chhorz/javadoc-parser
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://github.com/chhorz/javadoc-parser/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.maven.plugins:maven-source-plugin)
BuildRequires:  mvn(org.assertj:assertj-core)
BuildRequires:  mvn(org.junit.jupiter:junit-jupiter)

%description
This library provides a parsing mechanism for Javadoc comments within
java files.

%package javadoc
Summary:        API documentation for %{name}

%description javadoc
API documentation for %{name}.

%prep
%autosetup -p1 -C
%pom_disable_module javadoc-parser-documentation
%pom_remove_plugin :maven-javadoc-plugin
%pom_remove_plugin :nexus-staging-maven-plugin

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%license LICENSE.txt

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt

%changelog
* Fri Feb 14 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.3.1-1
- Initial packaging
