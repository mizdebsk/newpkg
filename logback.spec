Name:           logback
Version:        1.0.10
Release:        1%{?dist}
Summary:        A Java logging library
Group:          Development/Tools
License:        LGPLv2 or EPL
URL:            http://logback.qos.ch/
Source0:        http://logback.qos.ch/dist/%{name}-%{version}.tar.gz
# use antrun-plugin instead of gmaven
Patch0:         %{name}-1.0.9-antrunplugin.patch
# remove core test-jar
Patch1:         %{name}-1.0.10-classic-pom.patch

# Java dependencies
BuildRequires: jpackage-utils
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
BuildRequires: maven-compiler-plugin
BuildRequires: maven-install-plugin
BuildRequires: maven-jar-plugin
BuildRequires: maven-javadoc-plugin
BuildRequires: maven-plugin-build-helper
BuildRequires: maven-plugin-bundle
BuildRequires: maven-resources-plugin
BuildRequires: maven-source-plugin
BuildRequires: maven-surefire-plugin

# Java runtime dependencies
Requires:      java >= 1:1.6.0
Requires:      jpackage-utils
# Java library dependencies
Requires:      geronimo-jms
Requires:      groovy
Requires:      janino
Requires:      jansi
Requires:      javamail

Requires:      slf4j
Requires:      tomcat-lib
Requires:      tomcat-servlet-3.0-api

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
Group:         Documentation
Requires:      jpackage-utils

%description javadoc
API documentation for the Logback library

%package access
Summary:       Logback-access module for Servlet integration
Group:         Development/Libraries
Requires:      %{name} = %{version}-%{release}
Requires:      janino
Requires:      javamail
Requires:      jetty
Requires:      tomcat-lib
Requires:      tomcat-servlet-3.0-api

%description access
The logback-access module integrates with Servlet containers, such as Tomcat
and Jetty, to provide HTTP-access log functionality. Note that you could
easily build your own module on top of logback-core. 

%package examples
Summary:       Logback Examples Module
Group:         Development/Libraries
Requires:      %{name} = %{version}-%{release}
Requires:      %{name}-access = %{version}-%{release}
Requires:      log4j
Requires:      slf4j
Requires:      tomcat-servlet-3.0-api

%description examples
logback-examples module.

%prep
%setup -q

%patch0 -p0
%patch1 -p0

%pom_remove_plugin org.codehaus.mojo:findbugs-maven-plugin
%pom_remove_plugin org.codehaus.gmaven:gmaven-plugin %{name}-classic

# remove test deps
%pom_remove_dep hsqldb:hsqldb %{name}-access
# type>test-jar
%pom_remove_dep ch.qos.logback:logback-core %{name}-access
%pom_add_dep ch.qos.logback:logback-core::compile %{name}-access
%pom_remove_dep com.h2database:h2 %{name}-classic
%pom_remove_dep postgresql:postgresql %{name}-classic
%pom_remove_dep mysql:mysql-connector-java %{name}-classic
%pom_remove_dep org.slf4j:integration %{name}-classic
%pom_remove_dep com.icegreen:greenmail %{name}-classic
%pom_remove_dep org.subethamail:subethasmtp %{name}-classic
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

# disable for now
#om_disable_module logback-site
sed -i 's#<module>logback-site</module>#<!--module>logback-site</module-->#' pom.xml

%build

# unavailable test dep maven-scala-plugin
# slf4jJAR and org.apache.felix.main are required by logback-examples modules for maven-antrun-plugin
mvn-rpmbuild -Dmaven.test.skip=true \
  -Dslf4jJAR=$(build-classpath slf4j/api) \
  -Dorg.apache.felix:org.apache.felix.main:jar=$(build-classpath felix/org.apache.felix.main) \
  package javadoc:aggregate

%install

install -d -m 755 %{buildroot}%{_mavenpomdir}

install -pm 644 pom.xml %{buildroot}/%{_mavenpomdir}/JPP.%{name}-%{name}-parent.pom
%add_maven_depmap JPP.%{name}-%{name}-parent.pom

install -d -m 755 %{buildroot}%{_javadir}/%{name}
# main
for sub in classic core; do
  install -m 644 %{name}-$sub/target/%{name}-$sub-%{version}.jar \
      %{buildroot}%{_javadir}/%{name}/%{name}-$sub.jar
  install -pm 644 %{name}-$sub/pom.xml %{buildroot}/%{_mavenpomdir}/JPP.%{name}-%{name}-$sub.pom
%add_maven_depmap JPP.%{name}-%{name}-$sub.pom %{name}/%{name}-$sub.jar
done

# optionals
for sub in access examples; do
  install -m 644 %{name}-$sub/target/%{name}-$sub-%{version}.jar \
    %{buildroot}%{_javadir}/%{name}/%{name}-$sub.jar
  install -pm 644 %{name}-$sub/pom.xml %{buildroot}/%{_mavenpomdir}/JPP.%{name}-%{name}-$sub.pom
%add_maven_depmap JPP.%{name}-%{name}-$sub.pom %{name}/%{name}-$sub.jar -f $sub
done

install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
# copy only apis docs
cp -r target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}

install -d -m 755 %{buildroot}%{_datadir}/%{name}-%{version}/examples
cp -r %{name}-examples/pom.xml %{name}-examples/src %{buildroot}%{_datadir}/%{name}-%{version}/examples

%files
%doc LICENSE.txt README.txt docs/*
%dir %{_javadir}/%{name}
%{_javadir}/%{name}/%{name}-classic.jar
%{_javadir}/%{name}/%{name}-core.jar
%{_mavenpomdir}/JPP.%{name}-%{name}-classic.pom
%{_mavenpomdir}/JPP.%{name}-%{name}-core.pom
%{_mavenpomdir}/JPP.%{name}-%{name}-parent.pom
%{_mavendepmapfragdir}/%{name}

%files javadoc
%doc LICENSE.txt
%{_javadocdir}/%{name}

%files access
%doc LICENSE.txt
%{_javadir}/%{name}/%{name}-access.jar
%{_mavenpomdir}/JPP.%{name}-%{name}-access.pom
%{_mavendepmapfragdir}/%{name}-access

%files examples
%doc LICENSE.txt
%{_datadir}/%{name}-%{version}
%{_javadir}/%{name}/%{name}-examples.jar
%{_mavendepmapfragdir}/%{name}-examples
%{_mavenpomdir}/JPP.%{name}-%{name}-examples.pom

%changelog
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
