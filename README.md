# Wildradar Analyser and Manager

## Setup

<b>Prerequisites</b>

- Python

<details><summary><b>Setup locally</b></summary>

First  instal Gentele containter
``
docker pull lowerquality/gentle


docker run -p 8765:8765 Gentel

``
More info on [gentel] (https://hub.docker.com/r/lowerquality/gentle)



To run the app open a new terminal and enter the following:
``` shell
# install dependencies
pip install -r requirements.txt

# go to app folder and run app in development
cd app
python -m uvicorn main:app --reload
```


send request to http://127.0.0.1:8000/text2video with transcript in the body

``
curl --location --request POST 'http://127.0.0.1:8000/text2video' \
--header 'Content-Type: text/plain' \
--data-raw 'transcript of a video here the output will be a video but for a start you see this text'
``
you can also use postman :)
</details>

<details><summary><b>Dokrize</b></summary>

ToDO

</details>

