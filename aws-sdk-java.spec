Name:           aws-sdk-java
Version:        1.9.32
Release:        1%{?dist}
Summary:        AWS SDK for Java
License:        ASL 2.0
URL:            http://aws.amazon.com/sdk-for-java/
BuildArch:      noarch

Source0:        https://github.com/aws/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  maven-local
BuildRequires:  mvn(com.fasterxml.jackson.core:jackson-databind)
BuildRequires:  mvn(commons-io:commons-io)
BuildRequires:  mvn(commons-logging:commons-logging)
BuildRequires:  mvn(javax.mail:javax.mail-api)
BuildRequires:  mvn(joda-time:joda-time)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.httpcomponents:httpclient)
BuildRequires:  mvn(org.easymock:easymock)

%description
The AWS SDK for Java enables Java developers to easily work with
Amazon Web Services and build scalable solutions with Amazon S3,
Amazon DynamoDB, Amazon Glacier, and more.

%package javadoc
Summary:        API documentation for %{name}

%description javadoc
This package provides %{summary}.

%prep
%setup -q

# Disable building of super-JAR
%pom_disable_module aws-java-sdk-osgi
# Missing dependency: aspectj
%pom_disable_module aws-java-sdk-swf-libraries
%pom_remove_dep :aws-java-sdk-swf-libraries aws-java-sdk

%build
# Tests require networking
%mvn_build -f

%install
%mvn_install

%files -f .mfiles
%doc README.md
%license LICENSE.txt NOTICE.txt

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt NOTICE.txt

%changelog
* Fri Apr 24 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.9.32-1
- Initial packaging

