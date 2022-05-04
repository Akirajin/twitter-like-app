Feature: Posts info tests

  Scenario: Listing posts for a specific user. It should show all posts from itself and its following friend list
    Given we have a empty database
    And there's user akirajin in the database
    And there's user strider in the database
    And user akirajin is following username strider
    And post creation api is called with the following username akirajin and the following message
    """
    {
    "message": "message of akirajin"
    }
    """
    And post creation api is called with the following username strider and the following message
    """
    {
    "message": "message of strider"
    }
    """
    When the http://localhost:9000/users/akirajin/posts is called using GET
    Then the request will return httpStatus 200
    And the payload will have the following lists
    """
     [{
        "id": 20,
        "username": "akirajin",
        "message": "message of akirajin",
        "date": "22:32 - April 5, 2022"
     }, {
        "id": 21,
        "username": "strider",
        "message": "message of strider",
        "date": "22:32 - April 5, 2022"
     }]
    """

  Scenario: Listing posts which contains reposts for a specific user. It should show all posts from itself and its following friend list
    Given we have a empty database
    And there's user akirajin in the database
    And there's user strider in the database
    And user akirajin is following username strider
    And post creation api is called with the following username akirajin and the following message
    """
    {
    "message": "message of akirajin"
    }
    """
    And post creation api is called with the following username strider and the following message
    """
    {
    "message": "message of strider"
    }
    """
    And post creation api is called with username akirajin and the message teste message passing the reference of strider last message
    When the http://localhost:9000/users/akirajin/posts is called using GET
    Then the request will return httpStatus 200
    And the payload will have the following lists
    """
    [{
    	"username": "akirajin",
    	"message": "message of akirajin"
    }, {
    	"username": "strider",
    	"message": "message of strider"
    }, {
    	"username": "akirajin",
    	"message": "teste message",
    	"repost": {
    		"username": "strider",
    		"message": "message of strider"
    	}
    }]
    """