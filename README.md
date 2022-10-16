# CSGO-Compare


## Running
### Step 1
Install docker you can find instructions for this [here](https://docs.docker.com/desktop/install/windows-install/).

## Step 2
Open a terminal and move to the directory containing the `docker-compose.yml` file then run the following command.

```
docker-compose -f docker-compose.yml up
```

## Step 3
If you see a message like `csgo-compare-app-1 exited with code 1` or `CSGO-Compare-main-app-1 exited with code 1` in the terminal press control and c to stop the docker containers and run the command from step 2 again. If you do not see this message continue to step 4.

## Step 4
In your web browser goto `127.0.0.1:80`