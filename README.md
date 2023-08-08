# P12

## installation 

* clone the repository in the desired directory and go in it with
  ```
  cd EPICEvents
  ```
* start the docker container with
  ```
  docker compose up --detach
  ```
* check that container a running
  ```
  docker ps
  ```
  > you should see someting like this
  ```
  CONTAINER ID   IMAGE            COMMAND                  CREATED          STATUS          PORTS                    NAMES 
  27919cbdabad   epicevents-web   "python manage.py ru…"   44 seconds ago   Up 23 seconds   0.0.0.0:8000->8000/tcp   epicevents-web-1
  9d539fa62040   postgres:15      "docker-entrypoint.s…"   2 minutes ago    Up 24 seconds   0.0.0.0:5432->5432/tcp   postgres15
  ```
> you need the name of the EPICEvent service here it's 'epicevents-web-1'
* if its the first time running the app  you need to : 
  - make migration

  ```
  docker exec epicevents-web-1 python manage.py makemigrations
  ```

  -  migrate

  ```
  docker exec epicevents-web-1 python manage.py migrate

  ```
  -  populate the db form initial_db.json

  ```
  docker exec epicevents-web-1 python manage.py loaddata initial_db.json
  ```

## accessing the admin page 
go to http://localhost:8000/admin
default admin user is 
username admin 
password admin 
you can change the password of the admin user within the admin page 
just edit the admin user and then use 'the hash password so user can login' action 

*here you go you have the running server*
