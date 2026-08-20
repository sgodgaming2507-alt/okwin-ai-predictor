    def calc_advanced_prediction(self, period, force=False):
        if not period:
            return

        if force or (period not in self.cached_predictions):
            history_len = len(self.history)
            
            # 1. Default State (Kam data hone par)
            if history_len < 3:
                seed = (period + "SALT_V2").encode('utf-8')
                val = int(hashlib.sha256(seed).hexdigest()[:8], 16)
                size = "BIG" if (val % 2 == 0) else "SMALL"
                conf = 50
                strategy_name = "Base Initialization"
            else:
                # 2. 1st-Order Markov Chain Transition Matrix
                transitions = {'00': 0, '01': 0, '10': 0, '11': 0}
                for i in range(history_len - 1):
                    pair = f"{self.history[i]}{self.history[i+1]}"
                    transitions[pair] += 1
                
                last_state = str(self.history[-1])
                prob_to_small = transitions.get(last_state + '0', 0)
                prob_to_big = transitions.get(last_state + '1', 0)
                total_trans = prob_to_small + prob_to_big

                # 3. Weighted Momentum (Recent inputs ko zyada weight)
                weights = [0.1, 0.2, 0.3, 0.4] if history_len >= 4 else [0.2, 0.3, 0.5]
                recent_samples = self.history[-len(weights):]
                weighted_sum = sum(w * val for w, val in zip(weights, recent_samples))

                # Combined Statistical Signal
                if total_trans > 0 and prob_to_big != prob_to_small:
                    if prob_to_big > prob_to_small:
                        size = "BIG"
                        conf = int(50 + (prob_to_big / total_trans) * 15)
                    else:
                        size = "SMALL"
                        conf = int(50 + (prob_to_small / total_trans) * 15)
                    strategy_name = "Markov Transition Flow"
                else:
                    size = "BIG" if weighted_sum >= 0.5 else "SMALL"
                    conf = int(50 + abs(weighted_sum - 0.5) * 20)
                    strategy_name = "Weighted Moving Trend"

            # Number & Color Mapping
            num_list = [5, 6, 7, 8, 9] if size == "BIG" else [0, 1, 2, 3, 4]
            p_seed = int(hashlib.md5(period.encode('utf-8')).hexdigest()[:6], 16)
            num = num_list[p_seed % len(num_list)]

            if num in [1, 3, 7, 9]:
                color = "[color=#00ff66]GREEN 🟢[/color]"
            elif num in [2, 4, 6, 8]:
                color = "[color=#ff3333]RED 🔴[/color]"
            elif num == 0:
                color = "[color=#ff3333]RED[/color] + [color=#cc33ff]VIOLET 🟣[/color]"
            else:
                color = "[color=#00ff66]GREEN[/color] + [color=#cc33ff]VIOLET 🟣[/color]"

            self.cached_predictions[period] = {
                "size": size,
                "num": num,
                "color": color,
                "conf": conf,
                "strategy": strategy_name
            }

            d = self.cached_predictions[period]
            self.r.text = (
                f"[b]FORECAST RESULT (LIVE)[/b]\n\n"
                f"Prediction: [color=#ffff00][b]{d['size']}[/b][/color]\n"
                f"Target Number: [color=#00ffff][b]{d['num']}[/b][/color]\n"
                f"Color Signal: {d['color']}\n"
                f"Engine Model: [color=#00ff88]{d['strategy']}[/color]\n"
                f"Statistical Bias: [color=#ffbb00]{d['conf']}%[/color]"
            )
