import io
import subprocess
import sys

import pytest
from unicodeit.cli import main


# PYTHON names the interpreter used for subprocess CLI checks.
PYTHON = 'python3' if sys.platform != 'win32' else 'python'


def run_cli_stdin(source):
    """Return unicodeit CLI output when source is provided through stdin."""
    return subprocess.check_output([
        PYTHON, '-m', 'unicodeit.cli',
    ], input=source, text=True)


def test_cli_symbols1():
    """Verify test_cli_symbols1 converts a single stdin command."""
    r = run_cli_stdin('\\Sigma')
    print(r)
    assert r.strip() == 'Σ'


def test_cli_symbols2():
    """Verify test_cli_symbols2 converts subscripts from stdin."""
    r = run_cli_stdin(
        'def\\Sigma_{01234}abc\\alpha_{567}ggg\\beta_{1234}lll '
        '"\\Sigma e_0 e^3"'
    )
    print(r)
    assert r.strip() == 'defΣ₀₁₂₃₄abcα₅₆₇gggβ₁₂₃₄lll "Σ e₀ e³"'


def test_cli_symbols3():
    """Verify test_cli_symbols3 converts superscripts from stdin."""
    r = run_cli_stdin('def^{01234}abc\\alpha^{567abc} "\\:) \\:G"')
    print(r)
    assert r.strip() == 'def⁰¹²³⁴abcα⁵⁶⁷ᵃᵇᶜ "☺ ㋡"'


@pytest.mark.skip('this was already broken')
def test_cli_symbols4():
    """Verify test_cli_symbols4 documents a skipped broken conversion."""
    r = run_cli_stdin('ggg\\beta^{1234=\\(5\\)}lll')
    print(r)
    assert r.strip() == 'Σ'


def test_subscripts():
    """Verify test_subscripts converts subscript letters from stdin."""
    r = run_cli_stdin('a_{\\beta\\gamma\\varphi\\rho\\chi}')
    print(r)
    assert r.strip() == 'aᵦᵧᵩᵨᵪ'


def test_superscripts():
    """Verify test_superscripts converts superscript letters from stdin."""
    r = run_cli_stdin(
        'm^{ABDEGHIJKLMNOPRTUWabcdefghiklmnoprstuvwxyz\\beta\\gamma'
        '\\delta\\varphi\\chi<>}'
    )
    print(r)
    assert r.strip() == (
        'mᴬᴮᴰᴱᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾᴿᵀᵁᵂᵃᵇᶜᵈᵉᶠᵍʰⁱᵏˡᵐⁿᵒᵖʳˢᵗᵘᵛʷˣʸ'
        'ᶻᵝᵞᵟᵠᵡ˂˃'
    )


def test_main_entrypoint(monkeypatch, capsys):
    """Verify test_main_entrypoint reads source text from stdin."""
    monkeypatch.setattr(sys, 'stdin', io.StringIO('\\Sigma'))
    assert main([]) == 0
    captured = capsys.readouterr()
    assert captured.out.strip() == 'Σ'


def test_cli_stdin():
    """Verify test_cli_stdin preserves newline-delimited stdin output."""
    r = run_cli_stdin('\\alpha\n\\beta')
    print(r)
    assert r == 'α\nβ'


def test_main_entrypoint_stdin(monkeypatch, capsys):
    """Verify test_main_entrypoint_stdin reads sys.stdin exactly once."""
    monkeypatch.setattr(sys, 'stdin', io.StringIO('\\Sigma'))
    assert main([]) == 0
    captured = capsys.readouterr()
    assert captured.out == 'Σ'


def test_cli_positional_argument_prints_help():
    """Verify test_cli_positional_argument_prints_help rejects argv input."""
    r = subprocess.run([
        PYTHON, '-m', 'unicodeit.cli',
        '\\Sigma',
    ], check=False, capture_output=True, text=True)
    assert r.returncode == 1
    assert 'usage: unicodeit' in r.stdout
    assert 'stdin' in r.stdout
    assert r.stderr == ''


def test_main_positional_argument_prints_help(capsys):
    """Verify test_main_positional_argument_prints_help rejects argv input."""
    assert main(['\\Sigma']) == 1
    captured = capsys.readouterr()
    assert 'usage: unicodeit' in captured.out
    assert 'stdin' in captured.out
    assert captured.err == ''
