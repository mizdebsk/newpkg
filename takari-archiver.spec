%bcond_without bootstrap

Name:           takari-archiver
Version:        0.1.8
Release:        1%{?dist}
Summary:        TBD
License:        EPL
URL:            http://takari.io
BuildArch:      noarch

Source0:        https://github.com/takari/%{name}/archive/%{name}-%{version}.tar.gz

BuildRequires:  maven-local
BuildRequires:  mvn(com.google.guava:guava)
BuildRequires:  mvn(javax.inject:javax.inject)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.commons:commons-compress)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)

%if ! %{with bootstrap}
BuildRequires:  mvn(io.takari:takari:pom:)
%endif


%description
TODO

%package javadoc
Summary:        API documentation for %{name}

%description javadoc
This package provides %{summary}.


%prep
%setup -q -n %{name}-%{name}-%{version}

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


# TODO license
%files -f .mfiles

%files javadoc -f .mfiles-javadoc


%changelog
* Fri Mar 06 2015 Michael Simacek <msimacek@redhat.com> - 0.1.8-1
- Initial packaging
