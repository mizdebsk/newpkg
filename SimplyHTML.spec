Name:	SimplyHTML		
Version:	0.16.7
Release:	4%{?dist}
Summary:	Application and a java component for rich text processing

License:	GPLv2 and BSD
URL:		http://simplyhtml.sourceforge.net/
Source0:	http://downloads.sourceforge.net/simplyhtml/%{name}_src_0_16_07.tar.gz
Patch0:	simplyhtml-build.xml-classpath.patch
Patch1:	simplyhtml-manifest-classpath.patch

BuildRequires:	ant
BuildRequires:	gnu-regexp
BuildRequires:	java-devel
BuildRequires:	javahelp2
BuildRequires:	jpackage-utils

Requires:	gnu-regexp
Requires:	java
Requires:	javahelp2
Requires:	jpackage-utils

BuildArch: noarch

%description
SimplyHTML is an application for text processing. 
It stores documents as HTML files in combination with 
Cascading Style Sheets (CSS). SimplyHTML is not intended 
to be used as an editor for web pages. 
The application combines text processing features as known from 
popular word processors with a simple and generic way of 
storing textual information and styles.

%package javadoc
Summary: API documentation for %{name}
Requires:	jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n simplyhtml-0_16_07
%patch0 -p1
%patch1 -p1
find -name '*.class' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;

%build
export CLASSPATH=
CLASSPATH=
cd src
ant full-dist dist
cd ..

%install
mkdir -p %{buildroot}%{_javadir}/%{name}


cp -a dist/lib/SimplyHTML.jar %{buildroot}%{_javadir}/%{name}/%{name}.jar

cp -a dist/lib/SimplyHTMLHelp.jar %{buildroot}%{_javadir}/%{name}/%{name}-help.jar

%jpackage_script com.lightdev.app.shtm.App "" "" gnu-regexp:javahelp2:SimplyHTML simplyhtml true

mkdir -p %{buildroot}%{_javadocdir}/%{name}
cp -a dist/help/* %{buildroot}%{_javadocdir}/%{name}

# Workaround for RPM bug #646523 - can't change symlink to directory
# TODO: Remove this in F-23
%pretrans javadoc -p <lua>
dir = "%{_javadocdir}/%{name}"
dummy = posix.readlink(dir) and os.remove(dir)

%files
%{_javadir}/%{name}
%{_bindir}/simplyhtml*
%doc gpl.txt 

%files javadoc
%{_javadocdir}/%{name}
%doc readme.txt


%changelog
* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jan 07 2014 Michael Simacek <msimacek@redhat.com> - 0.16.7-3
- Adapt to current packaging guidelines (rhbz#1022163)

* Fri Aug 02 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 29 2013 Johannes Lips <hannes@fedoraproject.org> 0.16.7-1
- update to latest upstream version 

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jan 19 2013 Johannes Lips <hannes@fedoraproject.org> 0.16.5-1
- update to latest upstream version 

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Oct  02 2010 Johannes Lips <Johannes.Lips@googlemail.com> 0.13.1-4
- changed the classpath of the sh file
- included the license in the package
- added java-devel as a build requirement and java as normal requirement

* Fri Oct  01 2010 Johannes Lips <Johannes.Lips@googlemail.com> 0.13.1-3
- removed the classpath from the manifest
- added a build and normal requirement for jpackage-utils
- changed installation routine of the sh file
- changed the source url
- consistent usage of the macro %%{buildroot}
- made a seperate dir in %%{javadir} for all the jars

* Sat Sep  11 2010 Johannes Lips <Johannes.Lips@googlemail.com> 0.13.1-2
- added ant as a build requirement 

* Sat Sep  11 2010 Johannes Lips <Johannes.Lips@googlemail.com> 0.13.1-1
- initial build 

