%bcond_without bootstrap

Name:           takari-archiver
Version:        0.1.8
Release:        2%{?dist}
Summary:        Takari Archiver
License:        EPL
URL:            http://takari.io
BuildArch:      noarch

# Clean tarball generated by running ./create-tarball.sh
Source0:        %{name}-%{version}-clean.tar.xz
Source1:        create-tarball.sh

# Replace use of bundled jgit class with jnr-posix.
Patch0:         takari-archiver-unbundle-jgit.patch

BuildRequires:  maven-local
BuildRequires:  mvn(com.github.jnr:jnr-posix)
BuildRequires:  mvn(com.google.guava:guava)
BuildRequires:  mvn(javax.inject:javax.inject)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.commons:commons-compress)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)

%if ! %{with bootstrap}
BuildRequires:  mvn(io.takari:takari:pom:)
%endif


%description
Takari Archiver is replacement for Maven Archiver for use with Takari
Lifecycle Plugin.

%package javadoc
Summary:        API documentation for %{name}

%description javadoc
This package provides %{summary}.


%prep
%setup -q
%patch0 -p1

%if %{with bootstrap}
%pom_remove_parent
%pom_xpath_set pom:project/pom:packaging jar
%pom_xpath_inject pom:project '<groupId>io.takari</groupId>'
%pom_add_plugin :maven-compiler-plugin '
<configuration>
<source>1.7</source>
<target>1.7</target>
</configuration>'
%endif

%build
%mvn_build -f

%install
%mvn_install


%files -f .mfiles
%license epl-v10.html

%files javadoc -f .mfiles-javadoc
%license epl-v10.html


%changelog
* Thu Mar 12 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.1.8-2
- Remove bundled JARs
- Unbundle part of jgit

* Fri Mar 06 2015 Michael Simacek <msimacek@redhat.com> - 0.1.8-1
- Initial packaging
