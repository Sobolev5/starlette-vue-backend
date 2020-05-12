# starlette-vue

Starlette-Vue is a simple example that allows you to quickly get started 
with the Starlette framework "the same as Django structure" with Vue.js frontend.

Starlette part (https://github.com/Sobolev5/starlette-vue-backend):
  - JWT authentication middleware with token refresh view
  - Extended User model
  - Register and login views
  - Tortoise ORM 

Vue.js part (https://github.com/Sobolev5/starlette-vue-frontend):
  - Vuex JWT authentication
  - Register and login views (with Starlette backend)
  - Bootstrap 4 on board
  - SB admin 2 on board 


# starlette-vue backend part

Make virtualenv, clone this project, modify .env.example and rename it.

```sh
$ python3.8 -m venv starlette_django_env
$ source starlette_django_env/bin/activate
$ git clone https://github.com/Sobolev5/starlette-vue-backend
$ cd starlette-vue-backend
$ pip install -r requirements.txt
$ nano .env.example
$ mv .env.example .env
$ pre-commit install
```

Run the project.

```sh
$ uvicorn app:entry_point --reload --port 9090
```

Open your browser at http://localhost:9090 and see response from the main endpoint of Starlette.













