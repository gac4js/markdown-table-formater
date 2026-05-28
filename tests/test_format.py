"""Tests for markdown-table-formater."""

import importlib.util
import sys
import unittest
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    'markdown_table_formater',
    Path(__file__).parent.parent / 'bin' / 'markdown-table-formater.py',
)
_mod = importlib.util.module_from_spec(_spec)  # type: ignore[arg-type]
_spec.loader.exec_module(_mod)  # type: ignore[union-attr]
process = _mod.process

SAMPLE = Path(__file__).parent.parent / 'sample'


def load(name: str) -> str:
    return (SAMPLE / name).read_text()


class TestSamples(unittest.TestCase):
    def _check(self, stem: str) -> None:
        result = process(load(f'{stem}.input.md'))
        expected = load(f'{stem}.expected.md')
        self.assertEqual(result, expected)

    def test_basic(self) -> None:
        self._check('basic')

    def test_aligned(self) -> None:
        self._check('aligned')

    def test_mixed(self) -> None:
        self._check('mixed')

    def test_emoji(self) -> None:
        self._check('emoji')

    def test_no_trailing_pipe(self) -> None:
        self._check('no_trailing_pipe')

    def test_mixed_trailing_pipe(self) -> None:
        self._check('mixed_trailing_pipe')

    def test_escaped_pipe(self) -> None:
        self._check('escaped_pipe')


class TestIdempotent(unittest.TestCase):
    """Running the formatter twice must produce the same result."""

    def _check(self, stem: str) -> None:
        first = process(load(f'{stem}.input.md'))
        second = process(first)
        self.assertEqual(first, second)

    def test_basic(self) -> None:
        self._check('basic')

    def test_aligned(self) -> None:
        self._check('aligned')

    def test_mixed(self) -> None:
        self._check('mixed')

    def test_emoji(self) -> None:
        self._check('emoji')

    def test_no_trailing_pipe(self) -> None:
        self._check('no_trailing_pipe')

    def test_mixed_trailing_pipe(self) -> None:
        self._check('mixed_trailing_pipe')

    def test_escaped_pipe(self) -> None:
        self._check('escaped_pipe')


class TestTrailingNewline(unittest.TestCase):
    def test_preserved_when_present(self) -> None:
        self.assertTrue(process('| a |\n|---|\n| b |\n').endswith('\n'))

    def test_absent_when_not_present(self) -> None:
        self.assertFalse(process('| a |\n|---|\n| b |').endswith('\n'))


class TestNonTablePassthrough(unittest.TestCase):
    def test_plain_text_unchanged(self) -> None:
        text = 'just some text\nno table here\n'
        self.assertEqual(process(text), text)


if __name__ == '__main__':
    unittest.main()
