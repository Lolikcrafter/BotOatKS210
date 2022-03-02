import requests as urlreq
import pandas as pd

rasp = {}
	
def get_schedule(needday):
	try:
		global rasp
		req = urlreq.get("https://www.oat.ru/students/raspisanie/schedule-campus_1/rspcls18.html", headers={"User-Agent":"Mozilla/5.0"}).text
		wp = req.replace("</td>", "###</td>")
		dfs = pd.read_html(wp)

		raspisanie = dfs[0].to_dict("list")
		raspisanie2 = dfs[0].to_dict("list")

		for key in raspisanie:
			raspisanie2[key] = list(map(lambda x:x.split("###"), raspisanie2[key]))
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
		return rasp[needday]
	except Exception as e:
		print("site_parsing", e)

if __name__ == "__main__":
	pass

