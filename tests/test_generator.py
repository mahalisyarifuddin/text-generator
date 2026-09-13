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

def test_utf8_corpus_file_reading():
    # Verify that generator loads UTF-8 corpus files with non-ASCII characters without UnicodeDecodeError
    env = dict(os.environ, LC_ALL="C", PYTHONUTF8="0")
    cmd = ["python3", "scripts/generator.py", "-language", "ru", "-generate", "100", "-kern", "typ", "-kernlevel", "b1"]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    assert res.returncode == 0
    assert "Just Another Test Text Generator" in res.stdout
    assert "UnicodeDecodeError" not in res.stderr
    assert "Traceback" not in res.stderr

def test_empty_and_short_duplet_lines_tsv(temp_language_file):
    content = """combined from test_empty_duplets
                  10\tword001

                  20\t_th
                  single_token
                  abc\t_th
                  15\ta
                  25\t_he
                  30\the_

"""
    lang = temp_language_file("test_empty_duplets", content)
    res = run_generator(lang)
    assert res.returncode == 0
    assert "Just Another Test Text Generator" in res.stdout
    assert "Traceback" not in res.stderr
    assert "IndexError" not in res.stderr

def test_character_filter_cli_flags():
    # Verify that -characters abc filters output text to 'a', 'b', 'c', and spaces, and prints 'abc' header
    cmd_chars1 = ["python3", "scripts/generator.py", "-language", "en", "-characters", "abc", "-generate", "100", "-seed", "42"]
    res1 = subprocess.run(cmd_chars1, capture_output=True, text=True)
    assert res1.returncode == 0
    assert "&nbsp;&nbsp;&nbsp;characters: \nabc" in res1.stdout
    text_part1 = res1.stdout.split("<br><br>\n")[1].split("&nbsp;&#150;")[0].rstrip(".")
    allowed_chars = set("abc ")
    assert all(c in allowed_chars for c in text_part1)

    # Verify that -chars abc produces identical character header and filtered output
    cmd_chars2 = ["python3", "scripts/generator.py", "-language", "en", "-chars", "abc", "-generate", "100", "-seed", "42"]
    res2 = subprocess.run(cmd_chars2, capture_output=True, text=True)
    assert res2.returncode == 0
    assert "&nbsp;&nbsp;&nbsp;characters: \nabc" in res2.stdout
    text_part2 = res2.stdout.split("<br><br>\n")[1].split("&nbsp;&#150;")[0].rstrip(".")
    assert all(c in allowed_chars for c in text_part2)
    assert text_part1 == text_part2

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
    text_part_50 = res_50.stdout.split("<br><br>\n")[1].split("&nbsp;&#150;")[0].rstrip(".")
    assert len(text_part_50) == 60

    cmd_120 = ["python3", "scripts/generator.py", "-language", "en", "-generate", "120"]
    res_120 = subprocess.run(cmd_120, capture_output=True, text=True)
    assert res_120.returncode == 0
    text_part_120 = res_120.stdout.split("<br><br>\n")[1].split("&nbsp;&#150;")[0].rstrip(".")
    assert len(text_part_120) == 130

def test_rtl_and_non_rtl_bdo_tags():
    # Non-RTL output (English) should not contain any <bdo> or </bdo> tags
    cmd_en = ["python3", "scripts/generator.py", "-language", "en", "-frequencies", "output", "-generate", "50"]
    res_en = subprocess.run(cmd_en, capture_output=True, text=True)
    assert res_en.returncode == 0
    assert "<bdo" not in res_en.stdout
    assert "</bdo>" not in res_en.stdout

    # RTL output (Arabic) should include <bdo dir='rtl'> and matching </bdo> tags
    cmd_ar = ["python3", "scripts/generator.py", "-language", "ar", "-frequencies", "output", "-generate", "50"]
    res_ar = subprocess.run(cmd_ar, capture_output=True, text=True)
    assert res_ar.returncode == 0
    assert "<bdo dir='rtl'>" in res_ar.stdout
    assert "</bdo>" in res_ar.stdout
    assert res_ar.stdout.count("<bdo dir='rtl'>") == res_ar.stdout.count("</bdo>")

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
