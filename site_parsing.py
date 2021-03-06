import urllib.request as urlreq
import pandas as pd
import time

rasp = {}

headers = { 
	"user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36", 
	"accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9", 
	"accept-encoding" : "gzip, deflate, br", 
	"cache-control"   : "no-cache", 
	"pragma" : "no-cache", 
	"upgrade-insecure-requests" : "1" 
}

proxies={"http": "http://195.91.221.230:55443", "http": "htpps://91.224.62.194:8080"}
	
def get_schedule(needday):
	global rasp
	#session = HTMLSession()
	req = urlreq.Request("https://www.oat.ru/students/raspisanie/schedule-campus_1/rspcls18.html", headers={"User-Agent":"Mozilla/5.0"})
	wp = urlreq.urlopen(req).read().decode("utf-8").replace("</td>", "###</td>")
	dfs = pd.read_html(wp)

	raspisanie = dfs[0].to_dict("list")
	raspisanie2 = dfs[0].to_dict("list")

	for key in raspisanie:
		#print(raspisanie2[key])
		raspisanie2[key] = list(map(lambda x:x.split("###"), raspisanie2[key]))
	#print(raspisanie2)
	raspisanie2.pop(0)
	raspisanie2.pop(1)

	for key in raspisanie2:
		rasp.update([(raspisanie2[key][0][0], raspisanie2[key][1:])])
	raspisanie = rasp
	for day in rasp:
		if "Воскресенье" in day:
			continue
		subjects = rasp[day]
		raspisanie[day] = {}
		for num in range(len(subjects)):
			subject = subjects[num]
			if len(subject) > 2:
				if "+" in subject[0]:
					try:
						teachers = [subject[1], subject[3]]
						cabinets = [subject[4], subject[5]]
						raspisanie[day].update([(f"{num+1} пара: ",f"{subject[0]}\n⠀1 подгруппа:\n⠀⠀Препод: {teachers[0][:-2]}\n⠀⠀Кабинет: {cabinets[0]}\n⠀2 подгруппа:\n⠀⠀Препод: {teachers[1][:-2]}\n⠀⠀Кабинет: {cabinets[1]}\n")])
					except:
						teacher = subject[1]
						cabinet = subject[2]
						raspisanie[day].update([(f"{num+1} пара: ",f"{subject[0]}\n⠀Препод: {teacher}\n⠀Кабинет: {cabinet}\n")])
				else:
					teacher = subject[1]
					cabinet = subject[2]
					raspisanie[day].update([(f"{num+1} пара: ",f"{subject[0]}\n⠀Препод: {teacher}\n⠀Кабинет: {cabinet}\n")])
	rasp = raspisanie
	#print("Done")
	return rasp[needday]

if __name__ == "__main__":
	print(get_schedule("1-Суббота"))

