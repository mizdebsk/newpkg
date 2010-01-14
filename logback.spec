%global with_gcj %{!?_without_gcj:1}%{?_without_gcj:0}

Name:		logback
Version:	0.9.18
Release:	3%{?dist}
Summary:	A Java logging library

Group:		Development/Tools
License:	LGPLv2 or EPL
URL:		http://logback.qos.ch/
Source0:	http://logback.qos.ch/dist/%{name}-%{version}.tar.gz
# Add dummy implementations of two new methods from Jetty 6
Patch0:		%{name}-LifecycleListener.patch
# Modify the POMs to remove unavailable dependencies, and to avoid
# building the "site" and "examples" directories
Patch1:		%{name}-%{version}-clean-poms.patch

BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	dos2unix
BuildRequires:	geronimo-specs
BuildRequires:	janino 
BuildRequires:	java-devel >= 1.6.0
BuildRequires:	javamail >= 1.4
BuildRequires:	jetty >= 6.1.20-7
BuildRequires:	jpackage-utils >= 0:1.5
BuildRequires:	slf4j
BuildRequires:	tomcat5-server-lib
BuildRequires:	tomcat5-servlet-2.4-api
BuildRequires:	tomcat5
BuildRequires:  easymock2
BuildRequires:	hsqldb >= 1:1.8.0.10-5

# Maven build requirements
BuildRequires:	maven2
BuildRequires:	maven2-plugin-assembly
BuildRequires:	maven-plugin-bundle
BuildRequires:	maven2-plugin-compiler
BuildRequires:	maven2-plugin-idea
BuildRequires:	maven2-plugin-install
BuildRequires:	maven2-plugin-jar
BuildRequires:	maven2-plugin-javadoc
BuildRequires:	maven2-plugin-resources
BuildRequires:	maven2-plugin-site
BuildRequires:	maven2-plugin-source
BuildRequires:	maven-surefire-maven-plugin

%if %{with_gcj}
BuildRequires:	java-gcj-compat-devel >= 1.0.31
Requires(post):	java-gcj-compat >= 1.0.31
Requires(postun):	java-gcj-compat >= 1.0.31
%else
BuildArch:	noarch
%endif

# Dependencies from the pom files
Requires:	dom4j
Requires:       easymock2
Requires:       geronimo-specs
Requires:	hsqldb >= 1:1.8.0.10-5
Requires:	janino
Requires:	javamail
Requires:	jetty
Requires:	slf4j
Requires:	tomcat5
Requires:	tomcat5-server-lib
Requires:	tomcat5-servlet-2.4-api

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
BuildArch:	noarch

%description javadoc
Documentation for the Logback library


%package examples
Summary:	Sample code for %{name}
Group:		Documentation
BuildArch:	noarch

%description examples
Sample code for the Logback library

%prep
%setup -q
%patch0 -p1
%patch1 -p1

find . -name "*.jar" | xargs rm -f

# Clean up the documentation
dos2unix LICENSE.txt README.txt docs/*.* docs/*/*.* docs/*/*/*.* docs/*/*/*/*.*
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
	install

mvn-jpp \
	-Dmaven.repo.local=$MAVEN_REPO_LOCAL \
	-Dmaven.test.skip=true \
	javadoc:javadoc

%install
rm -rf $RPM_BUILD_ROOT

install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/%{name}
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms

install -d -m 755 p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
(cd $RPM_BUILD_ROOT%{_javadocdir} && ln -sf %{name}-%{version} %{name})
cp -r target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}

install -pm 644 pom.xml $RPM_BUILD_ROOT/%{_datadir}/maven2/poms/JPP-%{name}-parent.pom
%add_to_maven_depmap ch.qos.logback %{name}-parent %{version} JPP %{name}-parent

for sub in logback-access logback-classic logback-core; do
	base=`echo $sub | sed 's/%{name}-//g'`
	install -m 644 $sub/target/$sub-%{version}.jar \
		$RPM_BUILD_ROOT%{_javadir}/%{name}/$base-%{version}.jar
	install -m 644 $sub/pom.xml $RPM_BUILD_ROOT/%{_datadir}/maven2/poms/JPP-$sub.pom
	%add_to_maven_depmap ch.qos.logback $sub %{version} JPP/%{name} $base
done

# Part 2 of the hack -- make sure that the Maven depmap info is there for others too
%add_to_maven_depmap org.apache.geronimo.specs geronimo-jms_1.1_spec 1.1 JPP/geronimo spec-jms-1.1
# End part 2 of the hack

(cd $RPM_BUILD_ROOT%{_javadir}/%{name} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/examples
cp -r logback-examples/pom.xml logback-examples/src $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/examples

%if %{with_gcj}
%{_bindir}/aot-compile-rpm
%endif



%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_maven_depmap
%if %{with_gcj}
  if [ -x %{_bindir}/rebuild-gcj-db ] 
  then
    %{_bindir}/rebuild-gcj-db
  fi
%endif

%postun
%update_maven_depmap
%if %{with_gcj}
  if [ -x %{_bindir}/rebuild-gcj-db ] 
  then
    %{_bindir}/rebuild-gcj-db
  fi
%endif


%files
%defattr(-,root,root,-)
%{_javadir}/%{name}
%config(noreplace) %{_mavendepmapfragdir}/%{name}
%doc LICENSE.txt README.txt docs/*
%{_datadir}/maven2/poms/*.pom
%if %{with_gcj}
%attr(-,root,root) %{_libdir}/gcj/%{name}
%endif

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

%files examples
%defattr(-,root,root,-)
%{_datadir}/%{name}-%{version}

%changelog
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
