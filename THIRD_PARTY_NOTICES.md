# Third-party notices

SPACX (MIT License) includes the following **direct** Python dependencies declared in [`pyproject.toml`](pyproject.toml). Transitive dependencies are listed in [`docs/DEPENDENCY_LICENSES.md`](docs/DEPENDENCY_LICENSES.md).

| Package | Declared constraint | SPDX / license name | Project URL |
|---------|---------------------|---------------------|-------------|
| **PyYAML** | `>=6.0.2` | MIT | https://pyyaml.org/ |
| **jsonschema** | `>=4.23.0` | MIT | https://github.com/python-jsonschema/jsonschema |
| **pytest** *(dev)* | `>=8.0` | MIT | https://docs.pytest.org/ |

## PyYAML

Copyright (c) 2017–2021 Ingy döt Net  
Copyright (c) 2006–2016 Kirill Simonov

Licensed under the MIT License.

## jsonschema

Copyright (c) 2013 Julian Berman

Licensed under the MIT License.

## pytest

Copyright (c) 2004–2020 Holger Krekel and contributors

Licensed under the MIT License.

---

Full license texts ship with each package on PyPI. Regenerate the complete dependency table:

```bash
pip install -e ".[dev]" pip-licenses
pip-licenses --format=markdown --with-urls > docs/DEPENDENCY_LICENSES.md
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for CI and manual regeneration notes.
