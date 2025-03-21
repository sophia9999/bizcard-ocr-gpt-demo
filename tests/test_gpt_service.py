import pytest
from app.service.gpt_service import parse_gpt_response

def test_parse_valid_multi_card_response():
    content = '''
    {
        "data": [
            {
                "name": ["Alice"],
                "company": ["OpenAI"],
                "telephone_number": ["010-1234-5678"],
                "email": ["alice@openai.com"],
                "etc": []
            },
            {
                "name": ["Bob"],
                "company": ["DeepMind"],
                "telephone_number": ["010-2345-6789"],
                "email": ["bob@deepmind.com"],
                "etc": []
            }
        ]
    }
    '''
    result = parse_gpt_response(content, expected_len=2)
    assert len(result) == 2
    assert result[0]["name"][0] == "Alice"
    assert result[1]["company"][0] == "DeepMind"

def test_parse_valid_single_card_response():
    content = '''
    {
        "name": ["Charlie"],
        "company": ["Anthropic"],
        "telephone_number": ["010-3456-7890"],
        "email": ["charlie@anthropic.com"],
        "etc": []
    }
    '''
    result = parse_gpt_response(content, expected_len=1)
    assert len(result) == 1
    assert result[0]["name"][0] == "Charlie"

def test_parse_mismatch_data_count():
    content = '''
    {
        "data": [
            {
                "name": ["Dave"]
            }
        ]
    }
    '''
    with pytest.raises(ValueError) as excinfo:
        parse_gpt_response(content, expected_len=2)
    assert "Mismatch" in str(excinfo.value)

def test_parse_invalid_format():
    content = '''["this", "is", "not", "a", "dict"]'''
    with pytest.raises(ValueError):
        parse_gpt_response(content, expected_len=1)

def test_parse_invalid_json():
    content = '''{ this is not valid json '''
    with pytest.raises(ValueError):
        parse_gpt_response(content, expected_len=1)
