# medias-crud
Crud de midias de video

## Documentation avaliable on route /doc/


## SET UP LOCAL DATABASE AND RUN APPLICATION LOCALY
You must execute these coomands bellow in order to set up your local database
* docker run --name container-dev-mysql -e MYSQL_ROOT_PASSWORD=123 -d mysql/mysql-server:latest
* docker exec -it container-dev-mysql bash
    * mysql -u root -p
    * CREATE USER 'dev'@'%' IDENTIFIED BY '123';
    * GRANT ALL PRIVILEGES ON *.* TO 'dev'@'%';
    * CREATE DATABASE dev;

* docker inspect container-dev-mysql
    * the field DB_HOST on config file will asume IPAddress

* **OBS:** Use these values on config.{stage}.json file
    * DB_CONNECTOR="mysql+mysqlconnector"
    * DB_USERNAME="dev"
    * DB_PASSWORD="123"
    * DB_HOST=IPAddress
    * DB_PORT="3306"
    * DB_NAME="dev"


* Install all packages and requirements


* To run migrations create a shell file like the example bellow and run the coomand **flask db upgrade**:
```
    export DB_CONNECTOR="mysql+mysqlconnector"
    export DB_USERNAME="dev"
    export DB_PASSWORD="123"
    export DB_HOST=IPAddress
    export DB_PORT="3306"
    export DB_NAME="dev"
```

* Fill the file config.{stage}.json based on config.stage.json.example

* Run the command **serverless wsgi serve --stage {stage}**



## STEP BY STEP TO RUN UNIT TESTS

* Install requirements-dev.txt and requirements.txt

* Fill the file config.test.json on module tests/ based on consig.test.json.example
    * use a dev test database (cleanable)

* Run these commands bellow:

```SHELL
$ coverage run -m pytest
```
e então

```SHELL
$ coverage report
```



## DEPLOY
* install packages

* Fill the file config.{stage}.json based on config.stage.json.example

* run the command at first deploy **serverless deploy --stage {stage} --aws-profile {profile}**
    * after the first one, use deploy function: **serverless deploy function --function app --stage {stage} --aws-profile {profile}**



## HOW TO UPLOAD COMPONENTS WORKS:

* First of all  you need to send a request to **/config/request/upload/file_name** so you'll get back a component to upload files directly with the AWS (**response.get('uploadObject')**) (https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.generate_presigned_post), before you send yourt media to S3 Bucket, you must change your file name to **response.get('filename')**, due to complicts on S3 is generated a new random name to this media, after a success upload to S3, you already have a valid url on **response.get('file_url')**



## FUTURE IMPROVEMENTS
* import schemas defined on **utils/schemas.json** to **doc/api.yml**
* CI/CD implementation