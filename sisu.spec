Name:           sisu
Version:        2.1.1
Release:        2%{?dist}
Summary:        Sonatype dependency injection framework


Group:          Development/Tools
License:        ASL 2.0
URL:            http://github.com/sonatype/sisu

# git clone git://github.com/sonatype/sisu
# git archive --prefix="sisu-2.1.1/" --format=tar sisu-2.1.1 | bzip2 > sisu-2.1.1.tar.bz2
Source0:        %{name}-%{version}.tar.bz2
Source1:        %{name}-depmap.xml
Patch0:         0001-Remove-test-deps.patch
Patch1:         0002-Fix-plexus-bundling.patch


BuildArch:      noarch

BuildRequires:  google-guice
BuildRequires:  maven
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
%setup -q
%patch0 -p1
%patch1 -p1


# TODO enable guice-eclipse
sed -i 's:.*guice-eclipse.*::g' sisu-inject/pom.xml
rm -rf sisu-inject/guice-eclipse

%build
mvn-rpmbuild \
  -Dmaven.local.depmap.file=%{SOURCE1} \
  -Dmaven.test.skip=true \
  install javadoc:aggregate

%install
install -d -m 0755 $RPM_BUILD_ROOT%{_javadir}/%{name}
install -d -m 0755 $RPM_BUILD_ROOT%{_mavenpomdir}

for dir1 in sisu-inject/guice-*;do
    pushd $dir1
    for module in guice-*;do
        install -pm 644 $module/target/$module-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/$module.jar
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
install -pm 644 $module/target/$module-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/$module.jar
install -pm 644 $module/pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP.%{name}-$module.pom
%add_to_maven_depmap org.sonatype.sisu $module %{version} JPP/%{name} $module
popd

pushd sisu-inject/guice-plexus
module="sisu-inject-plexus"
install -pm 644 $module/target/$module-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/$module.jar
install -pm 644 $module/pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP.%{name}-$module.pom
%add_to_maven_depmap org.sonatype.sisu $module %{version} JPP/%{name} $module
popd

# main poms
install -pm 644 sisu-inject/pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP.%{name}-inject.pom
%add_to_maven_depmap  org.sonatype.sisu sisu-inject %{version} JPP/%{name} inject

install -pm 644 pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP.%{name}-parent.pom
%add_to_maven_depmap  org.sonatype.sisu sisu-parent %{version} JPP/%{name} parent

# javadoc
install -d -m 0755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%pre javadoc
# workaround for rpm bug, can be removed in F-17
[ $1 -gt 1 ] && [ -L %{_javadocdir}/%{name} ] && \
rm -rf $(readlink -f %{_javadocdir}/%{name}) %{_javadocdir}/%{name} || :

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
* Tue Mar  1 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.1.1-2
- Add atinject into poms as dependency

* Mon Feb 28 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.1.1-1
- Update to 2.1.1
- Update patch
- Disable guice-eclipse for now

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.4.3.2-1
- Update to latest upstream version
- Versionless jars & javadocs

* Mon Oct 18 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.4.2-2
- Add felix-framework BR

* Thu Oct 14 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.4.2-1
- Initial version of the package


