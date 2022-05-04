Feature: User creation tests

  Scenario: Following another user
    Given we have a empty database
    And there's user akirajin in the database
    And there's user strider in the database
    When the http://localhost:8000/users/akirajin/follows is called using POST with payload
    """
    {
      "username":"strider"
    }
    """
    Then the request will return httpStatus 200
    And the payload will have the following json
    """
    {
      "following": [
      "strider"
      ],
      "followers": []
    }
    """

  Scenario: Trying to follow myself
    Given we have a empty database
    And there's user akirajin in the database
    When the http://localhost:8000/users/akirajin/follows is called using POST with payload
    """
    {
      "username":"akirajin"
    }
    """
    Then the request will return httpStatus 409
    And the payload must return the following message Cannot follow yourself


  Scenario: Unfollowing another user
    Given we have a empty database
    And there's user akirajin in the database
    And there's user strider in the database
    And user akirajin is following username strider
    And user strider is following username akirajin
    When the http://localhost:8000/users/akirajin/follows is called using DELETE with payload
    """
    {
      "username":"strider"
    }
    """
    Then the request will return httpStatus 200
    And the payload will have the following json
    """
    {
      "following": [],
      "followers": ["strider"]
    }
    """
