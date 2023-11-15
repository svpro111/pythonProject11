import requests

salary = lambda x: [x['salary']['from'], x['salary']['to'], x['salary']['currency'], x['salary']['gross']] if x[
                                                                                                                  'salary'] is not None else [
                                                                                                                                                 None] * 4
# salary=lambda x: [x['salary']['from'],x['salary']['to'],x['salary']['currency'],x['salary']['gross']] if x['salary'] is not None else [None]*4
snippet = lambda x: [x['snippet']['responsibility'], x['snippet']['requirement']] if ['snippet'] is not None else [
                                                                                                                      None] * 2
# snippet=lambda x: [x['snippet']['responsibility'],x['snippet']['requirement']] if ['snippet'] is not None else [None]*2

vac = []
'''
for i in range(10):
  url = 'https://api.hh.ru/vacancies?text=Программист&per_page=100&area=1&area=2&page={}'.format(str(i))
  vac+=[[x['id'],x['name']]+salary(x)+[x['employer']['name']]+[x['area']['name']]+snippet(x) for x in requests.get(url).json()['items']
'''
for i in range(10):
    url = 'https://api.hh.ru/vacancies?text=Программист&per_page=100&area=1&area=2&page={}'.format(str(i))
    vac += [[x['id'], x['name']] + salary(x) + [x['employer']['name']] + [x['area']['name']] + snippet(x) for x in
            requests.get(url).json()['items']]

d = dict()
n1 = 0

for i in vac:
    if (i[2] is not None) and (i[4] == 'RUR'):
        if i[2] > 50000:
            n1 += 1
            d.update({'Число вакансий больше 50000 руб': n1})
print(d)

result_set = set()

# делаем множество id вакансий в которых зп больше 50к + в рублях + питон в навыках
for elem in vac:
    if (elem[2] is not None) and (elem[-1] is not None):
        if (elem[2] > 50000) and ('RU' in elem[4]) and ('Python' in elem[-1]):
            result_set.add(elem[0])
print(result_set)

# теперь если id совпадает с 0 элементом (тоже id) в полном массиве вакансий, то выводим вакансию
for elements in vac:
    if elements[0] in result_set:
        print(elements)


# считаем среднее по мск и спб
def av_salary(x):
    if x[2] is not None and x[3] is not None:
        return (x[2] + x[3]) / 2
    elif x[2] is not None:  # если "от" пустое
        return x[2]
    else:
        return x[3]  # если "до" пустое


counter1 = 0
counter2 = 0
salary1 = 0
salary2 = 0

for i in vac:
    if ('python' in i[1].lower()) and (i[7] == 'Москва'):
        if (av_salary(i) is not None):
            salary1 += av_salary(i)
            counter1 += 1
    elif ('python' in i[1].lower()) and (i[7] == 'Санкт-Петербург'):
        if (av_salary(i) is not None):
            salary2 += av_salary(i)
            counter2 += 1

sal1 = salary1 / counter1
sal2 = salary2 / counter2

print('Moscow', round(sal1))
print('Piter', round(sal2))