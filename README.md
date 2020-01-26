
# Register new user 

http://www.drainware.com/ddi/?module=cloud&action=registerUser

# Notes

PHP doesnt like now pass variables by reference, it always pass variables by reference

We have to change func(&$var) by func($var)

# TODO

- Add /opt/drainware/scripts, sudo and setup sudoers
- Add dependencias (ssdeep, 7z, cat-doc, ...)
- Detect missing date in mongo schema
- identify mapreduce scripts
- Identify cron tasks to deploy in Jenkins
- Identify python daemons
- Integrate paypal
- scale mongo
- scale rabbitmq
- enable ssl for web

# Tests

- http://www.drainware.com/ddi/?module=main&action=showWireTransfer pass=SuP3rP455W0rD
- Email communications
- Cron tasks
- AMQP communications
- Windows client dlp
- Windows client sandbox
- Windows client inspector
- Windows Client communication
- Windows Update process
- Windows 10
