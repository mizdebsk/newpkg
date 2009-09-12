Name:           maven-plugin-build-helper
Version:        1.4
Release:        1%{?dist}
Summary:        Build Helper Maven Plugin

Group:          Development/Libraries
License:        MIT and ASL 2.0
URL:            http://mojo.codehaus.org/build-helper-maven-plugin/
# The source tarball has been generated from upstream VCS:
# svn export https://svn.codehaus.org/mojo/tags/build-helper-maven-plugin-%{version} 
#            %{name}-%{version}
# tar cjvf %{name}-%{version}.tar.bz2 %{name}-%{version}
Source0:        maven-plugin-build-helper-1.4.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch: noarch

BuildRequires: plexus-utils
BuildRequires: maven-plugin-cobertura
BuildRequires: maven2-plugin-plugin
BuildRequires: maven2-plugin-resources
BuildRequires: maven2-plugin-compiler
BuildRequires: maven2-plugin-install
BuildRequires: maven2-plugin-jar
BuildRequires: maven2-plugin-javadoc
BuildRequires: maven2-plugin-enforcer
BuildRequires: maven-surefire-maven-plugin
BuildRequires: maven-surefire-provider-junit
BuildRequires: maven-doxia-sitetools
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
* Thu Sep 10 2009 Alexander Kurtakov <akurtako@gmail.com> 1.4-1
- Initial package.
