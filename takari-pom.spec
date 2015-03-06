Name:           takari-pom
Version:        15
Release:        2%{?dist}
Summary:        Takari parent POM
License:        EPL
URL:            https://github.com/takari/takari-pom/
BuildArch:      noarch

Source0:        https://github.com/takari/%{name}/archive/takari-%{version}.tar.gz
# Requested upstream to include license text:
# https://github.com/tesla/tesla-pom/pull/1
Source1:        http://www.eclipse.org/legal/epl-v10.html

BuildRequires:  maven-local
BuildRequires:  mvn(io.takari.maven.plugins:takari-lifecycle-plugin)


%description
Takari is a next generation development infrastructure framework.  This
package provides Takari POM file to by used by Apache Maven.

%prep
%setup -q -n %{name}-takari-%{version}
cp -p %{SOURCE1} .
%mvn_alias : io.tesla:tesla

# takari expects no annotations processors on classpath by default, but we
# always have some in /usr/share/java
%pom_xpath_inject 'pom:pluginManagement/pom:plugins/pom:plugin[pom:artifactId="takari-lifecycle-plugin"]/pom:configuration' '<proc>none</proc>'

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc epl-v10.html

%changelog
* Fri Mar 06 2015 Michael Simacek <msimacek@redhat.com> - 15-2
- Add default for annotation processors config

* Fri Feb 20 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 15-1
- Initial packaging
