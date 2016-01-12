%global short_name guice
%global pkg_name google-%{short_name}
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

%if 0%{?fedora}
%bcond_without extensions
%endif

Name:           %{?scl_prefix}%{pkg_name}
Version:        4.0
Release:        2.1%{?dist}
Summary:        Lightweight dependency injection framework for Java 5 and above
License:        ASL 2.0
URL:            https://github.com/google/%{short_name}
BuildArch:      noarch

# ./create-tarball.sh %%{version}
Source0:        %{pkg_name}-%{version}.tar.xz
Source1:        create-tarball.sh

Patch0:         0001-Revert-Some-work-on-issue-910-ensure-that-anonymous-.patch

# Rejected upstream: https://github.com/google/guice/issues/492
Patch100:       https://raw.githubusercontent.com/sonatype/sisu-guice/master/PATCHES/GUICE_492_slf4j_logger_injection.patch
# Forwarded upstream: https://github.com/google/guice/issues/618
Patch101:       https://raw.githubusercontent.com/sonatype/sisu-guice/master/PATCHES/GUICE_618_extensible_filter_pipeline.patch

BuildRequires:  %{?scl_prefix_java_common}maven-local >= 3.2.4-2
BuildRequires:  %{?scl_prefix}maven-remote-resources-plugin
BuildRequires:  %{?scl_prefix}munge-maven-plugin
BuildRequires:  %{?scl_prefix}maven-gpg-plugin
BuildRequires:  %{?scl_prefix}apache-resource-bundles
BuildRequires:  %{?scl_prefix}aopalliance
BuildRequires:  %{?scl_prefix_java_common}atinject
BuildRequires:  %{?scl_prefix_java_common}cglib
BuildRequires:  %{?scl_prefix_java_common}guava
BuildRequires:  %{?scl_prefix_java_common}slf4j

%if %{with extensions}
BuildRequires:  %{?scl_prefix}hibernate-jpa-2.0-api
BuildRequires:  %{?scl_prefix}springframework-beans
%endif

# Test dependencies:
%if 0
BuildRequires:  %{?scl_prefix}maven-surefire-provider-testng
BuildRequires:  %{?scl_prefix}aqute-bnd
BuildRequires:  %{?scl_prefix_java_common}atinject-tck
BuildRequires:  %{?scl_prefix_java_common}easymock2
BuildRequires:  %{?scl_prefix_java_common}felix-framework
BuildRequires:  %{?scl_prefix}hibernate3-entitymanager
BuildRequires:  %{?scl_prefix}mvn(org.hsqldb:hsqldb-j5)
BuildRequires:  %{?scl_prefix}testng
%endif

%description
Put simply, Guice alleviates the need for factories and the use of new
in your Java code. Think of Guice's @Inject as the new new. You will
still need to write factories in some cases, but your code will not
depend directly on them. Your code will be easier to change, unit test
and reuse in other contexts.

Guice embraces Java's type safe nature, especially when it comes to
features introduced in Java 5 such as generics and annotations. You
might think of Guice as filling in missing features for core
Java. Ideally, the language itself would provide most of the same
features, but until such a language comes along, we have Guice.

Guice helps you design better APIs, and the Guice API itself sets a
good example. Guice is not a kitchen sink. We justify each feature
with at least three use cases. When in doubt, we leave it out. We
build general functionality which enables you to extend Guice rather
than adding every feature to the core framework.

%package -n %{short_name}-parent
Summary:        Guice parent POM

%description -n %{short_name}-parent
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides parent POM for Guice modules.

%package -n %{short_name}-servlet
Summary:        Servlet extension module for Guice

%description -n %{short_name}-servlet
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides Servlet module for Guice.

%if %{with extensions}

%package -n %{short_name}-assistedinject
Summary:        AssistedInject extension module for Guice

%description -n %{short_name}-assistedinject
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides AssistedInject module for Guice.

%package -n %{short_name}-extensions
Summary:        Extensions for Guice

%description -n %{short_name}-extensions
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides extensions POM for Guice.

%package -n %{short_name}-grapher
Summary:        Grapher extension module for Guice

%description -n %{short_name}-grapher
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides Grapher module for Guice.

%package -n %{short_name}-jmx
Summary:        JMX extension module for Guice

%description -n %{short_name}-jmx
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides JMX module for Guice.

