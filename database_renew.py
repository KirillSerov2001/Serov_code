import psycopg2
from datetime import datetime

def connect_db():
    try:
        connection = psycopg2.connect(
            host=input("Введите ip датабазы: "),
            database=input("Введите название датабазы: "),
            user=input("Введите имя пользователя: "),
            password=input("Введите пароль: ")
        )
        return connection
    except Exception as error:
        print(f"Ошибка при подключении к базе данных: {error}")
        return None

def update_oktmo(connection, old_oktmo, new_oktmo):
    try:
        cursor = connection.cursor()

        current_date = datetime.now().strftime('%Y-%m-%d')

        cursor.execute("""
            SELECT id_нп
            FROM автоформа.насел_пункт
            WHERE октмо_нп = %s
        """, (old_oktmo,))
        result = cursor.fetchone()

        if result is None:
            print("Населенный пункт с указанным ОКТМО не найден.")
            return

        id_np = result[0]

        cursor.execute("""
            UPDATE автоформа.история_нп
            SET дата_искл = %s
            WHERE id_нп = %s AND дата_искл IS NULL
        """, (current_date, id_np))

        new_oktmo_settlement_prefix = new_oktmo[:8]
        cursor.execute("""
            SELECT id_поселение
            FROM автоформа.насел_пункт
            WHERE октмо_поселение = %s
        """, (new_oktmo_settlement_prefix,))
        result = cursor.fetchone()

        if result is None:
            print("Поселение с указанным ОКТМО не найдено.")
            return

        id_new_poselenie = result[0]

        cursor.execute("""
            SELECT название_нп
            FROM автоформа.история_нп
            WHERE id_нп = %s
        """, (id_np,))
        result = cursor.fetchone()

        if result is None:
            print("Населенный пункт с указанным ID не найден.")
            return

        np_name = result[0]

        new_oktmo_last_3 = new_oktmo[-3:]
        cursor.execute("""
            INSERT INTO автоформа.история_нп (id_нп, октмо_нп, id_поселение, название_нп, дата_вкл)
            VALUES (%s, %s, %s, %s, %s)
        """, (id_np, new_oktmo_last_3, id_new_poselenie, np_name, current_date))

        cursor.execute("""
            INSERT INTO автоформа.перекодировочная (октмо_старый, октмо_новый)
            VALUES (%s, %s)
        """, (old_oktmo, new_oktmo))

        connection.commit()
        print("ОКТМО успешно обновлено.")

    except Exception as error:
        connection.rollback()
        print(f"Ошибка при обновлении ОКТМО: {error}")
    finally:
        cursor.close()


def update_np_name(connection, old_oktmo_np, new_np_name):
    try:
        cursor = connection.cursor()

        current_date = datetime.now().strftime('%Y-%m-%d')

        cursor.execute("""
            SELECT id_нп FROM автоформа.насел_пункт
            WHERE октмо_нп = %s
        """, (old_oktmo_np,))
        result = cursor.fetchone()

        if result is None:
            print("Населенный пункт с указанным ОКТМО не найден.")
            return

        id_np = result[0]

        cursor.execute("""
            SELECT октмо_нп, id_поселение
            FROM автоформа.история_нп
            WHERE id_нп = %s AND дата_искл IS NULL
        """, (id_np,))
        np = cursor.fetchone()

        if np is None:
            print("Населенный пункт с указанным ID не найден.")
            return

        old_oktmo, id_poselenie = np

        cursor.execute("""
            UPDATE автоформа.история_нп
            SET дата_искл = %s
            WHERE id_нп = %s AND дата_искл IS NULL
        """, (current_date, id_np))

        cursor.execute("""
            INSERT INTO автоформа.история_нп (id_нп, октмо_нп, id_поселение, название_нп, дата_вкл)
            VALUES (%s, %s, %s, %s, %s)
        """, (id_np, old_oktmo, id_poselenie, new_np_name, current_date))

        connection.commit()
        print("Название населенного пункта успешно обновлено.")

    except Exception as error:
        connection.rollback()
        print(f"Ошибка при обновлении названия населенного пункта: {error}")
    finally:
        cursor.close()

if __name__ == "__main__":
    conn = connect_db()
    if conn is not None:
        print("Выберите действие:")
        print("1. Обновить ОКТМО населенного пункта")
        print("2. Изменить название населенного пункта")

        action = input("Введите номер действия (1 или 2): ")

        if action == "1":
            old_oktmo = input("Введите старое ОКТМО: ")
            new_oktmo = input("Введите новое ОКТМО: ")
            update_oktmo(conn, old_oktmo, new_oktmo)
        elif action == "2":
            old_oktmo_np = input("Введите ОКТМО населенного пункта: ")
            new_np_name = input("Введите новое название населенного пункта: ")
            update_np_name(conn, old_oktmo_np, new_np_name)
        else:
            print("Неверный выбор действия.")

        conn.close()
