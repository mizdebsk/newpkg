%bcond_with bootstrap

Name:           takari-lifecycle
Version:        1.10.2
Release:        2%{?dist}
Summary:        Optimized replacement for the Maven default lifecycle
License:        EPL
URL:            http://takari.io
BuildArch:      noarch

Source0:        https://github.com/takari/%{name}/archive/%{name}-%{version}.tar.gz

# ProblemFactory class is not exported by JDT
Patch0:         0001-Use-DefaultProblemFactory.patch

BuildRequires:  maven-local
BuildRequires:  mvn(com.github.spullara.mustache.java:compiler)
BuildRequires:  mvn(com.google.code.gson:gson)
BuildRequires:  mvn(com.google.guava:guava)
BuildRequires:  mvn(io.takari:incrementalbuild)
BuildRequires:  mvn(io.takari.m2e.workspace:org.eclipse.m2e.workspace.cli)
BuildRequires:  mvn(io.takari:takari-archiver)
BuildRequires:  mvn(javax.inject:javax.inject)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.commons:commons-exec)
BuildRequires:  mvn(org.apache.maven:maven-aether-provider)
BuildRequires:  mvn(org.apache.maven:maven-artifact)
BuildRequires:  mvn(org.apache.maven:maven-compat)
BuildRequires:  mvn(org.apache.maven:maven-core)
BuildRequires:  mvn(org.apache.maven:maven-model)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  mvn(org.apache.maven:maven-settings)
BuildRequires:  mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildRequires:  mvn(org.apache.maven.wagon:wagon-file)
BuildRequires:  mvn(org.codehaus.plexus:plexus-classworlds)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  mvn(org.eclipse.aether:aether-api)
BuildRequires:  mvn(org.eclipse.aether:aether-connector-basic)
BuildRequires:  mvn(org.eclipse.aether:aether-impl)
BuildRequires:  mvn(org.eclipse.aether:aether-spi)
BuildRequires:  mvn(org.eclipse.aether:aether-transport-wagon)
BuildRequires:  mvn(org.eclipse.aether:aether-util)
BuildRequires:  mvn(org.eclipse.sisu:org.eclipse.sisu.plexus)
BuildRequires:  mvn(org.eclipse.sisu:sisu-maven-plugin)
BuildRequires:  mvn(org.eclipse.tycho:org.eclipse.jdt.core)
BuildRequires:  mvn(org.eclipse.tycho:org.eclipse.osgi)
BuildRequires:  mvn(org.hamcrest:hamcrest-core)
BuildRequires:  mvn(org.ow2.asm:asm)
BuildRequires:  mvn(org.slf4j:slf4j-api)
BuildRequires:  mvn(org.slf4j:slf4j-simple)
BuildRequires:  mvn(org.sonatype.sisu:sisu-guice::no_aop:)
BuildRequires:  mvn(xmlunit:xmlunit)


%if ! %{with bootstrap}
BuildRequires:  mvn(io.takari:takari:pom:)
%endif


%description
Takari Maven Lifecycle includes an optimized replacement for the Maven
default lifecycle.  The Takari Lifecycle Plugin is a Maven plugin with
a small set of dependencies that provides equivalent functionality to
five plugins with a large set of transitive dependencies.  This
reduces the download times to retrieve the needed components as well
as the storage space requirements in your repositories.

%package javadoc
Summary:        API documentation for %{name}

%description javadoc
This package provides %{summary}.


%prep
%setup -q -n %{name}-%{name}-%{version}

%patch0 -p1

# XXX skip ITs for now
%pom_disable_module takari-lifecycle-plugin-its

%pom_remove_plugin -r :animal-sniffer-maven-plugin
%pom_remove_plugin -r :license-maven-plugin

%if %{with bootstrap}
%pom_remove_parent
%pom_xpath_set pom:project/pom:packaging maven-plugin takari-lifecycle-plugin
%pom_add_plugin :maven-compiler-plugin '
<configuration>
<source>1.7</source>
<target>1.7</target>
</configuration>'
%pom_add_plugin org.apache.maven.plugins:maven-plugin-plugin takari-lifecycle-plugin '
<executions>
<execution>
<id>mojo-descriptor</id>
<configuration>
<phase>process-classes</phase>
<packagingTypes>
<packaging>maven-plugin</packaging>
</packagingTypes>
</configuration>
<goals>
<goal>descriptor</goal>
</goals>
</execution>
</executions>
'
%endif

# eclipse should provide the alias
%pom_remove_dep -r :org.eclipse.jdt.compiler.apt

%build
%mvn_build -f -- -Dproject.build.sourceEncoding=UTF-8

%install
%mvn_install


%files -f .mfiles
%license LICENSE.txt
%doc README.md

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt


%changelog
* Fri Mar 06 2015 Michael Simacek <msimacek@redhat.com> - 1.10.2-2
- Working build

* Fri Feb 20 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10.2-1
- Initial packaging
