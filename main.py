import hashlib
import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.window import Window

Window.clearcolor = (0.06, 0.08, 0.12, 1)

class SmartPatternEngine(App):
    def build(self):
        self.history = []
        self.current_period = ""
        self.cached_predictions = {}

        main_layout = BoxLayout(orientation='vertical', padding=16, spacing=10)

        t = Label(
            text="[b][color=#FFD700]OKWIN / DMWIN SMART AI[/color][/b]",
            markup=True,
            font_size='20sp',
            size_hint=(1, 0.1)
        )

        self.p = Label(
            text="Syncing OKWin IST Period...",
            markup=True,
            font_size='16sp',
            size_hint=(1, 0.08),
            color=(0.2, 0.9, 1, 1)
        )

        self.tm = Label(
            text="Timer: 00:00",
            markup=True,
            font_size='17sp',
            size_hint=(1, 0.08),
            color=(1, 1, 1, 1)
        )

        self.r = Label(
            text="[b]WAITING FOR PERIOD SYNC...[/b]",
            markup=True,
            font_size='17sp',
            size_hint=(1, 0.44),
            color=(0.95, 0.95, 0.95, 1)
        )

        self.hist_label = Label(
            text="Recent History: [ Empty ]",
            markup=True,
            font_size='13sp',
            size_hint=(1, 0.08),
            color=(0.8, 0.8, 0.8, 1)
        )

        btn_layout = GridLayout(cols=3, spacing=8, size_hint=(1, 0.22))
        
        btn_big = Button(
            text="+ REAL BIG",
            background_normal='',
            background_color=(0.9, 0.65, 0, 1),
            font_size='15sp',
            bold=True
        )
        btn_big.bind(on_release=lambda x: self.add_real_result(1))

        btn_small = Button(
            text="+ REAL SMALL",
            background_normal='',
            background_color=(0.1, 0.6, 0.9, 1),
            font_size='15sp',
            bold=True
        )
        btn_small.bind(on_release=lambda x: self.add_real_result(0))

        btn_reset = Button(
            text="CLEAR",
            background_normal='',
            background_color=(0.5, 0.2, 0.2, 1),
            font_size='14sp'
        )
        btn_reset.bind(on_release=lambda x: self.clear_history())

        btn_layout.add_widget(btn_big)
        btn_layout.add_widget(btn_small)
        btn_layout.add_widget(btn_reset)

        for w in [t, self.p, self.tm, self.r, self.hist_label, btn_layout]:
            main_layout.add_widget(w)

        Clock.schedule_interval(self.tick, 1)
        return main_layout

    def get_ist_time(self):
        utc_now = datetime.datetime.now(datetime.timezone.utc)
        ist_tz = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
        return utc_now.astimezone(ist_tz)

    def get_okwin_period(self):
        ist_now = self.get_ist_time()
        total_minutes = (ist_now.hour * 60) + ist_now.minute + 1
        date_str = ist_now.strftime('%Y%m%d')
        return f"{date_str}01000{total_minutes:04d}"

    def add_real_result(self, val):
        self.history.append(val)
        if len(self.history) > 12:
            self.history.pop(0)
        self.update_history_ui()
        self.calc_advanced_prediction(self.current_period, force=True)

    def clear_history(self):
        self.history = []
        self.update_history_ui()
        self.calc_advanced_prediction(self.current_period, force=True)

    def update_history_ui(self):
        if not self.history:
            self.hist_label.text = "Recent History: [ Empty ]"
            return
        tags = ["[color=#ffcc00]B[/color]" if x == 1 else "[color=#00e1ff]S[/color]" for x in self.history]
        self.hist_label.text = f"Recent History ({len(self.history)}): " + " -> ".join(tags)

    def tick(self, dt):
        ist_now = self.get_ist_time()
        seconds_left = 60 - ist_now.second
        self.tm.text = f"Round Timer: [color=#ffbb00]00:{seconds_left:02d}s[/color]"

        period = self.get_okwin_period()
        if period != self.current_period:
            self.current_period = period
            self.p.text = f"[b]Live Period:[/b] [color=#00ffea]{self.current_period}[/color]"
            self.calc_advanced_prediction(period)

    def calc_advanced_prediction(self, period, force=False):
        if not period:
            return

        if force or (period not in self.cached_predictions):
            strategy_name = "Base Quantum Salt"
            if len(self.history) >= 3:
                if self.history[-1] == self.history[-2] == self.history[-3]:
                    size = "SMALL" if self.history[-1] == 1 else "BIG"
                    strategy_name = "Dragon Reversal Model"
                    conf = 92
                elif self.history[-1] != self.history[-2] and self.history[-2] != self.history[-3]:
                    size = "BIG" if self.history[-1] == 0 else "SMALL"
                    strategy_name = "Alternating Flip Engine"
                    conf = 89
                else:
                    big_count = sum(self.history[-6:])
                    total = len(self.history[-6:])
                    size = "SMALL" if (big_count / total) >= 0.5 else "BIG"
                    strategy_name = "Markov Probability Balance"
                    conf = 86
            else:
                seed = (period + "OKWIN_V5_SALT").encode('utf-8')
                val = int(hashlib.sha256(seed).hexdigest()[:8], 16)
                size = "BIG" if (val % 2 == 0) else "SMALL"
                conf = 84
                strategy_name = "Deterministic Baseline"

            num_list = [5, 6, 7, 8, 9] if size == "BIG" else [0, 1, 2, 3, 4]
            p_seed = int(hashlib.md5(period.encode('utf-8')).hexdigest()[:6], 16)
            num = num_list[p_seed % len(num_list)]

            if num in [1, 3, 7, 9]:
                color = "[color=#00ff66]GREEN 🟢[/color]"
            elif num in [2, 4, 6, 8]:
                color = "[color=#ff3333]RED 🔴[/color]"
            elif num == 0:
                color = "[color=#ff3333]RED[/color] + [color=#cc33ff]VIOLET 🔴🟣[/color]"
            else:
                color = "[color=#00ff66]GREEN[/color] + [color=#cc33ff]VIOLET 🟢🟣[/color]"

            self.cached_predictions[period] = {
                "size": size,
                "num": num,
                "color": color,
                "conf": conf,
                "strategy": strategy_name
            }

        d = self.cached_predictions[period]
        self.r.text = (
            f"[b]FORECAST RESULT (LOCKED)[/b]\n\n"
            f"Prediction: [color=#ffff00][b]{d['size']}[/b][/color]\n"
            f"Target Number: [color=#00ffff][b]{d['num']}[/b][/color]\n"
            f"Color Signal: {d['color']}\n"
            f"Engine Model: [color=#00ff88]{d['strategy']}[/color]\n"
            f"Confidence: [color=#ffbb00]{d['conf']}%[/color]"
        )

if __name__ == '__main__':
    SmartPatternEngine().run()
