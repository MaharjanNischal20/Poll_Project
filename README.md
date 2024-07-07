step 1: Install django,djangorestframework,djangorestframework-simplejwt
step 2: Create Super User
step 3: In postman
        a) GET polls/ question details
        b) POST polls/ use "questions":"Your question here"
        c) POST choices/ use {"choice_text":"Options",
                                "poll":1 #queston ID
                                } #Repeat step 3 c) For  multiple options
        d) POST vote/ use {"choice": 1} #here 1 is the choice ID
        e) POST login/ use the username and password that you have created by createsuperuser command
