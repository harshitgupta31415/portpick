# Contributing to portpick

Contributions should keep portpick deterministic, cross-platform, and safe under concurrent local development.

## Local checks

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
```

Networking changes must include tests that release every socket they open. Avoid assumptions about a specific host, interface, or ephemeral-port range. Changes to selection order, exclusions, IPv6 handling, or JSON output should be called out explicitly in the pull-request description.

The project intentionally has no runtime dependencies; discuss any proposed dependency before adding it.
