Name:           takari-lifecycle
Version:        1.10.2
Release:        1%{?dist}
Summary:        Takari Maven Lifecycle
License:        EPL
URL:            https://github.com/takari/%{name}
BuildArch:      noarch

Source0:        https://github.com/takari/%{name}/archive/%{name}-%{version}.tar.gz

BuildRequires:  maven-local

%description
Takari Maven Lifecycle includes an optimized replacement for the Maven
default lifecycle.  The Takari Lifecycle Plugin is a Maven plugin with
a small set of dependencies that provides equivalent functionality to
five plugins with a large set of transitive dependencies.  This
reduces the download times to retrieve the needed components as well
as the storage space requirements in your repositories.

%prep
%setup -q -n %{name}-%{name}-%{version}

# XXX skip ITs for now
%pom_disable_module takari-lifecycle-plugin-its

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%license LICENSE.txt
%doc README.md

%changelog
* Fri Feb 20 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10.2-1
- Initial packaging

