%global short_name guice
%global tag     bd0d620

Name:           google-%{short_name}
Version:        3.1.2
Release:        2%{?dist}
Summary:        Lightweight dependency injection framework for Java 5 and above
Group:          Development/Libraries
License:        ASL 2.0
URL:            https://github.com/sonatype/sisu-%{short_name}
Source:         https://github.com/sonatype/sisu-%{short_name}/tarball/sisu-%{short_name}-%{version}#/%{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  java-devel
BuildRequires:  jpackage-utils
BuildRequires:  javapackages-tools >= 0.7.0
BuildRequires:  maven
BuildRequires:  maven-remote-resources-plugin
BuildRequires:  apache-resource-bundles
BuildRequires:  aopalliance
BuildRequires:  atinject
BuildRequires:  cglib
BuildRequires:  guava
BuildRequires:  hibernate-jpa-2.0-api
BuildRequires:  slf4j
BuildRequires:  springframework-beans
BuildRequires:  tomcat-servlet-3.0-api
# Test dependencies:
%if 0
BuildRequires:  maven-surefire-provider-testng
BuildRequires:  aqute-bnd
BuildRequires:  atinject-tck
BuildRequires:  easymock2
BuildRequires:  felix-framework
BuildRequires:  hibernate3-entitymanager
BuildRequires:  mvn(org.hsqldb:hsqldb-j5)
BuildRequires:  testng
%endif

Requires:       java
Requires:       jpackage-utils
Requires:       aopalliance
Requires:       atinject
Requires:       cglib
Requires:       guava
Requires:       slf4j
Requires:       %{short_name}-parent = %{version}-%{release}
Provides:       %{short_name} = %{version}-%{release}

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

%package -n %{short_name}-assistedinject
Summary:        AssistedInject extension module for Guice
Requires:       java
Requires:       jpackage-utils
Requires:       %{short_name} = %{version}-%{release}

%description -n %{short_name}-assistedinject
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides AssistedInject module for Guice.

%package -n %{short_name}-extensions
Summary:        Extensions for Guice
Requires:       jpackage-utils
Requires:       %{short_name} = %{version}-%{release}

%description -n %{short_name}-extensions
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides extensions POM for Guice.

%package -n %{short_name}-grapher
Summary:        Grapher extension module for Guice
Requires:       java
Requires:       jpackage-utils
Requires:       %{short_name} = %{version}-%{release}
Requires:       %{short_name}-assistedinject = %{version}-%{release}
Requires:       %{short_name}-multibindings = %{version}-%{release}

%description -n %{short_name}-grapher
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides Grapher module for Guice.

%package -n %{short_name}-jmx
Summary:        JMX extension module for Guice
Requires:       java
Requires:       jpackage-utils
Requires:       %{short_name} = %{version}-%{release}

%description -n %{short_name}-jmx
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides JMX module for Guice.

%package -n %{short_name}-jndi
Summary:        JNDI extension module for Guice
Requires:       java
Requires:       jpackage-utils
Requires:       %{short_name} = %{version}-%{release}

%description -n %{short_name}-jndi
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides JNDI module for Guice.

%package -n %{short_name}-multibindings
Summary:        MultiBindings extension module for Guice
Requires:       java
Requires:       jpackage-utils
Requires:       %{short_name} = %{version}-%{release}

%description -n %{short_name}-multibindings
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides MultiBindings module for Guice.

%package -n %{short_name}-parent
Summary:        Guice parent POM
Requires:       jpackage-utils

%description -n %{short_name}-parent
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides parent POM for Guice modules.

%package -n %{short_name}-persist
Summary:        Persist extension module for Guice
Requires:       java
Requires:       jpackage-utils
Requires:       hibernate-jpa-2.0-api
Requires:       tomcat-servlet-3.0-api
Requires:       %{short_name} = %{version}-%{release}

%description -n %{short_name}-persist
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides Persist module for Guice.

%package -n %{short_name}-servlet
Summary:        Servlet extension module for Guice
Requires:       java
Requires:       jpackage-utils
Requires:       tomcat-servlet-3.0-api
Requires:       %{short_name} = %{version}-%{release}

%description -n %{short_name}-servlet
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides Servlet module for Guice.

%package -n %{short_name}-spring
Summary:        Spring extension module for Guice
Requires:       java
Requires:       jpackage-utils
Requires:       springframework-beans
Requires:       %{short_name} = %{version}-%{release}

