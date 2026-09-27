# portpick

Find predictable available TCP ports for local development, test suites, and CI
jobs.

```bash
python -m pip install .
portpick
# 3000

portpick --from 8000 --to 8100 --count 3 --separator ","
# 8000,8001,8002
```

## Why another port utility?

Asking the operating system for an ephemeral port is correct inside one
process, but shell scripts and CI workflows often need a human-readable port
from a controlled range. `portpick` provides both workflows:

- A cross-platform CLI with stable output and JSON mode
- A Python context manager that keeps a socket bound, avoiding allocation races
- Explicit ranges, exclusions, IPv4/IPv6 hosts, and multiple-port selection
- No runtime dependencies

## CLI

```bash
portpick --from 3000 --to 3999
portpick --host ::1 --from 8000 --to 9000
portpick --count 2 --exclude 3000 --exclude 3001 --json
```

JSON output:

```json
{"ok": true, "host": "127.0.0.1", "ports": [3002, 3003]}
```

## Python API

Use `reserve_port` when a race-free reservation matters:

```python
from portpick import reserve_port

with reserve_port() as (port, socket):
    socket.listen()
    print(f"reserved {port}")
```

The socket remains bound until the context exits. Advanced callers can pass
its descriptor to a child process or use it directly in a test server.

## Development

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
```

CI runs the suite on Linux, Windows, and macOS.

## License

MIT
