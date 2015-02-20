Name:           takari-pom
Version:        15
Release:        1%{?dist}
Summary:        Takari parent POM
License:        EPL
URL:            https://github.com/takari/takari-pom/
BuildArch:      noarch

Source0:        https://github.com/takari/takari-pom/archive/takari-%{version}.tar.gz
# Requested upstream to include license text:
# https://github.com/tesla/tesla-pom/pull/1
Source1:        http://www.eclipse.org/legal/epl-v10.html

BuildRequires:  maven-local

%description
Takari is a next generation development infrastructure framework.  This
package provides Takari POM file to by used by Apache Maven.

%prep
%setup -q -n takari-pom-takari-%{version}
cp -p %{SOURCE1} .
%mvn_alias : io.tesla:tesla

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc epl-v10.html

%changelog
* Fri Feb 20 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 15-1
- Initial packaging

