%global pkg_name glassfish-legal
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

Name:          %{?scl_prefix}%{pkg_name}
Version:       1.1
Release:       7.1%{?dist}
Summary:       Legal License for glassfish code
License:       CDDL or GPLv2 with exceptions
URL:           http://glassfish.java.net/
# svn export https://svn.java.net/svn/glassfish~svn/tags/legal-1.1/ glassfish-legal-1.1
# tar czf glassfish-legal-1.1-src-svn.tar.gz glassfish-legal-1.1
Source0:       %{pkg_name}-%{version}-src-svn.tar.gz

BuildRequires: %{?scl_prefix}glassfish-master-pom
BuildRequires: %{?scl_prefix_java_common}maven-local
BuildRequires: %{?scl_prefix}maven-remote-resources-plugin

Requires:      %{?scl_prefix}glassfish-master-pom
BuildArch:     noarch

%description
An archive which contains license files for glassfish code.

%prep
%setup -q -n %{pkg_name}-%{version}

sed -i 's/\r//' src/main/resources/META-INF/LICENSE.txt
cp -p src/main/resources/META-INF/LICENSE.txt .

%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%mvn_file :legal %{pkg_name}
%{?scl:EOF}

%build
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%mvn_build -- -Dproject.build.sourceEncoding=UTF-8
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%mvn_install
%{?scl:EOF}

%files -f .mfiles
%doc LICENSE.txt

%changelog
* Mon Jan 11 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.1-7.1
- SCL-ize package

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Feb 03 2015 gil cattaneo <puntogil@libero.it> 1.1-6
- introduce license macro

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 1.1-4
- Use Requires: java-headless rebuild (#1067528)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 08 2013 gil cattaneo <puntogil@libero.it> 1.1-2
- switch to XMvn
- minor changes to adapt to current guideline

* Wed Jan 16 2013 gil cattaneo <puntogil@libero.it> 1.1-1
- initial rpm
