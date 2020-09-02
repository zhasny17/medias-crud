# medias-crud
Crud de midias de video

## SET UP LOCAL DATABASE
You must execute these coomands bellow in order to set up your local database
* docker run --name container-dev-mysql -e MYSQL_ROOT_PASSWORD=123 -d mysql/mysql-server:latest
* docker exec -it container-dev-mysql bash
    * mysql -u root -p
    * CREATE USER 'dev'@'%' IDENTIFIED BY '123';
    * GRANT ALL PRIVILEGES ON *.* TO 'dev'@'%';
    * CREATE DATABASE dev;

* docker inspect container-dev-mysql
    * the field DB_HOST on config file will asume IPAddress

* use these values on config file
    * DB_CONNECTOR="mysql+mysqlconnector"
    * DB_USERNAME="dev"
    * DB_PASSWORD="123"
    * DB_HOST=IPAddress
    * DB_PORT="3306"
    * DB_NAME="dev"


* to run migrations create a shell file like above and run the coomand **flask db upgrade**:
```
    export DB_CONNECTOR="mysql+mysqlconnector"
    export DB_USERNAME="dev"
    export DB_PASSWORD="123"
    export DB_HOST=IPAddress
    export DB_PORT="3306"
    export DB_NAME="dev"
```
