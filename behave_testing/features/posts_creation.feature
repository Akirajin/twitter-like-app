Feature: Posts creation tests


  Scenario: User creating post scenario
    Given we have a empty database
    And there's user abcDEFZ0123 in the database
    When post creation api is called with the following username abcDEFZ0123 and the following message
    """
    {
    "message": "Hello word"}
    """
    Then the request will return httpStatus 201
    And the database should have 1 message with the following message from username abcDEFZ0123
    """
    Hello word
    """

  Scenario: User trying to create message with 778 characters
    Given we have a empty database
    And there's user abcDEFZ0123 in the database
    When post creation api is called with the following username abcDEFZ0123 and the following message
    """
    {
    "message": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}
    """
    Then the request will return httpStatus 400
    And the payload must return the following message Message must be less or equal than 777 characters
    And the database should have 0 message with the following message from username abcDEFZ0123


  Scenario: User trying to create 6 posts sequentially simulating
    Given we have a empty database
    And there's user abcDEFZ0123 in the database
    When post creation api is called with the following username abcDEFZ0123 and the following message
    """
    {
    "message": "message1"
    }
    """
    And post creation api is called with the following username abcDEFZ0123 and the following message
    """
    {
    "message": "message2"
    }
    """
    And post creation api is called with the following username abcDEFZ0123 and the following message
    """
    {
    "message": "message3"
    }
    """
    And post creation api is called with the following username abcDEFZ0123 and the following message
    """
    {
    "message": "message4"
    }
    """
    And post creation api is called with the following username abcDEFZ0123 and the following message
    """
    {
    "message": "message5"
    }
    """
    And post creation api is called with the following username abcDEFZ0123 and the following message
    """
    {
    "message": "message6"
    }
    """
    Then the request will return httpStatus 400
    And the payload must return the following message Users cannot create more than 5 messages per day
    And the database should have 5 message with the following message from username abcDEFZ0123
