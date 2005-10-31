%define section         devel
%define gcj_support 	1

Summary:        High-performance, full-featured text search engine
Name:           lucene
Version:        1.4.3
Release:        1jpp_6fc
Epoch:          0
License:        Apache Software License
URL:            http://jakarta.apache.org/lucene/
Group:          Internet/WWW/Indexing/Search
Source0:        http://cvs.apache.org/dist/jakarta/lucene/lucene-1.4.3-src.tar.gz
%if %{gcj_support}
%else
BuildArch:	noarch
%endif
BuildRequires:  jpackage-utils >= 0:1.5
BuildRequires:  ant >= 0:1.6.2
BuildRequires:  ant-junit >= 0:1.6.2
BuildRequires:  junit >= 0:3.7
BuildRequires:  javacc
%if %{gcj_support}
BuildRequires:	java-gcj-compat-devel >= 1.0.43
Requires(post): java-1.4.2-gcj-compat
Requires(postun): java-1.4.2-gcj-compat
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Jakarta Lucene is a high-performance, full-featured text search engine
written entirely in Java. It is a technology suitable for nearly any
application that requires full-text search, especially cross-platform.

%package javadoc
Summary:        Javadoc for Lucene
Group:          Development/Documentation

%description javadoc
Javadoc for Lucene.

%package demo
Summary:        Lucene demonstrations and samples
Group:          Internet/WWW/Indexing/Search
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description demo
Lucene demonstrations and samples.

# TODO: webapp

# -----------------------------------------------------------------------------

%prep
%setup -q -n %{name}-%{version}
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;

# -----------------------------------------------------------------------------

%build
mkdir -p docs
export OPT_JAR_LIST="ant/ant-junit junit"
export CLASSPATH=
ant \
  -Djavacc.home=%{_bindir}/javacc \
  -Djavacc.jar=%{_javadir}/javacc.jar \
  -Djavacc.jar.dir=%{_javadir} \
  -Djavadoc.link=http://java.sun.com/j2se/1.4.2/docs/api/ \
  package

# -----------------------------------------------------------------------------

%install
rm -rf $RPM_BUILD_ROOT

# jars
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p build/%{name}-1.5-rc1-dev.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr build/docs/api/* \
  $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}

# demo
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}

cp -p build/%{name}-demos-1.5-rc1-dev.jar \
  $RPM_BUILD_ROOT%{_datadir}/%{name}//%{name}-demos-%{version}.jar

%if %{gcj_support}
aot-compile-rpm
%endif

# TODO: webapp: luceneweb.war / where do we install 'em?

# -----------------------------------------------------------------------------

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
/usr/bin/rebuild-gcj-db

%postun
/usr/bin/rebuild-gcj-db
%endif

# -----------------------------------------------------------------------------

%files
%defattr(0644,root,root,0755)
%doc CHANGES.txt LICENSE.txt README.txt
%{_javadir}/*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%{_libdir}/gcj/%{name}/%{name}-%{version}.jar.so
%{_libdir}/gcj/%{name}/%{name}-%{version}.jar.db
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}

%files demo
%defattr(0644,root,root,0755)
%{_datadir}/%{name}
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%{_libdir}/gcj/%{name}/%{name}-demos-%{version}.jar.so
%{_libdir}/gcj/%{name}/%{name}-demos-%{version}.jar.db
%endif

# TODO: webapp

# -----------------------------------------------------------------------------

%changelog
* Mon Oct 31 2005 Andrew Overholt <overholt@redhat.com> 1.4.3-1jpp_6fc
- Bump release.

* Thu Oct 27 2005 Andrew Overholt <overholt@redhat.com> 1.4.3-1jpp_5fc
- Remove ExclusiveArch.
- Use aot-compile-rpm.
- Remove now-unnecessary patches.

* Sun Oct 09 2005 Florian La Roche <laroche@redhat.com>
- always "exit 0" the scripts
- fix the requires for post/postun for java

* Tue Jul 05 2005 Andrew Overholt <overholt@redhat.com> 1.4.3-1jpp_2fc
- Bump release for FC4 update.

* Thu Jun 09 2005 Andrew Overholt <overholt@redhat.com> 1.4.3-1jpp_1fc
- Build for Fedora.
- Add patch for rmic (rh#133180 -- gbenson).  Should be fixed by forthcoming
  grmic patch.
- Don't run tests until we get a patched grmic (all pass except those needing
  stubs).
- Natively-compile.
- Add architectures to gcj_support block and build noarch otherwise.
- Remove Vendor and Distribution tags.
- Add patch to not link to external javadocs.

* Mon Jan 10 2005 Kaj J. Niemi <kajtzu@fi.basen.net> 0:1.4.3
- 1.4.3

* Mon Aug 23 2004 Fernando Nasser <fnasser at redhat.com> - 0:1.3-3jpp
- Rebuild with Ant 1.6.2

* Tue Jun 01 2004 Randy Watler <rwatler at finali.com> - 0:1.3-2jpp
- Upgrade to Ant 1.6.X

* Wed Jan 21 2004 David Walluck <david@anti-microsoft.org> 0:1.3-1jpp
- 1.3

* Wed Mar 26 2003 Ville Skytt� <ville.skytta at iki.fi> - 0:1.2-2jpp
- Rebuilt for JPackage 1.5.

* Thu Mar  6 2003 Ville Skytt� <ville.skytta at iki.fi> - 1.2-1jpp
- First JPackage release.
