Name:           zinc
Version:        0.3.1
Release:        1%{?dist}
Summary:        Incremental scala compiler
License:        ASL 2.0
URL:            https://github.com/typesafehub/zinc
BuildArch:      noarch

Source0:        https://github.com/typesafehub/zinc/archive/v%{version}.tar.gz
Source1:        http://repo1.maven.org/maven2/com/typesafe/zinc/zinc/%{version}/zinc-%{version}.pom
# ASL mandates that the licence file be included in redistributed source
Source2:        http://www.apache.org/licenses/LICENSE-2.0.txt

Patch0:         0001-Fix-file-filtering.patch

BuildRequires:  javapackages-local
BuildRequires:  mvn(org.scala-lang:scala-library)
BuildRequires:  mvn(org.scala-sbt:incremental-compiler)
BuildRequires:  mvn(com.martiansoftware:nailgun-server)

%description
Zinc is a stand-alone version of sbt's incremental compiler.

%prep
%setup -q
%patch0 -p1

cp %{SOURCE1} pom.xml
cp %{SOURCE2} LICENSE.txt

%pom_xpath_remove "pom:dependency[pom:classifier='sources']"
%pom_change_dep :incremental-compiler org.scala-sbt:

%build
scalac -cp $(build-classpath sbt nailgun) src/main/scala/com/typesafe/zinc/*
jar cf zinc.jar com
%mvn_artifact pom.xml zinc.jar

%install
%mvn_install

%files -f .mfiles
%doc README.md
%license LICENSE.txt

%changelog
* Wed Dec  2 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.3.1-1
- Initial packaging
