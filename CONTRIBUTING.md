# Contributing

## Dev env setup

1. Clone the project
2. Create a virtualenv
3. pip install -e .[test]

## Launch tests

With pytest:
```bash
pytest tests
```

With tox:
```bash
tox
```

## Update version (maintainers only)

Use [bump2version](https://github.com/c4urself/bump2version) (tip, use: `make bump`)
in order to change version number and update it in all needed files.

Remember to update [CHANGELOG.md](./CHANGELOG.md)
