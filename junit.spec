%define rhugversion 20031215
%define rhugsource1 %{name}%{version} upstream
%define rhugprep1 sh %{SOURCE2} %{name}%{version}
%define rhugpatches 2 3

Summary: Regression testing framework for Java
Name: junit
Version: 3.8.1
Release: 4
URL: http://www.junit.org/
Source: rhug-%{name}-%{rhugversion}.tar.bz2
Source1: %{name}%{version}.zip
Source2: build-srcdir.sh
Patch1: %{name}-rhjpp.patch
Patch2: %{name}-exitstatus.patch
Patch3: %{name}-classloader.patch
License: IBM Common Public License
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildPrereq: gcc34-c++
BuildPrereq: gcc34-java >= 3.4.0-1
Prereq: redhat-java-rpm-scripts >= 1.0.2-2
Requires: libgcj34 >= 3.4.0-1

%description
JUnit is a regression testing framework used to implement unit tests
in Java.

%package devel
Summary: CNI headers for developing JUnit applications
Group: Development/Libraries
Requires: junit = %{version}-%{release}

%description devel
The junit-devel package contains the headers required to develop
Cygnus Native Interface (CNI) extensions that use JUnit.

%prep
%setup -q -a 1
mv %{rhugsource1} && %{rhugprep1}
%patch1 -p0 -b .rhjpp
%patch2 -p1 -b .exitstatus
%patch3 -p1 -b .classloader
mv ChangeLog ChangeLog.rhug
mv TODO TODO.rhug

%build
CC=gcc34 CXX=g++34 GCJ=gcj34 GCJH=gcjh34 \
./configure \
    --disable-static \
    --prefix=%{_prefix} \
    --libdir=%{_libdir}
make
make check

%install
rm -rf ${RPM_BUILD_ROOT}
%makeinstall
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la
find ${RPM_BUILD_ROOT}%{_libdir} -type l | xargs rm -f

%post
%{_sbindir}/javaconfig \
    %{_libdir}/lib-junit.so \
    %{_datadir}/java/junit.jar

%postun
%{_sbindir}/javaconfig \
    %{_libdir}/lib-junit.so \
    %{_datadir}/java/junit.jar

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc *.rhug upstream/*.html
%{_libdir}/*.so
%{_datadir}/java/*.jar

%files devel
%defattr(-,root,root)
%{_includedir}/junit

%changelog
* Tue May  4 2004 Gary Benson <gbenson@redhat.com> 3.8.1-4
- Rebuild with new compiler.

* Thu Apr 15 2004 Gary Benson <gbenson@redhat.com> 3.8.1-3
- Rebuild with new compiler (#120844).

* Tue Mar  2 2004 Elliot Lee <sopwith@redhat.com>
- Rebuilt.

* Fri Feb 13 2004 Gary Benson <gbenson@redhat.com> 3.8.1-2
- Rebuild for Fedora.

* Mon Dec 15 2003 Gary Benson <gbenson@redhat.com>
- Apply hammer multilib fix to all multilib archs.
- Correctly link local libraries on hammer.

* Mon Dec  8 2003 Gary Benson <gbenson@redhat.com>
- Upgraded to fluorinated RHUG tarball.
- Picked up an accidentally omitted resource.

* Fri Sep 12 2003 Gary Benson <gbenson@redhat.com> 3.8.1-1
- Clarify the -devel subpackage's summary and description.
- Remove unnecessary -devel dependencies (#99077).
- Ensure we have a working javaconfig.

* Thu Jun  5 2003 Gary Benson <gbenson@redhat.com>
- Initial Red Hat Linux build.

* Tue Dec  3 2002 Gary Benson <gbenson@redhat.com>
- Initial RHUG build.
