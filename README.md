# CRM
## Description
This app is a prototype for a CRM coded as a CLI. It allows you to create users, clients, contracts and events.
A permission system is setup. Only specific users can do specific actions.

## Set Up
### App files download
Download all the files that are in this repository and place them in your preferred folder on your computer.

### Database creation
This app runs with a MySQL database. You will have to install MySQL on your computer in order to use it. You can download the community edition following this link : https://www.mysql.com/products/community/

I highly recommand installing MySQL Workbench at the same time to ease the database management.

Once MySQL is installed, you can create the database that will be used by the application. 

Log in on MySQL Workbench as the root user and create the database using this command line:
`CREATE DATABASE crm`
The name HAS to be `crm`. If you give it another name, the application will not work.

### App User
Once the database is created, you can define an `app_user` to you database that has restricted access. This will ensure that no unwanted action will be performed on the database.
Create an app_user in the `administration`, `Users and Privileges` tabs of MySQL Workbench.

Here are the necessary permissions:
* CREATE
* REFERENCES
* SELECT
* INSERT
* UPDATE
* DELETE

### Environment variables
For the application to run smoothly, you will have to define one last file, the `.env` file.

Go in the folder in which you placed all the application files earlier.
Create a file named `.env` without any extention.


Open it as a text file and fill it with these information:

DATABASE_URL=mysql+pymysql://user:password@localhost/crm
SENTRY_DSN=your_sentry_dns_right_here
JWT_SECRET_KEY=

Notes :
* Modify the DATABASE_URL with the username and password of the app user you just created.
* Modify the SENTRY_DSN with your own Sentry DSN link. That way, you will be able to track any user modification made on the database.
* Modify the JWT_SECRET_KEY with you own secret key. You can, for instance, use this website to generate a key: https://jwtsecret.com/generate

### Database setup

You are almost there. One last step and you are good to go.

In order to complete the database setup, run this command from a terminal. Your terminal has to point to the application folder in order for it to work:
`python database_setup.py`


## Use
Now that everything is setup, you can use the CRM.

All commands have to be executed from a terminal pointing to the application folder.
They all take the same form : `python epicevent.py your_command_here`

To discover which command are available, run this one : `python epicevent.py --help`

### Side note : Admin User
New users can only be created by users with the management role. In order to ease the process, a user with this role has been created for you. You can connect to it using these credentials :
* email : admin@admin.com
* password : admin

I highly recommand to not use the admin user other than for creating the first 'official' management user. You can even delete this admin user once this is done.