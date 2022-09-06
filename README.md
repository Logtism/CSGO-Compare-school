# CSGO-Compare


## Running
### Step 1
Install `pipenv` using the following relevant command.

Windows
```
pip install pipenv
```

Linux
```
pip3 install pipenv
```

### Step 2
In the same folder as the `manage.py` file install dependencies using the following command.

Windows and Linux
```
pipenv sync
```

### Step 3
In the same folder as the `manage.py` file create a file called `.env` and open it in a text editor and copy and paste the following into it.

Note: these recaptcha keys will not work in production as they are test keys
```
SECRET_KEY=random_string
DEBUG=True
RECAPTCHA_PUBLIC_KEY=6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI
RECAPTCHA_PRIVATE_KEY= 6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe
```

### Step 4
Open the virtual environment using the following command.

```
pipenv shell
```

### Step 5
Create the database using the following command.

```
python manage.py migrate
```

### Step 5.5 (optional)
Load example data using the following commands run each of them separately.

```
python manage.py loaddata catogory.yaml
```

```
python manage.py loaddata subcategory.yaml
```

```
python manage.py loaddata rarity.yaml
```

```
python manage.py loaddata update.yaml
```

```
python manage.py loaddata collection.yaml
```

```
python manage.py loaddata container.yaml
```


```
python manage.py loaddata pattern.yaml
```

```
python manage.py loaddata item.yaml
```

### Step 6
Run the application using the following command.

```
python manage.py runserver
```

### Setp 7
Open your browser and goto `127.0.0.1:8000`.