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

def test_seed_reproducibility():
    # Verify deterministic output when the same seed is provided
    cmd_seed1_a = ["python3", "scripts/generator.py", "-language", "en", "-seed", "42", "-generate", "100"]
    res1_a = subprocess.run(cmd_seed1_a, capture_output=True, text=True)
    assert res1_a.returncode == 0

    cmd_seed1_b = ["python3", "scripts/generator.py", "-language", "en", "-seed", "42", "-generate", "100"]
    res1_b = subprocess.run(cmd_seed1_b, capture_output=True, text=True)
    assert res1_b.returncode == 0

    # Outputs should be exactly equal
    assert res1_a.stdout == res1_b.stdout

    # Verify that different seeds produce different outputs
    cmd_seed2 = ["python3", "scripts/generator.py", "-language", "en", "-seed", "123", "-generate", "100"]
    res2 = subprocess.run(cmd_seed2, capture_output=True, text=True)
    assert res2.returncode == 0

    assert res1_a.stdout != res2.stdout

    # Verify that omitting -seed produces randomized (different) outputs by default
    cmd_no_seed_a = ["python3", "scripts/generator.py", "-language", "en", "-generate", "100"]
    res_no_seed_a = subprocess.run(cmd_no_seed_a, capture_output=True, text=True)
    assert res_no_seed_a.returncode == 0

    cmd_no_seed_b = ["python3", "scripts/generator.py", "-language", "en", "-generate", "100"]
    res_no_seed_b = subprocess.run(cmd_no_seed_b, capture_output=True, text=True)
    assert res_no_seed_b.returncode == 0

    assert res_no_seed_a.stdout != res_no_seed_b.stdout

def test_custom_generate_length():
    # Verify that generator correctly scales output length using the -generate CLI argument
    cmd_50 = ["python3", "scripts/generator.py", "-language", "en", "-generate", "50"]
    res_50 = subprocess.run(cmd_50, capture_output=True, text=True)
    assert res_50.returncode == 0
    text_part_50 = res_50.stdout.split("<br><br>\n")[1].split(".</bdo>")[0]
    assert len(text_part_50) == 60

    cmd_120 = ["python3", "scripts/generator.py", "-language", "en", "-generate", "120"]
    res_120 = subprocess.run(cmd_120, capture_output=True, text=True)
    assert res_120.returncode == 0
    text_part_120 = res_120.stdout.split("<br><br>\n")[1].split(".</bdo>")[0]
    assert len(text_part_120) == 130

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
