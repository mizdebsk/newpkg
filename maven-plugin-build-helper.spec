Name:           maven-plugin-build-helper
Version:        1.5
Release:        5%{?dist}
Summary:        Build Helper Maven Plugin

Group:          Development/Libraries
License:        MIT and ASL 2.0
URL:            http://mojo.codehaus.org/build-helper-maven-plugin/
# The source tarball has been generated from upstream VCS:
# svn export https://svn.codehaus.org/mojo/tags/build-helper-maven-plugin-%{version} 
#            %{name}-%{version}
# tar caf %{name}-%{version}.tar.xz %{name}-%{version}
Source0:        %{name}-%{version}.tar.xz
Patch0:         add-junit-dependency.patch
Patch1:         %{name}-core.patch

BuildArch: noarch

BuildRequires: jpackage-utils
BuildRequires: plexus-utils
BuildRequires: maven
BuildRequires: maven-plugin-cobertura
BuildRequires: maven-plugin-plugin
BuildRequires: maven-resources-plugin
BuildRequires: maven-compiler-plugin
BuildRequires: maven-install-plugin
BuildRequires: maven-jar-plugin
BuildRequires: maven-javadoc-plugin
BuildRequires: maven-enforcer-plugin
BuildRequires: maven-surefire-plugin
BuildRequires: maven-surefire-provider-junit4
BuildRequires: maven-doxia-sitetools
BuildRequires: mojo-parent
BuildRequires: junit4
Requires: jpackage-utils
Requires: plexus-utils
Requires: mojo-parent

%description
This plugin contains various small independent goals to assist with
Maven build lifecycle.

%package javadoc
Group:          Documentation
Summary:        Javadoc for %{name}
Requires:       jpackage-utils

%description javadoc
API documentation for %{name}.

%prep
%setup -q 
%patch0
%patch1 -p1

%build
mvn-rpmbuild install javadoc:aggregate

%install
# jars
install -d -m 0755 %{buildroot}%{_javadir}
install -m 644 target/build-helper-maven-plugin-%{version}.jar \
  %{buildroot}%{_javadir}/%{name}.jar


# poms
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml \
    %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom

%add_maven_depmap JPP-%{name}.pom %{name}.jar

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/api*/* %{buildroot}%{_javadocdir}/%{name}/

%files
%{_javadir}/%{name}.jar
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}

%files javadoc
%{_javadocdir}/%{name}

%changelog
* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Tomas Radej <tradej@redhat.com> - 1.5-4
- Update to current guidelines
- Fix build

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Oct 28 2010 Alexander Kurtakov <akurtako@redhat.com> 1.5-2
- Maven plugins should require parent poms because they are totally unusable without them.

* Thu Sep 16 2010 Alexander Kurtakov <akurtako@redhat.com> 1.5-1
- Update to 1.5.
- Use newer maven packages' names.

* Thu Sep 10 2009 Alexander Kurtakov <akurtako@gmail.com> 1.4-1
- Initial package.
