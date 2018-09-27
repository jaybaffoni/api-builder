# Node.js API Builder

Python script to build a node.js backend api from express generator with custom routes pulled from a mysql table.
Note: This version was built for and tested on a Linux system.  Contributors are welcome to make it more friendly for other operating systems!

## Running the script

These instructions will help you run the script on your local machine.

### Prerequisites

If they aren't already installed on your system, you'll need python (2.7 minimum) and Node Package Manager

* [Python](https://www.python.org/downloads/) - Python Installation
* [NPM](https://docs.npmjs.com/getting-started/installing-node) - NPM (Skip account registration)

### Usage

Download node-template.py and place it in the directory you want the project folder to be created

Run the script with superuser priveleges:

```
sudo python node-template.py
```

Enter mysql database details:

```
What is the database username? root
What is the database password? mypassword
What is the database address? (Default: 127.0.0.1) 
What is the database name? example

```

Enter the desired project name:

```
What is the project name? sample-project
```

Let the script run!

## Testing

Follow these steps to ensure your API configured properly

### Run the Server

In the command line, navigate into the newly created project folder and run server:

```
node app.js
```

### Check the Browser

Open a browser and navigate to your [API](http://localhost:4200)
You should see the default Express homepage

### cURL

To test the API, use cURL (or an HTTP client of your choice). Here are some tests based on the example database that is part of this project:
Get all-
```
curl http://localhost:4200/objects
```
Get by id-
```
curl http://localhost:4200/objects/1
```
Create-
```
curl -H "Content-Type: application/json" -X POST -d '{"object_id":"3","data":"hello","info":"world","details":"new row"}' http://localhost:4200/objects
```
Update-
```
curl -H "Content-Type: application/json" -X PUT -d '{"object_id":"3","data":"hello","info":"world","details":"new row"}' http://localhost:4200/objects
```
Delete-
```
curl -X "DELETE" http://localhost:4200/objects/3
```


## Contributing

Contributions welcome! Some enhancements might include checking that the prerequisites have been met, testing on platforms other than linux, or integrating authentication.


## Author

* **James Baffoni** - *Initial work* - [jaybaffoni](https://github.com/jaybaffoni)

Contributors list yourselves here!


