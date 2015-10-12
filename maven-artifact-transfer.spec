Name:           maven-artifact-transfer
Version:        3.0
Release:        0.1.20151012svn1708080%{?dist}
Summary:        Apache Maven Artifact Transfer
License:        ASL 2.0
URL:            http://maven.apache.org/shared/maven-artifact-transfer
BuildArch:      noarch

# svn export -r 1708080 http://svn.apache.org/repos/asf/maven/shared/trunk/maven-artifact-transfer maven-artifact-transfer-3.0
# tar caf maven-artifact-transfer-3.0-SNAPSHOT-svn1708080.tar.xz maven-artifact-transfer-3.0/
Source0:        %{name}-%{version}-SNAPSHOT-svn1708080.tar.xz

BuildRequires:  maven-local

%description
An API to either install or deploy artifacts with Maven 3.

%package javadoc
Summary:        API documentation for %{name}

%description javadoc
This package provides %{summary}.

%prep
%setup -q
%pom_remove_dep org.sonatype.aether:
%pom_remove_plugin :maven-shade-plugin

%build
%mvn_build -f

%install
%mvn_install

%files -f .mfiles
#doc LICENSE.txt NOTICE.txt

%files javadoc -f .mfiles-javadoc
#doc LICENSE.txt NOTICE.txt

%changelog
* Tue Jun  9 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0-0.1.20151012svn1708080
- Initial packaging
