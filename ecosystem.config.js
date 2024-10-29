module.exports = {
  apps: [{
    name: 'trading-bot-monitor',
    script: 'monitoring.sh',
    watch: false,
    cron_restart: '0 * * * *',
    autorestart: false
  }]
}