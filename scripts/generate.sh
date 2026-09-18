#!/usr/bin/env bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

rm -rf generated
mkdir -p generated
CLI=(npx --yes @openapitools/openapi-generator-cli@2.41.0)
SPEC=openapi/public-v1.json
VERSION=0.1.0-alpha.1
COMMON=(--git-host github.com --git-user-id SportsFoundry --git-repo-id sdks)

"${CLI[@]}" generate -g typescript-fetch -i "$SPEC" -o generated/typescript "${COMMON[@]}" \
  --additional-properties="npmName=@sportsfoundryapp/sdk,npmVersion=$VERSION,supportsES6=true,typescriptThreePlus=true,licenseName=Apache-2.0"

"${CLI[@]}" generate -g python -i "$SPEC" -o generated/python "${COMMON[@]}" \
  --additional-properties="packageName=sportsfoundry,projectName=sportsfoundry,packageVersion=0.1.0a1,packageUrl=https://github.com/SportsFoundry/sdks"

"${CLI[@]}" generate -g java -i "$SPEC" -o generated/java "${COMMON[@]}" \
  --additional-properties="groupId=app.sportsfoundry,artifactId=sportsfoundry-java,artifactVersion=$VERSION,invokerPackage=app.sportsfoundry,apiPackage=app.sportsfoundry.api,modelPackage=app.sportsfoundry.model,library=native,artifactUrl=https://github.com/SportsFoundry/sdks,developerName=SportsFoundry,developerOrganization=SportsFoundry,developerOrganizationUrl=https://sportsfoundry.app,licenseName=Apache-2.0,licenseUrl=https://www.apache.org/licenses/LICENSE-2.0.html,scmConnection=scm:git:https://github.com/SportsFoundry/sdks.git,scmDeveloperConnection=scm:git:ssh://git@github.com/SportsFoundry/sdks.git,scmUrl=https://github.com/SportsFoundry/sdks"

"${CLI[@]}" generate -g csharp -i "$SPEC" -o generated/dotnet "${COMMON[@]}" \
  --additional-properties="packageName=SportsFoundry,packageVersion=$VERSION,targetFramework=net8.0,licenseId=Apache-2.0,packageAuthors=SportsFoundry,packageTags=SportsFoundry;sports;api"

python3 scripts/normalize-package-metadata.py