%description -n %{short_name}-spring
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides Spring module for Guice.

%package -n %{short_name}-throwingproviders
Summary:        ThrowingProviders extension module for Guice
Requires:       java
Requires:       jpackage-utils
Requires:       %{short_name} = %{version}-%{release}

%description -n %{short_name}-throwingproviders
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides ThrowingProviders module for Guice.

%package javadoc
Summary:        API documentation for Guice
Group:          Documentation
Requires:       jpackage-utils
Provides:       %{short_name}-javadoc = %{version}-%{release}

%description javadoc
This package provides %{summary}.


%prep
%setup -q -n sonatype-sisu-%{short_name}-%{tag}
find -name '*.jar' -delete

# We don't have struts2 in Fedora yet.
%pom_disable_module struts2 extensions

# Remove additional build profiles, which we don't use anyways
# and which are only pulling additional dependencies.
%pom_xpath_remove pom:project/pom:profiles core

# Animal sniffer is only causing problems. Disable it for now.
%pom_remove_plugin :animal-sniffer-maven-plugin core
%pom_remove_plugin :animal-sniffer-maven-plugin extensions

# We don't have the custom doclet used by upstream. Remove
# maven-javadoc-plugin to generate javadocs with default style.
%pom_remove_plugin :maven-javadoc-plugin

%build
# Skip tests because of missing dependency (hsqldb-j5).
mvn-rpmbuild -e -Dmaven.test.skip=true verify javadoc:aggregate

