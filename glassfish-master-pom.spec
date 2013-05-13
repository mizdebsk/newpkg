Name:          glassfish-master-pom
Version:       8
Release:       2%{?dist}
Summary:       Master POM for Glassfish Maven projects
Group:         Development/Libraries
License:       CDDL or GPLv2 with exceptions
URL:           http://glassfish.java.net/
# svn export https://svn.java.net/svn/glassfish~svn/tags/master-pom-8/ glassfish-master-pom-8
# tar czf glassfish-master-pom-8-src-svn.tar.gz glassfish-master-pom-8
Source0:       %{name}-%{version}-src-svn.tar.gz
# wget -O glassfish-LICENSE.txt https://svn.java.net/svn/glassfish~svn/tags/legal-1.1/src/main/resources/META-INF/LICENSE.txt
# glassfish-master-pom package don't include the license file
Source1:       glassfish-LICENSE.txt

BuildRequires: java-devel
BuildRequires: maven-local
Requires:      java
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
# Nothing to do
%install

mkdir -p %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap JPP-%{name}.pom

%check
mvn-rpmbuild verify

%files
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}
%doc LICENSE.txt

%changelog
* Thu May 02 2013 gil cattaneo <puntogil@libero.it> 8-2
- fixed license tag

* Sat Aug 25 2012 gil cattaneo <puntogil@libero.it> 8-1
- initial rpm