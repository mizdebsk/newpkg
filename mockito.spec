%global pkg_name mockito
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

Name:           %{?scl_prefix}%{pkg_name}
Version:        1.10.19
Release:        7.1%{?dist}
Summary:        A Java mocking framework

License:        MIT
URL:            http://%{pkg_name}.org
Source0:        %{pkg_name}-%{version}.tar.xz
Source1:        make-%{pkg_name}-sourcetarball.sh
Patch0:         fixup-ant-script.patch
Patch1:         fix-bnd-config.patch
Patch2:         %{pkg_name}-matcher.patch
# Workaround for NPE in setting NamingPolicy in cglib
Patch3:         setting-naming-policy.patch
# because we have old objenesis
Patch4:         fix-incompatible-types.patch

BuildArch:      noarch
BuildRequires:  %{?scl_prefix_java_common}javapackages-local
BuildRequires:  %{?scl_prefix_java_common}ant
BuildRequires:  %{?scl_prefix_java_common}objenesis
BuildRequires:  %{?scl_prefix_java_common}cglib
BuildRequires:  %{?scl_prefix_java_common}junit
BuildRequires:  %{?scl_prefix_java_common}hamcrest
BuildRequires:  %{?scl_prefix}aqute-bnd

Requires:       %{?scl_prefix_java_common}objenesis
Requires:       %{?scl_prefix_java_common}cglib
Requires:       %{?scl_prefix_java_common}junit
Requires:       %{?scl_prefix_java_common}hamcrest

%description
Mockito is a mocking framework that tastes really good. It lets you write
beautiful tests with clean & simple API. Mockito doesn't give you hangover
because the tests are very readable and they produce clean verification
errors.

%package javadoc
Summary:        Javadocs for %{pkg_name}

%description javadoc
This package contains the API documentation for %{pkg_name}.

%prep
%setup -q -n %{pkg_name}-%{version}
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%patch0
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
# workaround rhbz#1292777 Files not found for javadoc generation
touch javadoc/stylesheet.css

%pom_add_dep net.sf.cglib:cglib maven/%{pkg_name}-core.pom
find . -name "*.java" -exec sed -i "s|org\.%{pkg_name}\.cglib|net\.sf\.cglib|g" {} +
mkdir -p lib/compile
%{?scl:EOF}

%build
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
build-jar-repository lib/compile objenesis cglib junit hamcrest/core
ant jar javadoc
# Convert to OSGi bundle
pushd target
%if 0%{?fedora} >= 23
bnd wrap \
 --version %{version} \
 --output %{pkg_name}-core-%{version}.bar \
 --properties ../conf/%{pkg_name}-core.bnd \
%else
java -jar $(build-classpath aqute-bnd) wrap \
 -output %{pkg_name}-core-%{version}.bar \
 -properties ../conf/%{pkg_name}-core.bnd \
%endif
 %{pkg_name}-core-%{version}.jar
mv %{pkg_name}-core-%{version}.bar %{pkg_name}-core-%{version}.jar
popd

sed -i -e "s|@version@|%{version}|g" maven/%{pkg_name}-core.pom
%mvn_artifact maven/%{pkg_name}-core.pom target/%{pkg_name}-core-%{version}.jar
%mvn_alias org.%{pkg_name}:%{pkg_name}-core org.%{pkg_name}:%{pkg_name}-all
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%mvn_install -J target/javadoc
%{?scl:EOF}

%files -f .mfiles
%doc LICENSE
%doc NOTICE

%files javadoc -f .mfiles-javadoc
%doc LICENSE
%doc NOTICE

%changelog
* Tue Jan 19 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10.19-7.1
- SCL-ize package

* Fri Dec 25 2015 Raphael Groner <projects.rg@smart.ms> - 1.10.19-7
- introduce License tag

* Fri Dec 25 2015 Raphael Groner <projects.rg@smart.ms> - 1.10.19-6
- reenable osgi

* Fri Dec 18 2015 Raphael Groner <projects.rg@smart.ms> - 1.10.19-5
- workaround rhbz#1292777 stylesheet.css not found

* Thu Jul 16 2015 Michael Simacek <msimacek@redhat.com> - 1.10.19-4
- Use aqute-bnd-2.4.1

* Mon Jun 22 2015 Mat Booth <mat.booth@redhat.com> - 1.10.19-3
- Switch to mvn_install

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 29 2015 Michal Srb <msrb@redhat.com> - 1.10.19-1
- Update to 1.10.19

* Mon Aug 25 2014 Darryl L. Pierce <dpierce@redhat.com> - 1.9.0-18
- First build for EPEL7
- Resolves: BZ#1110030

* Mon Jun 09 2014 Omair Majid <omajid@redhat.com> - 1.9.0-17
- Use .mfiles to pick up xmvn metadata
- Don't use obsolete _mavenpomdir and _mavendepmapfragdir macros
- Fix FTBFS

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 Severin Gehwolf <sgehwolf@redhat.com> - 1.9.0-16
- Use junit R/BR over junit4.

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 1.9.0-15
- Use Requires: java-headless rebuild (#1067528)

* Wed Dec 11 2013 Michael Simacek <msimacek@redhat.com> - 1.9.0-14
- Workaround for NPE in setting NamingPolicy

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 25 2013 Tomas Radej <tradej@redhat.com> - 1.9.0-12
- Patched LocalizedMatcher due to hamcrest update, (bug upstream)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Sep 6 2012 Severin Gehwolf <sgehwolf@redhat.com> 1.9.0-10
- More Import-Package fixes. Note that fix-cglib-refs.patch is
  not suitable for upstream: issue id=373

* Tue Sep 4 2012 Severin Gehwolf <sgehwolf@redhat.com> 1.9.0-9
- Fix missing Import-Package in manifest.

* Mon Aug 27 2012 Severin Gehwolf <sgehwolf@redhat.com> 1.9.0-8
- Add aqute bnd instructions for OSGi metadata

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 30 2012 Roman Kennke <rkennke@redhat.com> 1.9.0-6
- Place JavaDoc in directly under /usr/share/javadoc/%{pkg_name} instead
  of /usr/share/javadoc/%{pkg_name}/javadoc

* Wed Apr 25 2012 Roman Kennke <rkennke@redhat.com> 1.9.0-5
- Removed post/postun hook for update_maven_depmap

* Tue Apr 24 2012 Roman Kennke <rkennke@redhat.com> 1.9.0-4
- Fix groupId of cglib dependency
- Add additional depmap for mockito-all
- Update depmap on post and postun
- Fix version in pom

* Wed Feb 22 2012 Roman Kennke <rkennke@redhat.com> 1.9.0-3
- Added cglib dependency to pom

* Tue Feb 21 2012 Roman Kennke <rkennke@redhat.com> 1.9.0-2
- Include upstream Maven pom.xml in package
- Added missing Requires for cglib, junit4, hamcrest, objenesis
- Added source tarball generating script to sources

* Thu Feb 16 2012 Roman Kennke <rkennke@redhat.com> 1.9.0-1
- Initial package
