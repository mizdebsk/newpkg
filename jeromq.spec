Name:           jeromq
Version:        0.3.5
Release:        2%{?dist}
Summary:        Pure Java implementation of libzmq
# License is specified in pom.xml
License:        LGPLv3
URL:            https://github.com/zeromq/jeromq
BuildArch:      noarch

Source0:        https://github.com/zeromq/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  maven-local

%description
Pure Java implementation of libzmq.

%package        javadoc
Summary:        Javadoc for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q

%build
# Tests require network access and fail on Koji.
%mvn_build -f

%install
%mvn_install

%files -f .mfiles
%doc README.md CHANGELOG.md AUTHORS
%license COPYING.LESSER

%files javadoc -f .mfiles-javadoc
%license COPYING.LESSER

%changelog
* Mon Oct  5 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.3.5-2
- Skip running tests

* Wed Aug 26 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.3.5-1
- Initial packaging
