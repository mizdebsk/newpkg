Name:           mnemonicsetter
Version:        0.3
Release:        1%{?dist}
Summary:        Menu and toolbar mnemonic library
License:        ASL 2.0
URL:            https://github.com/dpolivaev/%{name}
BuildArch:      noarch

Source0:        https://github.com/dpolivaev/%{name}/archive/%{name}_%{version}.tar.gz

# Remove Gradle bintray plugin (not available in Fedora)
Patch0:         %{name}-remove-bintray-plugin.patch

BuildRequires:  gradle-local
BuildRequires:  mvn(org.mockito:mockito-all)

%description
Java library, which automatically assigns mnemonics to menu items and
toolbar elements.

%prep
%setup -q -n %{name}-%{name}_%{version}
%patch0
echo 'rootProject.name="%{name}"' >settings.gradle

%build
%gradle_build

%install
%mvn_install

%files -f .mfiles
%doc README.md
%license LICENSE

%changelog
* Mon Apr 11 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.3-1
- Initial packaging
