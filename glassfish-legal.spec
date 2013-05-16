Name:          glassfish-legal
Version:       1.1
Release:       1%{?dist}
Summary:       Legal License for glassfish code
Group:         Development/Libraries
License:       CDDL or GPLv2 with exceptions
URL:           http://glassfish.java.net/
# svn export https://svn.java.net/svn/glassfish~svn/tags/legal-1.1/ glassfish-legal-1.1
# tar czf glassfish-legal-1.1-src-svn.tar.gz glassfish-legal-1.1
Source0:       %{name}-%{version}-src-svn.tar.gz

BuildRequires: java-devel

BuildRequires: glassfish-master-pom
BuildRequires: maven-local
BuildRequires: maven-compiler-plugin
BuildRequires: maven-jar-plugin
BuildRequires: maven-remote-resources-plugin
BuildRequires: maven-resources-plugin
BuildRequires: maven-surefire-plugin

Requires:      glassfish-master-pom

Requires:      java
BuildArch:     noarch

%description
An archive which contains license files for glassfish code.

%prep
%setup -q -n %{name}-%{version}

sed -i 's/\r//' src/main/resources/META-INF/LICENSE.txt
cp -p src/main/resources/META-INF/LICENSE.txt .

%build

mvn-rpmbuild -Dproject.build.sourceEncoding=UTF-8 package

%install

mkdir -p %{buildroot}%{_javadir}
install -pm 644 target/legal-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar

mkdir -p %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap

%files
%{_javadir}/%{name}.jar
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}
%doc LICENSE.txt

%changelog
* Wed Jan 16 2013 gil cattaneo <puntogil@libero.it> 1.1-1
- initial rpm