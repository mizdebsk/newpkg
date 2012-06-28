Name:           aether
Version:        1.13.1
Release:        3%{?dist}
Summary:        Sonatype library to resolve, install and deploy artifacts the Maven way

Group:          Development/Libraries
License:        EPL or ASL 2.0
URL:            https://docs.sonatype.org/display/AETHER/Home
# git clone https://github.com/sonatype/sonatype-aether.git
# git archive --prefix="aether-1.11/" --format=tar aether-1.11 | bzip2 > aether-1.11.tar.bz2
Source0:        %{name}-%{version}.tar.bz2

BuildArch:      noarch

BuildRequires:  maven
BuildRequires:  maven-compiler-plugin
BuildRequires:  maven-install-plugin
BuildRequires:  maven-jar-plugin
BuildRequires:  maven-javadoc-plugin
BuildRequires:  maven-resources-plugin
BuildRequires:  maven-site-plugin
BuildRequires:  maven-surefire-plugin
BuildRequires:  maven-surefire-provider-junit4
BuildRequires:  plexus-containers-component-metadata >= 1.5.4-4
BuildRequires:  animal-sniffer >= 1.6-5
BuildRequires:  mojo-parent
BuildRequires:  async-http-client >= 1.6.1
BuildRequires:  sonatype-oss-parent

# required by netty really, but we push this dep on level higer
BuildRequires:  jboss-parent
Requires:       jboss-parent

Requires:       async-http-client >= 1.6.1
Requires:       java >= 1:1.6.0


%description
Aether is standalone library to resolve, install and deploy artifacts
the Maven way developed by Sonatype

%package javadoc
Summary:   API documentation for %{name}
Group:     Documentation
Requires:  jpackage-utils

%description javadoc
%{summary}.

%prep
# last part will have to change every time
%setup -q

# we'd need org.sonatype.http-testing-harness so let's remove async
# and wagon http tests (leave others enabled)
for module in asynchttpclient wagon; do (
    cd ./aether-connector-$module
    rm -rf src/test
    # Removes all dependencies with test scope
    %pom_xpath_remove "pom:dependency[pom:scope[text()='test']]"
) done

# Remove clirr plugin
%pom_remove_plugin :clirr-maven-plugin
%pom_remove_plugin :clirr-maven-plugin aether-api
%pom_remove_plugin :clirr-maven-plugin aether-spi

%build
mvn-rpmbuild install javadoc:aggregate


%install
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/%{name}
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}

for module in aether-api aether-connector-file aether-connector-wagon aether-connector-asynchttpclient\
         aether-impl aether-spi aether-test-util aether-util;do
pushd $module
      jarname=`echo $module | sed s:aether-::`
      install -m 644 target/$module-*.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/$jarname.jar

      install -pm 644 pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP.%{name}-$jarname.pom
      %add_maven_depmap JPP.%{name}-$jarname.pom %{name}/$jarname.jar
popd
done

install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

install -pm 644 pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP.%{name}-parent.pom
%add_maven_depmap JPP.%{name}-parent.pom

%files
%doc README.md
%{_javadir}/%{name}
%{_mavendepmapfragdir}/%{name}
%{_mavenpomdir}/*.pom

%files javadoc
%{_javadocdir}/%{name}

%changelog
* Thu Jun 28 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.13.1-3
- Replace pom.xml patches with pom macros

* Thu Apr 19 2012 Alexander Kurtakov <akurtako@redhat.com> 1.13.1-2
- Install aether-connector-asynchttpclient - it was build but not installed.

* Tue Jan 31 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.13.1-1
- Update to latest upstream
- Update spec to latest guidelines

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun 8 2011 Alexander Kurtakov <akurtako@redhat.com> 1.11-3
- Build with maven 3.x.
- Do not require maven - not found in dependencies in poms.
- Guidelines fixes.

* Mon Feb 28 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.11-2
- Rebuild after bugfix update to plexus-containers (#675865)

* Fri Feb 25 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.11-1
- Update to latest version
- Add ASL 2.0 back as optional license

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 19 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.9-1
- License changed to EPL
- Add async-http-client to BR/R
- Update to latest version

* Wed Dec  8 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.7-3
- Make jars/javadocs versionless
- Remove buildroot and clean section

* Wed Oct 13 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.7-2
- Explained how to get tarball properly
- Removed noreplace on depmap fragment

* Mon Oct 11 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.7-1
- Initial Package