%package -n %{short_name}-jndi
Summary:        JNDI extension module for Guice

%description -n %{short_name}-jndi
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides JNDI module for Guice.

%package -n %{short_name}-multibindings
Summary:        MultiBindings extension module for Guice

%description -n %{short_name}-multibindings
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides MultiBindings module for Guice.

%package -n %{short_name}-persist
Summary:        Persist extension module for Guice

%description -n %{short_name}-persist
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides Persist module for Guice.

%package -n %{short_name}-spring
Summary:        Spring extension module for Guice

%description -n %{short_name}-spring
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides Spring module for Guice.

%package -n %{short_name}-testlib
Summary:        TestLib extension module for Guice

%description -n %{short_name}-testlib
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides TestLib module for Guice.

%package -n %{short_name}-throwingproviders
Summary:        ThrowingProviders extension module for Guice

%description -n %{short_name}-throwingproviders
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides ThrowingProviders module for Guice.

%endif # with extensions

%package -n %{short_name}-bom
Summary:        Bill of Materials for Guice

%description -n %{short_name}-bom
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides Bill of Materials module for Guice.

%package javadoc
Summary:        API documentation for Guice

%description javadoc
This package provides %{summary}.


%prep
%setup -q -n %{pkg_name}-%{version}
%patch0 -p1
%patch100 -p1
%patch101 -p1
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x

# We don't have struts2 in Fedora yet.
%pom_disable_module struts2 extensions
# Android-specific extension
%pom_disable_module dagger-adapter extensions

# Remove additional build profiles, which we don't use anyways
# and which are only pulling additional dependencies.
%pom_xpath_remove "pom:profile[pom:id='guice.with.jarjar']" core

# Animal sniffer is only causing problems. Disable it for now.
%pom_remove_plugin :animal-sniffer-maven-plugin core
%pom_remove_plugin :animal-sniffer-maven-plugin extensions

# We don't have the custom doclet used by upstream. Remove
# maven-javadoc-plugin to generate javadocs with default style.
%pom_remove_plugin :maven-javadoc-plugin

# remove test dependency to make sure we don't produce requires
# see #1007498
%pom_remove_dep :guava-testlib extensions
%pom_xpath_remove "pom:dependency[pom:classifier[text()='tests']]" extensions

%pom_remove_parent
%pom_set_parent com.google.inject:guice-parent:%{version} jdk8-tests

# Don't try to build extension modules unless they are needed
%if %{without extensions}
sed -i '/<module>/s|extensions|&/servlet|' pom.xml
%endif

%mvn_package :jdk8-tests __noinstall
%{?scl:EOF}

%build
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%mvn_alias "com.google.inject.extensions:" "org.sonatype.sisu.inject:"

%mvn_package :::no_aop: guice

%mvn_file  ":guice-{*}"  %{short_name}/guice-@1
%mvn_file  ":guice" %{short_name}/%{pkg_name} %{pkg_name}
%mvn_alias ":guice" "org.sonatype.sisu:sisu-guice"
# Skip tests because of missing dependency guice-testlib
%mvn_build -f -s
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%mvn_install
%{?scl:EOF}

%files -f .mfiles-guice
%dir %{_javadir}/%{short_name}

%files -n %{short_name}-parent -f .mfiles-guice-parent
%doc COPYING

%files -n %{short_name}-servlet -f .mfiles-guice-servlet

%if %{with extensions}
%files -n %{short_name}-assistedinject -f .mfiles-guice-assistedinject
%files -n %{short_name}-extensions -f .mfiles-extensions-parent
%files -n %{short_name}-grapher -f .mfiles-guice-grapher
%files -n %{short_name}-jmx -f .mfiles-guice-jmx
%files -n %{short_name}-jndi -f .mfiles-guice-jndi
%files -n %{short_name}-multibindings -f .mfiles-guice-multibindings
%files -n %{short_name}-persist -f .mfiles-guice-persist
%files -n %{short_name}-spring -f .mfiles-guice-spring
%files -n %{short_name}-testlib -f .mfiles-guice-testlib
%files -n %{short_name}-throwingproviders -f .mfiles-guice-throwingproviders
%endif # with extensions

%files -n %{short_name}-bom -f .mfiles-guice-bom

%files javadoc -f .mfiles-javadoc
%doc COPYING


