# P12

## installation 

* clone the repository in the desired directory and go in it with
  cd EPICEvents
* start the docker container with
  docker compose up
* if its the first time startting you need to
* make migration
  docker exec epicevents-web-1 python manage.py makemigrations
*  migrate
  docker exec epicevents-web-1 python manage.py migrate
*  populate the db form initial_db.json
  docker exec epicevents-web-1 python manage.py loaddata initial_db.json 

## accessing the admin page 
go to http://localhost/admin
default admin user is 
username admin 
password admin 
you can change the password of the admin user within the admin page 
just edit the admin user and then use 'the hash password so user can login' action 
here you go you have the running server
