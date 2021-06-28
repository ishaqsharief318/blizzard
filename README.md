# Blizzard

Small webapp which renders requested Hearthstone data into a human readable page

### Requirements

Docker

### Steps

* Build the image using - `docker build -t blizzard .`
* Deploy the image using - `docker run --rm -d -p 5000:5000 -e client_id='your_client_id' -e client_secret='your_client_secret' blizzard`

Navigate to localhost:5000/druid or localhost:5000/warlock to view the data