%changelog
* Tue Jan 12 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.0-2.1
- SCL-ize package
- Unconditionally enable servlet extension

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 14 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.0-1
- Update to upstream version 4.0

* Mon Apr 27 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.6-1
- Update to upstream version 3.2.6

* Fri Mar 6 2015 Alexander Kurtakov <akurtako@redhat.com> 3.2.5-2
- Drop gone tomcat-servlet-3.0-api BR, builds fine without it.

* Fri Jan 23 2015 Michael Simacek <msimacek@redhat.com> - 3.2.5-1
- Update to upstream version 3.2.5

* Mon Sep 29 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.4-1
- Update to upstream version 3.2.4

* Fri Jun  6 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.2-1
- Update to upstream version 3.2.2

* Wed May 28 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.1-2
- Rebuild to regenerate Maven auto-requires

* Wed Apr 16 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.1-1
- Update to upstream version 3.2.1
- Add testlib subpackage

* Tue Mar  4 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.10-3
- Fix directory ownership

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.1.10-3
- Use Requires: java-headless rebuild (#1067528)

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.10-2
- Fix unowned directory

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.10-1
- Update to upstream version 3.1.10

* Mon Jan 20 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.9-1
- Update to upstream version 3.1.9

* Mon Nov 11 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.8-1
- Update to upstream version 3.1.8

* Wed Oct 23 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.3-10
- Rebuild to regenerate broken POMs
- Related: rhbz#1021484

* Fri Oct 18 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.3-9
- Don't force generation of pom.properties

* Wed Sep 25 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.3-8
- Install no_aop artifact after javapackages update

* Thu Sep 12 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.1.3-7
- Remove dependency on tests from runtime
- Related: rhbz#1007498

* Tue Sep 10 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.3-6
- Install no_aop artifact
- Resolves: rhbz#1006491

* Wed Sep  4 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.3-5
- Enable pom.properties
- Resolves: rhbz#1004360

* Wed Aug 07 2013 Michal Srb <msrb@redhat.com> - 3.1.3-4
- Add create-tarball.sh script to SRPM

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Apr 24 2013 Michal Srb <msrb@redhat.com> - 3.1.3-2
- Revert update to 3.1.4 (uses asm4)

* Thu Mar 14 2013 Michal Srb <msrb@redhat.com> - 3.1.3-1
- Update to upstream version 3.1.3
- Remove bundled JARs from tarball

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 3.1.2-11
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Jan 31 2013 Michal Srb <msrb@redhat.com> - 3.1.2-10
- Remove all requires
- Correct usage of xmvn's macros

* Mon Jan 28 2013 Michal Srb <msrb@redhat.com> - 3.1.2-9
- Build with xmvn

* Fri Nov 16 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.2-8
- Remove README

* Fri Nov 16 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.2-7
- Repackage tarball

* Fri Nov  9 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.2-6
- Don't try to build extension modules unless they are needed

* Fri Nov  9 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.2-5
- Conditionalize %%install section too

* Fri Nov  9 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.2-4
- Conditionally disable extensions

* Thu Nov  1 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.2-3
- Update to new add_maven_depmap macro

* Wed Oct 31 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.1.2-2
- Use new generated maven filelist feature from javapackages-tools

* Fri Oct  5 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.2-1
- Complete rewrite of the spec file
- New upstream, to ease future maintenance
- Build with maven instead of ant
- Split into multiple subpackages

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-0.7.rc2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb  9 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0-0.6.rc2
- Temporary fix for maven buildroots

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-0.5.rc2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 12 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0-0.4.rc2
- Build with aqute-bnd (#745176)
- Use new maven macros
- Few packaging tweaks

* Tue May 24 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0-0.3.rc2
- Add cglib and atinject to R

* Thu May 12 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0-0.2.rc2
- Remove test and missing deps from pom.xml

* Tue Mar  1 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.0-0.1.rc2
- Update to 3.0rc2
- Changes according to new guidelines (versionless jars & javadocs)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-4.1219svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Oct 14 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.0-3.1219svn
- Add java-devel >= 1:1.6.0 to BR

* Wed Oct 13 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.0-2.1219svn
- Moved munge repacking to prep
- Added -Dversion to change generated manifest version
- Removed http part of URL

* Thu Oct  7 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.0-1.1219svn
- Initial version of the package
