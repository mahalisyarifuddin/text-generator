import os
import subprocess
import pytest

LANGUAGES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "languages")

@pytest.fixture
def temp_language_file():
    created_files = []
    def _create(lang_name, content):
        filepath = os.path.join(LANGUAGES_DIR, f"triplets_{lang_name}.txt")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        created_files.append(filepath)
        return lang_name

    yield _create

    for filepath in created_files:
        if os.path.exists(filepath):
            os.remove(filepath)

def run_generator(lang_name):
    cmd = ["python3", "scripts/generator.py", "-language", lang_name]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result

def test_well_formed_tsv(temp_language_file):
    content = """combined from test_well_formed
                   2\tword001
                   5\tword002
                  10\t_th
                  20\tthe
"""
    lang = temp_language_file("test_well_formed", content)
    res = run_generator(lang)
    assert res.returncode == 0
    assert "Just Another Test Text Generator" in res.stdout
    assert "Traceback" not in res.stderr
    assert "ValueError" not in res.stdout

def test_missing_word_entries_tsv(temp_language_file):
    content = """combined from test_missing_word
                  10\t_th
                  20\tthe
"""
    lang = temp_language_file("test_missing_word", content)
    res = run_generator(lang)
    assert res.returncode == 0
    assert "Just Another Test Text Generator" in res.stdout
    assert "Traceback" not in res.stderr
    assert "ValueError" not in res.stdout

def test_malformed_word_entries_tsv(temp_language_file):
    content = """combined from test_malformed_word
                 abc\tword001
                  10\twordXYZ
                  20\t_th
                  30\tthe
"""
    lang = temp_language_file("test_malformed_word", content)
    res = run_generator(lang)
    assert res.returncode == 0
    assert "Just Another Test Text Generator" in res.stdout
    assert "Traceback" not in res.stderr
    assert "ValueError" not in res.stdout

def test_out_of_order_word_entries_tsv(temp_language_file):
    content = """combined from test_out_of_order
                  10\t_th
                   5\tword002
                  20\tthe
"""
    lang = temp_language_file("test_out_of_order", content)
    res = run_generator(lang)
    assert res.returncode == 0
    assert "Just Another Test Text Generator" in res.stdout
    assert "Traceback" not in res.stderr
    assert "ValueError" not in res.stdout
