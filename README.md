# Instructions

## step 1: Install django,djangorestframework,djangorestframework-simplejwt

## step 2: Create Super User

## step 3: In postman

- GET polls/ question details
- POST polls/ use "questions":"Your question here"
- POST choices/ use {"choice_text":"Options",
  "poll":1 #queston ID
  } **Repeat this step For multiple options**
- POST vote/ use {"choice": 1} **here 1 is the choice ID**
- POST login/ use the username and password that you have created by createsuperuser command
