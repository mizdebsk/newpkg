Name:           okio
Version:        1.0.1
Release:        1%{?dist}
Summary:        Java I/O library
License:        ASL 2.0
URL:            http://square.github.io/%{name}/
BuildArch:      noarch

Source0:        https://github.com/square/%{name}/archive/%{name}-parent-%{version}.tar.gz

BuildRequires:  maven-local

%description
Okio is a new library that complements java.io and java.nio to make it
much easier to access, store, and process data.

%package javadoc
Summary:        API documentation for %{name}

%description javadoc
this package provides %{summary}.

%prep
%setup -q -n %{name}-%{name}-parent-%{version}

# Remove dependency on Animal Sniffer (not usable in Fedora)
%pom_remove_plugin :animal-sniffer-maven-plugin
%pom_remove_dep :animal-sniffer-annotations okio
sed -i /IgnoreJRERequirement/d okio/src/main/java/okio/{DeflaterSink,Okio}.java

# Skip one test which fails on ARM due to poor JVM performance.
sed -i /writeWithTimeout/s/./@org.junit.Ignore/ okio/src/test/java/okio/SocketTimeoutTest.java

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%dir %{_javadir}/%{name}
%doc README.md LICENSE.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt

%changelog
* Fri Sep 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0.1-1
- Initial packaging
