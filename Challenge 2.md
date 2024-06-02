**Challenge 2**

**Steps to execute the code.**

**Run docker-compose up -d 
    OR 
Run main.py but we must change the API port in the postman collection which currently pointing to host port that is internally mapped to app container port ** 

**API Details** 

1. **/health**

   **Check Application Health.**

      <http://localhost:4000/challenge_1/health>

      **response**= {

    "status": "success",

    "message": "Healthy"

      }

2. **/search_images**

**provide min depth & max depth to get the image frames b/w min & max depth**

**Body=** 

{

    "depth_min": 9000.1,

    "depth_max": 9000.5

}

**Response=** 
    display image frame b/w min & max depth



