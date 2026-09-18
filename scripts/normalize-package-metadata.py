#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

REPO = "https://github.com/sportsfoundry/sdks"
DESCRIPTION = "Official SportsFoundry SDK generated from the canonical SportsFoundry Developer API contract."

# npm metadata
npm_path = Path("generated/typescript/package.json")
npm = json.loads(npm_path.read_text(encoding="utf-8"))
npm["description"] = DESCRIPTION
npm["author"] = "SportsFoundry"
npm["license"] = "Apache-2.0"
npm["homepage"] = "https://sportsfoundry.app/sportsfoundry/sdks.html"
npm["repository"] = {"type": "git", "url": REPO + ".git"}
npm["publishConfig"] = {"access": "public"}
npm_path.write_text(json.dumps(npm, indent=2) + "\n", encoding="utf-8")

# Python generator accepts packageUrl, but also replace any leftover placeholders in metadata/docs.
for path in (
    Path("generated/python/pyproject.toml"),
    Path("generated/python/README.md"),
    Path("generated/python/setup.py"),
):
    if path.exists():
        text = path.read_text(encoding="utf-8")
        text = text.replace("https://github.com/GIT_USER_ID/GIT_REPO_ID.git", REPO + ".git")
        text = text.replace("https://github.com/GIT_USER_ID/GIT_REPO_ID", REPO)
        text = text.replace("http://localhost", "https://sportsfoundry.app")
        text = text.replace('{name = "SportsFoundry",email = "team@openapitools.org"}', '{name = "SportsFoundry"}')
        text = text.replace('    author_email="team@openapitools.org",\n', '')
        path.write_text(text, encoding="utf-8")

# NuGet package metadata lives in the generated csproj.
csproj = next(Path("generated/dotnet").rglob("*.csproj"))
text = csproj.read_text(encoding="utf-8")
replacements = {
    r"<Authors>.*?</Authors>": "<Authors>SportsFoundry</Authors>",
    r"<Description>.*?</Description>": f"<Description>{DESCRIPTION}</Description>",
    r"<Copyright>.*?</Copyright>": "<Copyright>Copyright SportsFoundry</Copyright>",
    r"<RepositoryUrl>.*?</RepositoryUrl>": f"<RepositoryUrl>{REPO}.git</RepositoryUrl>",
    r"<PackageReleaseNotes>.*?</PackageReleaseNotes>": "<PackageReleaseNotes>Initial SportsFoundry SDK alpha release.</PackageReleaseNotes>",
}
for pattern, replacement in replacements.items():
    text = re.sub(pattern, replacement, text, flags=re.DOTALL)
if "<PackageLicenseExpression>" not in text:
    text = text.replace("</PropertyGroup>", "  <PackageLicenseExpression>Apache-2.0</PackageLicenseExpression>\n    <PackageProjectUrl>https://sportsfoundry.app</PackageProjectUrl>\n    <PackageReadmeFile>README.md</PackageReadmeFile>\n  </PropertyGroup>", 1)
if '<None Include="README.md" Pack="true" PackagePath="\\\\" />' not in text:
    text = text.replace("</Project>", '  <ItemGroup>\n    <None Include="README.md" Pack="true" PackagePath="\\\\" />\n  </ItemGroup>\n</Project>')
csproj.write_text(text, encoding="utf-8")


# Maven Central metadata: keep generator output, but replace generic project metadata.
pom = Path("generated/java/pom.xml")
pom_text = pom.read_text(encoding="utf-8")
pom_text = re.sub(r"<name>.*?</name>", "<name>SportsFoundry Java SDK</name>", pom_text, count=1, flags=re.DOTALL)
if "<description>" in pom_text:
    pom_text = re.sub(r"<description>.*?</description>", f"<description>{DESCRIPTION}</description>", pom_text, count=1, flags=re.DOTALL)
else:
    pom_text = pom_text.replace("</name>", f"</name>\n    <description>{DESCRIPTION}</description>", 1)
pom_text = re.sub(r"<url>.*?</url>", "<url>https://sportsfoundry.app</url>", pom_text, count=1, flags=re.DOTALL)
pom_text = pom_text.replace("            <email>team@openapitools.org</email>\n", "")
pom.write_text(pom_text, encoding="utf-8")


# Maven Central Publisher Portal plugin. This is inert during ordinary package builds
# and participates only when Maven deploy is explicitly invoked by release.yml.
central_plugin = """
            <plugin>
                <groupId>org.sonatype.central</groupId>
                <artifactId>central-publishing-maven-plugin</artifactId>
                <version>0.11.0</version>
                <extensions>true</extensions>
                <configuration>
                    <publishingServerId>central</publishingServerId>
                    <autoPublish>true</autoPublish>
                    <waitUntil>published</waitUntil>
                </configuration>
            </plugin>
"""
if "central-publishing-maven-plugin" not in pom_text:
    build_plugins = pom_text.find("<plugins>")
    if build_plugins < 0:
        raise SystemExit("generated Maven POM has no build/plugins section")
    close_plugins = pom_text.find("</plugins>", build_plugins)
    if close_plugins < 0:
        raise SystemExit("generated Maven POM has no closing build/plugins section")
    pom_text = pom_text[:close_plugins] + central_plugin + pom_text[close_plugins:]
pom.write_text(pom_text, encoding="utf-8")
