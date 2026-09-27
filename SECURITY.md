# Security policy

Security fixes target the latest release on the default branch.

Use GitHub's private vulnerability reporting for issues involving unintended network exposure, unsafe host binding, socket lifecycle errors, or command-line injection. Include the operating system, Python version, host/range arguments, and a minimal reproduction.

portpick only finds or reserves local TCP ports; it does not configure firewalls or make a service safe for public exposure.
