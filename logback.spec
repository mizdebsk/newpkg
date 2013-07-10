Name:           logback
Version:        1.0.10
Release:        2%{?dist}
Summary:        A Java logging library
Group:          Development/Tools
License:        LGPLv2 or EPL
URL:            http://logback.qos.ch/
Source0:        http://logback.qos.ch/dist/%{name}-%{version}.tar.gz
# use antrun-plugin instead of gmaven
Patch0:         %{name}-1.0.10-antrunplugin.patch
# with pom macros break build
Patch1:         %{name}-1.0.10-remove-core-test-jar.patch

# Java dependencies
BuildRequires: java-devel >= 1:1.6.0

# Required libraries
BuildRequires: geronimo-jms
BuildRequires: fusesource-pom
# require groovy 2.0.7
BuildRequires: groovy
BuildRequires: janino
BuildRequires: jansi
BuildRequires: javamail
BuildRequires: jetty
BuildRequires: log4j
BuildRequires: slf4j
BuildRequires: tomcat-lib
BuildRequires: tomcat-servlet-3.0-api

# groovy-all embedded libraries
BuildRequires: antlr-tool
BuildRequires: apache-commons-cli
BuildRequires: objectweb-asm

# Build tools -- build with ant for now because of circular dependencies
# antrun plugin deps
BuildRequires: ant-junit
BuildRequires: felix-main
BuildRequires: junit

# depend on rhbz#914056 BuildRequires: gmaven
BuildRequires: maven-local
BuildRequires: maven-antrun-plugin
BuildRequires: maven-plugin-build-helper
BuildRequires: maven-plugin-bundle
BuildRequires: maven-source-plugin

BuildArch:     noarch

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
Summary:       Javadoc for %{name}

%description javadoc
API documentation for the Logback library

%package access
Summary:       Logback-access module for Servlet integration

%description access
The logback-access module integrates with Servlet containers, such as Tomcat
and Jetty, to provide HTTP-access log functionality. Note that you could
easily build your own module on top of logback-core. 

%package examples
Summary:       Logback Examples Module

%description examples
logback-examples module.

%prep
%setup -q

%patch0 -p0
%patch1 -p1

%pom_remove_plugin org.codehaus.mojo:findbugs-maven-plugin
%pom_remove_plugin org.codehaus.gmaven:gmaven-plugin %{name}-classic

# remove test deps
%pom_remove_dep org.easytesting:fest-assert
%pom_remove_dep hsqldb:hsqldb %{name}-access
%pom_remove_dep com.h2database:h2 %{name}-classic
%pom_remove_dep postgresql:postgresql %{name}-classic
%pom_remove_dep mysql:mysql-connector-java %{name}-classic
%pom_remove_dep org.slf4j:integration %{name}-classic
%pom_remove_dep com.icegreen:greenmail %{name}-classic
%pom_remove_dep org.subethamail:subethasmtp %{name}-classic
%pom_remove_dep org.mockito:mockito-core %{name}-core
%pom_remove_dep org.scala-lang:scala-library %{name}-core
%pom_remove_plugin org.scala-tools:maven-scala-plugin %{name}-core    

rm -r %{name}-*/src/test/java/*

find . -name "*.class" -delete
find . -name "*.cmd" -delete
find . -name "*.jar" -delete

# Clean up the documentation
sed -i 's/\r//' LICENSE.txt README.txt docs/*.* docs/*/*.* docs/*/*/*.*
sed -i 's#"apidocs#"%{_javadocdir}/%{name}#g' docs/*.html
rm -rf docs/apidocs docs/project-reports docs/testapidocs docs/project-reports.html
rm -f docs/manual/.htaccess docs/css/site.css # Zero-length file

sed -i 's#<artifactId>groovy-all</artifactId#<artifactId>groovy</artifactId#' $(find . -name "pom.xml")

sed -i 's#<groupId>javax.servlet#<groupId>org.apache.tomcat#' $(find . -name "pom.xml")
sed -i 's#<artifactId>servlet-api#<artifactId>tomcat-servlet-api#' $(find . -name "pom.xml")

# disable for now
#om_disable_module logback-site
sed -i 's#<module>logback-site</module>#<!--module>logback-site</module-->#' pom.xml

%build

%mvn_package ":%{name}-access" access
%mvn_package ":%{name}-examples" examples
# unavailable test dep maven-scala-plugin
# slf4jJAR and org.apache.felix.main are required by logback-examples modules for maven-antrun-plugin
%mvn_build -f -- \
  -Dslf4jJAR=$(build-classpath slf4j/api) \
  -Dorg.apache.felix:org.apache.felix.main:jar=$(build-classpath felix/org.apache.felix.main)

%install
%mvn_install

install -d -m 755 %{buildroot}%{_datadir}/%{name}-%{version}/examples
cp -r %{name}-examples/pom.xml %{name}-examples/src %{buildroot}%{_datadir}/%{name}-%{version}/examples

%files -f .mfiles
%doc LICENSE.txt README.txt docs/*
%dir %{_javadir}/%{name}

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt

%files access -f .mfiles-access
%doc LICENSE.txt

%files examples -f .mfiles-examples
%doc LICENSE.txt
%{_datadir}/%{name}-%{version}

%changelog
* Wed Jul 10 2013 gil cattaneo <puntogil@libero.it> - 1.0.10-2
- switch to XMvn
- minor changes to adapt to current guideline

* Tue Mar 19 2013 gil cattaneo <puntogil@libero.it> - 1.0.10-1
- Update to 1.0.10

* Thu Mar 14 2013 gil cattaneo <puntogil@libero.it> - 1.0.9-4
- Use Maven build
- Removed un{used,available} plugin

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Dec 21 2012 Mary Ellen Foster <mefoster@gmail.com> - 1.0.9-2
- Remove F16 backward compatibility since it's EOL soon

* Sat Dec 08 2012 gil cattaneo <puntogil@libero.it> - 1.0.9-1
- Update to 1.0.9
- Preserved timestamp in pom files
- Applied changes to build against older jetty on F16, thanks to Mary Ellen F.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jul 13 2012 Orion Poplawski <orion@nwra.com> - 1.0.6-2
- Split off access module into sub-package (bug 663198)
- Change BR/R from servlet25 to tomcat-servlet-3.0-api (bug 819552)
- Update build.xml to include jetty jars, drop setting CLASSPATH

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
