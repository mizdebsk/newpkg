Name:           picocli
Version:        4.7.6
Release:        1%{?dist}
Summary:        A mighty tiny command line interface for Java
License:        Apache-2.0
URL:            https://picocli.info/
BuildArch:      noarch

Source0:        https://github.com/remkop/picocli/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  maven-local

%description
Picocli is a one-file framework for creating Java command line
applications with almost zero code. It supports a variety of command
line syntax styles including POSIX, GNU, MS-DOS and more. It generates
highly customizable usage help messages that use ANSI colors and
styles to contrast important elements and reduce the cognitive load on
the user.

Picocli-based applications can have command line TAB completion
showing available options, option parameters and subcommands, for any
level of nested subcommands. Picocli-based applications can be
ahead-of-time compiled to a GraalVM native image, with extremely fast
startup time and lower memory requirements, which can be distributed
as a single executable file.

Picocli generates beautiful documentation for your application (HTML,
PDF and Unix man pages).

%package javadoc
Summary:        API documentation for %{name}

%description javadoc
API documentation for %{name}.

%prep
%autosetup -p1 -C

%build
# Tests rely on system-rules junit extension
%mvn_build -f

%install
%mvn_install

%files -f .mfiles
%license LICENSE

%files javadoc -f .mfiles-javadoc

%changelog
* Thu Aug 08 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.7.6-1
- Initial packaging
