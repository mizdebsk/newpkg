Summary: Regression testing framework for Java
Name: junit
Version: 3.8.1
Release: 5
URL: http://www.junit.org/
Source: %{name}%{version}.zip
Source1: katana.omissions
Patch3: %{name}-classloader.patch
Patch4: %{name}-build.patch
License: IBM Common Public License
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildPrereq: katana-build
BuildPrereq: bootstrap-ant
Prereq: katana
Requires: libgcj >= 3.4.0
ExcludeArch: ppc64 ia64

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
%setup -q -n %{name}%{version}
jar xf src.jar && rm -Rf META-INF
%patch3 -p1 -b .classloader
%patch4 -p0 -b .build
katana prep

%build
bootstrap-ant

mv %{name}%{version}/%{name}.jar katana/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar \
    katana/lib-%{name}.so_%{name}-%{version}.jar
katana build

mv junit katana

%install
katana install

%post
%{_sbindir}/javaconfig \
    %{_libdir}/lib-junit.so \
    %{_datadir}/java/junit.jar

%postun
%{_sbindir}/javaconfig \
    %{_libdir}/lib-junit.so \
    %{_datadir}/java/junit.jar

%clean
katana clean

%files
%defattr(-,root,root)
%doc *.html doc javadoc
%{_libdir}/*.so
%{_datadir}/java/*.jar
%{_datadir}/katana/*.cp

%files devel
%defattr(-,root,root)
%{_includedir}/junit

%changelog
* Tue Jun  1 2004 Gary Benson <gbenson@redhat.com> 3.8.1-5
- Build with katana.
- Include the AWT runner and some more documentation.

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
