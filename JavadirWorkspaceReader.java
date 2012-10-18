package org.apache.maven.artifact.resolver;

import java.io.File;
import java.util.ArrayList;
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
    private static final char PATH_SEPARATOR = File.separatorChar;

    public JavadirWorkspaceReader() {
        workspaceRepository = new WorkspaceRepository("javadir-workspace");
    }

    public WorkspaceRepository getRepository() {
        return workspaceRepository;
    }

    private static final String LOG_FILE = System
            .getProperty("maven.resolver.logfile");
    private static final java.util.concurrent.Semaphore LOG_SEMAPHORE = new java.util.concurrent.Semaphore(
            1);

    public File findArtifact(Artifact artifact) {
        File f = findArtifactImpl(artifact);

        LOG_SEMAPHORE.acquireUninterruptibly();
        try {
            if (LOG_FILE != null && f != null) {
                java.io.FileOutputStream fos = new java.io.FileOutputStream(
                        LOG_FILE, true);
                java.io.PrintStream ps = new java.io.PrintStream(fos);
                ps.println(f.getAbsolutePath());
                ps.close();
            }
        } catch (Exception _) {
        } finally {
            LOG_SEMAPHORE.release();
            return f;
        }
    }

    private File findArtifactImpl(Artifact artifact) {
        MavenJPackageDepmap.debug("=============JAVADIRREADER-FIND_ARTIFACT: "
                + artifact.getArtifactId());
        StringBuffer path = new StringBuffer();
        File ret = new File("");
        String artifactId = artifact.getArtifactId();
        String groupId = artifact.getGroupId();
        String version = artifact.getVersion();
        String wantedVersion = new String(version);

        // let's check out local repo first
        String m2_path = System.getProperty("maven.repo.local");
        String gid_path = groupId.replace(".", File.separator);
        String art_path = m2_path + File.separator + gid_path + File.separator
                + artifactId + File.separator + version + File.separator
                + artifactId + "-" + version + "." + artifact.getExtension();

        ret = new File(art_path);
        if (ret.isFile()) {
            MavenJPackageDepmap.debug("Returning " + art_path.toString());
            return ret;
        }

        // maven.repo.local does not have needed GAV (that's normal), so let's
        // just continue with system packages
        MavenJPackageDepmap.debug("Wanted GROUPID=" + groupId);
        MavenJPackageDepmap.debug("Wanted ARTIFACTID=" + artifactId);
        MavenJPackageDepmap.debug("Wanted VERSION=" + version);
        ArrayList<Hashtable<String, String>> maps = new ArrayList<Hashtable<String, String>>();

        if (!groupId.startsWith("JPP")) {
            MavenJPackageDepmap map = MavenJPackageDepmap.getInstance();
            // let's try to get exact GAV first
            Hashtable<String, String> newInfo = map.getMappedInfo(groupId,
                    artifactId, version);
            if (newInfo == null) {
                // exact GAV does not exist in our mapping so let's just get all
                // GAs and iterate until we find one that exists. Note that only
                // one non-versioned jar/pom for given GA should exist in order
                // to ensure reproducibility

                maps = map.getUnversionedMappedInfo(groupId, artifactId,
                        version);
            } else {
                maps.add(newInfo);
            }
        }

        for (Hashtable<String, String> map : maps) {
            groupId = map.get("group");
            artifactId = map.get("artifact");
            version = map.get("version");

            MavenJPackageDepmap.debug("Resolved GROUPID=" + groupId);
            MavenJPackageDepmap.debug("Resolved ARTIFACTID=" + artifactId);
            MavenJPackageDepmap.debug("Resolved VERSION=" + version);

            if (artifact.getExtension().equals("pom")) {
                path = getPOMPath(groupId, artifactId, version);
                ret = new File(path.toString());
                if (ret.isFile()) {
                    MavenJPackageDepmap.debug("Returning " + path.toString());
                    return ret;
                }
            } else {
                String repos[] = { "/usr/share/maven/repository/",
                        "/usr/share/maven/repository-java-jni/",
                        "/usr/share/maven/repository-jni/" };
                String verRelativeArtifactPath = groupId + "/" + artifactId
                        + "-" + wantedVersion + "." + artifact.getExtension();
                String relativeArtifactPath = groupId + "/" + artifactId + "."
                        + artifact.getExtension();
                for (String repo : repos) {
                    path = new StringBuffer(repo + verRelativeArtifactPath);
                    ret = new File(path.toString());
                    if (ret.isFile()) {
                        MavenJPackageDepmap.debug("Returning " + repo
                                + verRelativeArtifactPath);
                        return ret;
                    }

                    path = new StringBuffer(repo + relativeArtifactPath);
                    ret = new File(path.toString());
                    if (ret.isFile()) {
                        MavenJPackageDepmap.debug("Returning " + repo
                                + relativeArtifactPath);
                        return ret;
                    }
                }
            }

        }
        // if file doesn't exist return null to delegate to other
        // resolvers (reactor/local repo)
        MavenJPackageDepmap.debug("Returning null for gid:aid =>" + groupId
                + ":" + artifactId);
        return null;
    }

    public List<String> findVersions(Artifact artifact) {
        List<String> ret = new LinkedList<String>();
        ret.add("LATEST");
        return ret;
    }

    private StringBuffer getPOMPath(String groupId, String artifactId,
            String version) {
        String fName = groupId.replace(PATH_SEPARATOR, GROUP_SEPARATOR) + "-"
                + artifactId + ".pom";
        String verfName = groupId.replace(PATH_SEPARATOR, GROUP_SEPARATOR)
                + "-" + artifactId + "-" + version + ".pom";
        File f;
        String[] pomRepos = { "/usr/share/maven2/poms/",
                "/usr/share/maven/poms/", "/usr/share/maven-poms/" };

        for (String pomRepo : pomRepos) {
            f = new File(pomRepo + verfName);
            if (f.exists()) {
                return new StringBuffer(f.getPath());
            }

            f = new File(pomRepo + fName);
            if (f.exists()) {
                return new StringBuffer(f.getPath());
            }
        }

        // final fallback to m2 default poms
        return new StringBuffer("/usr/share/maven2/default_poms/" + fName);
    }
}
