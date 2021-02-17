# Employee-Management-System

Contain Employee Management System Flask REST API

# Setup Env.

pip install requirement.txt

# How to run

python app.py

# credential

1. URL : /setup
   setup is set admin account and return admin login credential
   payload = {
   username : "",
   password : "",
   role : "Admin"
   }

2. URL : /register
   register Hr and generate credential
   payload = {
   username : "",
   password : "",
   role : "Hr"
   }
