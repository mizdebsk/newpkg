Name:           mockito
Version:        1.9.0
Release:        11%{?dist}
Summary:        A Java mocking framework

License:        MIT
URL:            http://code.google.com/p/mockito/
Source0:        mockito-%{version}.tar.xz
Source1:        make-mockito-sourcetarball.sh
Patch0:         fixup-ant-script.patch
Patch1:         fix-cglib-refs.patch
Patch2:         maven-cglib-dependency.patch
Patch3:         fix-bnd-config.patch

BuildArch:      noarch
BuildRequires:  jpackage-utils
BuildRequires:  java-devel
BuildRequires:  ant
BuildRequires:  objenesis
BuildRequires:  cglib
BuildRequires:  junit4
BuildRequires:  hamcrest
BuildRequires:  aqute-bnd

Requires:       jpackage-utils
Requires:       java
Requires:       objenesis
Requires:       cglib
Requires:       junit4
Requires:       hamcrest

%description
Mockito is a mocking framework that tastes really good. It lets you write
beautiful tests with clean & simple API. Mockito doesn't give you hangover
because the tests are very readable and they produce clean verification
errors.

%package javadoc
Summary:        Javadocs for %{name}
Group:          Documentation
Requires:       jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
# Set Bundle-Version properly
sed -i 's/Bundle-Version= ${version}/Bundle-Version= %{version}/' conf/mockito-core.bnd
%patch3

%build
ant jar javadoc
# Convert to OSGi bundle
pushd target
java -jar $(build-classpath aqute-bnd) wrap -output mockito-core-%{version}.bar -properties ../conf/mockito-core.bnd mockito-core-%{version}.jar
popd

%install
mkdir -p $RPM_BUILD_ROOT%{_javadir}
sed -i -e "s|@version@|%{version}|g" maven/mockito-core.pom
cp -p target/mockito-core-%{version}.bar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 maven/mockito-core.pom  \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom

mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -rp target/javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%add_maven_depmap JPP-%{name}.pom %{name}.jar -a "org.mockito:mockito-all"

%files
%{_javadir}/%{name}.jar
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}
%doc NOTICE
%doc LICENSE

%files javadoc
%{_javadocdir}/%{name}
%doc LICENSE
%doc NOTICE

%changelog
* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Sep 6 2012 Severin Gehwolf <sgehwolf@redhat.com> 1.9.0-10
- More Import-Package fixes. Note that fix-cglib-refs.patch is
  not suitable for upstream:
  http://code.google.com/p/mockito/issues/detail?id=373

* Tue Sep 4 2012 Severin Gehwolf <sgehwolf@redhat.com> 1.9.0-9
- Fix missing Import-Package in manifest.

* Mon Aug 27 2012 Severin Gehwolf <sgehwolf@redhat.com> 1.9.0-8
- Add aqute bnd instructions for OSGi metadata

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 30 2012 Roman Kennke <rkennke@redhat.com> 1.9.0-6
- Place JavaDoc in directly under %{_javadocdir}/%{name} instead
  of %{_javadocdir}/%{name}/javadoc

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
