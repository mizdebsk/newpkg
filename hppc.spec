Name:          hppc
Version:       0.5.3
Release:       3%{?dist}
Summary:       High Performance Primitive Collections for Java
License:       ASL 2.0
URL:           http://labs.carrotsearch.com/hppc.html
# NOTE newer relase use guava >= 14.x
Source0:       https://github.com/carrotsearch/hppc/archive/%{version}.tar.gz

Patch0:        %{name}-0.4.3-remove-retrotranslator.patch

BuildRequires: java-devel

BuildRequires: mvn(com.google.guava:guava)
BuildRequires: mvn(commons-io:commons-io)
BuildRequires: mvn(org.apache.ant:ant)
BuildRequires: mvn(org.apache.ant:ant-junit)
BuildRequires: mvn(org.apache.velocity:velocity)
BuildRequires: mvn(org.sonatype.oss:oss-parent)

%if 0
# hppc-benchmarks deps
# http://gil.fedorapeople.org/caliper-1.0-0.1.20120909SNAPSHOT.fc16.src.rpm
# http://gil.fedorapeople.org/caliper.spec
BuildRequires: mvn(com.google.caliper:caliper:0.5-rc1)
BuildRequires: mvn(com.google.code.gson:gson)
BuildRequires: mvn(com.h2database:h2)
BuildRequires: mvn(commons-io:commons-io)
BuildRequires: mvn(commons-lang:commons-lang)
BuildRequires: mvn(it.unimi.dsi:fastutil)
# http://gil.fedorapeople.org/trove-3.0.3-1.fc16.src.rpm
# http://gil.fedorapeople.org/trove.spec
BuildRequires: mvn(net.sf.trove4j:trove4j:3.0.3)
# https://bugzilla.redhat.com/show_bug.cgi?id=1000416
BuildRequires: mvn(org.apache.mahout:mahout-collections)

# test deps
# https://bugzilla.redhat.com/show_bug.cgi?id=1002166
BuildRequires: mvn(com.carrotsearch:junit-benchmarks)
BuildRequires: mvn(junit:junit)
# https://bugzilla.redhat.com/show_bug.cgi?id=1002157
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

# remove retrotranslator and backport-util-concurrent
%patch0 -p0

# remove ant-trax and ant-nodeps, fix jdk tools JAR location
%pom_xpath_remove "pom:project/pom:build/pom:pluginManagement/pom:plugins/pom:plugin[pom:artifactId = 'maven-antrun-plugin']/pom:dependencies/pom:dependency[pom:groupId = 'org.apache.ant']"
%pom_xpath_inject "pom:project/pom:build/pom:pluginManagement/pom:plugins/pom:plugin[pom:artifactId = 'maven-antrun-plugin']/pom:dependencies" "
<dependency>
  <groupId>org.apache.ant</groupId>
  <artifactId>ant</artifactId>
  <version>1.8.0</version>
</dependency>
<dependency>
  <groupId>org.apache.ant</groupId>
  <artifactId>ant-junit</artifactId>
  <version>1.8.0</version>
</dependency>
<dependency>
  <groupId>com.sun</groupId>
  <artifactId>tools</artifactId>
  <version>1.7.0</version>
</dependency>"

# Unavailable deps
%pom_disable_module %{name}-benchmarks
%pom_disable_module %{name}-examples

%pom_remove_plugin :findbugs-maven-plugin

%pom_remove_plugin :junit4-maven-plugin %{name}-core

sed -i 's/\r//' CHANGES

%build

%mvn_file :%{name} %{name}
%mvn_file :%{name}-templateprocessor %{name}-templateprocessor
%mvn_package :%{name}-templateprocessor %{name}-templateprocessor
# Disable test for now. Unavailable test deps
%mvn_build -f

%install
%mvn_install

%files -f .mfiles
%doc CHANGES LICENSE README

%files templateprocessor -f .mfiles-%{name}-templateprocessor
%doc LICENSE

%files javadoc -f .mfiles-javadoc
%doc LICENSE

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Dec 29 2013 gil cattaneo <puntogil@libero.it> 0.5.3-2
- add templateprocessor sub-package

* Thu Dec 05 2013 gil cattaneo <puntogil@libero.it> 0.5.3-1
- 0.5.3

* Sun Aug 25 2013 gil cattaneo <puntogil@libero.it> 0.5.2-1
- initial rpm