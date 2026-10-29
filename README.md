# quarkdown/atoms

This repository hosts the official `@atoms` packages for [Quarkdown](https://github.com/iamgio/quarkdown).

To include an atom in your Quarkdown document, call the `.include` function. For example:

```
.include {@atoms/kanban:1.0.0}
```

For more information about Quarkdown packages, see [wiki/Packages](https://quarkdown.com/wiki/packages).

## Publishing a package

0. Set up your package as explained in [wiki/Publishing-packages](https://quarkdown.com/wiki/publishing-packages).
1. Ensure your package works locally.
2. Fork this repository.
3. Add your package as `name/version` folder, e.g. `my-package/1.0.0`.
4. It's recommended to have at least one test case in your  `__tests` folder. See the [Testing](#testing) section for details.
5. Add a `README.md` file
6. Add a `THUMBNAIL.webp` file. It's required for templates and optional for other packages. See the [Thumbnails](#thumbnails) section for details.
7. Open a pull request to this repository, following the PR template.
8. Once merged, your package will be available to all Quarkdown users.

Optimally, a submitted package's structure should be as follows:

```
my-package/
    1.0.0/
        __tests/
        atom.toml
        main.qd
        ...other source files...
        README.md
        THUMBNAIL.webp
```

### Thumbnails

A thumbnail is a `THUMBNAIL.webp` (preferred) or `THUMBNAIL.png` file in the package folder.

- For a template, it's a preview of the template: ideally 794×1123 (an A4 page) for `paged` and `plain` documents, and 1123×705 for `slides` and `docs`.
- For any other package, it's optional: a 2:1 banner, ideally 800×400.

To generate it, run `scripts/images/generate.sh` with a demo document.

```
scripts/images/generate.sh my-package/1.0.0 demo.qd
```

If you use Claude Code, the [`generating-package-images`](.claude/skills/generating-package-images/SKILL.md) skill can also write the demo and run the script for you.

## Testing

`__tests` folders (two underscores) contain test cases for the package. Each test case contains, at minimum, a `main.qd` file and an `expect.html` file. The `main.qd` file is compiled to HTML and asserted against the `expect.html` file.

```
__tests/
    my-test-case/
        main.qd
        expect.html
    my-other-test-case/
        main.qd
        ...other files...
        expect.html
```

From a test case's `main.qd`, the package's main file can be included with a relative path: `.include {../../main.qd}`.

- To run all test cases in the repository, execute `scripts/test.sh` from the root of the repository.
- To run a specific test case, pass its path to the script, e.g. `scripts/test.sh my-package/1.0.0/__tests/my-test-case`.

## Updating a package

This repository strictly enforces frozen versions of packages. In order to update a package, a new version must be created.

If you want to update `my-package` from version `1.0.0` to `1.1.0`, create a new folder `my-package/1.1.0` and copy the contents of `my-package/1.0.0` into it. Then, make your changes in the new folder, and follow the same [publishing steps](#publishing-a-package) to submit the new version.

The only case where a package can be updated in place is for:
- Updates to `README.md` or a `THUMBNAIL` file.
- New test cases in the `__tests` folder.

## Deleting or renaming a package

Published packages can't be deleted or renamed.

The only exception is a severe reason, such as malicious code, a security issue, or a license or legal violation. In that case, please contact us privately in advance.