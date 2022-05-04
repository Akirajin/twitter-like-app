Feature: User information tests

  Scenario: Getting user info
    Given we have a empty database
    And there's user abcDEFZ0123 in the database
    And there's user user1 in the database
    And there's user user2 in the database
    And there's user user3 in the database
    And user user1 is following username abcDEFZ0123
    And user user2 is following username abcDEFZ0123
    And user user3 is following username abcDEFZ0123
    And user abcDEFZ0123 is following username user1
    And user abcDEFZ0123 is following username user2
    When the http://localhost:8000/users/abcDEFZ0123 is called using GET
    Then the request will return httpStatus 200
    And the payload will have the following json
    """
    {
      "username": "abcDEFZ0123",
      "joined_date": "March 25, 2021",
      "followers": 3,
      "following": 2,
      "posts": 0
    }
    """


  Scenario: User not found scenario
    Given we have a empty database
    When the http://localhost:8000/users/abcDEFZ0123 is called using GET
    Then the request will return httpStatus 404
    And the payload must return the following message User not found

  Scenario: Getting user following/follower info
    Given we have a empty database
    And there's user abcDEFZ0123 in the database
    And there's user user1 in the database
    And there's user user2 in the database
    And there's user user3 in the database
    And user user1 is following username abcDEFZ0123
    And user user2 is following username abcDEFZ0123
    And user user3 is following username abcDEFZ0123
    And user abcDEFZ0123 is following username user1
    And user abcDEFZ0123 is following username user2
    When the http://localhost:8000/users/abcDEFZ0123/follows is called using GET
    Then the request will return httpStatus 200
    And the payload will have the following json
    """
    {
      "following": [
      "user1", "user2"
      ],
      "followers": [
      "user1","user2","user3"
      ]
    }
    """