module.exports = {
  apps: [{
    name: 'cashbook',
    script: 'main.py',
    interpreter: 'python3',
    env: {
      DATABASE_URL: 'mysql+pymysql://cashbook:cashbook123@127.0.0.1:3306/cashbook?charset=utf8mb4',
      DEEPSEEK_API_KEY: 'sk-ebc...0846'
    }
  }]
}
