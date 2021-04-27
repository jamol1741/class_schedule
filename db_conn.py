import sqlite3


class DBHelper:
    def __init__(self, dbname="db/schedule.db"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname, check_same_thread=False)

    def get_items(self, user_id, day_id, part):
        """
        :param user_id: User id
        :param day_id: Day id
        :param part: part number
        :return: science_name
        :return: room_number
        :return: teacher_name
        """
        stmt = """SELECT s.name, r.number_room, t.name FROM schedules 
                    JOIN sciences s on s.id = schedules.science_id
                    JOIN rooms r on r.id = schedules.room_id
                    JOIN teachers t on t.id = s.teacher_id
                    WHERE s.group_id = (SELECT users.group_id FROM users WHERE _user_id = (?) LIMIT 1) 
                    AND day_id = (?) 
                    AND part_id = (?)
                    LIMIT 1;"""

        args = (user_id, day_id, part)

        res = self.conn.execute(stmt, args).fetchall()[0]
        # print(res)
        return res[0], res[1], res[2]

    def add_user(self, user_id, group_id='', user_level=1, user_name='', name='', method_id=1):
        """INSERT INTO memos(id,text)
        SELECT 5, 'text to insert'
        WHERE NOT EXISTS(SELECT 1 FROM memos WHERE id = 5 AND text = 'text to insert');"""
        stmt = """INSERT INTO users (_user_id, group_id, user_level, _user_name, _name, method_id) 
                            SELECT  ?, ?, ?, ?, ?, ? 
                            WHERE NOT EXISTS(SELECT 1 FROM users WHERE (?) = _user_id)"""
        args = (user_id, group_id, user_level, user_name, name, method_id, user_id)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_users_id(self):
        stmt = "SELECT _user_id FROM users WHERE _user_id > (?);"
        args = (1,)
        res = self.conn.execute(stmt, args).fetchall()
        if res:
            return res[0]
        else:
            return []

    def get_general_admin_id(self):
        stmt = "SELECT _user_id FROM users WHERE users.user_level = 256;"
        res = self.conn.execute(stmt).fetchall()
        if res:
            return res[0]
        else:
            return []

    def get_faculties(self):
        stmt = "SELECT name FROM faculties;"
        res = self.conn.execute(stmt).fetchall()
        if res:
            return res
        else:
            return []

    def get_stages(self, faculty_id):
        stmt = "SELECT name FROM stages WHERE faculty_id = (?);"
        args = (faculty_id,)
        res = self.conn.execute(stmt, args).fetchall()
        if res:
            return res
        else:
            return []

    def get_directions(self, stage_id, faculty_id):
        stmt = """SELECT d.name FROM directions d
                        JOIN stages s on d.stage_id = s.stage
                                WHERE stage_id = (?) AND s.faculty_id = (?);"""
        args = (stage_id, faculty_id)
        res = self.conn.execute(stmt, args).fetchall()
        if res:
            return res
        else:
            return []

    def get_groups(self, direction_id):
        stmt = "SELECT name FROM groups WHERE direction_id = (?);"
        args = (direction_id,)
        res = self.conn.execute(stmt, args).fetchall()
        if res:
            return res
        else:
            return []

    def get_faculty_id(self, faculty_name):
        stmt = "SELECT id FROM faculties WHERE name = (?);"
        args = (faculty_name,)
        res = self.conn.execute(stmt, args).fetchall()
        if res:
            return res[0][0]
        else:
            return []

    def get_stage_id(self, stage_name):
        stmt = "SELECT stage FROM stages WHERE name = (?);"
        args = (stage_name,)
        res = self.conn.execute(stmt, args).fetchall()
        if res:
            return res[0][0]
        else:
            return []

    def get_direction_id(self, direction_name):
        stmt = "SELECT id FROM directions WHERE name = (?);"
        args = (direction_name,)
        res = self.conn.execute(stmt, args).fetchall()
        if res:
            return res[0][0]
        else:
            return []

    def get_group_id(self, group_name):
        stmt = "SELECT id FROM groups WHERE name = (?);"
        args = (group_name,)
        res = self.conn.execute(stmt, args).fetchall()
        if res:
            return res[0][0]
        else:
            return []

    def set_group_id(self, user_id, group_id):
        stmt = "UPDATE users SET group_id = (?) WHERE _user_id = (?)"
        args = (group_id, user_id)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def is_group_iden(self, user_id):
        stmt = "SELECT group_id FROM users WHERE _user_id = (?);"
        args = (user_id,)
        res = self.conn.execute(stmt, args).fetchall()
        if res:
            return res[0][0]
        else:
            return []

    # def delete_item(self, item_text):
    #     stmt = "DELETE FROM items WHERE description = (?)"
    #     args = (item_text, )
    #     self.conn.execute(stmt, args)
    #     self.conn.commit()

    # def get_items(self):
    #     stmt = "SELECT description FROM items"
    #     return [x[0] for x in self.conn.execute(stmt)]

    # def get_name(self, id):
    #     stmt1 = "SELECT Arabcha FROM ismlar WHERE _id = (?)"
    #     stmt2 = "SELECT Oqilishi FROM ismlar WHERE _id = (?)"
    #     stmt3 = "SELECT Manosi FROM ismlar WHERE _id = (?)"
    #     args = (id,)
    #     arabcha = [x[0] for x in self.conn.execute(stmt1, args)][0]
    #     oqilishi = [x[0] for x in self.conn.execute(stmt2, args)][0]
    #     manosi = [x[0] for x in self.conn.execute(stmt3, args)][0]
    #
    #     ret = "[ {} ]   -   [ {} ] \n {}".format(arabcha, oqilishi, manosi)
    #
    #     return ret
    #
    # def get_name_by(self, name):
    #     stmt1 = "SELECT Arabcha FROM ismlar WHERE Oqilishi = (?)"
    #     stmt2 = "SELECT Oqilishi FROM ismlar WHERE Oqilishi = (?)"
    #     stmt3 = "SELECT Manosi FROM ismlar WHERE Oqilishi = (?)"
    #     args = (name,)
    #     arabcha = [x[0] for x in self.conn.execute(stmt1, args)][0]
    #     oqilishi = [x[0] for x in self.conn.execute(stmt2, args)][0]
    #     manosi = [x[0] for x in self.conn.execute(stmt3, args)][0]
    #
    #     ret = "[ {} ]   -   [ {} ] \n {}".format(arabcha, oqilishi, manosi)
    #
    #     return ret

    # def get_users(self, user_id):
    #     stmt = "SELECT COUNT(_user_id) FROM users WHERE _user_id = (?)"
    #     args = (user_id,)
    #
    #     return self.conn.execute(stmt, args)
    #
    # def get_names(self):
    #     stmt = "SELECT Oqilishi FROM ismlar"
    #     return self.conn.execute(stmt)
    #

    def cmd_delete_my_account(self, user_id):
        stmt = """DELETE FROM users
                    WHERE _user_id = (?);"""
        args = (user_id,)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_methods(self):
        stmt = "SELECT time_delta FROM method_remind;"
        res = self.conn.execute(stmt).fetchall()
        if res:
            return res
        else:
            return []

    def get_start_times(self, section_id=1):
        stmt = "SELECT number, start FROM parts WHERE section_id = (?);"
        args = (section_id,)
        res = self.conn.execute(stmt, args).fetchall()
        if res:
            return res
        else:
            return []

    def get_delta_times(self):
        stmt = "SELECT id, time_delta FROM method_remind;"
        res = self.conn.execute(stmt).fetchall()
        if res:
            return res
        else:
            return []

    def get_identified_user(self, section_id, part, method_id, day_id):
        stmt = """select _user_id from users
        INNER JOIN groups g ON users.group_id = g.id
            WHERE users.group_id IS NOT NULL
              AND method_id = (?)
              AND g.section_id = (?)
                AND users.group_id
                        IN (SELECT schedules.group_id FROM schedules
                                INNER JOIN parts p on p.id = schedules.part_id
                                    WHERE day_id = (?) AND p.number = (?));"""
        args = (method_id, section_id, day_id, part)
        res = self.conn.execute(stmt, args).fetchall()
        if res:
            return res
        else:
            return []

    def get_user_info(self, user_id):

        """:returns
                'user_id':
                'user_name':
                'name':
                'group':
                'level':
                'delta_time':
                    In dict
        """

        stmt = """select _user_id, _user_name, users._name, g.name, l.name, mr.time_delta from users
                INNER JOIN groups g ON users.group_id = g.id
                INNER JOIN levels l on users.user_level = l.level
                INNER JOIN method_remind mr ON users.method_id = mr.id
                    WHERE _user_id = (?)
                        LIMIT 1;
                """
        args = (user_id,)
        res = self.conn.execute(stmt, args).fetchall()
        # print(res[0])
        # print(len(res[0]))
        if len(res[0]) == 6:
            ret = {
                'user_id': res[0][0],
                'user_name': res[0][1],
                'name': res[0][2],
                'group': res[0][3],
                'level': res[0][4],
                'delta_time': res[0][5]
            }
            return ret
        else:
            return []
