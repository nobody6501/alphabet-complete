# test_flask_app.py

from flask_app import app, has_all_letters
import json
import pytest

true_input = "The quick brown fox jumps over the lazy dog"
false_input = "abccd121892"


def test_hello():
    response = app.test_client().get('/hello')

    assert response.status_code == 200
    assert response.data == b'Hello from Martin!'


def test_404():
    response = app.test_client().get('/chicken')
    assert response.status_code == 404


def test_alphabet_checker_page():
    response = app.test_client().get('/alphabet-checker')

    assert response.status_code == 200
    assert "input" in str(response.data)


def test_alphabet_checker_api_no_input():
    response = app.test_client().get('/api/alphabet-checker')
    assert response.status_code == 400
    assert "Bad Request" in str(response.data)


def test_alphabet_checker_api_has_input():
    response = app.test_client().get('/api/alphabet-checker?input=abc')
    assert response.status_code == 200


def test_alphabet_checker_api_false_input():
    response = app.test_client().get('/api/alphabet-checker?input=abccd12')
    assert response.status_code == 200
    assert response.data == b'{"input": "abccd12", "result": false}'


def test_alphabet_checker_api_true_input():
    response = app.test_client().get('/api/alphabet-checker?input=The quick brown fox jumps over the lazy dog')
    assert response.status_code == 200
    assert response.data == b'{"input": "The quick brown fox jumps over the lazy dog", "result": true}'


def test_has_all_letters_none_input():
    with pytest.raises(Exception) as err:
        has_all_letters(None)
    assert str(err.value) == "400 Bad Request: Input cannot be None"
    assert err.value.code == 400


def test_has_all_letters_false_input():

    result_json = has_all_letters(false_input)
    result = json.loads(result_json)
    assert result["input"] == false_input
    assert result["result"] == False


def test_has_all_letters_true_input():
    result_json = has_all_letters(true_input)
    result = json.loads(result_json)
    assert result["input"] == true_input
    assert result["result"] == True


def test_emoji_input():
    response = app.test_client().get('/api/alphabet-checker?input=😀')
    result = json.loads(response.data)
    assert response.status_code == 200
    assert result["input"] == '😀'
    assert result["result"] == False
