"""Tests for prompt categorizer."""

from model_router.categorizer import categorize


def test_code_detection():
    assert categorize("write a python function to sort a list") == "code"
    assert categorize("debug this script for me") == "code"
    assert categorize("implement a binary search") == "code"
    assert categorize("refactor the auth module") == "code"


def test_reasoning_detection():
    assert categorize("explain why the sky is blue") == "reasoning"
    assert categorize("analyze this data step by step") == "reasoning"
    assert categorize("compare these two approaches") == "reasoning"


def test_vision_detection():
    assert categorize("describe this image for me") == "vision"
    assert categorize("what do you see in this screenshot") == "vision"


def test_search_detection():
    assert categorize("what is the latest news about AI") == "search"
    assert categorize("search for python tutorials") == "search"


def test_default_to_chat():
    assert categorize("hello how are you") == "chat"
    assert categorize("tell me a joke") == "chat"
    assert categorize("what should I have for dinner") == "chat"
