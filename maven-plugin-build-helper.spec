Name:           maven-plugin-build-helper
Version:        1.5
Release:        1%{?dist}
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
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch: noarch

BuildRequires: plexus-utils
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
Requires: plexus-utils
Requires(post): jpackage-utils
Requires(postun): jpackage-utils

%description
This plugin contains various small independent goals to assist with
Maven build lifecycle.

%package javadoc
Group:          Documentation
Summary:        Javadoc for %{name}

%description javadoc
API documentation for %{name}.

%prep
%setup -q 
%patch0

%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mvn-jpp \
        -e \
        -Dmaven2.jpp.mode=true \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        package javadoc:javadoc

%install
rm -rf %{buildroot}

# jars
install -d -m 0755 %{buildroot}%{_javadir}
install -m 644 target/build-helper-maven-plugin-%{version}.jar \
  %{buildroot}%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar

(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; \
    do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

%add_to_maven_depmap org.codehaus.mojo build-helper-maven-plugin %{version} JPP maven-plugin-build-helper

# poms
install -d -m 755 %{buildroot}%{_datadir}/maven2/poms
install -pm 644 pom.xml \
    %{buildroot}%{_datadir}/maven2/poms/JPP-%{name}.pom

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr target/site/api*/* %{buildroot}%{_javadocdir}/%{name}-%{version}/
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}
rm -rf target/site/api*

%clean
%{__rm} -rf %{buildroot}

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(-,root,root,-)
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar
%{_datadir}/maven2/poms/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

%changelog
* Thu Sep 16 2010 Alexander Kurtakov <akurtako@redhat.com> 1.5-1
- Update to 1.5.
- Use newer maven packages' names.

* Thu Sep 10 2009 Alexander Kurtakov <akurtako@gmail.com> 1.4-1
- Initial package.
