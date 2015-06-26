Name:           openid4java-team
Version:        1.0
Release:        1%{?dist}
Summary:        Team extension for openid4java
# License is specified in pom.xml
License:        MIT
URL:            https://github.com/cloudbees/%{name}-extension/
BuildArch:      noarch

Source0:        https://github.com/cloudbees/%{name}-extension/archive/%{name}-extension-%{version}.tar.gz
# Text copied from http://www.opensource.org/licenses/mit-license.php
Source1:        LICENSE.txt

BuildRequires:  maven-local
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.openid4java:openid4java-nodeps)

%description
This package provides team extension for openid4java.

%package        javadoc
Summary:        Javadoc for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n %{name}-extension-%{name}-extension-%{version}
cp %{SOURCE1} .

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%license LICENSE.txt

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt

%changelog
* Fri Jun 26 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-1
- Initial packaging
