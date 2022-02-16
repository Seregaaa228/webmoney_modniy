from models.bill import BillModel
import sqlite3
import uuid




class BillCRUD:
    def create(self, conn: sqlite3.Connection, user_id) -> None:
        cur = conn.cursor()
        id = uuid.uuid4()
        try:
            cur.execute(
                "INSERT INTO Bill VALUES(?, ?, ?,?)",
                (str(id), user_id, 0, 1),
            )
        finally:
            cur.close()

    def get(self, conn: sqlite3.Connection, id: str) -> BillModel or None:
        cur = conn.cursor()

        try:
            cur.execute(
                "SELECT Bill.id,Bill.owner,Bill.balance,Bill.status FROM Bill WHERE Bill.id=?",
                (id,),
            )
            row = cur.fetchone()

            if row is None:
                return None

            id, owner, balance, status = row

            return BillModel(id=id, balance=balance, owner=owner, status=status)
        finally:
            cur.close()

    def decrease_money(self, conn: sqlite3.Connection, money: float, sender_bill_id: str,
                       sender_current_balance: float):
        cur = conn.cursor()
        try:
            owner = self.get(conn, sender_bill_id).owner
            cur.execute("DELETE FROM Bill WHERE Bill.id=?", (sender_bill_id,))
            cur.execute("INSERT INTO Bill VALUES (?,?,?,?)",
                        (sender_bill_id, owner, sender_current_balance - money, 1), )

        finally:
            cur.close()

    def add_money(self, conn: sqlite3.Connection, money: float, receiver_current_balance: float, receiver_bill_id: str):
        cur = conn.cursor()
        try:
            owner = self.get(conn, receiver_bill_id).owner
            cur.execute("DELETE FROM bill WHERE Bill.id=?", (receiver_bill_id,))
            cur.execute("INSERT INTO Bill VALUES (?,?,?,?)",
                        (receiver_bill_id, owner, receiver_current_balance + money, 1), )

        finally:
            cur.close()

    def transfer_money(self, conn: sqlite3.Connection, sender_bill_id: str, receiver_bill_id: str, money: int):
        cur = conn.cursor()
        try:
            sender_current_balance = self.get(conn, sender_bill_id).balance
            receiver_current_balance = self.get(conn, receiver_bill_id).balance
            print(sender_current_balance, receiver_current_balance)
            if money < sender_current_balance:
                self.decrease_money(conn, money, sender_bill_id, sender_current_balance)
                self.add_money(conn, money, receiver_current_balance, receiver_bill_id)
                self.fill_transaction(conn, sender_bill_id, receiver_bill_id, money)
            else:
                return False
            return None

        finally:
            cur.close()

    def get_unactive(self, conn: sqlite3.Connection, bill_id: str):
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM Bill WHERE id=?", (bill_id,))

        finally:
            cur.close()

    def fill_transaction(self, conn: sqlite3.Connection, sender, receiver, money):
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO Transact VALUES(?,?,?,?)", (None, sender, receiver, money))
        finally:
            cur.close()

    def delete_bills(self, conn: sqlite3.Connection, owner_id: str):
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM Bill WHERE owner=?", (owner_id,))

        finally:
            cur.close()

    def get_bills(self, conn: sqlite3.Connection, owner_id: str):
        cur = conn.cursor()
        try:
            cur.execute("SELECT Bill.id,Bill.balance,Bill.status FROM Bill WHERE owner=?", (owner_id,))
            row = cur.fetchall()
            return row

        finally:
            cur.close()