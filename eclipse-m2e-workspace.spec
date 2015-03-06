%global short_name m2e-workspace

Name:           eclipse-m2e-workspace
Version:        0.2.0
Release:        1%{?dist}
Summary:        TBD
License:        EPL
URL:            TBD
BuildArch:      noarch

Source0:        http://git.eclipse.org/c/m2e/org.eclipse.m2e.workspace.git/snapshot/%{short_name}-%{version}.tar.bz2

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
TBD

%package javadoc
Summary:        API documentation for %{name}

%description javadoc
This package provides %{summary}.


%prep
%setup -q -n %{short_name}-%{version}

%pom_remove_dep org.sonatype.aether
rm src/main/java/org/eclipse/m2e/workspace/internal/Maven30WorkspaceReader.java

%build
%mvn_build

%install
%mvn_install


# TODO license
%files -f .mfiles

%files javadoc -f .mfiles-javadoc


%changelog
* Fri Mar 06 2015 Michael Simacek <msimacek@redhat.com> - 0.2.0-1
- Initial packaging
