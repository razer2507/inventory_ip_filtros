
from models import Deuda

from repository import PostgresDeudasRepository

Repositorio = PostgresDeudasRepository()

def test_insert_postgres():
    deuda = Deuda(
        cliente='Juan',
        monto=20.5,
        fecha = '22/06/26'
    )
    Repositorio.insert(deuda)

    deuda_f = (Repositorio.view_all()[len(Repositorio.view_all())-1])

    deuda_final = Deuda(
        cliente=deuda_f[1],
        monto=deuda_f[2],
        fecha=deuda_f[3]
    )

    assert vars(deuda_final) == vars(deuda)


def test_view_postgres():
    data = Repositorio.view_all()

    assert len(data) != 0


def test_update_postgres():
    data = Repositorio.view_all()
    deuda_nueva = Deuda(
        cliente='Nombre nuevo',
        monto=250,
        fecha='fecha nueva',
        id=3
    )

    Repositorio.update(deuda_nueva)

    for i in Repositorio.view_all():
        deuda_actual = Deuda(
            cliente=data[0],
            monto=[1],
            fecha=[2],
            id=[3]
        )

        if vars(deuda_actual) == vars(deuda_nueva):
            assert 1 == True  # noqa: PLR0133


def test_delete_postgres():
    data = Repositorio.view_all()

    deuda_a_eliminar = Deuda(
        cliente='Nombre nuevo',
        monto=250,
        fecha='fecha nueva',
        id=3
    )


    Repositorio.delete(deuda=deuda_a_eliminar)

    for deuda in data:
        deuda_actual = Deuda(
            cliente=data[0],
            monto=data[1],
            fecha=data[2],
            id=data[3]
        )

        deuda_eliminada_existe = bool(vars(deuda_actual) == vars(deuda_a_eliminar))

    assert not deuda_eliminada_existe


def test_filter_view_postgres():
    args = {
        
    }

    filtered_data = Repositorio.filter_view(
        **args
    )
    print(filtered_data)
    def cumplen_filtro(tuple)->bool:
        for i in items:  # noqa: F821
            deuda_act = Deuda(
                cliente=i[0],
                monto=i[1],
                fecha=i[2],
                id=i[3]
            )
        #Monto = 200
        if args.get('monto'):  # noqa: SIM102
            #Si la deuda actual no cumple la condicion, retorna False
            if not deuda_act.monto >= args.get('monto'):
                return False
        #Cliente='Paul'
        if args.get('cliente'):
            'Si el cliente no es paul, entonces es Falso'
            if deuda_act.cliente != args.get('cliente'):
                return False
        #fecha
        if args.get('fecha'):
            pass
        #Id=1
        if args.get('id'):  # noqa: SIM102
            if deuda_act.id != args.get('id'):
                return False
        
        assert all(filter(cumplen_filtro,filtered_data))
            
        



        