%install
# directories
install -d -m 755 %{buildroot}%{_javadir}/%{short_name}
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
# JARs
install -p -m 644 extensions/assistedinject/target/%{short_name}-assistedinject-%{version}.jar %{buildroot}%{_javadir}/%{short_name}/%{short_name}-assistedinject.jar
install -p -m 644 extensions/grapher/target/%{short_name}-grapher-%{version}.jar %{buildroot}%{_javadir}/%{short_name}/%{short_name}-grapher.jar
install -p -m 644 extensions/jmx/target/%{short_name}-jmx-%{version}.jar %{buildroot}%{_javadir}/%{short_name}/%{short_name}-jmx.jar
install -p -m 644 extensions/jndi/target/%{short_name}-jndi-%{version}.jar %{buildroot}%{_javadir}/%{short_name}/%{short_name}-jndi.jar
install -p -m 644 extensions/multibindings/target/%{short_name}-multibindings-%{version}.jar %{buildroot}%{_javadir}/%{short_name}/%{short_name}-multibindings.jar
install -p -m 644 extensions/persist/target/%{short_name}-persist-%{version}.jar %{buildroot}%{_javadir}/%{short_name}/%{short_name}-persist.jar
install -p -m 644 extensions/servlet/target/%{short_name}-servlet-%{version}.jar %{buildroot}%{_javadir}/%{short_name}/%{short_name}-servlet.jar
install -p -m 644 extensions/spring/target/%{short_name}-spring-%{version}.jar %{buildroot}%{_javadir}/%{short_name}/%{short_name}-spring.jar
install -p -m 644 extensions/throwingproviders/target/%{short_name}-throwingproviders-%{version}.jar %{buildroot}%{_javadir}/%{short_name}/%{short_name}-throwingproviders.jar
install -p -m 644 core/target/sisu-%{short_name}-%{version}.jar %{buildroot}%{_javadir}/%{short_name}/%{name}.jar
# POMs
install -p -m 644 extensions/assistedinject/pom.xml %{buildroot}%{_mavenpomdir}/JPP.%{short_name}-%{short_name}-assistedinject.pom
install -p -m 644 extensions/pom.xml %{buildroot}%{_mavenpomdir}/JPP.%{short_name}-%{short_name}-extensions.pom
install -p -m 644 extensions/grapher/pom.xml %{buildroot}%{_mavenpomdir}/JPP.%{short_name}-%{short_name}-grapher.pom
install -p -m 644 extensions/jmx/pom.xml %{buildroot}%{_mavenpomdir}/JPP.%{short_name}-%{short_name}-jmx.pom
install -p -m 644 extensions/jndi/pom.xml %{buildroot}%{_mavenpomdir}/JPP.%{short_name}-%{short_name}-jndi.pom
install -p -m 644 extensions/multibindings/pom.xml %{buildroot}%{_mavenpomdir}/JPP.%{short_name}-%{short_name}-multibindings.pom
install -p -m 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP.%{short_name}-%{short_name}-parent.pom
install -p -m 644 extensions/persist/pom.xml %{buildroot}%{_mavenpomdir}/JPP.%{short_name}-%{short_name}-persist.pom
install -p -m 644 extensions/servlet/pom.xml %{buildroot}%{_mavenpomdir}/JPP.%{short_name}-%{short_name}-servlet.pom
install -p -m 644 extensions/spring/pom.xml %{buildroot}%{_mavenpomdir}/JPP.%{short_name}-%{short_name}-spring.pom
install -p -m 644 extensions/throwingproviders/pom.xml %{buildroot}%{_mavenpomdir}/JPP.%{short_name}-%{short_name}-throwingproviders.pom
install -p -m 644 core/pom.xml %{buildroot}%{_mavenpomdir}/JPP.%{short_name}-%{name}.pom
# depmaps
%add_maven_depmap JPP.%{short_name}-%{short_name}-assistedinject.pom %{short_name}/%{short_name}-assistedinject.jar -f assistedinject -a com.google.inject.extensions:guice-assistedinject
%add_maven_depmap JPP.%{short_name}-%{short_name}-extensions.pom -f extensions
%add_maven_depmap JPP.%{short_name}-%{short_name}-grapher.pom %{short_name}/%{short_name}-grapher.jar -f grapher -a com.google.inject.extensions:guice-grapher
%add_maven_depmap JPP.%{short_name}-%{short_name}-jmx.pom %{short_name}/%{short_name}-jmx.jar -f jmx -a com.google.inject.extensions:guice-jmx
%add_maven_depmap JPP.%{short_name}-%{short_name}-jndi.pom %{short_name}/%{short_name}-jndi.jar -f jndi -a com.google.inject.extensions:guice-jndi
%add_maven_depmap JPP.%{short_name}-%{short_name}-multibindings.pom %{short_name}/%{short_name}-multibindings.jar -f multibindings -a com.google.inject.extensions:guice-multibindings
%add_maven_depmap JPP.%{short_name}-%{short_name}-parent.pom -f parent
%add_maven_depmap JPP.%{short_name}-%{short_name}-persist.pom %{short_name}/%{short_name}-persist.jar -f persist -a com.google.inject.extensions:guice-persist
%add_maven_depmap JPP.%{short_name}-%{short_name}-servlet.pom %{short_name}/%{short_name}-servlet.jar -f servlet -a com.google.inject.extensions:guice-servlet
%add_maven_depmap JPP.%{short_name}-%{short_name}-spring.pom %{short_name}/%{short_name}-spring.jar -f spring -a com.google.inject.extensions:guice-spring
%add_maven_depmap JPP.%{short_name}-%{short_name}-throwingproviders.pom %{short_name}/%{short_name}-throwingproviders.jar -f throwingproviders -a com.google.inject.extensions:guice-throwingproviders
%add_maven_depmap JPP.%{short_name}-%{name}.pom %{short_name}/%{name}.jar -a com.google.inject:guice
# javadoc
cp -pr target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}
# compat symlink
ln -sf %{short_name}/%{name}.jar %{buildroot}%{_javadir}


%files -f maven-files-%{name}
%doc README
%{_javadir}/%{name}.jar

%files -n %{short_name}-assistedinject -f maven-files-%{name}-assistedinject

%files -n %{short_name}-extensions -f maven-files-%{name}-extensions

%files -n %{short_name}-grapher -f maven-files-%{name}-grapher

%files -n %{short_name}-jmx -f maven-files-%{name}-jmx

%files -n %{short_name}-jndi -f maven-files-%{name}-jndi

%files -n %{short_name}-multibindings -f maven-files-%{name}-multibindings

%files -n %{short_name}-parent -f maven-files-%{name}-parent
%doc COPYING

%files -n %{short_name}-persist -f maven-files-%{name}-persist

%files -n %{short_name}-servlet -f maven-files-%{name}-servlet

%files -n %{short_name}-spring -f maven-files-%{name}-spring

%files -n %{short_name}-throwingproviders -f maven-files-%{name}-throwingproviders

%files javadoc
%doc COPYING
%{_javadocdir}/%{name}


%changelog
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
