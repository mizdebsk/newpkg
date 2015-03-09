%bcond_with bootstrap
%global artifact_name io.takari.incrementalbuild

Name:           takari-incrementalbuild
Version:        0.10.0
Release:        2%{?dist}
Summary:        Takari Incremental Build
License:        EPL
URL:            http://takari.io
BuildArch:      noarch

Source0:        https://github.com/takari/%{artifact_name}/archive/%{artifact_name}-%{version}.tar.gz

Patch0:         0001-Workaround-for-mtime-truncation.patch

BuildRequires:  maven-local
BuildRequires:  mvn(com.google.guava:guava)
BuildRequires:  mvn(javax.enterprise:cdi-api)
BuildRequires:  mvn(javax.inject:javax.inject)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven:maven-artifact)
BuildRequires:  mvn(org.apache.maven:maven-compat)
BuildRequires:  mvn(org.apache.maven:maven-core)
BuildRequires:  mvn(org.apache.maven:maven-model)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  mvn(org.eclipse.aether:aether-api)
BuildRequires:  mvn(org.eclipse.sisu:org.eclipse.sisu.plexus)
BuildRequires:  mvn(org.eclipse.sisu:sisu-maven-plugin)
BuildRequires:  mvn(org.slf4j:slf4j-api)
BuildRequires:  mvn(org.slf4j:slf4j-simple)
BuildRequires:  mvn(org.sonatype.plugins:sisu-maven-plugin)
BuildRequires:  mvn(org.sonatype.sisu:sisu-guice)


%if ! %{with bootstrap}
BuildRequires:  mvn(io.takari:takari:pom:)
%endif


%description
Incremental build support library for Apache Maven.

%package javadoc
Summary:        API documentation for %{name}

%description javadoc
This package provides %{summary}.


%prep
%setup -q -n %{artifact_name}-%{artifact_name}-%{version}

%patch0 -p1

# XXX skip ITs for now
%pom_disable_module incrementalbuild-its

# Component with different release cycle that upstream keeps disabled, but is needed
%pom_xpath_inject pom:modules '<module>incrementalbuild-workspace</module>'
%pom_set_parent io.takari:io.takari.incrementalbuild:%{version} incrementalbuild-workspace
%pom_change_dep :incrementalbuild-workspace ::%{version} incrementalbuild

%pom_remove_plugin -r :animal-sniffer-maven-plugin

%if %{with bootstrap}
%pom_remove_parent
%pom_xpath_set pom:project/pom:packaging jar incrementalbuild incrementalbuild-workspace
%pom_add_plugin :maven-compiler-plugin '
<configuration>
<source>1.7</source>
<target>1.7</target>
</configuration>'
%endif

# XXX optional
%pom_remove_dep -r :takari-plugin-testing
rm -rf incrementalbuild/src/main/java/io/takari/incrementalbuild/maven/testing

%build
%mvn_build -f

%install
%mvn_install


%files -f .mfiles

%files javadoc -f .mfiles-javadoc

%changelog
* Fri Mar 06 2015 Michael Simacek <msimacek@redhat.com> - 0.10.0-2
- Working build

* Fri Feb 20 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.10.0-1
- Initial packaging
