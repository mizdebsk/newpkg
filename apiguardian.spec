Name:           apiguardian
Version:        1.0.0
Release:        1%{?dist}
Summary:        API Guardian Java annotation
License:        ASL 2.0
URL:            https://github.com/apiguardian-team/apiguardian
BuildArch:      noarch

Source0:        https://github.com/apiguardian-team/apiguardian/archive/r%{version}.tar.gz

Source100:      https://repo1.maven.org/maven2/org/apiguardian/apiguardian-api/%{version}/apiguardian-api-%{version}.pom

BuildRequires:  maven-local

%description
API Guardian indicates the status of an API element and therefore its
level of stability as well.  It is used to annotate public types,
methods, constructors, and fields within a framework or application in
order to publish their API status and level of stability and to
indicate how they are intended to be used by consumers of the API.

%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
API documentation for %{name}.

%prep
%setup -q -n apiguardian-r%{version}
cp -p %{SOURCE100} pom.xml

# Inject OSGi manifest required by Eclipse
%pom_xpath_inject pom:project "
  <build>
    <pluginManagement>
      <plugins>
	<plugin>
          <artifactId>maven-jar-plugin</artifactId>
          <configuration>
            <archive>
            <manifestEntries>
              <Bundle-ManifestVersion>2</Bundle-ManifestVersion>
              <Bundle-SymbolicName>org.apiguardian</Bundle-SymbolicName>
              <Bundle-Version>%{version}</Bundle-Version>
              <Export-Package>org.apiguardian.api;version=\"%{version}\"</Export-Package>
            </manifestEntries>
            </archive>
          </configuration>
	</plugin>
      </plugins>
    </pluginManagement>
  </build>"


%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%license LICENSE

%files javadoc -f .mfiles-javadoc
%license LICENSE

%changelog
* Thu Sep 14 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0.0-1
- Initial packaging
