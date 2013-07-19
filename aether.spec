# Conditionals to build Aether with or without AHC connector
# (connector for Async Http Client).
%if 0%{?fedora}
%bcond_without ahc
%endif

%global vertag M2

Name:           aether
Epoch:          1
Version:        0.9.0
Release:        0.%{vertag}.1%{?dist}
Summary:        Sonatype library to resolve, install and deploy artifacts the Maven way
License:        EPL or ASL 2.0
URL:            https://docs.sonatype.org/display/AETHER/Home
BuildArch:      noarch

Source0:        http://git.eclipse.org/c/%{name}/%{name}-core.git/snapshot/%{name}-%{version}.%{vertag}.tar.bz2

# Temporarly BuildRequire Sonatype Aether
BuildRequires:  aether < 1:0

BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.maven.wagon:wagon-provider-api)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin) >= 1.7
BuildRequires:  mvn(org.codehaus.plexus:plexus-classworlds)
BuildRequires:  mvn(org.codehaus.plexus:plexus-component-annotations)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  mvn(org.slf4j:slf4j-api)
BuildRequires:  mvn(org.sonatype.forge:forge-parent)
BuildRequires:  mvn(org.sonatype.plugins:sisu-maven-plugin)
BuildRequires:  mvn(org.sonatype.sisu:sisu-inject-plexus)
%if %{with ahc}
BuildRequires:  mvn(com.ning:async-http-client)
%endif

%description
Aether is a standalone library to resolve, install and deploy artifacts
the Maven way.

%package api
Summary: Aether API

%description api
Aether is a standalone library to resolve, install and deploy
artifacts the Maven way.  This package provides application
programming interface for Aether repository system.

%if %{with ahc}
%package connector-asynchttpclient
Summary: Aether connector for Async Http Client

%description connector-asynchttpclient
Aether is a standalone library to resolve, install and deploy
artifacts the Maven way.  This package provides Aether repository
connector implementation based on Async Http Client.
%endif

%package connector-file
Summary: Aether connector for file URLs

%description connector-file
Aether is a standalone library to resolve, install and deploy
artifacts the Maven way.  This package provides Aether repository
connector implementation for repositories using file:// URLs.

%package connector-wagon
Summary: Aether connector for Maven Wagon

%description connector-wagon
Aether is a standalone library to resolve, install and deploy
artifacts the Maven way.  This package provides Aether repository
connector implementation based on Maven Wagon.

%package impl
Summary: Implementation of Aether repository system

%description impl
Aether is a standalone library to resolve, install and deploy
artifacts the Maven way.  This package provides implementation of
Aether repository system.

%package spi
Summary: Aether SPI

%description spi
Aether is a standalone library to resolve, install and deploy
artifacts the Maven way.  This package contains Aether service
provider interface (SPI) for repository system implementations and
repository connectors.

%package test-util
Summary: Aether test utilities

%description test-util
Aether is a standalone library to resolve, install and deploy
artifacts the Maven way.  This package provides collection of utility
classes that ease testing of Aether repository system.

%package util
Summary: Aether utilities

%description util
Aether is a standalone library to resolve, install and deploy
artifacts the Maven way.  This package provides a collection of
utility classes to ease usage of Aether repository system.

%package javadoc
Summary: Java API documentation for Aether

%description javadoc
Aether is a standalone library to resolve, install and deploy
artifacts the Maven way.  This package provides Java API documentation
for Aether.

%prep
%setup -q -n %{name}-%{version}.%{vertag}

%if %{without ahc}
%pom_disable_module aether-connector-asynchttpclient
%endif

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

# Animal sniffer is not useful in Fedora
for module in . aether-connector-wagon aether-util aether-api   \
              aether-impl aether-connector-asynchttpclient      \
              aether-connector-file aether-test-util; do
    %pom_remove_plugin :animal-sniffer-maven-plugin $module
done

%pom_remove_plugin :maven-enforcer-plugin

# Workaround for rhbz#911365
%pom_xpath_inject pom:project "<dependencies/>"
%pom_add_dep cglib:cglib:any:test
%pom_add_dep aopalliance:aopalliance:any:test

# Keep compatibility with packages that use old JAR locations until
# they migrate.
%mvn_file ":{%{name}-{*}}" %{name}/@1 %{name}/@2

%build
%mvn_build -s

%install
%mvn_install

install -d -m 755 %{buildroot}%{_javadir}/sonatype-%{name}
for jar in %{_javadir}/sonatype-%{name}/*; do
    mod=`basename ${jar/.jar/}`
    cp -p %{_javadir}/%{name}/$mod.jar %{buildroot}%{_javadir}/sonatype-%{name}/
    cp -p %{_mavenpomdir}/JPP.%{name}-$mod.pom %{buildroot}%{_mavenpomdir}/JPP.sonatype-%{name}-$mod.pom
    %add_maven_depmap JPP.sonatype-%{name}-$mod.pom sonatype-%{name}/$mod.jar -f $mod
done
cp -p %{_mavenpomdir}/JPP.%{name}-org.sonatype.%{name}@%{name}.pom %{buildroot}%{_mavenpomdir}/JPP.sonatype-%{name}-%{name}.pom
%add_maven_depmap JPP.sonatype-%{name}-%{name}.pom -f %{name}

%files -f .mfiles-%{name}
%doc README.md
%doc epl-v10.html notice.html

%files api -f .mfiles-%{name}-api
%doc README.md
%doc epl-v10.html notice.html
%dir %{_javadir}/%{name}
%dir %{_javadir}/sonatype-%{name}

%files connector-file -f .mfiles-%{name}-connector-file
%files connector-wagon -f .mfiles-%{name}-connector-wagon
%files impl -f .mfiles-%{name}-impl
%files spi -f .mfiles-%{name}-spi
%files test-util -f .mfiles-%{name}-test-util
%files util -f .mfiles-%{name}-util
%files javadoc -f .mfiles-javadoc
%doc epl-v10.html notice.html

%if %{with ahc}
%files connector-asynchttpclient -f .mfiles-%{name}-connector-asynchttpclient
%endif

%changelog
* Fri Jul 19 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:0.9.0-0.M2.1
- Switch upstream from Sonatype to Eclipse
- Update to upstream version 0.9.0.M2
- Install Sonatype Aether in pararell to Eclipse Aether

* Fri Jul 19 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.13.1-12
- Add symlinks to Sonatype Aether

* Wed Jun 26 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.13.1-11
- Install license files
- Resolves: rhbz#958116

* Fri May 10 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.13.1-10
- Conditionally build without AHC connector

* Thu May  2 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.13.1-9
- Install compat JAR symlinks
- Resolves: rhbz#958558

* Tue Apr 30 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.13.1-8
- Complete spec file rewrite
- Build with xmvn
- Split into multiple subpackages, resolves: rhbz#916142
- Update to current packaging guidelines

* Thu Feb  7 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.13.1-7
- Build with xmvn
- Disable animal sniffer
- Remove R on jboss-parent, resolves: rhbz#908583

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.13.1-6
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Mon Aug 27 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.13.1-5
- Disable animal-sniffer on RHEL

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

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
