import subprocess

# Dono bots ko ek saath start karne ke liye
subprocess.Popen(["python", "app.py"])
subprocess.Popen(["python", "telegram_bot.py"])

# Render ko zinda rakhne ke liye infinite loop
while True:
    pass
