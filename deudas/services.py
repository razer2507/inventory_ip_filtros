from models import Deuda
from validation import DeudaValidator
from repository import DeudasRepository
from datetime import date, datetime  # noqa: F401


class DeudasServices:
    def __init__(self, repository: DeudasRepository):
        self.repository = repository

    def insert(self, deuda: Deuda) -> None:
        if self._validar_deuda(deuda):
            self.repository.insert(deuda)
        else:
            raise ValueError

    def view_all(self) -> list[tuple]:
        pass

    def update(self, deuda: Deuda) -> None:
        pass

    def delete(self, deuda: Deuda) -> None:
        pass

    def filter_view(self, **kwargs):
        pass

    def _validar_deuda(self, deuda: Deuda):
        return bool(
            all(
                [
                    self._validar_cliente(deuda.cliente),
                    self._validar_monto(deuda.monto),
                    self._validar_fecha(deuda.fecha),
                ]
            )
        )

    def _validar_cliente(self, cliente: str) -> bool:
        if not len(cliente):
            return False
        if not isinstance(cliente, str):  # noqa: SIM103
            return False
        return True

    def _validar_monto(self, monto: float) -> bool:
        if monto <= 0:
            return False
        if not isinstance(monto, float):  # noqa: SIM103
            return False
        return True

    def _validar_fecha(self, fecha: date) -> bool:
        if not isinstance(fecha, date):  # noqa: SIM103
            return False
        return True
