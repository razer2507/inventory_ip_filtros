from dataclasses import dataclass


@dataclass
#El modelo de la deuda(el esqueleto)
class Deuda:
    cliente:str
    monto:float
    fecha:str
    id: int |None= None
    
    def __str__(self)-> str:
        return f"\nCLIENTE:{self.cliente}\nMONTO:{self.monto}\nFECHA:{self.fecha}\nID:{self.id}\n"
    
deuda_loca = Deuda(
    cliente='Paul',
    monto=99999999999999999,
    fecha='manana',
    id=902231
)

print(deuda_loca)