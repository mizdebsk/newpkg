package org.apache.maven.artifact.resolver;

import java.io.File;
import java.util.Hashtable;
import java.util.LinkedList;
import java.util.List;

import org.apache.maven.artifact.repository.MavenJPackageDepmap;
import org.sonatype.aether.artifact.Artifact;
import org.sonatype.aether.repository.WorkspaceReader;
import org.sonatype.aether.repository.WorkspaceRepository;

public class JavadirWorkspaceReader implements WorkspaceReader {
    private WorkspaceRepository workspaceRepository;

    private static final char GROUP_SEPARATOR = '.';
    private static final char PATH_SEPARATOR = '/';

    public JavadirWorkspaceReader() {
        workspaceRepository = new WorkspaceRepository("javadir-workspace");
    }

    public WorkspaceRepository getRepository() {
        return workspaceRepository;
    }

    public File findArtifact(Artifact artifact) {
        MavenJPackageDepmap.debug("=============JAVADIRREADER-FIND_ARTIFACT: "
                + artifact.getArtifactId());
        StringBuffer path = new StringBuffer();

        String artifactId = artifact.getArtifactId();
        String groupId = artifact.getGroupId();
        String version = artifact.getVersion();

        MavenJPackageDepmap.debug("Wanted GROUPID=" + groupId);
        MavenJPackageDepmap.debug("Wanted ARTIFACTID=" + artifactId);

        if (!groupId.startsWith("JPP")) {
            MavenJPackageDepmap map = MavenJPackageDepmap.getInstance();
            Hashtable<String, String> newInfo = map.getMappedInfo(groupId,
                    artifactId, version);

            groupId = (String) newInfo.get("group");
            artifactId = (String) newInfo.get("artifact");
        }
        MavenJPackageDepmap.debug("Resolved GROUPID=" + groupId);
        MavenJPackageDepmap.debug("Resolved ARTIFACTID=" + artifactId);

        if (artifact.getExtension().equals("pom")) {
            path = getPOMPath(groupId, artifactId);
        } else if (artifact.getExtension().equals("signature")) {
            path.append("/usr/share/maven/repository/");
            path.append(groupId).append('/');
            path.append(artifactId).append(".signature");
        } else if (artifact.getExtension().equals("zip")) {
            path.append("/usr/share/maven/repository/");
            path.append(groupId).append('/');
            path.append(artifactId).append(".zip");
        } else {
            path.append("/usr/share/maven/repository/");
            path.append(groupId).append('/');
            path.append(artifactId).append(".jar");
        }

        MavenJPackageDepmap.debug("Returning " + path.toString());
        File ret = new File(path.toString());
        // if file doesn't exist return null to delegate to other
        // resolvers (reactor/local repo)
        if (ret.isFile()) {
            MavenJPackageDepmap.debug("Returning " + path.toString());
            return ret;
        } else {
            MavenJPackageDepmap.debug("Returning null for gid:aid =>" + groupId
                    + ":" + artifactId);
            return null;
        }
    }

    public List<String> findVersions(Artifact artifact) {
        List<String> ret = new LinkedList<String>();
        ret.add("latest");
        return ret;
    }

    private StringBuffer getPOMPath(String groupId, String artifactId) {

        String fName = groupId.replace(PATH_SEPARATOR, GROUP_SEPARATOR) + "-"
                + artifactId + ".pom";
        String m2path = System.getProperty("maven2.local.pom.path",
                "JPP/maven2/poms") + "/" + fName;
        String m3path = System.getProperty("maven.local.pom.path",
                "JPP/maven/poms") + "/" + fName;
        File f;

        // let's try maven 2 repo first
        f = new File(System.getProperty("maven2.local.default.repo",
                "/usr/share/maven2/repository") + "/" + m2path);
        if (f.exists()) {
            return new StringBuffer(f.getPath());
        }

        // now maven 3 specific repository
        f = new File(System.getProperty("maven.local.default.repo",
                "/usr/share/maven/repository") + "/" + m3path);
        if (f.exists()) {
            return new StringBuffer(f.getPath());
        }

        // now try new path in /usr. This will be the only check after all
        // packages are rebuilt
        f = new File("/usr/share/maven-poms/" + fName);
        if (f.exists()) {
            return new StringBuffer(f.getPath());
        }

        // final fallback to m2 default poms
        return new StringBuffer("/usr/share/maven2/repository/"
                + System.getProperty("maven.local.default.repo",
                        "JPP/maven2/default_poms") + "/" + fName);
    }
}
