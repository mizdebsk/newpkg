Name:		logback
Version:	1.0.6
Release:	1%{?dist}
Summary:	A Java logging library

Group:		Development/Tools
License:	LGPLv2 or EPL
URL:		http://logback.qos.ch/
Source0:	http://logback.qos.ch/dist/%{name}-%{version}.tar.gz
Source1:        %{name}-%{version}-00-build.xml
Source2:        %{name}-%{version}-core-osgi.bnd
Source3:        %{name}-%{version}-classic-osgi.bnd
Source4:        %{name}-%{version}-access-osgi.bnd
# Use Janino 2.6 API
Patch0:		%{name}-%{version}-janino-2_6.patch

# Java dependencies
BuildRequires:	jpackage-utils
BuildRequires:	java-devel >= 1:1.6.0

# Required libraries
BuildRequires:	jms
BuildRequires:	janino
# require jansi 1.8
BuildRequires:	jansi
# Using the version of jetty in the pom.xml file
BuildRequires:	jetty >= 7.5.1
BuildRequires:	slf4j
BuildRequires:	servlet25
BuildRequires:	tomcat-lib
BuildRequires:	javamail
BuildRequires:	apache-commons-cli
BuildRequires:	antlr-tool

# Build tools -- build with ant for now because of circular dependencies
BuildRequires:	ant
BuildRequires:	aqute-bnd
BuildRequires:	groovy

BuildArch:	noarch

# Java runtime dependencies
Requires:	java >= 1:1.6.0
Requires:	jpackage-utils

# Java library dependencies
Requires:	jansi
Requires:	jms
Requires:	janino
Requires:	jetty >= 7.5.1
Requires:	slf4j
Requires:	tomcat-lib
Requires:	servlet25

%description
Logback is intended as a successor to the popular log4j project. At present
time, logback is divided into three modules, logback-core, logback-classic
and logback-access.

The logback-core module lays the groundwork for the other two modules. The
logback-classic module can be assimilated to a significantly improved
version of log4j. Moreover, logback-classic natively implements the SLF4J
API so that you can readily switch back and forth between logback and other
logging frameworks such as log4j or java.util.logging (JUL).

The logback-access module integrates with Servlet containers, such as
Tomcat and Jetty, to provide HTTP-access log functionality. Note that you
could easily build your own module on top of logback-core.

%package javadoc
Summary:	Javadoc for %{name}
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
API documentation for the Logback library

%package examples
Summary:	Sample code for %{name}
Group:		Documentation
Requires:	%{name} = %{version}

%description examples
Sample code for the Logback library

%prep
%setup -q
%{__cp} %{SOURCE1} ./build.xml
%patch0 -p0

find . -name "*.jar" -delete

# Clean up the documentation
sed -i 's/\r//' LICENSE.txt README.txt docs/*.* docs/*/*.* docs/*/*/*.*
sed -i 's#"apidocs#"%{_javadocdir}/%{name}#g' docs/*.html
rm -rf docs/apidocs docs/project-reports docs/testapidocs docs/project-reports.html
rm -f docs/manual/.htaccess docs/css/site.css # Zero-length file

cp -p %{SOURCE2} osgi-core.bnd
cp -p %{SOURCE3} osgi-classic.bnd
cp -p %{SOURCE4} osgi-access.bnd

sed -i 's#<artifactId>groovy-all</artifactId#<artifactId>groovy</artifactId#' $(find . -name "pom.xml")

%build
export CLASSPATH=`build-classpath antlr groovy janino javamail commons-compiler commons-cli tomcat6-servlet-api objectweb-asm jms slf4j jetty tomcat/catalina`
ant dist javadoc

%install
install -d -m 755 p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -r dist/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/%{name}
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}

install -pm 644 pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP.%{name}-%{name}-parent.pom
%add_maven_depmap JPP.%{name}-%{name}-parent.pom

for sub in logback-access logback-classic logback-core; do
	install -m 644 dist/$sub-%{version}.jar \
		$RPM_BUILD_ROOT%{_javadir}/%{name}/$sub.jar
	install -m 644 $sub/pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP.%{name}-$sub.pom
    %add_maven_depmap JPP.%{name}-$sub.pom %{name}/$sub.jar
done

install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/examples
cp -r logback-examples/pom.xml logback-examples/src $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/examples

%files
%doc LICENSE.txt README.txt docs/*
%{_javadir}/%{name}
%{_mavendepmapfragdir}/%{name}
%{_mavenpomdir}/*.pom

%files javadoc
%doc LICENSE.txt
%{_javadocdir}/%{name}

%files examples
%doc LICENSE.txt
%{_datadir}/%{name}-%{version}

%changelog
* Wed Jul 11 2012 gil cattaneo <puntogil@libero.it> - 1.0.6-1
- Update to 1.0.6

* Tue Mar 20 2012 Mary Ellen Foster <mefoster at gmail.com> - 1.0.1-1
- Update to 1.0.1
- Prepare for re-review

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.18-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec  7 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.9.18-5
- Make jars and javadoc versionless
- Fix pom filenames (#655813)
- Remove gcj bits
- Other packaging cleanups/fixes

* Wed Jan 13 2010 Mary Ellen Foster <mefoster at gmail.com> - 0.9.18-4
- Change (Build)Requirement from geronimo-specs to jms

* Wed Jan 13 2010 Mary Ellen Foster <mefoster at gmail.com> - 0.9.18-3
- Add some missing (Build)Requirements

* Tue Jan 12 2010 Mary Ellen Foster <mefoster at gmail.com> - 0.9.18-2
- Add maven2 BuildRequirements
- Remove requirement for specific slf4j version

* Mon Jan 11 2010 Mary Ellen Foster <mefoster at gmail.com> - 0.9.18-1
- Update to new upstream version -- many bugfixes, see
  http://qos.ch/pipermail/announce/2009/000068.html
- Include new license tag
- Add all referenced dependencies to the Requires list
- Specify which bits of tomcat are actually used, instead of requiring
  all of it
- Don't remove hsqldb from poms any more; Maven metadata has been added

* Wed Jan  6 2010 Mary Ellen Foster <mefoster at gmail.com> - 0.9.17-3
- Manually add the Maven metadata for geronimo-specs-jms

* Wed Dec  2 2009 Mary Ellen Foster <mefoster at gmail.com> - 0.9.17-2
- Use Maven build instead (with all that entails), and include POMs
- Add -examples subpackage
- Depend on javamail 1.4

* Wed Nov 18 2009 Mary Ellen Foster <mefoster at gmail.com> - 0.9.17-1
- Initial package (using build.xml from Debian)
