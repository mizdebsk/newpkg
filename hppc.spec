Name:          hppc
Version:       0.7.1
Release:       1%{?dist}
Summary:       High Performance Primitive Collections for Java
License:       ASL 2.0
URL:           http://labs.carrotsearch.com/hppc.html
Source0:       https://github.com/carrotsearch/hppc/archive/%{version}.tar.gz

BuildRequires: mvn(com.google.guava:guava)
BuildRequires: mvn(commons-io:commons-io)
BuildRequires: mvn(org.apache.ant:ant)
BuildRequires: mvn(org.apache.ant:ant-junit)
BuildRequires: mvn(org.apache.velocity:velocity)
BuildRequires: mvn(org.sonatype.oss:oss-parent:pom:)
BuildRequires: mvn(org.antlr:antlr4-maven-plugin)

%if 0
# hppc-benchmarks deps
# http://gil.fedorapeople.org/caliper-1.0-0.1.20120909SNAPSHOT.fc16.src.rpm
BuildRequires: mvn(com.google.caliper:caliper:0.5-rc1)
BuildRequires: mvn(com.google.code.gson:gson)
BuildRequires: mvn(com.h2database:h2)
BuildRequires: mvn(commons-io:commons-io)
BuildRequires: mvn(commons-lang:commons-lang)
BuildRequires: mvn(it.unimi.dsi:fastutil)
# http://gil.fedorapeople.org/trove-3.0.3-1.fc16.src.rpm
BuildRequires: mvn(net.sf.trove4j:trove4j:3.0.3)
BuildRequires: mvn(org.apache.mahout:mahout-collections)

# test deps
BuildRequires: mvn(com.carrotsearch:junit-benchmarks)
BuildRequires: mvn(junit:junit)
BuildRequires: mvn(com.carrotsearch.randomizedtesting:junit4-maven-plugin)
BuildRequires: mvn(com.carrotsearch.randomizedtesting:randomizedtesting-runner)
%endif

BuildRequires: maven-local
BuildRequires: maven-antrun-plugin
BuildRequires: maven-enforcer-plugin
BuildRequires: maven-plugin-build-helper

BuildArch:     noarch

%description
Fundamental data structures (maps, sets, lists, stacks, queues) generated for
combinations of object and primitive types to conserve JVM memory and speed
up execution.

%package templateprocessor
Summary:       HPPC Template Processor

%description templateprocessor
Template Processor and Code Generation for HPPC.

%package javadoc
Summary:       Javadoc for HPPC

%description javadoc
This package contains javadoc for HPPC.

%prep
%setup -q
find . -name "*.class" -print -delete
find . -name "*.jar" -print -delete

# Unavailable deps
%pom_disable_module %{name}-benchmarks
%pom_remove_plugin :junit4-maven-plugin
%pom_remove_plugin :forbiddenapis
%pom_remove_plugin :junit4-maven-plugin hppc

sed -i 's/\r//' CHANGES.txt

%mvn_file :%{name} %{name}
%mvn_file :%{name}-template-processor %{name}-templateprocessor
%mvn_package :%{name}-template-processor %{name}-templateprocessor

%build

# Disable test for now. Unavailable test deps
%mvn_build -f

%install
%mvn_install

%files -f .mfiles
%doc CHANGES.txt README.txt
%license LICENSE.txt

%files templateprocessor -f .mfiles-%{name}-templateprocessor
%license LICENSE.txt

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt

%changelog
* Wed Jan 20 2016 Alexander Kurtakov <akurtako@redhat.com> 0.7.1-1
- Update to upstream 0.7.1 release.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Feb 05 2015 gil cattaneo <puntogil@libero.it> 0.6.1-2
- introduce license macro

* Wed Dec 17 2014 gil cattaneo <puntogil@libero.it> 0.6.1-1
- update to 0.6.1

* Tue Jun 17 2014 gil cattaneo <puntogil@libero.it> 0.5.3-4
- fix BR list

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Dec 29 2013 gil cattaneo <puntogil@libero.it> 0.5.3-2
- add templateprocessor sub-package

* Thu Dec 05 2013 gil cattaneo <puntogil@libero.it> 0.5.3-1
- 0.5.3

* Sun Aug 25 2013 gil cattaneo <puntogil@libero.it> 0.5.2-1
- initial rpm
