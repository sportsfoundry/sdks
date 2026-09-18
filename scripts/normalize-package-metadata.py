#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

REPO = "https://github.com/SportsFoundry/sdks"
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
):
    if path.exists():
        text = path.read_text(encoding="utf-8")
        text = text.replace("https://github.com/GIT_USER_ID/GIT_REPO_ID.git", REPO + ".git")
        text = text.replace("https://github.com/GIT_USER_ID/GIT_REPO_ID", REPO)
        text = text.replace("http://localhost", "https://sportsfoundry.app")
        path.write_text(text, encoding="utf-8")

# NuGet package metadata lives in the generated csproj.
csproj = next(Path("generated/dotnet").rglob("*.csproj"))
text = csproj.read_text(encoding="utf-8")
replacements = {
    r"<Authors>.*?</Authors>": "<Authors>SportsFoundry</Authors>",
    r"<Description>.*?</Description>": f"<Description>{DESCRIPTION}</Description>",
    r"<Copyright>.*?</Copyright>": "<Copyright>Copyright SportsFoundry</Copyright>",
    r"<RepositoryUrl>.*?</RepositoryUrl>": f"<RepositoryUrl>{REPO}.git</RepositoryUrl>",
}
for pattern, replacement in replacements.items():
    text = re.sub(pattern, replacement, text, flags=re.DOTALL)
if "<PackageLicenseExpression>" not in text:
    text = text.replace("</PropertyGroup>", "  <PackageLicenseExpression>Apache-2.0</PackageLicenseExpression>\n    <PackageProjectUrl>https://sportsfoundry.app</PackageProjectUrl>\n  </PropertyGroup>", 1)
csproj.write_text(text, encoding="utf-8")
