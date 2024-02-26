from datetime import datetime


class Utilize:

    def get_time(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M")
