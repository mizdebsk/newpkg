# FIXME: split into subpackages (ant, eclipse, webkit, ...)
# FIXME: build and install javadocs
# FIXME: add runtime requires
# FIXME: correct directory layout
# FIXME: use distro-specific cflags

# TODO: licensing
# TODO: generate-tarball script
# TODO: enable optional features (webkit, media)

Name:           openjfx
Version:        8.0.91
Release:        1%{?dist}
Summary:        Rich client application platform for Java
# Licensing according to Debian (not verified)
# See: http://anonscm.debian.org/cgit/pkg-java/openjfx.git/tree/debian/copyright
License:        GPL v2 with exceptions and BSD and LGPL v2+ and (LGPL v2+ or BSD)
URL:            http://openjdk.java.net/projects/openjfx/

Source0:        http://hg.openjdk.java.net/openjfx/8u-dev/rt/archive/8u91-b14.tar.bz2

Patch0:         0001-Fix-wait-call-in-PosixPlatform.patch
Patch1:         0002-Bulid-in-Gradle-local-mode.patch

BuildRequires:  gradle-local
BuildRequires:  mvn(antlr:antlr)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.antlr:antlr:3.1.3)
BuildRequires:  mvn(org.antlr:stringtemplate)
BuildRequires:  mvn(org.apache.ant:ant)
BuildRequires:  mvn(org.eclipse.swt:swt)

BuildRequires:  pkgconfig(gtk+-2.0)
BuildRequires:  pkgconfig(gthread-2.0)
BuildRequires:  pkgconfig(xtst)
BuildRequires:  libjpeg-turbo-devel

BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  gperf

%description
JavaFX/OpenJFX is a set of graphics and media APIs that enables Java
developers to design, create, test, debug, and deploy rich client
applications that operate consistently across diverse platforms.

%prep
%setup -q -n rt-8u91-b14
%patch0 -p1
%patch1 -p1

%build
gradle-local -s --offline -P GRADLE_VERSION_CHECK=false

%install
install -d -m 755 %{buildroot}%{_jvmdir}
cp -a build/sdk %{buildroot}%{_jvmdir}/%{name}

%files
%{_jvmdir}/%{name}

%changelog
* Tue Apr 26 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 8.0.91-1
- Update to upstream version 8.0.91

* Tue Apr 26 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 8.0.60-1
- Update to upstream version 8.0.60

* Mon Jul  6 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 8.0.40-1
- Initial packaging
