"""Example steps that exercise integrated Python config modules."""

from behave import given, when, then


@given("the config bundle is initialized")
def step_config_bundle_initialized(context):
    assert hasattr(context, "config_bundle"), "Config bundle was not attached in before_all"
    assert hasattr(context, "property_reader"), "Property reader is missing from context"


@when('I resolve token "{token}"')
def step_resolve_token(context, token):
    context.resolved_value = context.property_reader.resolve_value(token)


@then("the resolved value should not be empty")
def step_resolved_not_empty(context):
    assert isinstance(context.resolved_value, str)
    assert context.resolved_value.strip() != "", "Resolved value is empty"


@when("I read timeout values from integrated config")
def step_read_timeouts(context):
    context.timeout_values = context.config_bundle.get_timeouts()


@then("timeouts should be positive integers")
def step_verify_timeouts(context):
    timeouts = context.timeout_values
    for key in ("page_load", "implicit", "explicit"):
        assert key in timeouts, f"Missing timeout key: {key}"
        assert isinstance(timeouts[key], int), f"Timeout {key} is not an integer"
        assert timeouts[key] > 0, f"Timeout {key} must be > 0"

