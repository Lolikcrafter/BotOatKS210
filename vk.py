import vk_api
import vk_api.bot_longpoll as vklongpoll
import vk_api.keyboard as vkkb
import random
import time
from main import keywords, nickname
from site_parsing import get_schedule
from excel import find_changes, download_file
import datetime
import calendar
import json

days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
week_word = ["","Перв", "Втор"]

vk_session = vk_api.VkApi(token='cb139e4ed8d35ffde7aa7699ea7d0acdea71c6946433baa0963fcc50f2b950535b9dc2386b870a392c781', api_version="5.131")
longpoll = vklongpoll.VkBotLongPoll(vk_session, group_id=210946341)
vk = vk_session.get_api()
kb = vkkb.VkKeyboard()
kb.add_callback_button("Сегодня",payload={"type":"today"})
kb.add_callback_button("Завтра",payload={"type":"tommorow"})

def listening():

	for event in longpoll.listen():
		action = event.raw['type']
		if action == "message_new":
			text = event.raw['object']['message']['text'].split()
			date = event.raw['object']['message']['date']
			conversation_id = event.raw['object']['message']['peer_id']
			if text:
				#try:
				chat_name = vk.messages.getConversationsById(peer_ids=conversation_id)['items'][0]['chat_settings']['title']
				if text[0].capitalize() == nickname and text[1] == "расписание":
					week_num = 0
					dayofweek = 0
					counts = 0
					if "завтра" in text:
						date += time.timezone + 86400
						week_num = 2 - (datetime.date(datetime.datetime.fromtimestamp(date).year,datetime.datetime.fromtimestamp(date).month, datetime.datetime.fromtimestamp(date).day).isocalendar().week) % 2
						dayofweek = datetime.datetime.weekday(datetime.datetime.fromtimestamp(date))
					else:
						date += time.timezone
						week_num = 2 - (datetime.date(datetime.datetime.fromtimestamp(date).year,datetime.datetime.fromtimestamp(date).month, datetime.datetime.fromtimestamp(date).day).isocalendar().week) % 2
						dayofweek = datetime.datetime.weekday(datetime.datetime.fromtimestamp(date))
					if dayofweek != 6:
						schedule = get_schedule(f"{week_num}-{days[dayofweek]}")
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
						message = f"Расписание {chat_name}\n{week_name} {days[dayofweek]}\n\n"
						filename = download_file("Ленина")
						changes = find_changes(filename, group=chat_name, date=f"{datetime.datetime.fromtimestamp(date).strftime('%d.%m')}")
						#print(changes)
						for key in schedule:
							message += f"{key}{schedule[key]}\n"
						for change in changes:
							message += f"{change}\n"
						if counts == 1 or counts == 3:
							message += "Сегодня классный час"
						elif counts == 2 or counts == 4:
							message += "Сегодня методический час"
						send_message(message, conversation_id, kb)
					else:
						send_message(f"{week_word[week_num]}ое воскресенье\n\nПриятного отдыха", kb)
				#except Exception as e:
					#send_message(e, peer_id, kb)
					#print("Заебали", e)

		elif action == "message_event":
			event_type = event.raw['object']['payload']['type']
			user_id = event.raw['object']['user_id']
			peer_id = event.raw['object']['peer_id']
			event_id = event.raw['object']['event_id']
			message = ""
			event_data = ""
			date = vk.utils.getServerTime()
			print(date)
			try:
				chat_name = vk.messages.getConversationsById(peer_ids=peer_id)['items'][0]['chat_settings']['title']
				week_num = 0
				dayofweek = 0
				counts = 0
				if event_type == "tommorow":
					date += 86400 #time.timezone + 86400
					print(date)
					week_num = 2 - (datetime.date(datetime.datetime.fromtimestamp(date).year,datetime.datetime.fromtimestamp(date).month, datetime.datetime.fromtimestamp(date).day).isocalendar().week) % 2
					dayofweek = datetime.datetime.weekday(datetime.datetime.fromtimestamp(date))
				else:
					#date += time.timezone
					print(date)
					week_num = 2 - (datetime.date(datetime.datetime.fromtimestamp(date).year,datetime.datetime.fromtimestamp(date).month, datetime.datetime.fromtimestamp(date).day).isocalendar().week) % 2
					dayofweek = datetime.datetime.weekday(datetime.datetime.fromtimestamp(date))
				if dayofweek != 6:
					schedule = get_schedule(f"{week_num}-{days[dayofweek]}")
					print(week_num, days[dayofweek])
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
					message = f"Расписание {chat_name}\n{week_name} {days[dayofweek]}\n\n"
					filename = download_file("Ленина")
					changes = find_changes(filename, group=chat_name, date=f"{datetime.datetime.fromtimestamp(date).strftime('%d.%m')}")
					print(f"{datetime.datetime.fromtimestamp(date).strftime('%d.%m')}")
					#print(changes)
					for key in schedule:
						message += f"{key}{schedule[key]}\n"
					for change in changes:
						message += f"{change}\n"
					if counts == 1 or counts == 3:
						message += "Сегодня классный час"
					elif counts == 2 or counts == 4:
						message += "Сегодня методический час"
				else:
					message = f"{week_word[week_num]}ое воскресенье\n\nПриятного отдыха"
			except Exception as e:
				print("Заебали", e)
				#send_message(e, peer_id, kb)
			send_message(message, peer_id, kb)

def send_event(event_data, user_id, peer_id, event_id):
	try:
		vk.messages.sendMessageEventAnswer(event_id=event_id, user_id=user_id, peer_id=peer_id, event_data=event_data)
	except Exception as e:
		print(e)

def send_message(message, peer_id, keyboard=kb):
	try:
		#print(kb.get_keyboard())
		vk.messages.send(message=message, peer_id=peer_id, random_id=random.randint(0, 32000), keyboard=keyboard.get_keyboard())
		return True
	except Exception as e:
		print(e)

if __name__ == "__main__":
	listening()
