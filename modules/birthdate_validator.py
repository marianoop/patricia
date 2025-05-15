import datetime
from modules.tone_player import TonePlayer

"""
A  class for validating birthdates using datetime and customized tones.
"""
class BirthdateValidator:
    def __init__(self):
        self.player = TonePlayer()

    def _handle_error(self, message):
        print(message)
        self.player.play_error_tone()
        return False

    def _handle_valid(self, message):
        print(message)
        self.player.play_valid_tone()
        return True

    def validate(self, user_input):
        standard_input = user_input.replace('.', '/') # Replace '.' with '/'

        if '/' in standard_input: # Check if there are separators in standard_input
            parts = standard_input.split('/') # Split the input in parts by the '/' separator
            if len(parts) != 3:
                return self._handle_error("❌ Invalid date")
            try: # Convert each part into an integer an assign them to day, month and year variables
                day = int(parts[0])
                month = int(parts[1])
                year = int(parts[2])
            except ValueError: # Check if any part contains a non-digit character, raise an exception
                return self._handle_error("❌ Numbers only")
        else: # if there are not separators, create a digits list containing a character for each of the characters in standard input that is a digit
            if not all(c.isdigit() for c in standard_input):
                return self._handle_error("❌ Numbers only")

            digits = list(standard_input)
            if len(digits) != 8:
                return self._handle_error("❌ Invalid date")
            day = int(''.join(digits[0:2])) # Join digits 1-2 (index 0 and 1) from the digits list to an empty string to convert it into integer "day"
            month = int(''.join(digits[2:4])) # Join digits 3-4 (index 2 and 3) from the digits list to an empty string to convert it into integer "month"
            year = int(''.join(digits[4:8])) # Join digits 5-8 (index 4 to 7) from the digits list to an empty string to convert it into integer "year"

        """Validate month"""

        if not (1 <= month <= 12): # Check if month isn't equal or greater than 1 or equal or less than 12
            return self._handle_error("❌ Invalid date")

        """Days per month"""

        if month == 2: # Check if month is February
            is_leap = (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) # If year is divisible by 4 and not by 100, unless it is divisible by 400
            max_day = 29 if is_leap else 28 # 29 days if it is a leap year, otherwise 28
        elif month in [4, 6, 9, 11]: # Check if month is April, June, September or November
            max_day = 30 # 30 days
        else: # Check if month is January, March, May, July, August, October or December
            max_day = 31 # 31 days

        if not (1 <= day <= max_day):
            return self._handle_error("❌ Invalid date")

        try:
            date = datetime.date(year, month, day) # Validate date using datetime
            if date >= datetime.date(2032, 1, 1):  # Check if date is before 01/01/2032
                return self._handle_error("❌ Adults only")

        except ValueError:
            return self._handle_error("❌ Numbers only")

        return self._handle_valid("✅ Password validated ")