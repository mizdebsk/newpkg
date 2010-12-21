package org.apache.maven.artifact.repository;


import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.Hashtable;
import java.util.StringTokenizer;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;


import org.xml.sax.SAXException;

import org.w3c.dom.*;


public class MavenJPackageDepmap {

	private static class ArtifactDefinition {
		String groupId = null;
		String artifactId = null;
		String version = null;
	}

	private static  MavenJPackageDepmap instance;
	private static Hashtable<String, String> jppArtifactMap;

	private MavenJPackageDepmap() {
		jppArtifactMap = new Hashtable<String,String>();
		buildJppArtifactMap();
	}

	public static MavenJPackageDepmap getInstance() {
		if (instance == null) {
			instance = new MavenJPackageDepmap();
		}

		return instance;
	}

	public Hashtable<String, String> getMappedInfo(Hashtable<String, String> mavenDep) {
		return getMappedInfo((String) mavenDep.get("group"),
				(String) mavenDep.get("artifact"),
				(String) mavenDep.get("version"));
	}

	public Hashtable<String, String> getMappedInfo(String groupId, String artifactId, String version) {

		Hashtable<String, String> jppDep;
		String idToCheck, jppCombination;

		if (System.getProperty("maven.ignore.versions") == null && System.getProperty("maven.jpp.mode") == null) {
			idToCheck = groupId+","+artifactId+","+version;
		} else {
			idToCheck = groupId+","+artifactId;
		}

		jppCombination = (String) jppArtifactMap.get(idToCheck);

		//System.err.println("*** " + groupId+","+artifactId+","+version + " => " + jppCombination);

		jppDep = new Hashtable<String, String>();
		if (jppCombination != null && jppCombination != "") {

			StringTokenizer st = new StringTokenizer(jppCombination, ",");

			jppDep.put("group", st.nextToken());
			jppDep.put("artifact",st.nextToken());
			jppDep.put("version",st.nextToken());

		} else {
			jppDep.put("group", groupId);
			jppDep.put("artifact", artifactId);
			jppDep.put("version", version);
		}

		return jppDep;
	}


	/**
	 *	Returns whether or not the given dependency should be dropped.
	 */
	public boolean shouldEliminate(String groupId, String artifactId, String version) {
		String idToCheck;

		if (System.getProperty("maven.ignore.versions") == null && System.getProperty("maven.jpp.mode") == null) {
			idToCheck = groupId+","+artifactId+","+version;
		} else {
			idToCheck = groupId+","+artifactId;
		}

		return jppArtifactMap.get(idToCheck) != null && jppArtifactMap.get(idToCheck).equals("");

	}

	private static void buildJppArtifactMap() {

		if (System.getProperty("maven.ignore.versions") != null || System.getProperty("maven.jpp.mode") != null) {
			debug("Processing file: /usr/share/java-utils/xml/maven2-versionless-depmap.xml");
			processDepmapFile("/etc/maven/maven2-versionless-depmap.xml");
		}

		debug("Processing file: /usr/share/java-utils/xml/maven2-depmap.xml");
		processDepmapFile("/etc/maven/maven2-depmap.xml");

		String customFileName = System.getProperty("maven.jpp.depmap.file", null);
		if (customFileName != null) {
			debug("Processing file: " + customFileName);
			processDepmapFile(customFileName);
		}
	}

	private static void processDepmapFile(String fileName) {

		Document mapDocument;
		debug("Loading depmap file: " + fileName);
		try {
			DocumentBuilderFactory fact = DocumentBuilderFactory.newInstance();
			fact.setNamespaceAware(true);
			DocumentBuilder builder = fact.newDocumentBuilder();
			mapDocument = builder.parse(fileName);
		} catch (FileNotFoundException fnfe) {
			System.err.println("ERROR: Unable to find map file: " + fileName);
			fnfe.printStackTrace();
			return;
		} catch (IOException ioe) {
			System.err.println("ERROR: I/O exception occured when opening map file");
			ioe.printStackTrace();
			return;
		} catch (ParserConfigurationException pce) {
			System.err.println("ERROR: Parsing of depmap file failed - configuration");
			pce.printStackTrace();
			return;
		} catch (SAXException se) {
			System.err.println("ERROR: Parsing of depmap file failed");
			se.printStackTrace();
			return;
		}
		
		NodeList depNodes = (NodeList) mapDocument.getElementsByTagName("dependency");

		for (int i = 0; i < depNodes.getLength(); i++) {
			Element depNode = (Element) depNodes.item(i);

			NodeList mavenNodeList = (NodeList) depNode.getElementsByTagName("maven");
			if (mavenNodeList.getLength() != 1) {
				debug("Number of maven sub-elements is not 1. Bailing from depmap generation");
				debug("Maven node: " + depNode.getTextContent());
				return;
			}
			ArtifactDefinition mavenAD = getArtifactDefinition((Element) mavenNodeList.item(0));

			ArtifactDefinition jppAD = null;
			NodeList jppNodeList = (NodeList) depNode.getElementsByTagName("jpp");
			
			if (jppNodeList.getLength() == 1) {
				jppAD = getArtifactDefinition((Element) jppNodeList.item(0));
				if (System.getProperty("maven.ignore.versions") == null && System.getProperty("maven.jpp.mode") == null) {
					debug("*** Adding: " + mavenAD.groupId + "," + mavenAD.artifactId + "," + mavenAD.version + " => "
							+  jppAD.groupId + "," + jppAD.artifactId + "," + jppAD.version + " to map...");

					jppArtifactMap.put(mavenAD.groupId + "," + mavenAD.artifactId + "," + mavenAD.version,
							jppAD.groupId + "," + jppAD.artifactId + "," + jppAD.version);
				} else {
					debug("*** Adding: " + mavenAD.groupId+"," + mavenAD.artifactId + " => " 
							+  jppAD.groupId + "," + jppAD.artifactId + "," + jppAD.version + " to map...");

					jppArtifactMap.put(mavenAD.groupId+","+mavenAD.artifactId, 
							jppAD.groupId + "," + jppAD.artifactId + "," + jppAD.version);
				}
			} else {
				debug("Number of jpp sub-elements is not 1. Dropping dependency");
				debug("*** Adding: " + mavenAD.groupId+","+mavenAD.artifactId+"," + " => " +  "JPP/maven2,empty-dep,"+mavenAD.version + " to map...");
				jppArtifactMap.put(mavenAD.groupId+","+mavenAD.artifactId, "JPP/maven2,empty-dep,"+mavenAD.version);
			}
		} 
	}

	private static ArtifactDefinition getArtifactDefinition(Element element) {
		ArtifactDefinition ad = new ArtifactDefinition();
		
		NodeList nodes = element.getElementsByTagName("groupId");
		if (nodes.getLength() != 1) {
			debug("groupId definition not found in depmap");
			return null;
		}
		ad.groupId = nodes.item(0).getTextContent();

		nodes = element.getElementsByTagName("artifactId");
		if (nodes.getLength() != 1) {
			debug("artifactId definition not found in depmap");
			return null;
		}
		ad.artifactId = nodes.item(0).getTextContent();

		nodes = element.getElementsByTagName("version");
		if (nodes.getLength() != 1) {
			ad.version = "DUMMY_VER";
		} else {
			ad.version = nodes.item(0).getTextContent();
		}
		return ad;
	}


	public static void debug(String msg) {
		if (System.getProperty("maven.jpp.debug") != null)
			System.err.println(msg);
	}
}
