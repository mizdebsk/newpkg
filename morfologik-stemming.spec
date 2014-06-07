Name:          morfologik-stemming
Version:       1.8.3
Release:       2%{?dist}
Summary:       Morfologik stemming library
License:       BSD
URL:           http://morfologik.blogspot.com/
Source0:       https://github.com/morfologik/morfologik-stemming/archive/%{version}.tar.gz

BuildRequires: java-devel

BuildRequires: mvn(com.carrotsearch:hppc)
BuildRequires: mvn(com.google.guava:guava)
BuildRequires: mvn(commons-cli:commons-cli)
BuildRequires: mvn(commons-lang:commons-lang)
BuildRequires: mvn(org.sonatype.oss:oss-parent)

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

# remove classpath from manifest files
for m in morfologik-polish morfologik-speller %{name} morfologik-tools ;do
%pom_xpath_set "pom:project/pom:build/pom:plugins/pom:plugin[pom:artifactId = 'maven-jar-plugin']/pom:configuration/pom:archive/pom:manifest/pom:addClasspath" false ${m}
done

%pom_remove_dep org.easytesting:fest-assert-core %{name}

%pom_disable_module morfologik-distribution
%pom_remove_plugin com.pyx4me:proguard-maven-plugin morfologik-tools

chmod 644 README
sed -i 's/\r//' CHANGES CONTRIBUTOR README morfologik.LICENSE

%pom_add_dep org.hamcrest:hamcrest-core::test morfologik-tools
sed -i "s|org.junit.internal.matchers.StringContains|org.hamcrest.core.StringContains|" \
 morfologik-tools/src/test/java/morfologik/tools/FSABuildToolTest.java

%build
# Test skipped for unavailable test deps
%mvn_build -f

%install
%mvn_install

%files -f .mfiles
%dir %{_javadir}/%{name}
%doc CHANGES CONTRIBUTOR README morfologik.LICENSE

%files javadoc -f .mfiles-javadoc
%doc morfologik.LICENSE

%changelog
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