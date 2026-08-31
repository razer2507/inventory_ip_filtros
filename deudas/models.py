from dataclasses import dataclass


@dataclass
class Deuda:
    cliente:str
    monto:float
    fecha:str
    id: int |None= None
    
    def __str__(self)-> str:
        return f"\nCLIENTE:{self.cliente}\nMONTO:{self.monto}\nFECHA:{self.fecha}\nID:{self.id}\n"