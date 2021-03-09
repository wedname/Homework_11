import json
import re

"""
Description of the work of the authorization and registration.
"""

f = open('./users.json', 'r')
users = json.loads(f.read())
file_check = open('./todo.json', 'r')


def check_name():
    while True:
        name = input("Введите ФИО: ")
        if len(name.split()) < 3:
            print("Не верно! Введите ФИО.")
            continue
        else:
            return name


def check_email():
    file = open('./users.json', 'r')
    users_list = json.loads(file.read())
    file.close()
    regex = r'(^|\s)[-a-z0-9_.]+@([-a-z0-9]+\.)+[a-z]{2,6}(\s|$)'
    email_regex = re.compile(regex)
    while True:
        email = input("Введите email: ")
        is_valid = email_regex.findall(email)
        for i in range(0, len(users_list)):
            if users_list[i]["email"] != email and is_valid:
                return email
            elif not is_valid:
                print("Не верный email!")
            elif users_list[i]["email"] == email:
                print("Пользователь с таким email уже есть! Введите другой.")
                continue


def check_password_for_registration():
    is_correct_password = False
    while not is_correct_password:
        password = input("Введите пароль: ")
        has_upper = False
        has_lower = False
        has_digit = False
        has_spec_char = False
        if not len(password) > 8:
            print("Пароль должен быть > 8 символов!")
            continue
        for char in password:
            if char.isupper():
                has_upper = True
            if char.islower():
                has_lower = True
            if char.isdigit():
                has_digit = True
            if not char.isalnum():
                has_spec_char = True
        if not has_upper:
            print("В пароле должна быть минимум 1 большая буква!")
            continue
        if not has_lower:
            print("В пароле должна быть минимум 1 маленькая буква!")
            continue
        if not has_digit:
            print("В пароле должна быть минимум 1 цифра!")
            continue
        if not has_spec_char:
            print("В пароле должен быть минимум 1 спецсимвол!")
            continue
        return password


def registration():
    name = check_name()
    username = input("Введите ник: ")
    email = check_email()
    password = check_password_for_registration()
    while True:
        password_check = input("Подтвердите пароль: ")
        if password_check != password:
            print("Не верный пароль!")
            continue
        else:
            break

    users.append({"ID": len(users) + 1, "name": name, "username": username, "email": email, "password": password})
    file = open('./users.json', 'w')
    file.write(json.dumps(users))
    file.close()


def authorization():
    file = open('./users.json', 'r')
    users_list = json.loads(file.read())
    file.close()
    while True:
        email = input("Введите email: ")
        for i in range(0, len(users_list)):
            if users_list[i]["email"] != email:
                continue
            elif users_list[i]["email"] == email:
                check_password(i, users_list)
                print(f"Здраствуйте, {users_list[i]['name']}")
                todo_list(users_list[i]["ID"])
                break
        break


def check_password(user_idx, users_list):
    while True:
        password = input("Введите пароль: ")
        if password != users_list[user_idx]["password"]:
            print("Не верный пароль!")
            continue
        else:
            break


"""
Description of the work of the todo list.
"""


def todo_list(current_user):
    while True:
        controls_list = input("1 - Добавить задачу\n"
                              "2 - Изменить задачу\n"
                              "3 - Удалить задачу\n"
                              "4 - Просмотреть задачи\n"
                              "0 - Выйти из аккаунта\n"
                              "Введите действие: ")
        if controls_list == "1":
            add_task_in_todo(current_user)
        elif controls_list == "2":
            edit_task_in_todo(current_user)
        elif controls_list == "3":
            delete_task_in_todo(current_user)
        elif controls_list == "4":
            show_users_todo_list(current_user)
        elif controls_list == "0":
            break
        else:
            print("Нет такого действия!")
            continue


def add_task_in_todo(user_id):
    file = open('./todo.json', 'r')
    users_todo_list = json.loads(file.read())
    file.close()
    date = input("Введите дату для задачи: ")
    case_name = input("Введите название задачи: ")
    description = input("Введите описание задачи: ")
    priority = input("Введите приортет задачи: ")
    users_todo_list.append({"user_id": user_id, "date": date, "case name": case_name, "description": description,
                            "priority": priority})
    file = open('./todo.json', 'w')
    file.write(json.dumps(users_todo_list))
    file.close()


def edit_task_in_todo(user_id):
    file = open('./todo.json', 'r')
    users_todo_list = json.loads(file.read())
    file.close()
    search_name = input("Введите название задачи, которую хотите отредактировать: ")
    for i in range(0, len(users_todo_list)):
        if users_todo_list[i]['case name'] == search_name and users_todo_list[i]['user_id'] == user_id:
            edit_date = input("Введите дату для задачи: ")
            edit_case_name = input("Введите название задачи: ")
            edit_description = input("Введите описание задачи: ")
            edit_priority = input("Введите приортет задачи: ")
            users_todo_list[i] = {"user_id": user_id, "date": edit_date, "case name": edit_case_name,
                                  "description": edit_description, "priority": edit_priority}
            file = open('./todo.json', 'w')
            file.write(json.dumps(users_todo_list))
            file.close()
            break
    else:
        print("Нет такой задачи!")


def delete_task_in_todo(user_id):
    file = open('./todo.json', 'r')
    users_todo_list = json.loads(file.read())
    file.close()
    search_name = input("Введите название задачи, которую хотите удалить: ")
    for i in range(0, len(users_todo_list)):
        if users_todo_list[i]['case name'] == search_name and users_todo_list[i]['user_id'] == user_id:
            users_todo_list.pop(i)
            file = open('./todo.json', 'w')
            file.write(json.dumps(users_todo_list))
            file.close()
            break
    else:
        print("Нет такой задачи!")


def show_users_todo_list(user_id):
    file = open('./todo.json', 'r')
    users_todo_list = json.loads(file.read())
    file.close()
    for i in range(len(users_todo_list)):
        if users_todo_list[i]['user_id'] == user_id:
            print(f"\n{users_todo_list[i]['date']}: {users_todo_list[i]['case name']} - "
                  f"{users_todo_list[i]['description']} ({users_todo_list[i]['priority']})\n")


while True:
    controls_enter = input("1 - Регистрация\n"
                           "2 - Вход\n"
                           "0 - Выход из программы\n"
                           "Введите действие: ")
    if controls_enter == "1":
        registration()
    elif controls_enter == "2":
        authorization()
    elif controls_enter == "0":
        exit()
    else:
        print("Нет такого действия!")
        continue
