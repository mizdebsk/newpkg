%global mod_name openid-plugin
%global short_name openid
%global plugin_home %{_datadir}/jenkins/webroot/WEB-INF/plugins/

Name:           jenkins-openid-plugin
Version:        2.1.1
Release:        1%{?dist}
Summary:        Jenkins OpenID Plugin
# License is specified in pom.xml
License:        MIT
URL:            https://github.com/jenkinsci/openid-plugin
BuildArch:      noarch

Source0:        https://github.com/jenkinsci/%{mod_name}/archive/%{short_name}-%{version}.tar.gz
# Text copied from http://www.opensource.org/licenses/mit-license.php
Source1:        LICENSE.txt

BuildRequires:  maven-local
BuildRequires:  mvn(com.cloudbees:openid4java-team-extension)
BuildRequires:  mvn(org.apache.maven.plugins:maven-release-plugin)
BuildRequires:  mvn(org.jenkins-ci.main:jenkins-core)
BuildRequires:  mvn(org.jenkins-ci.plugins:mailer)
BuildRequires:  mvn(org.jenkins-ci.plugins:plugin:pom:)
BuildRequires:  mvn(org.kohsuke:access-modifier-checker)
BuildRequires:  mvn(org.openid4java:openid4java)

%description
This package provides OpenID plugin for Jenkins.

%package        javadoc
Summary:        Javadoc for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n %{mod_name}-%{short_name}-%{version}

cp %{SOURCE1} .
%mvn_file ::hpi:: %{name}/%{short_name}

%pom_change_dep :openid4java org.openid4java:
%pom_add_dep com.cloudbees:openid4java-team-extension:1.0

%build
# incompatible version of htmlunit
%mvn_build -f

%install
install -d -m 755 %{buildroot}/%{plugin_home}
unzip -d target/%{short_name}.hpi-unpacked target/%{short_name}.hpi
pushd target/%{short_name}.hpi-unpacked/WEB-INF/lib/
  rm %{short_name}.jar && ln -s %{_javadir}/%{name}/%{short_name}.jar .
  rm ./tools-any.jar
  xmvn-subst -s .
popd
pushd target/%{short_name}.hpi-unpacked/
  zip -y -r %{short_name}.hpi .
popd
mv target/%{short_name}.hpi-unpacked/%{short_name}.hpi target/
cp target/%{short_name}.hpi %{buildroot}/%{plugin_home}/
%mvn_install

%files -f .mfiles
%license LICENSE.txt
%{plugin_home}

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt

%changelog
* Fri Jun 26 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.1.1-1
- Initial packaging
