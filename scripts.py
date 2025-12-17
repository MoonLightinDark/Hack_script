from datacenter.models import Mark
from datacenter.models import Schoolkid
from datacenter.models import Chastisement
from datacenter.models import Lesson
from datacenter.models import Subject
from datacenter.models import Commendation

from random import choice


COMPLIMENTS = ['Молодец!', 'Отлично!', 'Хорошо!', 'Гораздо лучше, чем я ожидал!','Ты меня приятно удивил!'
				'Великолепно!', 'Прекрасно!', 'Ты меня очень обрадовал!', 'Именно этого я давно ждал от тебя!',
				'Сказано здорово – просто и ясно!', 'Ты, как всегда, точен!', 'Очень хороший ответ!', 
				'Талантливо!','Ты сегодня прыгнул выше головы!', 'Я поражен!', 'Уже существенно лучше!',
				'Потрясающе!', 'Замечательно!', 'Прекрасное начало!', 'Так держать!', 'Ты на верном пути!',
				'Здорово!', 'Это как раз то, что нужно!', 'Я тобой горжусь!', 'С каждым разом у тебя получается всё лучше!',
				'Мы с тобой не зря поработали!', 'Я вижу, как ты стараешься!', 'Ты растешь над собой!',
				'Ты многое сделал, я это вижу!', 'Теперь у тебя точно все получится!'
]

def find_child(child_name):
	try:
		child = Schoolkid.objects.get(full_name__contains=child_name)
		return child
	except Schoolkid.DoesNotExist:
		print('Такого ученика нет в базе данных либо допущена ошибка в имени')
	except Schoolkid.MultipleObjectsReturned:
		print('Слишком много подходящих учеников, введите полное имя')

def fix_marks(schoolkid):
	marks = Mark.objects.filter(schoolkid=schoolkid, points__in=['2','3'])
	for mark in marks:
		mark.points = choice(['4', '5'])

def remove_chastisements(schoolkid):
	chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
	chastisements.delete()

def create_commendation(schoolkid, lesson_name=None):
	try:
		class_num = schoolkid.year_of_study
		class_letter = schoolkid.group_letter
		if lesson_name is None:
			subject = Subject.objects.filter(year_of_study=class_num).order_by('?').first()
			lesson = Lesson.objects.filter(year_of_study__contains=class_num, group_letter__contains=class_letter).last()
		else:
			cap_lesson_name = lesson_name.capitalize()
			subject = Subject.objects.get(title=cap_lesson_name, year_of_study=class_num)
			lesson = Lesson.objects.get(year_of_study__contains=class_num, group_letter__contains=class_letter, subject=subject).last()

		Commendation.objects.create(text=choice(COMPLIMENTS),
								created=lesson.date,
								schoolkid=schoolkid,
								subject=subject,
								teacher=lesson.teacher)
	except Subject.DoesNotExist:
		print('Такого предмета нет или Вы ошиблись в названии')