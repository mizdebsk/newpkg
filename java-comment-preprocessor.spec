%global section		devel

Summary:	The Most Powerful Multi-Pass Java Preprocessor
Name:		java-comment-preprocessor
Version:	6.0.1
Release:	1%{?dist}
License:	ASL 2.0

URL:		https://github.com/raydac/java-comment-preprocessor
Source0:	https://github.com/raydac/java-comment-preprocessor/archive/%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	jpackage-utils
BuildRequires:	java-devel >= 1:1.8
BuildRequires:	maven-local
BuildRequires:	exec-maven-plugin
BuildRequires:	maven-shade-plugin
# Test requirements
BuildRequires:	maven-shared-jar
BuildRequires:	ant-testutil
BuildRequires:	maven-verifier
BuildRequires:	mockito
Requires:	jpackage-utils
Requires:	java-headless >= 1:1.8

%description
It is the most powerful multi-pass preprocessor for Java
but also it can be used everywhere for text processing
if the destination technology supports Java like comment definitions. 

%package javadoc
Summary:	API docs for %{name}
Group:		Documentation

%description javadoc
This package contains the API Documentation for %{name}.

%prep

%setup -c -q
mv -f %{name}-%{version}/* .

%pom_remove_plugin :animal-sniffer-maven-plugin pom.xml

# remove any binary libs
find -name "*.jar" -or -name "*.class" | xargs rm -f

%build
%mvn_build

%install
%mvn_install

%check

%files -f .mfiles
%license texts/LICENSE-2.0.txt
%doc texts/readme.txt 

%files javadoc
%license texts/LICENSE-2.0.txt
%doc %{_javadocdir}/%{name}

%changelog
* Tue Jan 5 2016 Pavel Kajaba <pkajaba@redhat.com>
- Initial creation of java-comment-preprocessor package
