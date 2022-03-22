keywords = [
	"Какие пары?"
]
nickname = "Бот"

if __name__ == "__main__":
	import excel, site_parsing, time, datetime, calendar
	days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
	week_word = ["","Перв", "Втор"]
	counts = 0
	date = time.time() + 86400 #time.timezone + 86400					#print(date)
	week_num = 2 - (datetime.date(datetime.datetime.fromtimestamp(date).year,datetime.datetime.fromtimestamp(date).month, datetime.datetime.fromtimestamp(date).day).isocalendar().week) % 2
	dayofweek = datetime.datetime.weekday(datetime.datetime.fromtimestamp(date))
	schedule = site_parsing.get_schedule(f"{week_num}-{days[dayofweek]}")
	filename = excel.download_file("Ленина")
	changes = excel.find_changes(filename, group="КС210", date=f"{datetime.datetime.fromtimestamp(date).strftime('%d.%m')}")
	week_name = week_word[week_num]
	if any(dayofweek == num for num in (2, 4, 5)):
		week_name += "ая"
	else:
		if week_num == 1:
			week_name += "ый"
		else:
			week_name += "ой"
	thursday_state = ""

	if dayofweek == 3:
		today = datetime.datetime.fromtimestamp(date).day
		cal = calendar.Calendar(datetime.datetime.weekday(datetime.datetime.fromtimestamp(date - (86400 * (datetime.datetime.fromtimestamp(date).day - 1)))))
		for day, name in cal.itermonthdays2(datetime.datetime.fromtimestamp(date).year, datetime.datetime.fromtimestamp(date).month):
			if day != today and name == 3 and day:
				counts += 1
			if day == today:
				counts += 1
				break
	message = f"Расписание КС-210\n{week_name} {days[dayofweek]}\n\n"
	#print(changes)
	for key in schedule:
		message += f"{key}{schedule[key]}\n"
	for change in changes:
		message += f"{change}\n"
	if counts == 1 or counts == 3:
		message += "Сегодня классный час"
	elif counts == 2 or counts == 4:
		message += "Сегодня методический час"
	print(message)