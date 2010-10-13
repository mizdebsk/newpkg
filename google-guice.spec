%global short_name guice
%global revision 1219

Name:           google-%{short_name}
Version:        2.0
Release:        2.1219svn%{?dist}
Summary:        Lightweight dependency injection framework


Group:          Development/Tools
License:        ASL 2.0
URL:            http://code.google.com/p/%{name}

# svn export -r1219 http://google-guice.googlecode.com/svn/trunk/ guice-2.0-1219
# tar caf guice-2.0-1219.tar.xz guice-2.0-1219
Source0:        %{short_name}-%{version}-%{revision}.tar.xz

# TODO upstream
Patch0:         0001-aop-fix.patch
# see http://code.google.com/p/google-guice/issues/detail?id=436
# needed for sisu-inject (and maven-3)
Patch1:         0002-get-type-converter-binding.patch
# remove aopalliacne dep from pom and parent pom
Patch2:         0003-aopaliance.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  ant
BuildRequires:  jarjar => 1.0
BuildRequires:  cglib
BuildRequires:  aqute-bndlib
BuildRequires:  objectweb-asm
BuildRequires:  junit
BuildRequires:  atinject

Requires:       java >= 1:1.6.0
Requires(post): jpackage-utils
Requires(postun): jpackage-utils

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

%package        javadoc
Summary:        API documentation for %{name}
Group:          Documentation
Requires:       jpackage-utils

%description    javadoc
%{summary}.

%prep
%setup -q -n %{short_name}-%{version}-%{revision}
%patch0 -p1
%patch1 -p1
%patch2 -p1

# remove bundled libraries
find . -name '*.class' -delete
find . -name '*.bar' -delete
# we'll repack munge.jar so don't delete it just yet
find . -name '*.jar' -not -name 'munge.jar' -delete

# re-create symlinks
pushd lib/build
build-jar-repository -s -p . aqute-bndlib cglib \
                     jarjar junit objectweb-asm \

mv aqute-bndlib*.jar bnd-0.0.384.jar
mv cglib*.jar cglib-2.2.1-snapshot.jar
mv jarjar*.jar jarjar-1.0rc8.jar
mv objectweb-asmasm-all.jar asm-3.1.jar

popd
ln -sf `build-classpath atinject` lib/javax.inject.jar

# there is munge.jar defining ant task it's a mixture of files, but
# there are sources in jar so we re-compile the jar to verify it
# builds
mkdir munge-repack
unzip lib/build/munge.jar -d munge-repack
rm lib/build/munge.jar

pushd munge-repack
rm *.class
javac -cp `build-classpath ant junit` *.java
zip -r ../lib/build/munge.jar .
popd

rm -rf munge-repack
#end munge.jar repack

%build
# create no-aop build environment
ant no_aop

pushd build/no_aop/
# javadoc fails without this directory
mkdir -p servlet/lib/build

ant -Dversion=%{version} jar javadoc
popd

%install
rm -rf $RPM_BUILD_ROOT

install -d -m 0755 $RPM_BUILD_ROOT%{_javadir}
pushd build/no_aop
install -pm 644 build/dist/%{short_name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|google-||g"`; done)
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)

install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 %{short_name}-parent/pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP-%{short_name}-parent.pom

install -pm 644 pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP-%{name}.pom
%add_to_maven_depmap com.google.inject %{short_name} %{version} JPP %{name}
# provide sisu group/artifact (should be just mavenized google-guice
# with
%add_to_maven_depmap org.sonatype.sisu sisu-%{short_name} %{version} JPP %{name}


# javadoc
install -d -m 0755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr build/javadoc/* %{buildroot}%{_javadocdir}/%{name}-%{version}/
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}



%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_maven_depmap

%postun
%update_maven_depmap


%files
%defattr(-,root,root,-)
%doc COPYING
%{_javadir}/*.jar
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*


%files javadoc
%defattr(-,root,root,-)
%doc COPYING
%doc %{_javadocdir}/%{name}*



%changelog
* Wed Oct 13 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.0-2.1219svn
- Moved munge repacking to prep
- Added -Dversion to change generated manifest version
- Removed http part of URL

* Thu Oct  7 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.0-1.1219svn
- Initial version of the package


