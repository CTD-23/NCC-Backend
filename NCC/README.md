# `Rating API`

## Description
- This API requires authorized users only.
- This API allows multiple ratings and feedback from users.

### Create a Rating
- URL: `/api/rating/`
- Method: `POST`
- Headers:
  - `Authorization: Bearer <jwt_token>`
- Body:
  - `feedback` (string): The feedback provided by the user.
  - `rating` (int): The rating value given by the user.

#### Example Response
```
{
    "id": 1,
    "user": "prasad",
    "rating": 5,
    "feedBack": "Great"
}
```

### List Rating
- URL: `/api/ratings/`
- Method: `GET`
- Headers:
  - `Authorization: Bearer <jwt_token>`
- Body:
  

#### Example Response
```
[
    {
        "id": 1,
        "user": "prasad",
        "rating": 5,
        "feedBack": "Great"
    },
    {
        "id": 2,
        "user": "testuser1",
        "rating": 5,
        "feedBack": "Hello"
    }
]
```



# `Question API`

## Description
- This API requires authorized users only.
- This API responsible to retrieve and list questions based on  categories (junior,senior,both).

### List Questions
- URL: `/api/questions/`
- Method: `GET`
- Headers:
  - `Authorization: Bearer <jwt_token>`
- Body:
  
#### Example Response
```
[
    {
        "questionId": "2611d",
        "solvedByTeam": false,
        "questionNumber": 1,
        "title": "Reverse String",
        "description": "Hello World",
        "ipFormate": "Hello World",
        "opFormate": "Hello World",
        "constraints": "Hello World",
        "sampleIp": "Hello World",
        "sampleOp": "Hello World",
        "difficultyLevel": 0,
        "maxPoints": 0,
        "points": 0,
        "timeLimit": 1,
        "memoryLimit": 524288,
        "accuracy": 0,
        "totalSubmissions": 0,
        "author": "pandeji",
        "category": "junior"
    },
    {
        "questionId": "6c806",
        "solvedByTeam": false,
        "questionNumber": 2,
        "title": "Question 3",
        "description": "Hello World",
        "ipFormate": "Hello World",
        "opFormate": "Hello World",
        "constraints": "Hello World",
        "sampleIp": "Hello World",
        "sampleOp": "Hello World",
        "difficultyLevel": 0,
        "maxPoints": 0,
        "points": 0,
        "timeLimit": 1,
        "memoryLimit": 524288,
        "accuracy": 0,
        "totalSubmissions": 0,
        "author": "pandeji",
        "category": "both"
    }
]
```

### Retrieve a Question
- URL: `/api/questions/{id}/`
- Method: `GET`
- Headers:
    - Authorization:` Bearer <jwt_token>`
- Example Request: `/api/questions/2611d/`
- Example Response
```
{
    "questionId": "2611d",
    "solvedByTeam": false,
    "questionNumber": 1,
    "title": "Reverse String",
    "description": "Hello World",
    "ipFormate": "Hello World",
    "opFormate": "Hello World",
    "constraints": "Hello World",
    "sampleIp": "Hello World",
    "sampleOp": "Hello World",
    "difficultyLevel": 0,
    "maxPoints": 0,
    "points": 0,
    "timeLimit": 1,
    "memoryLimit": 524288,
    "accuracy": 0,
    "totalSubmissions": 0,
    "author": "pandeji",
    "category": "junior"
}
```

# `Leaderboard API`

## Description
- This API provides access to the leaderboard rankings for junior and senior users. It also includes personal rank if a token is provided.


### Junior Leaderboard
- URL: `/api/leaderboard/`
- Method: `GET`
- Headers:
  - `Authorization: Bearer <jwt_token>` (optional)

