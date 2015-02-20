Name:           takari-incrementalbuild
Version:        0.10.0
Release:        1%{?dist}
Summary:        Takari Incremental Build
License:        EPL
URL:            https://github.com/takari/io.takari.incrementalbuild
BuildArch:      noarch

Source0:        https://github.com/takari/io.takari.incrementalbuild/archive/io.takari.incrementalbuild-%{version}.tar.gz

BuildRequires:  maven-local

BuildRequires:  mvn(io.takari:takari:pom:)

%description
TODO

%prep
%setup -q -n io.takari.incrementalbuild-io.takari.incrementalbuild-%{version}

# XXX skip ITs for now
%pom_disable_module incrementalbuild-its

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%license LICENSE.txt
%doc README.md

%changelog
* Fri Feb 20 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.10.0-1
- Initial packaging
