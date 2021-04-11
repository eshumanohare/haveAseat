# haveASeat

To install `virtualenv` use this command 
```
pip install virtualenv
```

## Creating a virtual environment

To create a virtual environment, use the following command.
```
virtualenv environment
```

In order to activate the environment and use it, open the console in the directory where this environment is stored and run the following command.
```
environment\Scripts\activate
```


To install the dependencies stored in `requirements.txt` use the following command. Make sure that you're using the environment, otherwise, all the modules will be installed for the global python.
```
pip install -r requirements.txt
```

Download the `haveAseat` repository and paste it inside the environment.

## Start Server

```
python manage.py runserver
```

## To check if django and other packages installed

```
pip freeze
```
