# Usage Instructions
URL: https://osu-cs467-team-chinchillas.herokuapp.com/

1. Register as an adopter user on the Sign up page.
2. Go to the Login page and login with the information you have registered.
3. Animal profiles will appear and you can browse the profiles of your favorite animals.
4. If the animal status is available, you can click the "Adopt this animal" button to send an adoption request to the shelter.
5. Click "advanced" next to the search bar to narrow down the list of animal profiles.


# Run the backend server by Docker
If you run the app for the first time, please run this command.

```
docker-compose up --build
```

Press Ctrl+C to quit


Next time, you just run
```
docker-compose up
```

# Run the frontend
First, go to front_end directory.

```
cd animal_adoption/front_end/
```

Then, run the following commands
```
npm install
npm start
```

# Reset local database
```
make reset_local_sqlite
```

### How to get into a Docker container
First, check your container id
```
docker ps
```

Then, run the command.
```
docker exec -it {CONTAINER_ID} /bin/bash
```

After connecting to your container, if you want to initialize your DB data, run the following command
```
python animal_adoption/models/initialize_db_data.py 
```
