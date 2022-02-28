import vk_api
import vk_api.bot_longpoll as vklongpoll
import random
import time
from main import keywords, nickname
from site_parsing import get_schedule
import datetime

days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]

vk_session = vk_api.VkApi(token='cb139e4ed8d35ffde7aa7699ea7d0acdea71c6946433baa0963fcc50f2b950535b9dc2386b870a392c781', api_version="5.131")
longpoll = vklongpoll.VkBotLongPoll(vk_session, group_id=210946341)
vk = vk_session.get_api()

def listening():

	for event in longpoll.listen():
		action = event.raw['type']
		text = event.raw['object']['message']['text'].split()
		date = event.raw['object']['message']['date']
		conversation_id = event.raw['object']['message']['peer_id']

		if action == "message_new":
			#print(event.text)
			if text[0].capitalize() == nickname and text[1] == "расписание":
				if "завтра" in text:
					date += time.timezone + 86400
					week_num = 2 - (datetime.date(datetime.datetime.fromtimestamp(date).year,datetime.datetime.fromtimestamp(date).month, datetime.datetime.fromtimestamp(date).day).isocalendar().week) % 2
					dayofweek = datetime.datetime.weekday(datetime.datetime.fromtimestamp(date))
				else:
					date += time.timezone
					week_num = 2 - (datetime.date(datetime.datetime.fromtimestamp(date).year,datetime.datetime.fromtimestamp(date).month, datetime.datetime.fromtimestamp(date).day).isocalendar().week) % 2
					dayofweek = datetime.datetime.weekday(datetime.datetime.fromtimestamp(date))
				schedule = get_schedule(f"{week_num}-{days[dayofweek]}")
				print(schedule)
				message = ""
				for key in schedule:
					message += f"{key}{schedule[key]}"
				print(send_message(message, conversation_id))
		print(event.raw)

def send_message(message, peer_id):
	try:
		vk.messages.send(message=message, peer_id=peer_id, random_id=random.randint(0, 32000))
		return True
	except Exception as e:
		return e

if __name__ == "__main__":
	listening()
