from app.extensions import db

from app.dominios.pagos.modelos import Pago


class PagoRepositorio:

    @staticmethod
    def obtener_por_id(
        pago_id
    ):

        return Pago.query.get(
            pago_id
        )


    @staticmethod
    def obtener_por_referencia(
        referencia
    ):

        return Pago.query.filter_by(
            referencia=referencia
        ).first()


    @staticmethod
    def obtener_por_id_transaccion(
        id_transaccion
    ):

        return Pago.query.filter_by(
            id_transaccion=id_transaccion
        ).first()


    @staticmethod
    def listar_por_orden(
        orden_id
    ):

        return Pago.query.filter_by(
            orden_id=orden_id
        ).all()


    @staticmethod
    def crear(
        pago
    ):

        db.session.add(
            pago
        )

        db.session.commit()

        return pago


    @staticmethod
    def actualizar():

        db.session.commit()


    @staticmethod
    def eliminar(
        pago
    ):

        db.session.delete(
            pago
        )

        db.session.commit()