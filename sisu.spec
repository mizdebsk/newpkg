Name:           sisu
Version:        2.2.3
Release:        2%{?dist}
Summary:        Sonatype dependency injection framework


Group:          Development/Tools
License:        ASL 2.0 and EPL
URL:            http://github.com/sonatype/sisu

# git clone git://github.com/sonatype/sisu
# git archive --prefix="sisu-2.2.3/" --format=tar sisu-2.1.1 | xz > sisu-2.2.3.tar.xz
Source0:        %{name}-%{version}.tar.xz
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
BuildRequires:  forge-parent
BuildRequires:  maven-surefire-provider-testng
BuildRequires:  maven-surefire-provider-junit4


Requires:       forge-parent
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

# add backward compatible location
cp sisu-inject/containers/guice-plexus/guice-plexus-lifecycles/src/main/java/org/sonatype/guice/plexus/lifecycles/*java \
   sisu-inject/containers/guice-plexus/guice-plexus-lifecycles/src/main/java/org/codehaus/plexus/
sed -i 's/org.sonatype.guice.plexus.lifecycles/org.codehaus.plexus/' \
       sisu-inject/containers/guice-plexus/guice-plexus-lifecycles/src/main/java/org/codehaus/plexus/*java

# TODO enable guice-eclipse
sed -i 's:.*guice-eclipse.*::g' sisu-inject/pom.xml
rm -rf sisu-inject/guice-eclipse
sed -i 's:.*sisu-eclipse-registry.*::g' sisu-inject/registries/pom.xml
rm -rf sisu-inject/registries/sisu-eclipse-registry

%build
mvn-rpmbuild -X \
  -Dmaven.local.depmap.file=%{SOURCE1} \
  -Dmaven.test.skip=true \
  install javadoc:aggregate

%install
install -d -m 0755 $RPM_BUILD_ROOT%{_javadir}/%{name}
install -d -m 0755 $RPM_BUILD_ROOT%{_mavenpomdir}

pushd sisu-inject
# main pom
install -pm 644 pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP.%{name}-inject.pom
%add_maven_depmap JPP.%{name}-inject.pom


pushd containers
# main poms
install -pm 644 pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP.%{name}-containers.pom
%add_maven_depmap JPP.%{name}-containers.pom

for submod in guice-*;do
    pushd $submod
    for module in guice-*;do
        install -pm 644 $module/target/$module-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/$module.jar
        install -pm 644 $module/pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP.%{name}-$module.pom
        %add_maven_depmap JPP.%{name}-$module.pom %{name}/$module.jar
    done
    # $dir is sisu-inject/XX so we strip the first part
    install -pm 644 pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP.%{name}-$submod.pom
    %add_maven_depmap JPP.%{name}-$submod.pom
    popd
done

pushd guice-bean
module="sisu-inject-bean"
install -pm 644 $module/target/$module-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/$module.jar
install -pm 644 $module/pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP.%{name}-$module.pom
%add_maven_depmap JPP.%{name}-$module.pom %{name}/$module.jar
popd # guice-bean

pushd guice-plexus
module="sisu-inject-plexus"
install -pm 644 $module/target/$module-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/$module.jar
install -pm 644 $module/pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP.%{name}-$module.pom
%add_maven_depmap JPP.%{name}-$module.pom %{name}/$module.jar
popd # guice-plexus

popd # containers

pushd registries
# main poms
install -pm 644 pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP.%{name}-registries.pom
%add_maven_depmap JPP.%{name}-containers.pom

for module in *registry*;do
    install -pm 644 $module/target/$module-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/$module.jar
    install -pm 644 $module/pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP.%{name}-$module.pom
    %add_maven_depmap JPP.%{name}-$module.pom %{name}/$module.jar
done
popd # registries

popd # sisu-inject


install -pm 644 pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP.%{name}-parent.pom
%add_maven_depmap JPP.%{name}-parent.pom

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
%doc LICENSE-ASL.txt LICENSE-EPL.txt
%{_javadir}/%{name}
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*


%files javadoc
%doc LICENSE-ASL.txt LICENSE-EPL.txt
%doc %{_javadocdir}/%{name}


%changelog
* Fri Aug 19 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.3-2
- Add backward compatible package path for lifecycles
- Remove temporary BRs/Rs

* Thu Jun 23 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.3-1
- Update to latest upstream 2.2.3 (#683795)
- Add forge-parent to Requires
- Rework spec to be more simple, update patches

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


