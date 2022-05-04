Feature: User creation tests

  Scenario: Happy scenario
    Given we have a empty database
    When users creation api is called with the following username abcDEFZ0123
    Then the request will return httpStatus 200
    And the username abcDEFZ0123 should appear 1 time(s) in the users base

  Scenario: Non-alphanumeric name scenario
    Given we have a empty database
    When users creation api is called with the following username abcDE$Z0123
    Then the request will return httpStatus 400
    And the payload must return the following message Only alphanumeric characters can be used for username
    And the username abcDE$Z0123 should appear 0 time(s) in the users base

  Scenario: 15 characters length scenario
    Given we have a empty database
    When users creation api is called with the following username abcdefghijklkmn
    Then the request will return httpStatus 400
    And the payload must return the following message Maximum 14 characters for username
    And the username abcdefghijklkmn should appear 0 time(s) in the users base

  Scenario: Same username scenario
    Given there's user abcDEFZ0123 in the database
    When users creation api is called with the following username abcDEFZ0123
    Then the request will return httpStatus 409
    And the payload must return the following message Username already exist
    And the username abcDEFZ0123 should appear 1 time(s) in the users base