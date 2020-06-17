import os
import subprocess

# # create virtual env
# if not os.path.exists("./venv"):
#     subprocess.call(["mkdir", "venv"])
#     subprocess.call(["virtualenv", "-p", "python3", "venv/"])
#     #os.system('/bin/bash --rcfile activate_venv.sh')
#     subprocess.call('. venv/bin/activate', shell=True)
#     subprocess.call(["pip", "install", "-r", "requirements.txt"])
#     subprocess.call(["pip", "list"])
#
# else:
#     # activate virtualenv
#     #os.system('/bin/bash --rcfile activate_venv.sh')
#     subprocess.call('. venv/bin/activate', shell=True)
#     subprocess.call(["pip", "install", "-r", "requirements.txt"])


# works only when this is run from inside server directory
# creates super user if sqlite database is not found
if not os.path.exists("./db.sqlite3"):
    subprocess.call(["python", "manage.py", "makemigrations"])
    subprocess.call(["python", "manage.py", "migrate"])
    subprocess.call(["python", "manage.py", "createsuperuser2",
                     "--username", "admin",
                     "--password", "adminadmin",
                     "--noinput",
                     "--email", "msg2shanth@gmail.com"
                     ])
