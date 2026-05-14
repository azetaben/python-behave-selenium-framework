@config_only @config
Feature: Python config integration examples

  Scenario: Resolve user and faker tokens
    Given the config bundle is initialized
    When I resolve token "user:STANDARD_USERNAME"
    Then the resolved value should not be empty
    When I resolve token "faker:email"
    Then the resolved value should not be empty

  Scenario: Read timeout values from integrated config services
    Given the config bundle is initialized
    When I read timeout values from integrated config
    Then timeouts should be positive integers

