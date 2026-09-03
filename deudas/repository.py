import os
from abc import ABC, abstractmethod
from pathlib import Path

import psycopg2
from dotenv import load_dotenv
from models import Deuda

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")


class DeudasRepository(ABC):
    @abstractmethod
    def insert(self, deuda: Deuda) -> None:
        pass

    def view_all(self) -> list:
        pass

    def update(self, deuda: Deuda) -> None:
        pass

    def delete(self, deuda: Deuda) -> None:
        pass

    def filter_view(self, **kwargs) -> list:
        pass


class PostgresDeudasRepository(DeudasRepository):
    def __init__(self):
        self.conn = psycopg2.connect(
            host=os.getenv("host"),
            port=os.getenv("port"),
            dbname=os.getenv("dbname"),
            user=os.getenv("user"),
            password=os.getenv("password"),
            sslmode=os.getenv("sslmode"),
        )

        self.cursor = self.conn.cursor()

    def insert(self, deuda: Deuda) -> None:
        query = "INSERT INTO deudas(cliente,monto_deudor,fecha_venc) VALUES(%s,%s,%s)"
        self.cursor.execute(query, (deuda.cliente, deuda.monto, deuda.fecha))
        self.conn.commit()
        

    def view_all(self) -> list:
        query = "SELECT *FROM deudas"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def update(self, deuda: Deuda) -> None:
        query = "UPDATE deudas SET cliente = %s,monto_deudor = %s,fecha_venc = %s WHERE id = %s;"
        self.cursor.execute(query, (deuda.cliente, deuda.monto, deuda.fecha, deuda.id))
        self.conn.commit()

    def delete(self, deuda: Deuda) -> None:
        query = "DELETE FROM deudas WHERE id=%s"
        self.cursor.execute(query, (deuda.id,))
        self.conn.commit()
    
    def filter_view(self, **kwargs):
        # Crea una consulta base, luego dependiendo de los parametros pasados, nuevas condiciones se sumaran.
        base_query = "SELECT *FROM deudas WHERE 1=1"

        if kwargs.get("monto"):
            base_query += " AND monto_deudor >= %s "
        if kwargs.get("id"):
            base_query += " AND id =%s "
        if kwargs.get("cliente"):
            base_query += " AND CLIENTE =%s "
        if kwargs.get("start_date") and kwargs.get("end_date"):
            base_query += " AND fecha_venc BETWENN %s AND %s"
        if kwargs.get("start_date") and not kwargs.get("end_date"):
            base_query += " AND fecha_venc =%s"
        #Si no hay argumentos pasados, haz una excepcion
        if not kwargs:
            raise ValueError

        # Ejecuta la consulta, y transforma los parametros a una tupla
        self.cursor.execute(base_query, tuple(kwargs.values()))
        # Retorna los datos que cumplen las condiciones pasadas por el usuario
        return self.cursor.fetchall()

