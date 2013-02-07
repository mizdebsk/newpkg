Name:           aether
Version:        1.13.1
Release:        7%{?dist}
Summary:        Sonatype library to resolve, install and deploy artifacts the Maven way

License:        EPL or ASL 2.0
URL:            https://docs.sonatype.org/display/AETHER/Home
# git clone https://github.com/sonatype/sonatype-aether.git
# git archive --prefix="aether-1.11/" --format=tar aether-1.11 | bzip2 > aether-1.11.tar.bz2
Source0:        %{name}-%{version}.tar.bz2

BuildArch:      noarch

BuildRequires:  maven-local
BuildRequires:  maven-surefire-provider-junit4
BuildRequires:  plexus-containers-component-metadata >= 1.5.4-4
BuildRequires:  forge-parent
BuildRequires:  async-http-client >= 1.6.1


%description
Aether is standalone library to resolve, install and deploy artifacts
the Maven way developed by Sonatype

%package javadoc
Summary:   API documentation for %{name}

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

for module in . aether-connector-wagon aether-util aether-api   \
              aether-impl aether-connector-asynchttpclient      \
              aether-connector-file aether-demo aether-test-util; do
    %pom_remove_plugin :animal-sniffer-maven-plugin $module
done

# Tests would fail without cglib dependency
%pom_xpath_inject pom:project "<dependencies/>"
%pom_add_dep cglib:cglib:2.2:test

%build
%mvn_file ":%{name}-{*}" %{name}/@1
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc README.md
%dir %{_javadir}/%{name}

%files javadoc -f .mfiles-javadoc

%changelog
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
