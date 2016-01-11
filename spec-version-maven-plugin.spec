%global pkg_name spec-version-maven-plugin
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

Name:          %{?scl_prefix}%{pkg_name}
Version:       1.2
Release:       7.1%{?dist}
Summary:       Spec Version Maven Plugin
License:       CDDL or GPLv2 with exceptions
URL:           http://glassfish.java.net/
# svn export https://svn.java.net/svn/glassfish~svn/tags/spec-version-maven-plugin-1.2
# tar czf spec-version-maven-plugin-1.2-src-svn.tar.gz spec-version-maven-plugin-1.2
Source0:       %{pkg_name}-%{version}-src-svn.tar.gz
# wget -O glassfish-LICENSE.txt https://svn.java.net/svn/glassfish~svn/tags/legal-1.1/src/main/resources/META-INF/LICENSE.txt
# spec-version-maven-plugin package don't include the license file
Source1:       glassfish-LICENSE.txt


BuildRequires: %{?scl_prefix}mvn(net.java:jvnet-parent:pom:)
BuildRequires: %{?scl_prefix}mvn(org.apache.maven:maven-core)
BuildRequires: %{?scl_prefix}mvn(org.apache.maven:maven-model)
BuildRequires: %{?scl_prefix}mvn(org.apache.maven:maven-plugin-api)
BuildRequires: %{?scl_prefix}mvn(org.codehaus.plexus:plexus-resources)

# test dep
BuildRequires: %{?scl_prefix_java_common}mvn(junit:junit)
BuildRequires: %{?scl_prefix}mvn(org.apache.felix:maven-bundle-plugin)

BuildRequires: %{?scl_prefix_java_common}maven-local
BuildRequires: %{?scl_prefix}maven-plugin-build-helper
BuildRequires: %{?scl_prefix}maven-plugin-plugin

BuildArch:     noarch

%description
Maven Plugin to configure APIs version and
specs in a MANIFEST.MF file.

%package javadoc
Summary:       Javadoc for %{pkg_name}

%description javadoc
This package contains javadoc for %{pkg_name}.

%prep
%setup -q -n %{pkg_name}-%{version}

sed -i "s|mvn|mvn-rpmbuild|" src/main/resources/checkVersion.sh

cp -p %{SOURCE1} LICENSE.txt
sed -i 's/\r//' LICENSE.txt

%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%mvn_file :%{pkg_name} %{pkg_name}
%{?scl:EOF}

%build
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%mvn_build
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%mvn_install
%{?scl:EOF}

%files -f .mfiles
%doc LICENSE.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt

%changelog
* Mon Jan 11 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2-7.1
- SCL-ize package

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Feb 11 2015 gil cattaneo <puntogil@libero.it> 1.2-6
- introduce license macro

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 1.2-4
- Use Requires: java-headless rebuild (#1067528)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 02 2013 gil cattaneo <puntogil@libero.it> 1.2-2
- build with XMvn
- minor changes to adapt to current guideline

* Wed May 22 2013 gil cattaneo <puntogil@libero.it> 1.2-1
- initial rpm
