# Introduction

This is a project that takes in text as an input and outputs short compelling videos.

# Project owners

The project owner or client is Thomas de Groot, contact info: t.d.groot@infoland.nl, 
alternatively it is possible to contact Niels Heeren at n.heeren@infoland.nl

The project belongs to Zenya by Infoland.


# Project context 

- Zenya is developing a new module called Boost to boost user knowledge in a nonintrusive way.

- The Boost module provides tools to deliver microlearning to users over time.

- The goal of this project is to develop a working concept for generating a video based on a Dutch piece of text.

- The solution should be scalable to support 1.5M Zenya users and future growth, support multiple tenants, be GDPR compliant, and deployable on Azure.

- Integration with Zenya is not part of this project, and cost management should be done by using existing AI/NLP services on Zenya SaaS infrastructure.
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

