%define section         devel

Summary:        High-performance, full-featured text search engine
Name:           lucene
Version:        1.4.3
Release:        1jpp
Epoch:          0
License:        Apache Software License
URL:            http://jakarta.apache.org/lucene/
Group:          Internet/WWW/Indexing/Search
Vendor:         JPackage Project
Distribution:   JPackage
Source0:        http://cvs.apache.org/dist/jakarta/lucene/lucene-1.4.3-src.tar.gz
BuildRequires:  jpackage-utils >= 0:1.5
BuildRequires:  ant >= 0:1.6.2
BuildRequires:  ant-junit >= 0:1.6.2
BuildRequires:  junit >= 0:3.7
BuildRequires:  javacc
BuildArch:      noarch
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
  package test-unit

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

# TODO: webapp: luceneweb.war / where do we install 'em?

# -----------------------------------------------------------------------------

%clean
rm -rf $RPM_BUILD_ROOT

# -----------------------------------------------------------------------------

%files
%defattr(0644,root,root,0755)
%doc CHANGES.txt LICENSE.txt README.txt
%{_javadir}/*

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}

%files demo
%defattr(0644,root,root,0755)
%{_datadir}/%{name}

# TODO: webapp

# -----------------------------------------------------------------------------

%changelog
* Mon Jan 10 2005 Kaj J. Niemi <kajtzu@fi.basen.net> 0:1.4.3
- 1.4.3

* Mon Aug 23 2004 Fernando Nasser <fnasser at redhat.com> - 0:1.3-3jpp
- Rebuild with Ant 1.6.2

* Tue Jun 01 2004 Randy Watler <rwatler at finali.com> - 0:1.3-2jpp
- Upgrade to Ant 1.6.X

* Wed Jan 21 2004 David Walluck <david@anti-microsoft.org> 0:1.3-1jpp
- 1.3

* Wed Mar 26 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.2-2jpp
- Rebuilt for JPackage 1.5.

* Thu Mar  6 2003 Ville Skyttä <ville.skytta at iki.fi> - 1.2-1jpp
- First JPackage release.
