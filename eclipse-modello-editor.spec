%global commit 6d1a7d310d6f1196ea014b9a3244b8e6d2bfbf87
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           eclipse-modello-editor
Version:        0.1.0
Release:        0.1.git%{shortcommit}%{?dist}
Summary:        Modello editor for Eclipse
License:        EPL
URL:            https://github.com/takari/modello-editor
BuildArch:      noarch

Source0:        https://github.com/takari/modello-editor/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz

BuildRequires:  maven-local
BuildRequires:  mvn(io.takari.tycho:tycho-support:pom:)
BuildRequires:  osgi(org.eclipse.core.databinding)
BuildRequires:  osgi(org.eclipse.core.databinding.beans)
BuildRequires:  osgi(org.eclipse.core.databinding.property)
BuildRequires:  osgi(org.eclipse.core.resources)
BuildRequires:  osgi(org.eclipse.core.runtime)
BuildRequires:  osgi(org.eclipse.jdt.core)
BuildRequires:  osgi(org.eclipse.jdt.debug.ui)
BuildRequires:  osgi(org.eclipse.jdt.ui)
BuildRequires:  osgi(org.eclipse.jface.databinding)
BuildRequires:  osgi(org.eclipse.jface.text)
BuildRequires:  osgi(org.eclipse.license)
BuildRequires:  osgi(org.eclipse.osgi)
BuildRequires:  osgi(org.eclipse.ui)
BuildRequires:  osgi(org.eclipse.ui.forms)
BuildRequires:  osgi(org.eclipse.ui.ide)
BuildRequires:  osgi(org.eclipse.ui.workbench.texteditor)
BuildRequires:  osgi(org.eclipse.wst.sse.core)
BuildRequires:  osgi(org.eclipse.wst.sse.ui)
BuildRequires:  osgi(org.eclipse.wst.xml.core)
BuildRequires:  osgi(org.eclipse.wst.xml.ui)
BuildRequires:  osgi(org.eclipse.wst.xsd.core)
BuildRequires:  osgi(org.eclipse.xsd)

%description
This is a plugin for Eclipse IDE which provides editor for Modello models.

%prep
%setup -q -n modello-editor-%{commit}

%build
xmvn -B -o -f io.takari.modello.editor.mapping install
%mvn_artifact -Dtype=eclipse-plugin io.takari.modello.editor:io.takari.modello.editor.mapping:0.1.0-SNAPSHOT *mapping/target/*.jar
%mvn_build -j
jar xf *feature/target/*.jar

%install
%mvn_install
xmvn-subst -s `find %{buildroot} -name jars`

%files -f .mfiles
%doc README.md
%license epl-v10.html license.html

%changelog
* Tue Jan 27 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.1.0-0.1.git6d1a7d3
- Initial packaging
