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
4. Add at least one test case in your  `__tests` folder. See the [Testing](#testing) section for details.
5. Open a pull request to this repository, following the PR template.
6. Once merged, your package will be available to all Quarkdown users.

Optimally, a submitted package's structure should be as follows:

```
my-package/
    1.0.0/
        __tests/
        atom.toml
        main.qd
        ...other source files...
        README.md
```

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

## Updating a package

This repository strictly enforces frozen versions of packages. In order to update a package, a new version must be created.

If you want to update `my-package` from version `1.0.0` to `1.1.0`, create a new folder `my-package/1.1.0` and copy the contents of `my-package/1.0.0` into it. Then, make your changes in the new folder, and follow the same [publishing steps](#publishing-a-package) to submit the new version.