"""The live watcher reads the run folder and nothing else. These pin what it
derives from disk: persona progress, the auth pause, lens state, the newest
run under a parent, and the one-line status."""
import json
import os
import subprocess
import sys
import tempfile
import unittest

import fixtures as fx

sys.path.insert(0, fx.SCRIPTS)
import watch  # noqa: E402

MARK = os.path.join(fx.SCRIPTS, "mark.py")


class State(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.mkdtemp(prefix="understudy-w-")
        self.run = fx.clean_run(self.t, with_lens=False)
        fx.manifest(self.run, objectives=["ux", "bugs"],
                    personas=[{"name": "a", "device": "desktop-1440x900"},
                              {"name": "b", "device": "iphone-13"}],
                    time_cap_minutes=45, objectives_under_test=[{"objective": "x"}])
        for d in os.listdir(self.run):
            if d.startswith("persona-"):
                import shutil
                shutil.rmtree(os.path.join(self.run, d))

    def test_pending_running_done(self):
        fx.persona(self.run, "a")                       # complete → done
        pdir = os.path.join(self.run, "persona-b")
        os.makedirs(os.path.join(pdir, "screenshots"))
        fx.write(os.path.join(pdir, "session.log"),
                 "[00:00] /today. A big box.\n[03:10] Where are my programs?\n")
        s = watch.read_state(self.run)
        self.assertEqual([p["state"] for p in s["personas"]], ["done", "running"])
        self.assertEqual(s["active"]["name"], "b")
        self.assertEqual(s["active"]["seconds"], 190)
        self.assertEqual(s["persona_progress"], (2, 2))
        self.assertEqual(s["cap"], 45 * 60)

    def test_auth_pause_is_read_from_the_log(self):
        pdir = os.path.join(self.run, "persona-a")
        os.makedirs(pdir)
        fx.write(os.path.join(pdir, "session.log"),
                 "[00:20] Login it is.\n[00:30] --- shape 0: auth wall. PAUSED for the human. ---\n")
        s = watch.read_state(self.run)
        self.assertTrue(s["active"]["paused"])
        self.assertIn("⏸", watch.status_line(s, colour=False))
        fx.write(os.path.join(pdir, "session.log"),
                 "[00:20] Login it is.\n[00:30] --- PAUSED for the human. ---\n"
                 "[00:00 persona] --- wall cleared by the human; resuming at /today ---\n"
                 "[00:05] /today. Good afternoon.\n")
        s = watch.read_state(self.run)
        self.assertFalse(s["active"]["paused"])
        self.assertIn("▶ a 00:05/45:00", watch.status_line(s, colour=False))

    def test_lenses_from_mark_and_disk(self):
        fx.persona(self.run, "a")
        fx.persona(self.run, "b")
        p = subprocess.run([sys.executable, MARK, self.run, "--phase", "scoring",
                            "--lens", "ux:opus", "--lens", "bugs:sonnet", "--lens", "objectives:opus"],
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        fx.lens(self.run, "ux", [fx.finding("ux", "Nav has three names for one thing", sev="P2")])
        s = watch.read_state(self.run)
        self.assertEqual(s["phase"], "scoring")
        by = {l["name"]: l for l in s["lenses"]}
        self.assertEqual((by["ux"]["state"], by["ux"]["model"]), ("done", "opus"))
        self.assertEqual(by["bugs"]["state"], "running")
        self.assertEqual(by["objectives"]["state"], "running")
        line = watch.status_line(s, colour=False)
        self.assertIn("scoring 1/3 done", line)
        self.assertIn("running: bugs, objectives", line)

    def test_newest_run_under_a_parent(self):
        old = os.path.join(self.t, "run-old")
        os.makedirs(old)
        fx.manifest(old, started_utc="2026-09-01T09:00:00+00:00")
        new = os.path.join(self.t, "run-new")
        os.makedirs(new)
        fx.manifest(new, started_utc="2026-09-02T09:00:00+00:00")
        self.assertEqual(watch.find_run(self.t), new)
        self.assertEqual(watch.find_run(old), old)
        self.assertIsNone(watch.find_run(os.path.join(self.t, "nope")))

    def test_line_mode_never_fails(self):
        p = subprocess.run([sys.executable, os.path.join(fx.SCRIPTS, "watch.py"),
                            os.path.join(self.t, "nope"), "--line"], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0)
        self.assertIn("no run", p.stdout)

    def test_complete_line_clears_after_an_hour(self):
        import datetime as dt
        fx.persona(self.run, "a")
        fx.persona(self.run, "b")
        finished = "2026-09-16T08:59:23+00:00"
        fx.manifest(self.run, objectives=["ux", "bugs"], phase="complete", finished_utc=finished,
                    personas=[{"name": "a", "device": "desktop-1440x900"},
                              {"name": "b", "device": "iphone-13"}])
        s = watch.read_state(self.run)
        self.assertEqual(s["phase"], "complete")
        t0 = dt.datetime.fromisoformat(finished)
        # Just finished: say so.
        self.assertIn("complete", watch.status_line(s, colour=False, now=t0 + dt.timedelta(minutes=5)))
        # Two days later: say nothing, so Claude Code hides the line.
        self.assertEqual("", watch.status_line(s, colour=False, now=t0 + dt.timedelta(days=2)))
        # No finished_utc at all (older manifests): fall back to the file's mtime,
        # which is "now" here, so the line still shows.
        fx.manifest(self.run, objectives=["ux", "bugs"], phase="complete", finished_utc=None,
                    personas=[{"name": "a", "device": "desktop-1440x900"},
                              {"name": "b", "device": "iphone-13"}])
        s = watch.read_state(self.run)
        self.assertIn("complete", watch.status_line(s, colour=False))

    def test_no_filesystem_path_in_status_line(self):
        fx.persona(self.run, "a")
        s = watch.read_state(self.run)
        self.assertNotIn(self.t, watch.status_line(s))


class NoPath(unittest.TestCase):
    """No path ever has to be typed: the run command remembers the newest run
    and the status line is written by a script, not pasted by hand."""
    def setUp(self):
        self.home = tempfile.mkdtemp(prefix="understudy-home-")
        self._env = dict(os.environ)
        os.environ["HOME"] = self.home
        os.environ["UNDERSTUDY_HOME"] = os.path.join(self.home, ".understudy")
        watch.UNDERSTUDY_HOME = os.environ["UNDERSTUDY_HOME"]

    def tearDown(self):
        os.environ.clear()
        os.environ.update(self._env)
        watch.UNDERSTUDY_HOME = os.environ["UNDERSTUDY_HOME"]

    def test_init_run_records_the_last_run_and_watch_finds_it(self):
        t = tempfile.mkdtemp(prefix="understudy-w-")
        target = os.path.join(t, "target.yaml")
        fx.write(target, "product_name: Nimbus Notes\nbase_url: https://example-nimbus.test\n"
                         "objectives: [ux]\npersonas:\n  - name: p\n    device: desktop-1440x900\n")
        out = os.path.join(t, "runs")
        p = subprocess.run([sys.executable, os.path.join(fx.SCRIPTS, "init_run.py"), "--target", target,
                            "--output-dir", out, "--traversal-model", "m",
                            "--persona-mode", "generic"],
                           capture_output=True, text=True, env=os.environ)
        self.assertEqual(p.returncode, 0, p.stderr)
        run = p.stdout.strip().splitlines()[0]
        self.assertTrue(os.path.exists(os.path.join(run, "manifest.json")))
        self.assertEqual(watch.last_run(), run)
        self.assertEqual(watch.find_run(None), run)
        line = subprocess.run([sys.executable, os.path.join(fx.SCRIPTS, "watch.py"), "--line", "--no-colour"],
                              capture_output=True, text=True, env=os.environ).stdout
        self.assertIn("Nimbus Notes", line)

    def test_no_run_anywhere_is_a_calm_line(self):
        self.assertIsNone(watch.find_run(None))
        line = subprocess.run([sys.executable, os.path.join(fx.SCRIPTS, "watch.py"), "--line"],
                              capture_output=True, text=True, env=os.environ).stdout
        self.assertIn("no run", line)

    def test_setup_statusline_keeps_everything_else(self):
        cfg = os.path.join(self.home, ".claude", "settings.json")
        fx.write(cfg, json.dumps({"theme": "dark", "hooks": {"Stop": [{"hooks": [{"type": "command", "command": "say done"}]}]}}))
        p = subprocess.run([sys.executable, os.path.join(fx.SCRIPTS, "watch.py"), "--setup-statusline"],
                           capture_output=True, text=True, env=os.environ)
        self.assertEqual(p.returncode, 0, p.stderr)
        with open(cfg) as fh:
            got = json.load(fh)
        self.assertEqual(got["theme"], "dark")
        self.assertEqual(got["hooks"]["Stop"][0]["hooks"][0]["command"], "say done")
        self.assertEqual(got["statusLine"]["type"], "command")
        self.assertIn("--line", got["statusLine"]["command"])
        self.assertTrue(os.path.exists(cfg + ".bak"))
        # broken JSON is never overwritten
        fx.write(cfg, "{not json")
        p = subprocess.run([sys.executable, os.path.join(fx.SCRIPTS, "watch.py"), "--setup-statusline"],
                           capture_output=True, text=True, env=os.environ)
        self.assertNotEqual(p.returncode, 0)
        with open(cfg) as fh:
            self.assertEqual(fh.read(), "{not json")


class FakeScreen:
    """A 24×100 grid that raises, as curses does, on any write outside it."""
    def __init__(self, h=24, w=100):
        self.h, self.w = h, w
        self.rows = [[" "] * w for _ in range(h)]

    def getmaxyx(self):
        return self.h, self.w

    def erase(self):
        self.rows = [[" "] * self.w for _ in range(self.h)]

    def refresh(self):
        pass

    def addstr(self, y, x, text, attr=0):
        if y >= self.h or x + len(text) > self.w:
            raise AssertionError(f"write outside the window at {y},{x}: {text!r}")
        for i, ch in enumerate(text):
            self.rows[y][x + i] = ch

    def text(self):
        return "\n".join("".join(r).rstrip() for r in self.rows)


class Dashboard(State):
    def test_draw_fits_the_window_and_shows_the_feed(self):
        fx.persona(self.run, "a")
        pdir = os.path.join(self.run, "persona-b")
        os.makedirs(os.path.join(pdir, "screenshots"))
        fx.write(os.path.join(pdir, "screenshots", "04-dead-link.png"), "x")
        fx.write(os.path.join(pdir, "session.log"),
                 "[02:32] Clicked the link it gave me. Chrome says this site can't be reached. "
                 "Great — the one thing I paid for, and it goes nowhere at all.\n")
        scr = FakeScreen()
        watch.draw(scr, watch.read_state(self.run), 0)
        out = scr.text()
        self.assertIn("CAPTURE 2 of 2", out)
        self.assertIn("02:32 / 45:00", out)
        self.assertIn("✓ a", out)
        self.assertIn("▶ b", out)
        self.assertIn("PERSONA · b · iphone-13", out)
        self.assertIn("[02:32] Clicked the link", out)
        self.assertIn("goes nowhere at all", out)          # wrapped, not truncated
        self.assertIn("last shot  04-dead-link.png", out)
        self.assertIn("· ux", out)

    def test_draw_survives_a_tiny_window(self):
        watch.draw(FakeScreen(5, 40), watch.read_state(self.run), 0)


if __name__ == "__main__":
    unittest.main()
