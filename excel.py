import requests as req

url = "https://www.oat.ru/students/raspisanie"

def download_file(name="Ленина"):
	try:
		xl_url = "/izmenenia/Ленина 24.xlsx"
		html = req.get(f"{url}/izmenenia.php", allow_redirects=True, headers={"User-Agent":"Mozilla/5.0"})
		html = html.content.decode("utf-8").split("\n")
		for i in html:
			if name in i and "href" in i:
				xl_url = i.split("\"")[1]
				break
		file = req.get(f"{url}/{xl_url}", allow_redirects=True)
		filename = xl_url.split("/")[-1]
		open(f"{filename}", "wb").write(file.content)
		return filename
	except Exception as e:
		print("download_file", e)

def find_changes(filename, group="КС210", date="13.10"):
	if len(group) > 5:
		group = group[:2] + group[3:]
	#print(group)
	raw_changes = []
	changes = []
	try:
		if "xlsx" in filename:
			import openpyxl as xl
			xls = xl.load_workbook(filename)
			for row in xls[date].values:
				if group in row:
					#print(row)
					raw_changes.append(row)
		else:
			import xlrd as xl
			xls = xl.open_workbook(filename)
			for i in xls.sheet_by_name(date):
				#print(i[1])
				if i[1].value == group:
					row = ()
					for cell in i:
						if cell.value:
							row += (cell.value,)
						else:
							row += (None,)
					raw_changes.append(row)
	except Exception as e:
		print("excel -", e)
	if raw_changes:
		changes.append("Изменения:")
		for row in raw_changes:
			subject_num_was = row[2]
			subject_was = row[4]
			reason = row[6]
			subject_num_will = row[7]
			cabinet = row[8]
			subject_will = row[9]
			subject_teacher = row[10]
			if subject_will != "Отмена":
				changes.append(f"⠀{int(subject_num_will)} пара: {subject_will}\n⠀⠀Препод: {subject_teacher}\n⠀⠀Кабинет: {cabinet}\n")
			else:
				changes.append(f"⠀{int(subject_num_was)} пара: {subject_was}\n⠀⠀Состояние: {subject_will}")
	else:
		changes.append("Изменений нет")
	#print(changes, group, date, sep="\n")
	return changes



if __name__ == "__main__":
	print(find_changes(download_file(), date="02.03", group="КС210"))

