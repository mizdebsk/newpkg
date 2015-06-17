Name:          glassfish-master-pom
Version:       8
Release:       7%{?dist}
Summary:       Master POM for Glassfish Maven projects
License:       CDDL or GPLv2 with exceptions
URL:           http://glassfish.java.net/
# svn export https://svn.java.net/svn/glassfish~svn/tags/master-pom-8/ glassfish-master-pom-8
# tar czf glassfish-master-pom-8-src-svn.tar.gz glassfish-master-pom-8
Source0:       %{name}-%{version}-src-svn.tar.gz
# wget -O glassfish-LICENSE.txt https://svn.java.net/svn/glassfish~svn/tags/legal-1.1/src/main/resources/META-INF/LICENSE.txt
# glassfish-master-pom package don't include the license file
Source1:       glassfish-LICENSE.txt

BuildRequires: maven-local
BuildArch:     noarch

%description
This is a shared POM parent for Glassfish Maven projects.

%prep
%setup -q
# remove wagon-webdav
%pom_xpath_remove pom:build/pom:extensions
%pom_xpath_inject "pom:build/pom:plugins/pom:plugin[pom:artifactId ='maven-compiler-plugin']" "<groupId>org.apache.maven.plugins</groupId><version>2.5.1</version>"
cp -p %{SOURCE1} LICENSE.txt
sed -i 's/\r//' LICENSE.txt

%build

%mvn_build

%install
%mvn_install

%files -f .mfiles
%license LICENSE.txt

%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Feb 03 2015 gil cattaneo <puntogil@libero.it> 8-6
- introduce license macro

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 05 2013 gil cattaneo <puntogil@libero.it> 8-3
- switch to XMvn
- minor changes to adapt to current guideline

* Thu May 02 2013 gil cattaneo <puntogil@libero.it> 8-2
- fixed license tag

* Sat Aug 25 2012 gil cattaneo <puntogil@libero.it> 8-1
- initial rpm