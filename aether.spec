Name:           aether
Version:        1.11
Release:        4%{?dist}
Summary:        Sonatype library to resolve, install and deploy artifacts the Maven way

Group:          Development/Libraries
License:        EPL or ASL 2.0
URL:            https://docs.sonatype.org/display/AETHER/Home
# git clone https://github.com/sonatype/sonatype-aether.git
# git archive --prefix="aether-1.11/" --format=tar aether-1.11 | bzip2 > aether-1.11.tar.bz2
Source0:        %{name}-%{version}.tar.bz2

Patch0:         0001-Remove-sonatype-test-dependencies.patch

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


Requires:       async-http-client >= 1.6.1
Requires:       java >= 1:1.6.0
Requires(post): jpackage-utils
Requires(postun): jpackage-utils


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
%patch0 -p1
rm -rf aether-connector-asynchttpclient/src/test
rm -rf aether-connector-wagon/src/test

%build
mvn-rpmbuild install javadoc:aggregate


%install
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/%{name}
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}

for module in aether-api aether-connector-file aether-connector-wagon \
         aether-impl aether-spi aether-test-util aether-util;do
pushd $module
      jarname=`echo $module | sed s:aether-::`
      install -m 644 target/$module-*.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/$jarname.jar

      install -pm 644 pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP.%{name}-$jarname.pom
      %add_to_maven_depmap org.sonatype.aether $module %{version} JPP/%{name} $jarname
popd
done

install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

install -pm 644 pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP.%{name}-parent.pom
%add_to_maven_depmap  org.sonatype.aether %{name}-parent %{version} JPP/%{name} parent

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%doc README.md
%{_javadir}/%{name}
%{_mavendepmapfragdir}/%{name}
%{_mavenpomdir}/*.pom

%files javadoc
%{_javadocdir}/%{name}

%changelog
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
