# Poke Trainers

This application expose a simple API to create trainers, teams, manage pokemons and their abilities.

NOTE: all the steps, commands and more, are intended to be executed in a linux based operating system.

## Build and Run

There are two approaches you can use to run this project. First, you can use Docker with the provided Dockerfile which already has the minimum configuration for the project deployment. On the other hand, you can manually configure a python environment on your machine and run the application.

### First steps and requirements
- Clone the git repository to a local directory
`$ git clone https://github.com/ruizcauich/poketrainers.git`

- If you are going to run manually, make sure of having a python3.8+ version installed on your machine.


### Using Docker
There is a Dockerfile you can use to build and run the application, lets look at this example of how to build and run.

1. From your terminal, move to the repo directory

`$  cd path/to/directory/poketrainers`

2. Build the docker image

`$ docker build -t poketrainers .`

3. Run the docker image

`$docker run --name poketrainers -p 8000:8000 -d poketrainers`

4. Open your browser and go to http://localhost:8000

NOTE: The docker approach uses a sqlite3 database, but the project is prepared to run with MySQL too.

There are some environment variables you can set to the **docker run** command in order to customize some configurations.

- SECRETE_KEY: If not provided to the run command, the dockerfile sets a development and insecure secret key
- DEBUG: Default is True, you can provide False
- DATABASE_URL: Uses the django-environ database url fashion, [click here to learn more.](https://django-environ.readthedocs.io/en/latest/types.html)


### Run manually
If your choice is to run manually, follow the these steps:

1. One inside the project directory (poketrainers), create a new virtual environment (You need python3.8 to run this project) and activate it.
```
$ python -m venv venv
$ source venv/bin/activate
```

2. Use pip to install the required packages
`$ pip install -r requirements.txt`

3. To avoid setting manually the environment variables need by the settings, create a .env file inside of the sub directory poketrainers, at the same level of the settings.py file as you can see below.

```
.
├── api/
├── core/
├── db.sqlite3
├── Dockerfile
├── manage.py
├── poketrainers/
│   ├── asgi.py
│   ├── __init__.py
│   ├── settings.py
│   ├── .env
│   ├── urls.py
│   └── wsgi.py
├── README.md
└── requirements.txt
```

4. Copy the next lines to set the environment variables values.
```
SECRET_KEY=django-insecure-4a-l)zxb%!3)3q*a%62!yaa74#ds6@qe%@@n-4-%r_zcnsn60!
DEBUG=True
```
 If you are going to use MySQL as the RDBMS, set the **DATABASE_URL** environment variable, as:
`DATABASE_URL=mysql://user:password@127.0.0.1:3306/dbname`


5. Run the following commands to migrate the models and fetch initial data from the pokeapi.co API
```
$ python manage.py migrate
$ python manage.py get_pokemons
```
Optionally you can pass **--limit** parameter to the **get_pokemons** command in order to fetch a custom amount of pokemons from the API, you can not fetch more than 100 pokemons. Default amount is 20.

6. Finally run the development server:
`$ python manage.py runserver 0:8000`



NOTE: If you are USING MYSQL as RDBMS, make sure that the target database already has been created, django does not create a database by default. If you are using sqlite3 (default database), django creates the db file.


## Poketrainers API usage documentation.

### URL mapping

Here are the endpoints of the Poketrainers API

| Endpoint | Methods | Description | Request body |
|------------|-----------|---------------|-----------------|
|/api/ | GET | API root, returns the 3 base endpoints |   |
|/api/trainers/ | GET, POST | On GET returns the registered trainers, on POST create a trainer | { "name": "", "hometown": "" }|
|/api/trainers/<trainer_id>/| GET, PUT, PATCH, DELETE | Get, update or delete a single trainer | On PUT the same as POST on /trainers/. On PATCH any of the fields can be omitted.|
|/api/pokemon/ |  GET, POST |  On GET returns the registered pokemon, on POST create a pokemon. On POST, the abilities field can be an empty list but is required. | { "name": "bulbasaur", "height": 7, "weight": 69, "abilities":[ {"name": "overgrow"}, {"name": "chlorophyll"} ] } |
|/api/pokemon/<pokemon_id>/ | GET, PUT, PATCH, DELETE | Get, update or delete a single pokemon | On PUT the same as POST on /pokemon/. On PATCH any of the fields can be omitted.|
|/api/teams/ |  GET, POST |  On GET returns the registered teams, on POST create a team. On POST, the pokemons field can be omtted but not empty.| { "owner": "http://localhost:8000/api/trainers/1/", "pokemons":[] } |
|/api/teams/<team_id>/ | GET, PUT, PATCH, DELETE | Get, update or delete a single team | On PUT the same as POST on /teams/. On PATCH any of the fields can be omitted.|
|/api/teams/<team_id>/pokemon/ | GET, POST | On GET returns the related pokemons, on POST create a new Pokemon and associate it to the team. | On POST the same as on /api/pokemon/ |
|/api/teams/<team_id>/pokemon/<pokemon_id> | DELETE | Removes the pokemon from the relation, it does not deletes the pokemon from the database. | |



### Example
In order to illustrate some examples, wget will be used.

1. Create a pokemon trainer
```
wget -O - --post-data '{ "name": "Ash Ketchum", "hometown": "Pallete Town" }'   \
     --header='Content-Type:application/json'   \
     http://localhost:8000/api/trainers/
```

2. Create a team WITHOUT pokemons, we need the url of the previous registered trainer.
```
wget -O - --post-data '{ "owner": "http://localhost:8000/api/trainers/1/" }'   \
     --header='Content-Type:application/json'   \
     http://localhost:8000/api/teams/
```
3. If you have executed the *python manage.py get_pokemons*, you already have available some pokemons. If not, lets create one using the /api/teams/<team_id>/pokemon/ endpoint.
```
wget -O - --post-data ' { "name": "bulbasaur", "height": 7, "weight": 69, "abilities":[ {"name": "overgrow"}, {"name": "chlorophyll"} ] }'   \
     --header='Content-Type:application/json'   \
     http://localhost:8000/api/teams/1/pokemon/
```

4. You can fetch data from the endpoints executing wget like:
```
wget -O - --header='Content-Type:application/json'        http://localhost:8000/api/teams/1/
```

NOTE: If you try to register more than 6 pokemons, with either /teams/, /teams/<team_id> or the /teams/<team_id>/pokemon/, you **will get a 400 Bad Request error, since the team is limited to 6 pokemons.**