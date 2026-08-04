"""
Tests for games/Rock-Paper-Scissor/Rock-Paper-Scissor.py

Focus areas:
- Regression test for the "final statistics printed twice on quit" bug
  (issue #1824): the stats block must appear exactly once when the
  player declines to play again.
- Unit tests for the small helper functions (compute_favorite, parse_results)
  that support the game and leaderboard.

The module file uses hyphens in its name, so it's loaded via importlib
rather than a normal `import` statement.
"""

import importlib.util
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

MODULE_PATH = (
    Path(__file__).resolve().parent.parent
    / "games"
    / "Rock-Paper-Scissor"
    / "Rock-Paper-Scissor.py"
)


def load_module(tmp_path, monkeypatch):
    """Import the game module fresh, with its results file redirected to tmp_path."""
    spec = importlib.util.spec_from_file_location("rps_game", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules["rps_game"] = module
    spec.loader.exec_module(module)
    # Redirect results file so tests never touch the real game_results.txt
    module.RESULTS_FILE = tmp_path / "game_results.txt"
    return module


@pytest.fixture
def rps(tmp_path, monkeypatch):
    return load_module(tmp_path, monkeypatch)


# ── compute_favorite ─────────────────────────────────────────────────────────

def test_compute_favorite_empty(rps):
    assert rps.compute_favorite([]) == (None, None)


def test_compute_favorite_basic(rps):
    fav, pct = rps.compute_favorite(["rock", "rock", "paper"])
    assert fav == "rock"
    assert pct == 67  # round(2/3 * 100)


# ── parse_results / view_leaderboard ─────────────────────────────────────────

def test_parse_results_no_file(rps):
    assert rps.parse_results() == []


def test_parse_results_reads_valid_lines(rps):
    rps.RESULTS_FILE.write_text(
        "Player: Alice, Final Score: 3 - 1 (User-Computer), Rounds: 4\n"
        "Player: Bob, Final Score: 0 - 2 (User-Computer), Rounds: 2\n"
    )
    records = rps.parse_results()
    assert len(records) == 2
    assert records[0] == {"name": "Alice", "wins": 3, "losses": 1, "rounds": 4}
    assert records[1] == {"name": "Bob", "wins": 0, "losses": 2, "rounds": 2}


def test_parse_results_skips_malformed_lines(rps):
    rps.RESULTS_FILE.write_text(
        "Player: Alice, Final Score: 3 - 1 (User-Computer), Rounds: 4\n"
        "this is not a valid line\n"
    )
    records = rps.parse_results()
    assert len(records) == 1
    assert records[0]["name"] == "Alice"


def test_save_result_appends_line(rps):
    ok = rps.save_result("Carol", 2, 1, 3)
    assert ok is True
    content = rps.RESULTS_FILE.read_text()
    assert "Player: Carol, Final Score: 2 - 1 (User-Computer), Rounds: 3" in content


def test_save_result_defaults_to_anonymous(rps):
    rps.save_result("", 1, 0, 1)
    content = rps.RESULTS_FILE.read_text()
    assert "Player: Anonymous" in content


# ── Regression test: final stats printed exactly once on quit ───────────────

def test_final_stats_printed_once_on_quit(rps, capsys):
    """
    Reproduces the steps from issue #1824:
      1. Run the game
      2. Play one round
      3. Choose not to play again
      4. The "Game Statistics" block must appear exactly ONCE, not twice.
    """
    # Scripted input sequence for main():
    #   "p"          -> proceed to Play (skip leaderboard)
    #   "rock"       -> user's move for round 1
    #   "no"         -> decline to play again
    #   "TestPlayer" -> name to save results
    user_inputs = iter(["p", "rock", "no", "TestPlayer"])

    with patch("builtins.input", lambda *_: next(user_inputs)):
        with patch("random.choice", return_value="scissors"):
            with patch("random.random", return_value=0.99):
                rps.main()

    captured = capsys.readouterr().out
    assert captured.count("--- Game Statistics ---") == 1
    assert "Thanks for playing" in captured


def test_stats_printed_once_per_round_across_multiple_rounds(rps, capsys):
    """Playing 3 rounds then quitting should still show exactly one final
    stats block per round shown (3 rounds played + quit == 3 prints total,
    since the quit branch no longer prints an extra block)."""
    user_inputs = iter(
        ["p", "rock", "yes", "paper", "yes", "scissors", "no", "Dana"]
    )

    with patch("builtins.input", lambda *_: next(user_inputs)):
        with patch("random.choice", return_value="rock"):
            with patch("random.random", return_value=0.99):
                rps.main()

    captured = capsys.readouterr().out
    assert captured.count("--- Game Statistics ---") == 3
    assert captured.count("Thanks for playing") == 1


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))