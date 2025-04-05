# Versioning Scheme

This document outlines the versioning scheme used in the `pygenutils` package.

## Version Format

The package follows semantic versioning (SemVer) with the format `vX.Y.Z`

Where:

- **X** (Major): Incremented when making incompatible API changes or significant structural modifications
- **Y** (Minor): Incremented when adding functionality in a backward-compatible manner
- **Z** (Patch): Incremented when making backward-compatible bug fixes or minor improvements

## Version Components

### Major Version (X)

The major version number is incremented when:

- Breaking changes are introduced that are incompatible with previous versions
- Significant structural changes are made to the package
- Major refactoring of code or architecture occurs
- Sub-packages are moved to separate packages
- Package name changes occur

Examples from our history:

- v14.0.0 → v15.0.0: Package renamed from `pyutils` to `pygenutils`
- v13.0.0 → v14.0.0: Function renames and terminology updates
- v12.0.0 → v13.0.0: File operations refactoring

### Minor Version (Y)

The minor version number is incremented when:

- New features are added in a backward-compatible manner
- New modules or sub-packages are introduced
- Significant enhancements to existing functionality are made
- New dependencies are added

Examples from our history:

- v15.7.0 → v15.8.0: Added dynamic file discovery in audio and video manipulation
- v15.6.0 → v15.7.0: Added base conversion utilities and array flipping functions

### Patch Version (Z)

The patch version number is incremented when:

- Bug fixes are made
- Minor improvements to existing functionality occur
- Documentation updates are made
- Code optimisations that don't affect functionality are implemented
- Variable or function name changes for clarity are made

Examples from our history:

- v15.7.6 → v15.7.7: Terminology updates for better clarity
- v15.7.5 → v15.7.6: Minor syntax improvements

## Pre-release Versions

For pre-release versions, we may use the following suffixes:

- `alpha`: For early testing
- `beta`: For beta testing
- `rc`: For release candidates
- `dev`: For development versions

Example: `v15.8.0-beta.1`

## Version History

The complete version history can be found in the [CHANGELOG.md](CHANGELOG.md) file.

## Best Practices

1. **Backward Compatibility**:
   - Minor and patch versions must maintain backward compatibility
   - Breaking changes should be reserved for major version increments

2. **Documentation**:
   - All version changes must be documented in the CHANGELOG.md
   - Breaking changes should be clearly marked
   - Migration guides should be provided for major version changes

3. **Release Process**:
   - Each release should be tagged in the repository
   - Release notes should be created for each version
   - Dependencies should be updated as needed

4. **Testing**:
   - All changes should be tested before release
   - Breaking changes should include migration tests
   - Regression tests should be maintained

## Version Decision Process

When deciding which version number to increment:

1. **Major (X)**:
   - Does this change break existing functionality?
   - Does this require significant changes to user code?
   - Does this change the package structure?

2. **Minor (Y)**:
   - Does this add new functionality?
   - Is it backward compatible?
   - Does it introduce new dependencies?

3. **Patch (Z)**:
   - Is this a bug fix?
   - Does it improve existing functionality without breaking changes?
   - Is it a documentation or code style update?
