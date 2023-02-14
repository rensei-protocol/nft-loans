# NFT Loans aggregator backend

## About the project structure
- All project was written with [django](https://docs.djangoproject.com/)
- Database is `mysql`. You can set up mysql db with script in `./db_local` folder


## Conventions:
- create app names in plural form
- use only single scope for strings: `'` not `"`


### Before migrations, must todo:
1. create  migration file, it is very important to run it with app name (otherwise will run globally), e.g: `./manage.py makemigrations app_name`
2. add migrated file via git: `git add app_name/migrations/migrate_file.py`
3. run migration: `./manage.py migrate app_name`
