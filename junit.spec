%define	name		junit
%define	version		3.8.1
%define	release		3jpp_3fc
%define	section		free

Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		0
Summary:	Java regression test package
License:	IBM Public License
Url:		http://www.junit.org/
Group:		Development/Testing
#Vendor:		JPackage Project
#Distribution:	JPackage
Source:		http://osdn.dl.sourceforge.net/junit/junit3.8.1.zip
BuildRequires:	ant
BuildRequires:	jpackage-utils >= 0:1.5
Buildarch:	noarch
Buildroot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
JUnit is a regression testing framework written by Erich Gamma and Kent
Beck. It is used by the developer who implements unit tests in Java.
JUnit is Open Source Software, released under the IBM Public License and
hosted on SourceForge.

%package manual
Group:		Development/Testing
Summary:	Manual for %{name}

%description manual
Documentation for %{name}.

%package javadoc
Group:		Development/Documentation
Summary:	Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%package demo
Group:		Development/Testing
Summary:	Demos for %{name}
Requires:	%{name} = %{version}-%{release}

%description demo
Demonstrations and samples for %{name}.

%prep
rm -rf $RPM_BUILD_ROOT
%setup -n %{name}%{version}
# extract sources
jar xvf src.jar
# delete stuff that doesn't work with libgcj (#130006).
if java -version 2>&1 | grep -q "gcj"; then
    rm -f junit/swingui/AboutDialog.java
    rm -f junit/swingui/CounterPanel.java
    rm -f junit/swingui/FailureRunView.java
    rm -f junit/swingui/TestHierarchyRunView.java
    rm -f junit/swingui/TestRunner.java
    rm -f junit/swingui/TestSelector.java
    rm -f junit/swingui/TestSuitePanel.java
fi

%build
ant dist

%install
# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 %{name}%{version}/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} ${jar/-%{version}/}; done)
# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr %{name}%{version}/javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
# demo
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -pr %{name}%{version}/%{name}/* $RPM_BUILD_ROOT%{_datadir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
rm -f %{_javadir}/%{name}.jar

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ "$1" = "0" ]; then
    rm -f %{_javadocdir}/%{name}
fi

%files
%defattr(0644,root,root,0755)
%doc README.html
%{_javadir}/*
%dir %{_datadir}/%{name}

%files manual
%defattr(0644,root,root,0755)
%doc %{name}%{version}/doc/*

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}

%files demo
%defattr(0644,root,root,0755)
%{_datadir}/%{name}/*

%changelog
* Mon Nov  1 2004 Gary Benson <gbenson@redhat.com> 0:3.8.1-3jpp_3fc
- Build into Fedora.

* Fri Mar 26 2004 Frank Ch. Eigler <fche@redhat.com> 0:3.8.1-3jpp_2rh
- add RHUG upgrade cleanup

* Thu Mar  4 2004 Frank Ch. Eigler <fche@redhat.com> 0:3.8.1-3jpp_1rh
- RH vacuuming

* Fri May 09 2003 David Walluck <david@anti-microsoft.org> 0:3.8.1-3jpp
- update for JPackage 1.5

* Fri Mar 21 2003 Nicolas Mailhot <Nicolas.Mailhot (at) JPackage.org> 3.8.1-2jpp
- For jpackage-utils 1.5

* Fri Sep 06 2002 Henri Gomez <hgomez@users.sourceforge.net> 3.8.1-1jpp
- 3.8.1

* Sun Sep 01 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 3.8-2jpp 
- used original zip file

* Thu Aug 29 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 3.8-1jpp 
- 3.8
- group, vendor and distribution tags

* Sat Jan 19 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 3.7-6jpp
- versioned dir for javadoc
- no dependencies for manual and javadoc packages
- stricter dependency for demo package
- additional sources in individual archives
- section macro

* Sat Dec 1 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 3.7-5jpp
- javadoc in javadoc package

* Wed Nov 21 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 3.7-4jpp
- fixed previous releases ...grrr

* Wed Nov 21 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 3.7-3jpp
- added jpp extension
- removed packager tag

* Sun Sep 30 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 3.7-2jpp
- first unified release
- s/jPackage/JPackage

* Mon Sep 17 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 3.7-1mdk
- 3.7
- vendor tag
- packager tag
- s/Copyright/License/
- truncated description to 72 columns in spec
- spec cleanup
- used versioned jar
- moved demo files to %{_datadir}/%{name}

* Sat Feb 17 2001 Guillaume Rousse <g.rousse@linux-mandrake.com> 3.5-1mdk
- first Mandrake release
