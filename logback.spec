
Name:		logback
Version:	0.9.18
Release:	6%{?dist}
Summary:	A Java logging library

Group:		Development/Tools
License:	LGPLv2 or EPL
URL:		http://logback.qos.ch/
Source0:	http://logback.qos.ch/dist/%{name}-%{version}.tar.gz
Source1:        %{name}-depmap.xml

# Add dummy implementations of two new methods from Jetty 6
Patch0:		%{name}-LifecycleListener.patch
# Modify the POMs to remove unavailable dependencies, and to avoid
# building the "site" and "examples" directories
Patch1:		%{name}-%{version}-clean-poms.patch

BuildRequires:	jms
BuildRequires:	janino
BuildRequires:	java-devel >= 1.6.0
BuildRequires:	javamail >= 1.4
BuildRequires:	jetty >= 6.1.20-7
BuildRequires:	jpackage-utils >= 0:1.5
BuildRequires:	slf4j
BuildRequires:	servlet25
BuildRequires:	tomcat6
BuildRequires:  easymock2
BuildRequires:	hsqldb >= 1:1.8.0.10-5

# Maven build requirements
BuildRequires:	maven2
BuildRequires:	maven-assembly-plugin
BuildRequires:	maven-plugin-bundle
BuildRequires:	maven-compiler-plugin
BuildRequires:	maven-idea-plugin
BuildRequires:	maven-install-plugin
BuildRequires:	maven-jar-plugin
BuildRequires:	maven-javadoc-plugin
BuildRequires:	maven-resources-plugin
BuildRequires:	maven-site-plugin
BuildRequires:	maven-source-plugin
BuildRequires:	maven-surefire-plugin
BuildRequires:  ant-junit
BuildRequires:  apache-commons-modeler

BuildArch:	noarch

# Dependencies from the pom files
Requires:	dom4j
Requires:       easymock2
Requires:       jms
Requires:	hsqldb >= 1:1.8.0.10-5
Requires:	janino
Requires:	javamail
Requires:	jetty
Requires:	slf4j
Requires:	tomcat6
Requires:	servlet25

Requires(post):	jpackage-utils
Requires(postun):	jpackage-utils


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
Requires:       jpackage-utils

%description javadoc
API documentation for the Logback library


%package examples
Summary:	Sample code for %{name}
Group:		Documentation

%description examples
Sample code for the Logback library

%prep
%setup -q
%patch0 -p1
%patch1 -p1

find . -name "*.jar" -delete

# Clean up the documentation
sed -i 's/\r//' LICENSE.txt README.txt docs/*.* docs/*/*.* docs/*/*/*.* docs/*/*/*/*.*
sed -i 's#"apidocs#"%{_javadocdir}/%{name}-%{version}#g' docs/*.html
rm -rf docs/apidocs docs/project-reports docs/testapidocs docs/project-reports.html
rm -f docs/manual/.htaccess docs/css/site.css # Zero-length file

%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL

# Temporary hack to add metadata for jms from geronimo-specs
# Based on mbooth's hack in the jakarta-commons-modeler spec
mkdir -p $MAVEN_REPO_LOCAL/org/apache/geronimo/specs/geronimo-jms_1.1_spec/1.0/
pushd $MAVEN_REPO_LOCAL/org/apache/geronimo/specs/geronimo-jms_1.1_spec/1.0
ln -s %{_javadir}/geronimo/spec-jms-1.1.jar geronimo-jms_1.1_spec-1.0.jar
cat <<HEREDOC > geronimo-jms_1.1_spec-1.0.pom
<project>
  <modelVersion>4.0.0</modelVersion>
  <groupId>org.apache.geronimo.specs</groupId>
  <artifactId>geronimo-jms_1.1_spec</artifactId>
  <version>1.0</version>
</project>
HEREDOC
popd
# TODO: remove the hack above when geronimo-specs has metadata

mvn-jpp \
	-Dmaven.repo.local=$MAVEN_REPO_LOCAL \
	-Dmaven.test.skip=true \
        -Dmaven2.jpp.depmap.file=%{SOURCE1} \
	install javadoc:aggregate

%install
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/%{name}
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}

install -d -m 755 p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -r target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

install -pm 644 pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP-%{name}-parent.pom
%add_to_maven_depmap ch.qos.logback %{name}-parent %{version} JPP %{name}-parent

for sub in logback-access logback-classic logback-core; do
	base=`echo $sub | sed 's/%{name}-//g'`
	install -m 644 $sub/target/$sub-%{version}.jar \
		$RPM_BUILD_ROOT%{_javadir}/%{name}/$base.jar
	install -m 644 $sub/pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP.%{name}-$base.pom
	%add_to_maven_depmap ch.qos.logback $sub %{version} JPP/%{name} $base
done

# Part 2 of the hack -- make sure that the Maven depmap info is there for others too
%add_to_maven_depmap org.apache.geronimo.specs geronimo-jms_1.1_spec 1.1 JPP/geronimo spec-jms-1.1
# End part 2 of the hack

install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/examples
cp -r logback-examples/pom.xml logback-examples/src $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/examples


%post
%update_maven_depmap

%postun
%update_maven_depmap

%pre javadoc
# workaround for rpm bug, can be removed in F-17
[ $1 -gt 1 ] && [ -L %{_javadocdir}/%{name} ] && \
rm -rf $(readlink -f %{_javadocdir}/%{name}) %{_javadocdir}/%{name} || :


%files
%defattr(-,root,root,-)
%{_javadir}/%{name}
%config(noreplace) %{_mavendepmapfragdir}/%{name}
%doc LICENSE.txt README.txt docs/*
%{_mavenpomdir}/*.pom

%files javadoc
%defattr(-,root,root,-)
%doc LICENSE.txt
%{_javadocdir}/%{name}

%files examples
%defattr(-,root,root,-)
%doc LICENSE.txt
%{_datadir}/%{name}-%{version}

%changelog
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
