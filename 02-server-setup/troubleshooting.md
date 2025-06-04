# Server Setup Troubleshooting

> **Status**: Documentation in progress
>
> Common issues and solutions for Matrix Online server setup.

## Connection Issues

### "Cannot connect to auth server"
**Symptoms**: Client hangs at login screen

**Solutions**:
1. Check firewall settings
2. Verify auth server is running: `tasklist | findstr Auth`
3. Test port accessibility: `telnet localhost 10000`
4. Check client patches are applied correctly

### "Database connection failed"
**Symptoms**: Server crashes on startup

**Solutions**:
1. Verify MySQL is running: `net start mysql`
2. Check database credentials in config
3. Ensure database exists: `SHOW DATABASES;`
4. Test connection: `mysql -u root -p`

### "World server timeout"
**Symptoms**: Login works but world won't load

**Solutions**:
1. Check world server status
2. Verify world database population
3. Check character creation process
4. Review world server logs

## Performance Issues

### High CPU Usage
- Check for infinite loops in server code
- Monitor player count vs server capacity
- Review database query efficiency

### Memory Leaks
- Restart server regularly during testing
- Monitor memory usage patterns
- Check for unclosed database connections

## Client Issues

### Patch Failures
- Verify patch server accessibility
- Check file permissions
- Review client version compatibility

### Graphics/Display Problems
- Update graphics drivers
- Check compatibility mode settings
- Verify DirectX installation

## Common Error Messages

### "LTLO_NOAUTHSERVERADDR"
- Auth server address not configured properly
- Check client patches
- Verify DNS resolution

### "LTAS_USERNAMEPASSWORDMISMATCH"  
- Account doesn't exist in database
- Password hash mismatch
- Database corruption

## Debug Tools

### Server Logging
Enable detailed logging in server configuration for troubleshooting.

### Network Monitoring
Use Wireshark or similar tools to monitor network traffic.

### Database Tools
Use MySQL Workbench or command line tools for database debugging.

---

[← Back to Server Setup](index.md) | [Community Support →](../08-community/index.md)