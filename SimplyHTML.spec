Name:	SimplyHTML		
Version:	0.13.1
Release:	4%{?dist}
Summary:	Application and a java component for rich text processing

Group:		Development/Libraries
License:	GPLv2 and BSD
URL:		http://simplyhtml.sourceforge.net/
Source0:	http://downloads.sourceforge.net/simplyhtml/%{name}_src_0_13_1.tar.gz
Source1:	simplyhtml.sh
Patch0:	simplyhtml-build.xml-classpath.patch
Patch1:	simplythml-manifest-classpath.patch

BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

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
Group: Documentation
Requires: %{name} = %{version}-%{release}
Requires:	jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n simplyhtml-0_13_1
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
rm -rf %{buildroot}



mkdir -p %{buildroot}%{_javadir}/%{name}


cp -a dist/lib/SimplyHTML.jar %{buildroot}%{_javadir}/%{name}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}/%{name}.jar
ln -s %{name}.jar %{buildroot}%{_javadir}/%{name}/simplyhtml-%{version}.jar
ln -s simplyhtml-%{version}.jar %{buildroot}%{_javadir}/%{name}/simplyhtml.jar

cp -a dist/lib/SimplyHTMLHelp.jar %{buildroot}%{_javadir}/%{name}/%{name}-help-%{version}.jar
ln -s %{name}-help-%{version}.jar %{buildroot}%{_javadir}/%{name}/%{name}-help.jar
ln -s %{name}-help-%{version}.jar %{buildroot}%{_javadir}/%{name}/simplyhtmlhelp-%{version}.jar
ln -s simplyhtmlhelp-%{version}.jar %{buildroot}%{_javadir}/%{name}/SimplyHTMLHelp-%{version}.jar
ln -s simplyhtmlhelp-%{version}.jar %{buildroot}%{_javadir}/%{name}/simplyhtmlhelp.jar


install -pD -m755 -T %{SOURCE1} %{buildroot}%{_bindir}/%(basename %{SOURCE1})

mkdir -p %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -a dist/api/* %{buildroot}%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_javadir}/%{name}
%{_bindir}/simplyhtml*
%doc gpl.txt 

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}
%doc readme.txt





%changelog
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

