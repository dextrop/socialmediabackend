# Social Media Application Backend

The Project is a social media application backend designed using Django and (Django Rest Framework) DRF.
API Included
1. Signup API

## Setup Project

#### 1. Clone

```shell
git clone https://github.com/dextrop/socialmediabackend.git
```

#### 2. Install Dependencies

```shell
make install
```
*Make sure you are using virtual environment with python 3.7+ for the project.*


#### 3. Migrate Database

```shell
make migrate
```

*for the current project we are using sqlite database, external database can also be added.*


#### 4. Create SuperUser

```shell
make createsuperuser
```

*The project requires a super user for creating OAuth Application, We will use the user in django admin to create an OAuth Application*

#### 5. Create OAuth Application

- Make sure migration is done before going through below step.
- Run project using `make run`
- Navigate to [http://localhost:8000/admin/](http://localhost:8000/admin/) and login with your creentials

- Once Logged in Go to application
![admin](images/adminpanel.png)

- Click on create new application and fill the below information
  - `Callback`: `http://localhost:8000/callback`
  - `Client type`: `Confidential`
  - `Authorization grant type`: ` Authorization code`
  - `Skip authorization`: Checked

*make sure you copy client_secret before saving the application*

![admin](images/create_oauth_app.png)

- Create an .env file with below information

```
BASE_URL=http://localhost:8000
OAUTH_CLIENT_SECRET=CLIENT_SECRET
```

Replace the `CLIENT_SECRET` with `client_secret` copied before, also you can replace the base url to IP or domain if the project is hosted on a server.

## Test API's

To test the api's use the postman script provided inside scripts.

**Run project using**
```shell
make run
```


