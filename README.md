# Event Driven Microservices
Event driven microservice architecture - Python Flask Docker RabbitMQ React

## Commands
```bash
# install packages in pipenv using pipenv instead of pip
pipenv install django

# make requirements.txt from Pipfile
pipenv run pip freeze > requirements.txt

# to check if compose file is made correctly 
docker-compose config

# to start containers from docker compose
docker-compose up

# start container in detached mode
docker-compose up -d

# to stop containers from docker compose
docker-compose down
```

## Results

- Output after starting containers from docker compose 
	```bash
	((event_driven_microservices_python) )  $ docker ps
	CONTAINER ID   IMAGE           COMMAND                  CREATED          STATUS          PORTS                                       NAMES
	8e3d76363096   admin_backend   "python manage.py ru…"   11 minutes ago   Up 11 minutes   0.0.0.0:8000->8000/tcp, :::8000->8000/tcp   admin_backend_1
	```
	If it's not a detached terminal then the containers will come down to halt as soon we close the terminal with `docker-compose up` command. 
	We can access the django homepage at `localhost:8000`

- If we choose latest mysql version in docker compose then we can directly connect with mysql running inside container from localhost.
	```bash
	mysql -uroot -proot -P33066 -h 127.0.0.1
	```
	another way is to enter into container and use the regular command to connect to mysql.
	```
	 $ docker exec -it admin_db_1 bash
	root@22e70d1c7ab5:/# mysql -u'root' -p'root'
	```

- If a file is created in docker container then it is assigned o docker_user but we can change it's ownership in host.
```
rwxrwxr-x. 1 himanshu         himanshu          661 Feb 23 17:08 manage.py*
drwxr-xr-x. 4 root             root             4096 Feb 26 16:08 products/
-rw-rw-r--. 1 himanshu         himanshu          259 Feb 23 21:00 requirements.txt
 $ sudo chown -R $USER:$USER products/
[sudo] password for himanshu: 
 $ ll
drwxrwxr-x. 3 himanshu         himanshu         4096 Feb 26 11:02 admin/
-rw-rw-r--. 1 himanshu         himanshu         1223 Feb 26 15:24 docker-compose.yml
-rw-rw-r--. 1 himanshu         himanshu          144 Feb 24 03:01 Dockerfile
drwxr-xr-x. 4 himanshu         himanshu         4096 Feb 26 16:08 products/
```

- While creating `main` app the Dockerfile is same as it was in `admin` app. But compose file need updates like changing of ports.

- Some of the packages used in `main` are not supported now so the issue comes in makeing migrations of flask models. Use exact requirements.txt

- After starting `docker-compose` for `main` app. Enter into backend service container and execute below command to make migrations and apply them to database service.
```bash
root@069dc17d198d:/app# python manager.py db init
  Creating directory /app/migrations ...  done
  Creating directory /app/migrations/versions ...  done
  Generating /app/migrations/README ...  done
  Generating /app/migrations/alembic.ini ...  done
  Generating /app/migrations/script.py.mako ...  done
  Generating /app/migrations/env.py ...  done
  Please edit configuration/connection/logging settings in '/app/migrations/alembic.ini'
  before proceeding.
root@069dc17d198d:/app# python manager.py db migrate
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'product'
INFO  [alembic.autogenerate.compare] Detected added table 'product_user'
  Generating /app/migrations/versions/f48cea754e19_.py ...  done
root@069dc17d198d:/app# python manager.py db upgrade
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> f48cea754e19, empty message
```

- To run a rabbitmq container
```bash
$ docker run -d --hostname rabbitmq-host --name rabbitmq -e RABBITMQ_DEFAULT_USER=admin -e RABBITMQ_DEFAULT_PASS=admin -p 5672:5672 -p 15672:15672 rabbitmq:3.9-management
```
