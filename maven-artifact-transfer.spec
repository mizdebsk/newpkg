Name:           maven-artifact-transfer
Version:        3.0
Release:        0.1.20151012svn1708080%{?dist}
Summary:        Apache Maven Artifact Transfer
License:        ASL 2.0
URL:            http://maven.apache.org/shared/maven-artifact-transfer
BuildArch:      noarch

# svn export -r 1708080 http://svn.apache.org/repos/asf/maven/shared/trunk/maven-artifact-transfer
# mvn -f maven-artifact-transfer -P apache-release package
# cp maven-artifact-transfer/target/maven-artifact-transfer-3.0-SNAPSHOT-source-release.zip .
Source0:        %{name}-%{version}-SNAPSHOT-source-release.zip
#Source0:        http://repo1.maven.org/maven2/org/apache/maven/shared/%{name}/%{version}/%{name}-%{version}-source-release.zip

Patch0:         0001-Compatibility-with-Maven-3.0.3-and-later.patch

BuildRequires:  maven-local
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.maven:maven-artifact)
BuildRequires:  mvn(org.apache.maven:maven-core)
BuildRequires:  mvn(org.apache.maven.plugins:maven-enforcer-plugin)
BuildRequires:  mvn(org.apache.maven.shared:maven-common-artifact-filters) >= 3.0
BuildRequires:  mvn(org.apache.maven.shared:maven-shared-components:pom:)
BuildRequires:  mvn(org.apache.rat:apache-rat-plugin)
BuildRequires:  mvn(org.codehaus.plexus:plexus-component-annotations)
BuildRequires:  mvn(org.codehaus.plexus:plexus-component-metadata)
BuildRequires:  mvn(org.eclipse.aether:aether-api)
BuildRequires:  mvn(org.eclipse.aether:aether-impl)
BuildRequires:  mvn(org.eclipse.aether:aether-util)

%description
An API to either install or deploy artifacts with Maven 3.

%package javadoc
Summary:        API documentation for %{name}

%description javadoc
This package provides %{summary}.

%prep
%setup -q -n %{name}-%{version}-SNAPSHOT
%patch0 -p1

%pom_remove_plugin :maven-shade-plugin
%pom_remove_plugin :animal-sniffer-maven-plugin

# We don't want to support legacy Maven versions (older than 3.1)
%pom_remove_dep org.sonatype.aether:
find -name Maven30\*.java -delete

%build
%mvn_build -f

%install
%mvn_install

%files -f .mfiles
%license LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%license LICENSE NOTICE

%changelog
* Tue Jun  9 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0-0.1.20151012svn1708080
- Initial packaging
