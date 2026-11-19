# Settings in release v0.9.0

This is the settings screen as `v0.9.0` shipped it. Later builds moved the
expert-only options into a collapsed *Advanced* group; the preference keys, their
defaults and what each one does are unchanged — only the place on the screen
moved.

In `v0.9.0` everything network-related was one flat list under **Network**:

| Group | Items in v0.9.0 |
| --- | --- |
| Appearance | *Dynamic color (Material You)*, *Show server address*, *Live traffic* |
| Network | *Split tunneling*, *Blocked traffic*, *Bypass local network*, *Tunnel MTU*, *TCP buffer per connection*, *Disable path MTU discovery*, *Answer ping locally*, *Answer DNS in the tunnel*, *Custom DNS server*, *Test latency on launch* |
| Diagnostics | *Test tunnel*, *Export logs* |
| About | *About* |

From the release after `v0.9.0`, *Network* keeps only *Split tunneling*,
*Blocked traffic*, *Bypass local network* and *Tunnel MTU*; the rest is under
**Network → Advanced**, which starts collapsed. Nothing else about a setting
changed, so a device that upgrades keeps every value it had: the underlying keys
are the same.
