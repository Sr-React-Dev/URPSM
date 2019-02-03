# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* Quick summary

 URPSM is basically an application which is dedicated to various phone repairing shops and agencies.
Easy to use
This user friendly application shall let you organize your job in an efficient and easy way avoiding hassles.
This shall also allow you to add clients by their individual IMEI numbers along with their names as well. You can also print ticket and the ticket will contain a QR Code which shall notify you regarding the phone’s status whether it is ready or not or in case the technician need your attention. This has also got a very descriptive dashboard and backend with SEO, analytics of all your income along with an unlocking section which is to be unlocked by the users. Thus, URPSM is all about a one stop solution for organizing your phone repairing tasks and strategies. This provides a user friendly experience, much required for the smooth flow of an application. .
* Version 1.0b
* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

### How do I get set up? ###

* Summary of set up
* Configuration
* Dependencies
* Database configuration
* How to run tests
* Deployment instructions

### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact

### Developers guide ###

 * Set virtual environment(virtualenv wrapper)
   [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)

   ```
   mkvirtualenv vurpsm --python=/usr/bin/python2
   ```

 ```
 workon vurpsm
 ```

 ```
 cd $VIRTUAL_ENV
 ```

 * Clone the project

 ```
 git clone git@bitbucket.org:esoufien4/urpsm.git
 ```

 ```
 cd urpsm
 ```

 * Install requirements

 ```
 pip install -r requirements.txt
 ```

 * Create local_env.py

 ```
 local env file is dedicated to locale requirements, like database, debug=True...
 ```

 * Run migrations

 ```
 python manage.py migrate
 ```

 * Run server

 until now everything is up.

 ```
 python manage.py runserver
 ```