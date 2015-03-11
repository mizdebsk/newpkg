%global short_name m2e-workspace

Name:           eclipse-m2e-workspace
Version:        0.2.0
Release:        1%{?dist}
Summary:        M2E CLI workspace resolver
License:        EPL
URL:            https://www.eclipse.org/m2e/
BuildArch:      noarch

Source0:        http://git.eclipse.org/c/m2e/org.eclipse.m2e.workspace.git/snapshot/%{short_name}-%{version}.tar.bz2
Source1:        http://www.eclipse.org/legal/epl-v10.html

BuildRequires:  maven-local
BuildRequires:  mvn(javax.inject:javax.inject)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven:maven-core)
BuildRequires:  mvn(org.apache.maven.plugins:maven-source-plugin)
BuildRequires:  mvn(org.codehaus.plexus:plexus-component-annotations)
BuildRequires:  mvn(org.codehaus.plexus:plexus-component-metadata)
BuildRequires:  mvn(org.eclipse.aether:aether-api)
BuildRequires:  mvn(org.sonatype.plugins:sisu-maven-plugin)

%description
Workspace dependency resolver implementation for Maven command line
build.

%package javadoc
Summary:        API documentation for %{name}

%description javadoc
This package provides %{summary}.


%prep
%setup -q -n %{short_name}-%{version}

cp -a %{SOURCE1} .

# Remove support for Maven 3.0.x (requires Sonatype Aether, which is
# not available in Fedora)
%pom_remove_dep org.sonatype.aether
rm src/main/java/org/eclipse/m2e/workspace/internal/Maven30WorkspaceReader.java

%build
%mvn_build

%install
%mvn_install


%files -f .mfiles
%license epl-v10.html

%files javadoc -f .mfiles-javadoc
%license epl-v10.html


%changelog
* Fri Mar 06 2015 Michael Simacek <msimacek@redhat.com> - 0.2.0-1
- Initial packaging
