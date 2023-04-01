# Python Assignment Solution
## Objective
The objective of this project is to retrieve the financial data of two given stocks (IBM, Apple Inc.) for the most recently two weeks using AlphaVantage API, and provide in-house 
API services for the access to the financial data and the statistics(average open/close price, volume etc.).   

## Tech Stack
- Programming language: ***Python 3(.8)***
- Web framework: ***FastAPI***
- ORM tool: ***SQLAlchemy***
- logging: ***loguru***
- Server: ***Uvicorn***
- Operating system: ***Ubuntu20.04*** (in WSL2.0 for development)
- DevOps: ***Docker***, ***github***


As a web framework, FastAPI is modern, high performance, easy to learn, fast to code, ready for production. With integrated automatic data validation, serialization and documentation, we can easily develop the API service efficiently with FastAPI. Its simplicity makes the code very easy to maintain. 

SQLAlchemy is an ORM tool for python, it helps simplify our development around database access.

Uvicorn is an ASGI server for python and for async frameworks. The API services will run on top of it.

## Installation & Run
The recommended operating system for installation is Ubuntu20.04.
### Download source code
Either cloning via git or downloading through url is OK.
1. Use git clone 
```
git clone https://github.com/liuxq92/python_assignment.git
```
2. Download from project page, the page url is https://github.com/liuxq92/python_assignment/tree/dev.


### Configuration
#### 1. Set environment variable
The command template below will be executed to set environment variables:
```bash
export ALPHA_VANTAGE_AK="your access key" 
export MYSQL_HOST=172.30.243.202
export MYSQL_PORT=33306
export MYSQL_USER=root 
export MYSQL_PASSWD=password 
```

- Replace value of ***ALPHA_VANTAGE_AK*** with your own access key provided by AlphaVantage
- Replace value of ***MYSQL_HOST*** with the host ip (via command `ifconfig`)
- Replace value of ***MYSQL_PORT*** with the port available
- Replace value of ***MYSQL_PASSWD*** with the value align with MySQL password requirements and your preference

***Attention***: here ALPHA_VANTAGE_AK is set as environment variable, the program will read its value in runtime. The real value of access key and password are decoupled from code, but the access to environment variables makes this approach not fully secure. It would be better store the access key ALPHA_VANTAGE_AK in a configuration service provided by the target deployment platform(or an in-house configuration service). Then the get_raw_data script fetches ALPHA_VANTAGE_AK value by SDK with other credentials to access the configuration service.

#### 2. Create docker image for financial data API service
Under the project root folder, run following command
```bash
docker build -t financial_image:v1 .
```
check if image is created successfully on local machine
```bash
docker image list
```

### How to Run
#### Run contianers for MySQL and financial data 

```bash
docker-compose up -d
```
check if MySQL and financial data API service are running
```bash
docker ps -a
```
check if MySQL database and table are successfully created
```bash
docker exec -it "contianer id" /bin/bash  // go inside the MySQL container
mysql -u root -p  // connect to MySQL server
show databases; // check if `python_assignment` is present
use python_assignment;
show tables; // check if table `financial_data` is present
describe financial_data; // check table schema
```
 
## How to test
### 1. Retrieve data from AlphaVantage
Please make sure python3.8 is installed on local machine and *python* command is correctly linked to python3.8. 
Under project root folder, run command below
```
python get_raw_data.py
```
### 2. Test API service
- Query financial data

Sample requst
```bash
curl -X GET 'http://localhost:5000/api/financial_data?start_date=2023-03-20&end_date=2023-03-22&symbol=IBM&limit=1&page=2'

```
Sample response
```json
{
    "info": {
        "error": ""
    },
    "data": [
        {
            "symbol": "IBM",
            "date": "2023-03-21",
            "open_price": "126.9",
            "close_price": "126.57",
            "volume": "3856345"
        }
    ],
    "pagination": {
        "count": 1,
        "page": 2,
        "limit": 1,
        "pages": 2
    }
}
```

- Query statistics

Sample requst
```bash
curl -X GET 'http://localhost:5000/api/statistics?start_date=2023-03-20&end_date=2023-03-22&symbol=IBM'
```
Sample response
```json
{
    "info": {
        "error": ""
    },
    "data": {
        "start_date": "2023-03-20",
        "end_date": "2023-03-22",
        "symbol": "IBM",
        "average_daily_open_price": 126.07,
        "average_daily_closing_price": 125.52,
        "average_daily_volume": 3997891
    }
}
```