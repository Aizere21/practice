from datetime import date, datetime, timedelta


def main():
    today = date.today()

    
    five_days_ago = today - timedelta(days=5)
    print("Five days ago:", five_days_ago)

    
    print("Yesterday:", today - timedelta(days=1))
    print("Today:", today)
    print("Tomorrow:", today + timedelta(days=1))

    
    current_datetime = datetime.now()
    without_microseconds = current_datetime.replace(microsecond=0)
    print("Datetime without microseconds:", without_microseconds)

   
    first_datetime = datetime(2024, 1, 1, 12, 0, 0)
    second_datetime = datetime(2024, 1, 2, 12, 30, 0)
    difference_seconds = abs((second_datetime - first_datetime).total_seconds())
    print("Difference in seconds:", difference_seconds)


if __name__ == "__main__":
    main()