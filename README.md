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
Create a network for to which rabbitmq container can be attached.
```bash
$ docker network create rabbitmq_network
40ffe55bf076ed16f102efdc6de398cffd69e2052579f12aa2ccf06fad33ec41
$ docker network ls
NETWORK ID     NAME               DRIVER    SCOPE
b583128f4fa1   admin_default      bridge    local
4654075b5176   bridge             bridge    local
cc30fcb154e5   host               host      local
61225df90f5a   main_default       bridge    local
a719b9b7a55c   none               null      local
40ffe55bf076   rabbitmq_network   bridge    local
```
We do have `main_default` and `admin_default` network which got created with docker compose of `main` and `admin` app. But we can't connect rabbitmq container to two network at a time so we have to create a seperaete network for connecting all three.
```bash
$ docker run -d --hostname rabbitmq-host --name rabbitmq --network rabbitmq_network -e RABBITMQ_DEFAULT_USER=admin -e RABBITMQ_DEFAULT_PASS=admin -p 5672:5672 -p 15672:15672 rabbitmq:3.9-management
```
We need to attach rabbitmq container to same network bridge in which container which is requesting for connection is present. Then the container making request can directly mention host as `rabbitmq` (name of rabbitmq container).

Update the `docker-compose` files of **admin** and **main** app as well. So that they connect to `rabbitmq_network`.

For more refer: https://docs.docker.com/compose/networking/

- For API call to happen between `admin` and `main` app. We should have both services on same network and hostname of these services should not have `_` in name like `admin_app` (as django do not recognize them as host).

```bash
# create a network
docker network create product_level_network
# attach it to both the services
docker network connect product_level_network main_backend_1
docker network connect product_level_network admin_backend_1
# now these services can communicate with each other try by curl command from one container to another
# use host name of another container 
```

- For connecton of main app to admin app. We assigned a hostname to admin app and use to refer the admin app API.
```bash
http://adminApp:8000/api/user'
```
