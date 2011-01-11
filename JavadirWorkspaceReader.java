package org.apache.maven.artifact.resolver;

import org.apache.maven.artifact.repository.MavenJPackageDepmap;

import java.io.File;
import java.util.List;
import java.util.LinkedList;
import java.util.Hashtable;

import org.sonatype.aether.repository.WorkspaceReader;
import org.sonatype.aether.repository.WorkspaceRepository;
import org.sonatype.aether.artifact.Artifact;


public class JavadirWorkspaceReader
    implements WorkspaceReader
{
    private WorkspaceRepository workspaceRepository;

    private static final char GROUP_SEPARATOR = '.';
    private static final char PATH_SEPARATOR = '/';


    public JavadirWorkspaceReader() {
        workspaceRepository = new WorkspaceRepository("javadir-workspace");
    }

    public WorkspaceRepository getRepository() {
        return workspaceRepository;
    }

    public File findArtifact( Artifact artifact ) {
    	MavenJPackageDepmap.debug("=============JAVADIRREADER-FIND_ARTIFACT: " + artifact.getArtifactId());
        StringBuffer path = new StringBuffer();

        String artifactId = artifact.getArtifactId();
        String groupId = artifact.getGroupId();
        String version = artifact.getVersion();

        MavenJPackageDepmap.debug("Wanted GROUPID=" + groupId);
        MavenJPackageDepmap.debug("Wanted ARTIFACTID=" + artifactId);
        
        if (!groupId.startsWith("JPP")) {
            MavenJPackageDepmap map = MavenJPackageDepmap.getInstance();
            Hashtable<String,String> newInfo = map.getMappedInfo(groupId, artifactId, version);

            groupId = (String) newInfo.get("group");
            artifactId = (String) newInfo.get("artifact");
        }
        MavenJPackageDepmap.debug("Resolved GROUPID=" + groupId);
        MavenJPackageDepmap.debug("Resolved ARTIFACTID=" + artifactId);

        if (artifact.getExtension().equals("pom")) {
            path = getPOMPath(groupId, artifactId);
        } else if (artifact.getExtension().equals("signature")) {
        	path.append("/usr/share/maven/repository/");
            path.append( groupId ).append( '/' );
            path.append( artifactId ).append( ".signature" );
        } else {
        	path.append("/usr/share/maven/repository/");
            path.append( groupId ).append( '/' );
            path.append( artifactId ).append( ".jar" );
        }

        MavenJPackageDepmap.debug("Returning " + path.toString());
        File ret = new File(path.toString());
        // if file doesn't exist return null to delegate to other
        // resolvers (reactor/local repo)
        if ( ret.isFile() ) {
            MavenJPackageDepmap.debug("Returning " + path.toString());
            return ret;
        } else {
            MavenJPackageDepmap.debug("Returning null for gid:aid" + groupId + ":" + artifactId);
            return null;
        }
    }

    public List<String> findVersions( Artifact artifact ) {
        List<String> ret = new LinkedList<String>();
        ret.add("latest");
        return ret;
    }

    private StringBuffer getPOMPath(String groupId, String artifactId) {

        StringBuffer path = new StringBuffer();
        String fName = groupId.replace(PATH_SEPARATOR, GROUP_SEPARATOR) + "-" + artifactId + ".pom";
        path.append(System.getProperty("maven.jpp.pom.path", "JPP/maven2/poms")).append("/").append(fName);
        java.io.File f;

        // NOTE: We are returning default_poms/ as the path for this pom
        // even though it may not exist there. This may cause an error,
        // but that is fine because if the pom is not there, there is
        // a serious problem anyways..
        f = new java.io.File(System.getProperty("maven.jpp.default.repo", "/usr/share/maven2/repository") + "/" + path.toString());
        //System.err.println("Checking path " + f.getAbsolutePath() + " for the pom");
        if (!f.exists()) {
            path = new StringBuffer();
            path.append(System.getProperty("maven.jpp.default.pom.path", "JPP/maven2/default_poms")).append("/").append(fName);
        }
        path.insert(0, "/usr/share/maven2/repository/");
        return path;
    }
}
