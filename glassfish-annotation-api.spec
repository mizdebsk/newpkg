%global namedreltag %{nil}
%global namedversion %{version}%{?namedreltag}
%global oname javax.annotation-api
Name:          glassfish-annotation-api
Version:       1.2
Release:       3%{?dist}
Summary:       Common Annotations API Specification (JSR 250)
Group:         Development/Libraries
License:       CDDL or GPLv2 with exceptions
# http://jcp.org/en/jsr/detail?id=250
URL:           http://glassfish.java.net/
# svn export https://svn.java.net/svn/glassfish~svn/tags/javax.annotation-api-1.2/ glassfish-annotation-api-1.2
# tar czf glassfish-annotation-api-1.2-src-svn.tar.gz glassfish-annotation-api-1.2
Source0:       %{name}-%{namedversion}-src-svn.tar.gz

BuildRequires: java-devel
BuildRequires: jvnet-parent
BuildRequires: glassfish-legal

BuildRequires: maven-local
BuildRequires: maven-compiler-plugin
BuildRequires: maven-jar-plugin
BuildRequires: maven-javadoc-plugin
BuildRequires: maven-plugin-bundle
BuildRequires: maven-remote-resources-plugin
BuildRequires: maven-resources-plugin
BuildRequires: maven-source-plugin
BuildRequires: maven-surefire-plugin
BuildRequires: spec-version-maven-plugin

Requires:      java
BuildArch:     noarch

%description
Common Annotations APIs for the Java Platform (JSR 250).

%package javadoc
Group:         Documentation
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{name}-%{namedversion}

%pom_remove_plugin org.codehaus.mojo:findbugs-maven-plugin

%build

mvn-rpmbuild package javadoc:aggregate

sed -i 's/\r//' target/classes/META-INF/LICENSE.txt
cp -p target/classes/META-INF/LICENSE.txt .

%install

mkdir -p %{buildroot}%{_javadir}
install -pm 644 target/%{oname}-%{namedversion}.jar %{buildroot}%{_javadir}/%{name}.jar

mkdir -p %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap JPP-%{name}.pom %{name}.jar

mkdir -p %{buildroot}%{_javadocdir}/%{name}
cp -rp target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}

%files
%{_javadir}/%{name}.jar
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}
%doc LICENSE.txt

%files javadoc
%{_javadocdir}/%{name}
%doc LICENSE.txt

%changelog
* Sun May 26 2013 gil cattaneo <puntogil@libero.it> 1.2-3
- rebuilt with spec-version-maven-plugin support

* Wed May 22 2013 gil cattaneo <puntogil@libero.it> 1.2-2
- fixed manifest

* Tue May 07 2013 gil cattaneo <puntogil@libero.it> 1.2-1
- update to 1.2

* Tue Apr 02 2013 gil cattaneo <puntogil@libero.it> 1.2-0.1.b04
- initial rpm