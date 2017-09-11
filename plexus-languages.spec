Name:           plexus-languages
Version:        0.9.3
Release:        1%{?dist}
Summary:        Plexus Languages
License:        ASL 2.0
URL:            https://github.com/codehaus-plexus/plexus-languages
BuildArch:      noarch

Source0:        https://github.com/codehaus-plexus/plexus-languages/archive/plexus-languages-%{version}.tar.gz
Source1:        http://www.apache.org/licenses/LICENSE-2.0.txt

BuildRequires:  maven-local
BuildRequires:  mvn(com.google.inject:guice)
BuildRequires:  mvn(com.thoughtworks.qdox:qdox)
BuildRequires:  mvn(javax.inject:javax.inject)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.codehaus.plexus:plexus-component-annotations)
BuildRequires:  mvn(org.codehaus.plexus:plexus-component-metadata)
BuildRequires:  mvn(org.codehaus.plexus:plexus:pom:)
BuildRequires:  mvn(org.mockito:mockito-core)
BuildRequires:  mvn(org.ow2.asm:asm)

%description
Plexus Languages is a set of Plexus components that maintain shared
language features.

%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
API documentation for %{name}.

%prep
%setup -q -n plexus-languages-plexus-languages-%{version}
cp %{SOURCE1} .

#%pom_remove_plugin :animal-sniffer-maven-plugin

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%license LICENSE-2.0.txt

%files javadoc -f .mfiles-javadoc
%license LICENSE-2.0.txt

%changelog
* Mon Sep 11 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.9.3-1
- Initial packaging
