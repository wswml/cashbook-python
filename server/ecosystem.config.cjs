module.exports = {
  apps: [{
    name: 'cashbook',
    script: 'main.py',
    interpreter: 'python3',
    env: {
      DATABASE_URL: 'mysql+pymysql://cashbook:REDACTED@127.0.0.1:3306/cashbook?charset=utf8mb4',
      DEEPSEEK_API_KEY: 'sk-REDACTED'
    }
  }]
}
