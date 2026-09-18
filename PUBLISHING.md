# Publishing SportsFoundry SDKs

Package publication is intentionally separate from pull-request CI.

The only publishing workflow is `.github/workflows/release.yml`, invoked manually with one native registry at a time.

## Trusted publishers

Use GitHub repository `sportsfoundry/sdks` and workflow `release.yml`.

- npm: `@sportsfoundryapp/sdk`
- PyPI: `sportsfoundry`
- NuGet: `SportsFoundry`

npm, PyPI and NuGet use GitHub OIDC/trusted publishing. Do not add long-lived registry tokens to this repository for those registries.

NuGet additionally needs repository variable `NUGET_USER`, set to the nuget.org profile username (not an email address).

## Maven Central

Maven Central currently requires Central user-token credentials plus a GPG/PGP signing key.

Repository secrets used by the release workflow:

- `CENTRAL_TOKEN_USERNAME`
- `CENTRAL_TOKEN_PASSWORD`
- `MAVEN_GPG_PRIVATE_KEY`
- `MAVEN_GPG_PASSPHRASE`

The public half of the signing key must be distributed to a supported keyserver before publishing.

## Release discipline

Versions are immutable once public. Generate and validate the package set in CI before invoking any registry publishing job. If a published alpha needs correction, publish a later alpha rather than attempting to replace it.
