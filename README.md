# 50-State-Django
All 50 U.S. States and their capital cities. An example written in Python using Django and PostgreSQL.


## Requirements
- Built in Django with a Postgres Database.
- At least two distict Django "apps".
- Initial state and city data populated with data migrations.
- Basic editing of states and cities through Django Admin.
- App is publically hosted on AWS

## Prerequisits
- Docker Desktop (if running app or tests locally)


## Contents
- [Local Setup and Usage](#Local-Setup-and-Usage)
- [Running Tests](#Running-Tests)
- [Deploying to AWS](#Deploying-to-AWS)


### Local Setup and Usage

- **Starting the Docker Container**

  1. With Docker Desktop already running, use the following command to build and start the Docker container:

    ```
    docker-compose up
    ```
  
  2. Once the container is up and running, you should be able to view the app by opening your browser to [http://127.0.0.1](http://127.0.0.1). This will show a list of all 50 states and their capitals.

  3. Next, try using a query string in the URL to just get details on a specific state or capital. 
  
    Use [http://127.0.0.1/?state=SC](http://127.0.0.1/?state=SC) or [http://127.0.0.1/?state=South_Carolina](http://127.0.0.1/?state=South_Carolina) to get details for a specific state. Optionally you can write a state name made up of two words with a space instead of an underscore. The name or abbreviation is not case sensitive.
    
    Use [http://127.0.0.1/?capital=Columbia](http://127.0.0.1/?capital=Columbia) to get back the state for a specific capital name. Like with the state name, you can also write a capital name made up of two words with a space instead of an underscore. The name is also not case sensitive.

- **Accessing Django Admin**

  1. Click [here](http://127.0.0.1/admin) to login to Django Admin or open [http://127.0.0.1/admin](http://127.0.0.1/admin) in your browser.

  2. Enter **admin** for the username and **changeme123** for the password. Click Log in.

  3. Once logged in, notice that under _Location_ you can see **State** and **Capital**. You should be able to edit these as needed although please note that there can only be one of each state name, abbreviation and capital city name.
  
  _All fields must be unique and cannot be left blank!_


### Running Tests

- **Testing Using the Docker Container**

  In a new terminal window, with your Docker container already running, use the following command to enter the container:

  ```
  docker exec -it 50-state-django_web_1 /bin/sh
  ```

  To check for linting issues using Flake8, use the command:

  ```
  flake8
  ```
  
  Next, to run all 25 of the unit and integration tests, use the following command:

  ```
  python manage.py test
  ```

  The tests will check common model and view functionality as well as test specific validation and error conditions. Note that additional input validation was added to help keep data consistent. Examples include making sure all state names, abbreviations and capital city names are properly capitalized. Also none of the input fields may be left empty when trying to save changes. Finally, testing is done to validate not only that 50 states and 50 capital cities exist but that they are properly paired in the database.

  _When you are done with the container you can run `docker stop $(docker ps -qa) && docker system prune -af --volumes` to clear everything from Docker at once. If you have other Docker containers that you do not wish to remove, you should manually remove just the containers, volumes and images that you no longer wish to keep. Use `docker ps -a` to see a list of the containers that you have. To remove use `docker rm <CONTAINTER_NAME_OR_ID>`. To remove all unused volumes and images, use `docker system prune -af --volumes`._


### Deploying to AWS

- **Deploying app to AWS (Using Elastic Beanstalk)**

  1. Make sure you have the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) installed, then install the EB (Elastic Beanstalk) CLI. If you have Python 3 and pip installed  you can run:

  ```
  pip3 install awsebcli --upgrade --user
  ```

  2. Next, from the **50-state-django** directory, run `eb create` and follow the prompts. Press **return** twice to use default environment name and CNAME DNS prefix, then choose option **2** for the **application** type. Answer **N** regarding using Spot Fleet requests (this won't need to autoscale). Then sit back and relax while everything is provisioned and built.

  3. Once complete, you can use the `eb list` command to see a list of currently running applications.

  4. To view the site in a browser, run `eb open`. 

  5. Once you are done with the applicaiton and wish to remove it and all of the resources it uses, run `eb terminate --all`.


## Changelog

**v1.1.0**
- Added querystring support for _state_ and _capital_.
- Added additional unit and integration tests.

**v1.0.0**
- Initial Release
