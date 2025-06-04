# Server Setup FAQ

> **Status**: Documentation in progress
>
> Frequently asked questions about running Matrix Online servers.

## General Questions

### Q: Which server should I choose?
**A**: For beginners, start with **MXOEmu** for stability. For developers wanting latest features, try **Hardline Dreams**.

### Q: Can I run a server on Linux?
**A**: Currently, both major servers require Windows. Linux support may be possible with Wine but is not officially supported.

### Q: How many players can a server handle?
**A**: Typically 10-50 concurrent players depending on hardware. The original game supported hundreds but emulators have limitations.

### Q: Is combat implemented?
**A**: No, combat is not implemented in any current server. This is the biggest missing feature.

## Technical Questions

### Q: What database is required?
**A**: MySQL 5.7+ is recommended. MariaDB also works.

### Q: Can I customize the game world?
**A**: Limited customization is possible. You can modify NPCs, items, and some locations but major world changes require significant development.

### Q: How do I add new players?
**A**: Create accounts directly in the database or use admin commands if available.

### Q: Can I backup my server?
**A**: Yes, backup your database regularly and keep copies of your configuration files.

## Legal Questions

### Q: Is running a server legal?
**A**: Server emulation for preservation/education is generally considered fair use, but you should only allow players who own legitimate copies of the game.

### Q: Can I charge for access?
**A**: No, do not charge money for server access. This should be a free preservation effort only.

### Q: Can I modify the client?
**A**: Minor patches for connectivity are acceptable, but major modifications could raise legal concerns.

## Setup Questions

### Q: How long does setup take?
**A**: Expect 2-4 hours for a basic setup, longer if you encounter issues or want advanced configuration.

### Q: Do I need a static IP?
**A**: Not required but recommended. Dynamic DNS services can work for home servers.

### Q: What ports need to be open?
**A**: Typically 10000-10002 for the server components. See [Network Setup](network-setup.md) for details.

## Troubleshooting

### Q: My server won't start
**A**: Check the [Troubleshooting Guide](troubleshooting.md) for common solutions.

### Q: Players can't connect
**A**: Verify firewall settings, port forwarding, and that the server is actually running.

### Q: Database errors on startup
**A**: Ensure MySQL is running and credentials are correct in your config files.

## Community

### Q: Where can I get help?
**A**: Join the [community Discord](https://discord.gg/3QXTAGB9) or check [community resources](../08-community/index.md).

### Q: How can I contribute?
**A**: See the [contribution framework](../08-community/contribution-framework.md) for ways to help.

### Q: Are there other servers running?
**A**: Yes, check the community for lists of active servers and their status.

---

[← Back to Server Setup](index.md) | [Troubleshooting →](troubleshooting.md)