import socket
import unittest

from portpick.core import PortRangeError, find_available_ports, is_available, reserve_port


class PortPickTests(unittest.TestCase):
    def test_reserved_port_is_not_reported_available(self) -> None:
        with reserve_port() as (port, sock):
            sock.listen(1)
            self.assertFalse(is_available("127.0.0.1", port))

    def test_finds_a_port_and_honours_exclusions(self) -> None:
        with reserve_port() as (first, _):
            start = max(1024, first - 2)
            end = min(65535, first + 2)
            ports = find_available_ports(start, end, exclude={first})
            self.assertNotEqual(ports[0], first)

    def test_can_find_multiple_distinct_ports(self) -> None:
        ports = find_available_ports(40000, 50000, count=3)
        self.assertEqual(len(ports), 3)
        self.assertEqual(len(set(ports)), 3)

    def test_rejects_invalid_ranges(self) -> None:
        with self.assertRaises(PortRangeError):
            find_available_ports(4000, 3000)
        with self.assertRaises(PortRangeError):
            find_available_ports(0, 10)


if __name__ == "__main__":
    unittest.main()
