from mysql import connector

# ---------------------------------------------------------
# DATABASE CONNECTION
# ---------------------------------------------------------
try:
    conn1 = connector.connect(
        host="localhost",
        user="root",
        password="root",      # change to your MySQL password
        database="notesdb"
    )
    print("Connection successfull...!")
except connector.Error as e:
    print("Could not connect to database:", e)
    exit()

cursor = conn1.cursor()

# Create the table automatically if it does not exist yet
cursor.execute('''
create table if not exists notes(
    note_id int auto_increment primary key,
    title varchar(100) not null,
    description text not null,
    created_date timestamp default current_timestamp,
    updated_date timestamp default current_timestamp on update current_timestamp
)
''')
conn1.commit()


# ---------------------------------------------------------
# FUNCTIONS (one function per operation for reusability)
# ---------------------------------------------------------

# CREATE : add a new note
def add_note():
    try:
        title = input("Enter note title: ").strip()
        description = input("Enter note description: ").strip()

        # Validation: empty values are not allowed
        if title == "" or description == "":
            print("Title and description cannot be empty!")
            return

        cursor.execute(
            "INSERT INTO notes (title, description) VALUES (%s, %s)",
            (title, description)
        )
        conn1.commit()
        print("Note added successfully...!")
    except connector.Error as e:
        conn1.rollback()
        print("Database error:", e)
    except Exception:
        print("Something went wrong...!")


# READ : view all notes
def view_notes():
    try:
        cursor.execute("SELECT note_id, title, description, created_date, updated_date FROM notes")
        res = cursor.fetchall()

        if len(res) == 0:
            print("No notes found.")
            return

        print("\n" + "=" * 60)
        print("                      YOUR NOTES")
        print("=" * 60)
        for row in res:
            print("Note ID     :", row[0])
            print("Title       :", row[1])
            print("Description :", row[2])
            print("Created Date:", row[3])
            print("Updated Date:", row[4])
            print("-" * 60)
    except connector.Error as e:
        print("Database error:", e)
    except Exception:
        print("Something went wrong...!")


# Helper : check whether a Note ID exists
def note_exists(note_id):
    cursor.execute("SELECT note_id FROM notes WHERE note_id = %s", (note_id,))
    return cursor.fetchone() is not None


# UPDATE : modify an existing note
def update_note():
    try:
        note_id = int(input("Enter the Note ID to update: "))

        if not note_exists(note_id):
            print("No note found with Note ID", note_id)
            return

        title = input("Enter new title: ").strip()
        description = input("Enter new description: ").strip()

        if title == "" or description == "":
            print("Title and description cannot be empty!")
            return

        cursor.execute(
            "UPDATE notes SET title = %s, description = %s WHERE note_id = %s",
            (title, description, note_id)
        )
        conn1.commit()
        print("Note updated successfully...!")
    except ValueError:
        print("Invalid input! Note ID must be a number.")
    except connector.Error as e:
        conn1.rollback()
        print("Database error:", e)
    except Exception:
        print("Something went wrong...!")


# DELETE : remove a note
def delete_note():
    try:
        note_id = int(input("Enter the Note ID to delete: "))

        if not note_exists(note_id):
            print("No note found with Note ID", note_id)
            return

        # Ask for confirmation before deleting
        confirm = input("Are you sure you want to delete this note? (y/n): ").lower()
        if confirm != "y":
            print("Delete cancelled.")
            return

        cursor.execute("DELETE FROM notes WHERE note_id = %s", (note_id,))
        conn1.commit()
        print("Note deleted successfully...!")
    except ValueError:
        print("Invalid input! Note ID must be a number.")
    except connector.Error as e:
        conn1.rollback()
        print("Database error:", e)
    except Exception:
        print("Something went wrong...!")


# ---------------------------------------------------------
# MAIN MENU LOOP  (one option at a time)
# ---------------------------------------------------------
while True:
    try:
        inp = int(input(
            "\n===== NOTES SAVER =====\n"
            "0 --> Exit\n"
            "1 --> View Notes\n"
            "2 --> Add Note\n"
            "3 --> Update a Note\n"
            "4 --> Delete a Note\n"
            "Choose an option: "
        ))
    except ValueError:
        # Runs when the user types text instead of a number
        print("Invalid input! Please enter a number between 0 and 4.")
        continue

    if inp == 0:
        print("Thank you for using Notes Saver. Goodbye!")
        break
    elif inp == 1:
        view_notes()
    elif inp == 2:
        add_note()
    elif inp == 3:
        update_note()
    elif inp == 4:
        delete_note()
    else:
        print("Wrong Option")

# ---------------------------------------------------------
# CLOSE DATABASE CONNECTION
# ---------------------------------------------------------
cursor.close()
conn1.close()
print("Database connection closed.")
