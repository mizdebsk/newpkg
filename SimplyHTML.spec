Name:           SimplyHTML
Version:        0.16.15
Release:        1%{?dist}
Summary:        Application and a java component for rich text processing
License:        GPLv2 and BSD
URL:            http://simplyhtml.sourceforge.net/
BuildArch:      noarch

Source0:        http://heanet.dl.sourceforge.net/project/simplyhtml/stable/simplyhtml_src-%{version}.tar.gz

# Remove Gradle bintray plugin (not available in Fedora)
Patch0:         %{name}-remove-bintray-plugin.patch

BuildRequires:  gradle-local
BuildRequires:  mvn(gnu-regexp:gnu-regexp)
BuildRequires:  mvn(javax.help:javahelp)
BuildRequires:  mvn(org.dpolivaev.mnemonicsetter:mnemonicsetter)

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

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n simplyhtml-%{version}
%patch0
echo 'rootProject.name="%{name}"' >settings.gradle

%build
%gradle_build

%install
%mvn_install -J build/docs/javadoc

%files -f .mfiles
%doc readme.txt
%license gpl.txt 

%files javadoc -f .mfiles-javadoc

%changelog
* Mon Apr 11 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.16.15-1
- Update to upstream version 0.16.15

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Mar 25 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.16.7-5
- Remove workarunds for RPM bug #646523

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

