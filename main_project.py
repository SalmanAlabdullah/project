import sqlite3

# كائن ليطبق وضائف SQL
class sql:
    def __init__(self, sql):
        self.db = sqlite3.connect(f"{sql}")

    def insert(self, table, add):
        self.db.execute(f"INSERT INTO {table} VALUES ({add})")
        self.db.commit()
        # self.db.close()

    def remove(self, table, remove):
        self.db.execute(f"DELETE FROM {table} WHERE ID = {remove} ")
        self.db.commit()

    def edit(self, table, edit, ID):
        if edit != "n" and edit != '':
            self.db.execute(f"UPDATE {table} SET {edit} WHERE ID = {ID}")
        self.db.commit()

    def show(self, table, students_num):
        db_cursor = self.db.cursor()
        db_cursor.execute(f"SELECT NAME , NICKNAME, AGE , CLASS , REGISTER_DATE , LESSON FROM Students"
                          f" ST LEFT JOIN LESSONS LE ON ST.ID = LE.ID WHERE ST.ID = {students_num}")
        rows = db_cursor.fetchall()
        print(f'--- ID = {students_num} ---')
        for row in rows:
            print(row)

        if rows == []:
            print("الطالب غير موجود")
        else:
            print("تمت العملية بنجاح")

    def verify(self, remove):
        db_cursor = self.db.cursor()
        db_cursor.execute(f"SELECT * FROM Students WHERE ID = {remove}")
        rows = db_cursor.fetchall()

        if rows == []:
            return False
        else:
            return True

    def verify_message(self, remove):
        if self.verify(remove):
            print("تمت العملية بنجاح")
        else:
            print("الطالب غير موجود")

    def close(self):
        self.db.close()

    def commit(self):
        self.db.commit()

# الرباط مع SQL
academy_database = sql("ACADEMY.sqlite")

# دالة تهيئة للتعديل على جدول
def edit_1(data_type, str_int, data_type_print):
    order = input(f"أدخل {data_type_print} (إذا كنت لاتريد تغيير {data_type_print} اتركه فارغا)")
    edit_list = []
    if str_int == 'str':
        if order != '':
            return f'{data_type} = "{order}"'
    else:
        if order != '':
            return f'{data_type} = {order}'
    return "n"

# البرنامج
while True:
    try:
        command = input("الرجاء اختيار العملية التي تريد إجرائها:\n* لإضافة طالب إضغط على حرف a"
                        "\n* لحذف طالب إضغط على حرف d\n* لتعديل معلومات طالب إضغط على حرف u"
                        "\n* لعرض معلومات طالب إضغط على حرف s\n")


        while True:

            # شرط لإضافة طالب
            if command == "a":
                option_to_add = input("لإضافة درس جديد لطالب موجود [y] لإضافة طالب جديد [n]")
                ID = input("رقم الطالب")



                if option_to_add == 'n' :
                    data = [ID , f'"{input("الأسم")}"', f'"{input("الكنية")}"',
                            input("العمر"), f'"{input("الصف")}"', f'"{input("تاريخ التسجيل")}"']
                    str_data = []
                    for x in data:
                        str_data.append(str(x))
                    join_str_data = ",".join(str_data)



                    academy_database.insert("Students", join_str_data)

                lessons = f'"{input("الدروس")}"'
                academy_database.insert('LESSONS', f' {ID} , {lessons} ')

                print("تمت العملية بنجاح")
                break

            # شرط لحذف طالب
            elif command == "d":
                remove = input("أدخل رقم الطالب المراد حذفه")
                academy_database.verify_message(remove)
                academy_database.remove("LESSONS", remove)
                academy_database.remove("Students", remove)
                break

            # شرط لتعديل على طالب
            elif command == "u":
                ID = input("أدخل رقم الطالب")

                if academy_database.verify(ID) is False:
                    print("الطالب غير موجود")
                else:
                    edit = [edit_1('NAME', 'str', 'الأسم'),
                            edit_1('NICKNAME', 'str', 'الكنية'),
                            edit_1('AGE', 'int', 'العمر'),
                            edit_1('CLASS', 'str', 'الصف'),
                            edit_1('REGISTER_DATE', 'str', 'تاريخ التسجيل')]

                    lesson_edit = edit_1('LESSON', 'str', 'الدروس')

                    edit_list = []
                    for change in edit:
                        if change != 'n':
                            edit_list.append(change)

                    edit_join = ','.join(edit_list)

                    academy_database.edit("LESSONS", lesson_edit, ID)
                    academy_database.edit("Students", edit_join, ID)
                    academy_database.verify_message(ID)

                break

            # شرط لرؤية بيانات طالب
            elif command == "s":
                students_num = input("أدخل البيانات المراد إطهارها")
                academy_database.show("Students", students_num)
                break

            else:
                command = input("الإدخال خاطئ اعد الإدخال : ")

        end = input("هل تريد إنها البرنامج؟ إضغط [y]")
        if end == "y":
            academy_database.commit()
            academy_database.close()
            break

    except:
        print("هناك خطأ يرجى إعادة الإدخال")
