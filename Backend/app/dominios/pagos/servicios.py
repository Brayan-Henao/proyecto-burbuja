import secrets

import hashlib

from flask import current_app

from app.dominios.pagos.modelos import Pago

from app.dominios.pagos.repositorios import (
    PagoRepositorio
)

from app.dominios.ordenes.modelos import Orden


class PagoNoEncontradoError(Exception):

    pass


class PagoServicio:

    def crear_pago(
        self,
        usuario_id,
        orden_id
    ):

        orden = Orden.query.get(
            orden_id
        )

        if not orden:

            raise ValueError(
                "La orden no existe."
            )

        if orden.usuario_id != usuario_id:

            raise ValueError(
                "La orden no pertenece al usuario."
            )

        if orden.estado != "pendiente":

            raise ValueError(
                "Solo se pueden pagar órdenes pendientes."
            )

        if orden.subtotal <= 0:

            raise ValueError(
                "La orden debe tener un subtotal mayor que cero."
            )

        pagos_existentes = (
            PagoRepositorio.listar_por_orden(
                orden.id
            )
        )

        for pago in pagos_existentes:

            if pago.estado == "pendiente":

                raise ValueError(
                    "La orden ya tiene un pago pendiente."
                )

        referencia = self._generar_referencia(
            orden.id
        )

        pago = Pago(
            orden_id=orden.id,
            referencia=referencia,
            monto=orden.subtotal,
            estado="pendiente"
        )

        PagoRepositorio.crear(
            pago
        )

        return pago


    def _generar_referencia(
        self,
        orden_id
    ):

        while True:

            codigo = secrets.token_hex(
                4
            ).upper()

            referencia = (
                f"BURBUJA-ORDEN-{orden_id}-{codigo}"
            )

            pago_existente = (
                PagoRepositorio.obtener_por_referencia(
                    referencia
                )
            )

            if not pago_existente:

                return referencia


    def generar_firma_integridad(
        self,
        pago
    ):

        secreto = current_app.config[
            "WOMPI_INTEGRITY_SECRET"
        ]

        if not secreto:

            raise ValueError(
                "La clave de integridad de Wompi "
                "no está configurada."
            )

        monto_centavos = int(
            pago.monto * 100
        )

        cadena = (
            f"{pago.referencia}"
            f"{monto_centavos}"
            f"COP"
            f"{secreto}"
        )

        firma = hashlib.sha256(
            cadena.encode("utf-8")
        ).hexdigest()

        return firma


    def obtener_llave_publica(
        self
    ):

        llave_publica = current_app.config[
            "WOMPI_PUBLIC_KEY"
        ]

        if not llave_publica:

            raise ValueError(
                "La llave pública de Wompi "
                "no está configurada."
            )

        return llave_publica


    def obtener_pago(
        self,
        pago_id
    ):

        pago = PagoRepositorio.obtener_por_id(
            pago_id
        )

        if not pago:

            raise PagoNoEncontradoError(
                "Pago no encontrado."
            )

        return pago


    def listar_pagos_orden(
        self,
        usuario_id,
        orden_id
    ):

        orden = Orden.query.get(
            orden_id
        )

        if not orden:

            raise ValueError(
                "La orden no existe."
            )

        if orden.usuario_id != usuario_id:

            raise ValueError(
                "La orden no pertenece al usuario."
            )

        return PagoRepositorio.listar_por_orden(
            orden.id
        )