#### Example Response
```
{
    "personalRank": {
        "teamId": "919da",
        "user1": "testuser1",
        "user2": "prasad",
        "score": 0,
        "lastUpdate": "2023-07-07T21:39:30+05:30",
        "questionSolvedByUser": {
            "Q1": 0,
            "Q2": 0,
            "Q3": 0
        },
        "rank": 1
    },
    "juniorLeaderboard": [
        {
            "teamId": "919da",
            "user1": "testuser1",
            "user2": "prasad",
            "score": 0,
            "lastUpdate": "2023-07-07T21:39:30+05:30",
            "questionSolvedByUser": {
                "Q1": 0,
                "Q2": 0,
                "Q3": 0
            },
            "rank": 1
        },
    ],
    "seniorLeaderboard": [
        {
            "teamId": "ddc43",
            "user1": "testuser5",
            "user2": "testuser6",
            "score": 0,
            "lastUpdate": "2023-07-07T21:39:30+05:30",
            "questionSolvedByUser": {
                "Q1": 0,
                "Q2": 0
            },
            "rank": 1
        }
    ]
}
```

# `Submission API`

## Description
- This API requires authorized users only.
- This API provides submissions of user. It allows you to list all submissions or filter them based on a specific question.


### List Submissions
- URL: `/api/submissions/`
- Method: `GET`
- Headers:
  - `Authorization: Bearer <jwt_token>` 
- Parameters:
  - `question` (int, optional): Filter submissions by question ID.
- Example Request: `/api/submissions/`  OR  `/api/submissions/?question=1d0c0/` 

#### Example Response
```
[
    {
        "id": 2,
        "team": "919da",
        "question": "1d0c0",
        "language": "python",
        "code": "print(\"hello\")",
        "isCorrect": false,
        "points": 0,
        "submissionTime": "2023-07-07T22:10:16.370921+05:30",
        "status": "WA"
    },
    {
        "id": 1,
        "team": "919da",
        "question": "2611d",
        "language": "python",
        "code": "print(\"hello world\")",
        "isCorrect": false,
        "points": 0,
        "submissionTime": "2023-07-07T22:02:56.303079+05:30",
        "status": "WA"
    }
]
```
- When question is mentioned (List of submissions will receive for that question)
```
[
    {
        "id": 6,
        "team": "919da",
        "question": "1d0c0",
        "language": "python",
        "code": "print(\"hello\")",
        "isCorrect": false,
        "points": 0,
        "submissionTime": "2023-07-07T22:10:16.370921+05:30",
        "status": "WA"
    }
]
```

# `Submit Question API`

## Description
- This API requires authorized users only.
- This API allows users to submit code for a question. The submitted code will be associated with the user and the specified question.


### Submit Code for a Question
- URL: `/api/submit/`
- Method: `POST`
- Headers:
  - `Authorization: Bearer <jwt_token>`
- Body:
  - `question` (char): ID of the question for which the code is being submitted.
  - `code` (string): The code submitted by the user.
  - `language` (string): The programming language used in the submitted code.
  - `input` (string): *(optional)* Input value to run code.
  - `isSubmitted` (boolean): Set to `true` if the user is submitting code; set to `false` if the user is checking existing code.

#### Example Response
- Code Submitted (Submit btn clicked)
```
{
    "testcase1": {
        "returnCode": 0,
        "status": "AC"
    },
    "testcase2": {
        "returnCode": 0,
        "status": "AC"
    }
}
```
- Code Checking (Run btn clicked)
```
{
    "error": "",
    "output": "dasarp\n",
    "returnCode": 0,
    "status": "AC",
    "question": "2611d",
    "language": "python",
    "code": "def reverse_string(input_str):\n    # Reverse the string\n    return input_str[::-1]\nprint(reverse_string(input()))",
    "isSubmitted": false,
    "input": null
}
```

# `Login API`

## Description
- This API allows users to authenticate and obtain tokens by providing their username and password.


### User Login
- URL: `/api/login/`
- Method: `POST`
- Body:
  - `username` (string): The username of the user.
  - `password` (string): The password of the user.

#### Example Response
```
{
    "access": "ACCESS TOKEN"
}
```

