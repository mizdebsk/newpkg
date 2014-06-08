Name:           tesla-tycho-support
Version:        0.0.7
Release:        2%{?dist}
Summary:        Tesla Tycho Base
License:        EPL
URL:            https://github.com/tesla/tycho-support/
BuildArch:      noarch

Source0:        https://github.com/tesla/tycho-support/archive/tycho-support-%{version}.tar.gz
# Requested upstream to include license text:
# https://github.com/tesla/tycho-support/pull/1
Source1:        http://www.eclipse.org/legal/epl-v10.html

# Run feclipse-maven-plugin during build
Patch0:         %{name}-feclipse-maven-plugin.patch

BuildRequires:  maven-local
BuildRequires:  mvn(io.tesla:tesla:pom:)
BuildRequires:  mvn(org.eclipse.tycho:target-platform-configuration)
BuildRequires:  mvn(org.eclipse.tycho:tycho-maven-plugin)

# feclipse-maven-plugin is in a profile which is activated
# conditionally, so auto-requires are not generated for it.
Requires:       mvn(org.fedoraproject:feclipse-maven-plugin)

%description
Tesla is a next generation development infrastructure framework.  This
package provides Maven POM file which serves as the base of Tycho
projects which have plugins, tests, and deployable features.
Everything that is required is provided and parameterized by
specifying properties in the host POM.

%prep
%setup -q -n tycho-support-tycho-support-%{version}
cp -p %{SOURCE1} .
%patch0

# Remove plugins which are not useful in Fedora.
%pom_remove_plugin :maven-upload-plugin
%pom_remove_plugin :feature-zip-plugin

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc epl-v10.html

%changelog
* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jan 28 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.0.7-1
- Initial packaging
