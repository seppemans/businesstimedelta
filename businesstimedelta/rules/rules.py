from rule import Rule


class Rules(Rule):
    def __init__(self, rules, *args, **kwargs):
        self.available_rules = [x for x in rules if not x.time_off]
        self.unavailable_rules = [x for x in rules if x.time_off]
        super(Rules, self).__init__(*args, **kwargs)

    def next(self, dt):
        min_start = None
        min_end = None

        while True:
            # Find the first upcoming available time
            for rule in self.available_rules:
                start, end = rule.next(dt)

                if not min_start or start < min_start:
                    min_start = start
                    min_end = end

            # Check whether that time is not unavailable due to an
            # unavailability rule. If so, restart this process beginning
            # at the end of this unavailability period.
            for rule in self.unavailable_rules:
                start, end = rule.next(min_start)

                if start == min_start:
                    dt = end
                    min_start = None
                    break

            # We found the first time that is available.
            # Now see when it becomes unavailable.
            if min_start:
                for rule in self.unavailable_rules:
                    start, end = rule.next(min_start)

                    if end < min_end:
                        min_end = start

                if min_end != min_start:
                    return (min_start, min_end)
