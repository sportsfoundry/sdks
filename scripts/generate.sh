#!/usr/bin/env bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

rm -rf generated
mkdir -p generated
CLI=(npx --yes @openapitools/openapi-generator-cli@2.41.0)
SPEC=openapi/public-v1.json
VERSION=0.1.0-alpha.1

"${CLI[@]}" generate -g typescript-fetch -i "$SPEC" -o generated/typescript \
  --additional-properties="npmName=@sportsfoundryapp/sdk,npmVersion=$VERSION,supportsES6=true,typescriptThreePlus=true"

"${CLI[@]}" generate -g python -i "$SPEC" -o generated/python \
  --additional-properties="packageName=sportsfoundry,projectName=sportsfoundry,packageVersion=0.1.0a1"

"${CLI[@]}" generate -g java -i "$SPEC" -o generated/java \
  --additional-properties="groupId=app.sportsfoundry,artifactId=sportsfoundry-java,artifactVersion=$VERSION,invokerPackage=app.sportsfoundry,apiPackage=app.sportsfoundry.api,modelPackage=app.sportsfoundry.model,library=native"

"${CLI[@]}" generate -g csharp -i "$SPEC" -o generated/dotnet \
  --additional-properties="packageName=SportsFoundry,packageVersion=$VERSION,targetFramework=net8.0"
