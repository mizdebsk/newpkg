Name:          morfologik-stemming
Version:       2.0.1
Release:       1%{?dist}
Summary:       Morfologik stemming library
License:       BSD
URL:           http://morfologik.blogspot.com/
Source0:       https://github.com/morfologik/morfologik-stemming/archive/%{version}.tar.gz

BuildRequires: mvn(com.carrotsearch:hppc)
BuildRequires: mvn(com.google.guava:guava)
BuildRequires: mvn(commons-cli:commons-cli)
BuildRequires: mvn(commons-lang:commons-lang)
BuildRequires: mvn(org.sonatype.oss:oss-parent:pom:)
BuildRequires: mvn(com.carrotsearch:hppc)

%if 0
# test deps
BuildRequires: mvn(com.carrotsearch:junit-benchmarks)
BuildRequires: mvn(org.hamcrest:hamcrest-core)
BuildRequires: mvn(junit:junit)
BuildRequires: mvn(org.easytesting:fest-assert-core:2.0M10)
%endif

BuildRequires: maven-local

BuildArch:     noarch

%description
Morfologik provides high quality lemmatisation for the Polish language,
along with tools for building and using byte-based finite state automata.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q
find . -name "*.class" -print -delete
find . -name "*.jar" -print -delete

chmod 644 README.txt
sed -i 's/\r//' CHANGES.txt CONTRIBUTING.txt README.txt LICENSE.txt

%pom_add_dep org.hamcrest:hamcrest-core::test morfologik-tools
%pom_remove_plugin com.carrotsearch.randomizedtesting:junit4-maven-plugin
%pom_remove_plugin de.thetaphi:forbiddenapis
%pom_remove_plugin :maven-javadoc-plugin

sed -i 's/2.0.0/${project.version}/g' morfologik-speller/pom.xml

%build
# Test skipped for unavailable test deps
%mvn_build -f -- -Dfile.encoding=UTF-8 

%install
%mvn_install

%files -f .mfiles
%dir %{_javadir}/%{name}
%doc CHANGES.txt CONTRIBUTING.txt README.txt
%license LICENSE.txt

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt

%changelog
* Thu Jan 21 2016 Alexander Kurtakov <akurtako@redhat.com> 2.0.1-1
- Update to 2.0.1

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Feb 10 2015 gil cattaneo <puntogil@libero.it> 1.8.3-3
- introduce license macro

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Jan 11 2014 gil cattaneo <puntogil@libero.it> 1.8.3-1
- update to 1.8.3

* Sun Dec 29 2013 gil cattaneo <puntogil@libero.it> 1.8.2-1
- update to 1.8.2

* Thu Dec 05 2013 gil cattaneo <puntogil@libero.it> 1.8.1-1
- update to 1.8.1

* Mon Oct 21 2013 gil cattaneo <puntogil@libero.it> 1.7.2-1
- update to 1.7.2

* Sun Aug 25 2013 gil cattaneo <puntogil@libero.it> 1.5.5-1
- initial rpm
