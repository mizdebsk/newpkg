%global full_name sonatype-aether
%global githash g6ef7c04

Name:           aether
Version:        1.7
Release:        3%{?dist}
Summary:        Sonatype library to resolve, install and deploy artifacts the Maven way

Group:          Development/Libraries
License:        ASL 2.0
URL:            https://docs.sonatype.org/display/AETHER/Home
# it seems github has redirects plus it generates tarball on the fly
# to get tarball go to http://github.com/sonatype/sonatype-aether/tree/aether-1.7
# click "downloads" in upper right corner
# click "download .tar.gz"
Source0:        sonatype-%{full_name}-%{name}-%{version}-0-%{githash}.tar.gz

BuildArch:      noarch

BuildRequires:  maven2
BuildRequires:  maven-compiler-plugin
BuildRequires:  maven-install-plugin
BuildRequires:  maven-jar-plugin
BuildRequires:  maven-javadoc-plugin
BuildRequires:  maven-resources-plugin
BuildRequires:  maven-site-plugin
BuildRequires:  maven-surefire-plugin
BuildRequires:  maven-surefire-provider-junit4
BuildRequires:  plexus-containers-component-metadata >= 1.5.4-4
BuildRequires:  animal-sniffer >= 1.6-5
BuildRequires:  mojo-parent


Requires:       maven2
Requires:       java >= 1:1.6.0
Requires(post): jpackage-utils
Requires(postun): jpackage-utils


%description
Aether is standalone library to resolve, install and deploy artifacts
the Maven way developed by Sonatype

%package javadoc
Summary:   API documentation for %{name}
Group:     Documentation
Requires:  jpackage-utils

%description javadoc
%{summary}.

%prep
# last part will have to change every time
%setup -q -n sonatype-%{full_name}-074c2fb


%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL

mvn-jpp -e \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        install javadoc:aggregate


%install
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/%{name}
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}

for module in aether-api aether-connector-file aether-connector-wagon \
         aether-impl aether-spi aether-test-util aether-util;do
pushd $module
      jarname=`echo $module | sed s:aether-::`
      install -m 644 target/$module-*.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/$jarname.jar

      install -pm 644 pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP.%{name}-$jarname.pom
      %add_to_maven_depmap org.sonatype.aether $module %{version} JPP/%{name} $jarname
popd
done

install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

install -pm 644 pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP.%{name}-parent.pom
%add_to_maven_depmap  org.sonatype.aether %{name}-parent %{version} JPP/%{name} parent


%post
%update_maven_depmap

%postun
%update_maven_depmap


%files
%defattr(-,root,root,-)
%doc README.md
%{_javadir}/%{name}
%{_mavendepmapfragdir}/%{name}
%{_mavenpomdir}/*.pom

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}



%changelog
* Wed Dec  8 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.7-3
- Make jars/javadocs versionless
- Remove buildroot and clean section

* Wed Oct 13 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.7-2
- Explained how to get tarball properly
- Removed noreplace on depmap fragment

* Mon Oct 11 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.7-1
- Initial Package
