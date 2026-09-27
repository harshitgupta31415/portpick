from __future__ import annotations

from contextlib import contextmanager
import socket
from collections.abc import Iterator


class PortRangeError(ValueError):
    """Raised when a requested range cannot produce enough ports."""


def _validate_port(port: int) -> None:
    if not 1 <= port <= 65535:
        raise PortRangeError(f"port must be between 1 and 65535: {port}")


def _socket_family(host: str) -> socket.AddressFamily:
    return socket.AF_INET6 if ":" in host else socket.AF_INET


def is_available(host: str, port: int) -> bool:
    _validate_port(port)
    sock = socket.socket(_socket_family(host), socket.SOCK_STREAM)
    try:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 0)
        sock.bind((host, port))
        return True
    except OSError:
        return False
    finally:
        sock.close()


def find_available_ports(
    start: int = 3000,
    end: int = 3999,
    *,
    host: str = "127.0.0.1",
    count: int = 1,
    exclude: set[int] | None = None,
) -> list[int]:
    _validate_port(start)
    _validate_port(end)
    if end < start:
        raise PortRangeError("end port must be greater than or equal to start port")
    if count < 1:
        raise PortRangeError("count must be at least 1")

    blocked = exclude or set()
    selected: list[int] = []
    for port in range(start, end + 1):
        if port not in blocked and is_available(host, port):
            selected.append(port)
            if len(selected) == count:
                return selected

    raise PortRangeError(
        f"could not find {count} available port{'s' if count != 1 else ''} in {start}-{end}"
    )


@contextmanager
def reserve_port(host: str = "127.0.0.1", port: int = 0) -> Iterator[tuple[int, socket.socket]]:
    """Hold a TCP port for the lifetime of a context.

    Passing port 0 lets the operating system choose an ephemeral port. The
    bound socket is returned so callers can listen on it or pass its descriptor
    to a child process without a time-of-check/time-of-use race.
    """

    if port:
        _validate_port(port)
    sock = socket.socket(_socket_family(host), socket.SOCK_STREAM)
    try:
        sock.bind((host, port))
        selected = int(sock.getsockname()[1])
        yield selected, sock
    finally:
        sock.close()


@contextmanager
def reserve_ports(
    count: int,
    host: str = "127.0.0.1",
) -> Iterator[list[tuple[int, socket.socket]]]:
    """Reserve several distinct ephemeral TCP ports as one atomic resource.

    Every returned socket remains bound until the context exits. If any bind
    fails, sockets opened earlier in the operation are still closed.
    """

    if count < 1:
        raise PortRangeError("count must be at least 1")

    reservations: list[tuple[int, socket.socket]] = []
    try:
        for _ in range(count):
            sock = socket.socket(_socket_family(host), socket.SOCK_STREAM)
            sock.bind((host, 0))
            reservations.append((int(sock.getsockname()[1]), sock))
        yield reservations
    finally:
        for _, sock in reversed(reservations):
            sock.close()
