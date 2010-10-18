%global githash gae9a407

Name:           sisu
Version:        1.4.2
Release:        2%{?dist}
Summary:        Sonatype dependency injection framework


Group:          Development/Tools
License:        ASL 2.0
URL:            http://github.com/sonatype/sisu

# it seems github has redirects plus it generates tarball on the fly
# to get tarball go to http://github.com/sonatype/sisu/tree/sisu-1.4.2
# click "downloads" in upper right corner
# click "download .tar.gz"
Source0:        sonatype-sisu-sisu-%{version}-0-%{githash}.tar.gz
Source1:        %{name}-depmap.xml
Patch0:         0001-Fix-shading.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  google-guice
BuildRequires:  maven2
BuildRequires:  maven-install-plugin
BuildRequires:  maven-enforcer-plugin
BuildRequires:  maven-invoker-plugin
BuildRequires:  maven-site-plugin
BuildRequires:  maven-plugin-bundle
BuildRequires:  maven-shade-plugin
BuildRequires:  maven-dependency-plugin
BuildRequires:  maven-clean-plugin
BuildRequires:  maven-resources-plugin
BuildRequires:  maven-surefire-plugin
BuildRequires:  maven-javadoc-plugin
BuildRequires:  maven-jar-plugin
BuildRequires:  maven-compiler-plugin
BuildRequires:  atinject
BuildRequires:  felix-framework

Requires:       google-guice
Requires:       java >= 1:1.6.0
Requires(post): jpackage-utils
Requires(postun): jpackage-utils

%description
Java dependency injection framework with backward support for plexus and bean
style dependency injection.

%package        javadoc
Summary:        API documentation for %{name}
Group:          Documentation
Requires:       jpackage-utils

%description    javadoc
%{summary}.

%prep
%setup -q -n sonatype-sisu-18a9c2c
%patch0 -p1

%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL
mvn-jpp \
  -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
  -Dmaven2.jpp.depmap.file=%{SOURCE1} \
  -Dmaven.test.skip=true \
  install javadoc:aggregate

%install
rm -rf $RPM_BUILD_ROOT
install -d -m 0755 $RPM_BUILD_ROOT%{_javadir}/%{name}
install -d -m 0755 $RPM_BUILD_ROOT%{_mavenpomdir}

for dir1 in sisu-inject/guice-*;do
    pushd $dir1
    for module in guice-*;do
        install -pm 644 $module/target/$module-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/$module-%{version}.jar
        install -pm 644 $module/pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP.%{name}-$module.pom
        %add_to_maven_depmap  org.sonatype.sisu.inject $module %{version} JPP/%{name} $module
    done
    popd
    # $dir is sisu-inject/XX so we strip the first part
    submod=`echo $dir1 | sed -s 's:.*/::'`
    install -pm 644 sisu-inject/$submod/pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP.%{name}-$submod.pom
    %add_to_maven_depmap  org.sonatype.sisu.inject $submod %{version} JPP/%{name} $submod
done

pushd sisu-inject/guice-bean
module="sisu-inject-bean"
install -pm 644 $module/target/$module-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/$module-%{version}.jar
install -pm 644 $module/pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP.%{name}-$module.pom
%add_to_maven_depmap org.sonatype.sisu $module %{version} JPP/%{name} $module
popd

pushd sisu-inject/guice-plexus
module="sisu-inject-plexus"
install -pm 644 $module/target/$module-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/$module-%{version}.jar
install -pm 644 $module/pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP.%{name}-$module.pom
%add_to_maven_depmap org.sonatype.sisu $module %{version} JPP/%{name} $module
popd

# symlinks
(cd $RPM_BUILD_ROOT%{_javadir}/%{name} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)


# main poms
install -pm 644 sisu-inject/pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP.%{name}-inject.pom
%add_to_maven_depmap  org.sonatype.sisu sisu-inject %{version} JPP/%{name} inject

install -pm 644 pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP.%{name}-parent.pom
%add_to_maven_depmap  org.sonatype.sisu sisu-parent %{version} JPP/%{name} parent

# javadoc
install -d -m 0755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}


%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_maven_depmap

%postun
%update_maven_depmap


%files
%defattr(-,root,root,-)
%{_javadir}/%{name}
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*


%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}*



%changelog
* Mon Oct 18 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.4.2-2
- Add felix-framework BR

* Thu Oct 14 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.4.2-1
- Initial version of the package


