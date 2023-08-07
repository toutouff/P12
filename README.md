# P12

## installation 

* clone the repository in the desired directory and go in it
* then create a virutal environement with the foolowing command
  python3 -m venv venv
* you need to activate it with
source venv/bin/activate
> to exit the environement type deactivate
* intall the dependencies with
  pip install -r requirement.txt

start your postgres server with the app or method of choice 
i use postgress app on mac 
with the default db as 
username postgres
password postgres 

* run server with
python3 manage.py runserver

## accessing the admin page 
go to http://localhost/admin
default admin user is 
username admin 
password admin 
you can change the password of the admin user within the admin page 
just edit the admin user and then use 'the hash password so user can login' action 
here you go you have the running server 

to populate the db you can use the admin page or the server api endpoint within the DRF's page or postman 

the method of authentification is a basic auth so pass your crendidential within postman Authorization page 
here you have the application running 
