import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'

import './ProductoDetalle.css'

import {
  obtenerProductoPorId,
} from '../services/productosService'

import {
  crearPersonalizacion,
  subirFotoPersonalizacion,
} from '../services/personalizacionesService'


const API_BASE_URL = 'http://localhost:5000'


function ProductoDetalle() {

  const { id } = useParams()

  const [producto, setProducto] = useState(null)

  const [cargando, setCargando] = useState(true)

  const [error, setError] = useState(null)

  const [grabado, setGrabado] = useState('')

  const [mensaje, setMensaje] = useState('')

  const [foto, setFoto] = useState(null)

  const [vistaPreviaFoto, setVistaPreviaFoto] = useState(null)

  const [guardandoPersonalizacion, setGuardandoPersonalizacion] = useState(false)


  useEffect(() => {

    setCargando(true)

    setError(null)

    obtenerProductoPorId(id)
      .then((datos) => {

        console.log(
          'Producto recibido:',
          datos
        )

        setProducto(datos.data)

      })
      .catch((error) => {

        console.error(
          'Error obteniendo producto:',
          error
        )

        setError(
          'No fue posible cargar el producto.'
        )

      })
      .finally(() => {

        setCargando(false)

      })

  }, [id])


  useEffect(() => {

    return () => {

      if (vistaPreviaFoto) {

        URL.revokeObjectURL(
          vistaPreviaFoto
        )

      }

    }

  }, [vistaPreviaFoto])


  const manejarSeleccionFoto = (evento) => {

    const archivo = evento.target.files?.[0]

    if (!archivo) {
      return
    }


    const tiposPermitidos = [
      'image/jpeg',
      'image/png',
      'image/webp'
    ]


    if (!tiposPermitidos.includes(archivo.type)) {

      alert(
        'Formato de imagen no permitido. ' +
        'Use JPG, PNG o WEBP.'
      )

      evento.target.value = ''

      return
    }


    if (vistaPreviaFoto) {

      URL.revokeObjectURL(
        vistaPreviaFoto
      )

    }


    const nuevaVistaPrevia =
      URL.createObjectURL(archivo)


    setFoto(archivo)

    setVistaPreviaFoto(
      nuevaVistaPrevia
    )
  }


  const eliminarFoto = () => {

    if (vistaPreviaFoto) {

      URL.revokeObjectURL(
        vistaPreviaFoto
      )

    }

    setFoto(null)

    setVistaPreviaFoto(null)
  }


  const manejarAgregarAlCarrito = async () => {

    if (!producto) {
      return
    }


    setGuardandoPersonalizacion(true)

    setError(null)


    try {

      const datosPersonalizacion = {
        producto_id: producto.id,
        grabado: grabado || null,
        mensaje: mensaje || null
      }


      console.log(
        'Creando personalización:',
        datosPersonalizacion
      )


      const respuestaPersonalizacion =
        await crearPersonalizacion(
          datosPersonalizacion
        )


      const personalizacion =
        respuestaPersonalizacion.data


      console.log(
        'Personalización creada:',
        personalizacion
      )


      if (foto) {

        const respuestaFoto =
          await subirFotoPersonalizacion(
            personalizacion.id,
            foto
          )


        console.log(
          'Foto subida:',
          respuestaFoto
        )

      }


      alert(
        'Personalización creada correctamente.'
      )

    } catch (error) {

      console.error(
        'Error creando personalización:',
        error
      )

      setError(
        error.message ||
        'No fue posible guardar la personalización.'
      )

    } finally {

      setGuardandoPersonalizacion(false)

    }
  }


  if (cargando) {

    return (
      <section className="producto-detalle">

        <p>
          Cargando producto...
        </p>

      </section>
    )
  }


  if (error && !producto) {

    return (
      <section className="producto-detalle">

        <p>
          {error}
        </p>

      </section>
    )
  }


  if (!producto) {

    return (
      <section className="producto-detalle">

        <p>
          Producto no encontrado.
        </p>

      </section>
    )
  }


  const imagenProducto =
    producto.imagenes &&
    producto.imagenes.length > 0
      ? `${API_BASE_URL}${producto.imagenes[0].url_imagen}`
      : null


  return (
    <section className="producto-detalle">

      <div className="producto-detalle-contenido">

        <div className="producto-detalle-imagen">

          {imagenProducto ? (

            <img
              src={imagenProducto}
              alt={producto.nombre}
            />

          ) : (

            <span>
              Imagen del producto
            </span>

          )}

        </div>


        <div className="producto-detalle-info">

          <p className="producto-detalle-categoria">
            {producto.categoria}
          </p>


          <h1>
            {producto.nombre}
          </h1>


          <strong className="producto-detalle-precio">
            $
            {Number(
              producto.precio
            ).toLocaleString('es-CO')}
          </strong>


          <p className="producto-detalle-descripcion">

            {producto.descripcion ||
              'Producto personalizado de Burbuja.'}

          </p>


          <div className="producto-detalle-seccion">

            <h2>
              Personalización
            </h2>


            {producto.permite_grabado && (

              <div className="producto-detalle-opcion">

                <label htmlFor="grabado">
                  Texto para grabado
                </label>

                <input
                  id="grabado"
                  type="text"
                  value={grabado}
                  maxLength={
                    producto.max_caracteres_grabado
                  }
                  placeholder="Escribe tu mensaje"
                  onChange={(evento) => {
                    setGrabado(
                      evento.target.value
                    )
                  }}
                />

                <small>
                  Máximo{' '}
                  {producto.max_caracteres_grabado}{' '}
                  caracteres
                </small>

              </div>

            )}


            {producto.permite_tarjeta && (

              <div className="producto-detalle-opcion">

                <label htmlFor="mensaje">
                  Mensaje para la tarjeta
                </label>

                <textarea
                  id="mensaje"
                  value={mensaje}
                  maxLength={
                    producto.max_caracteres_tarjeta
                  }
                  placeholder="Escribe tu mensaje"
                  onChange={(evento) => {
                    setMensaje(
                      evento.target.value
                    )
                  }}
                />

                <small>
                  Máximo{' '}
                  {producto.max_caracteres_tarjeta}{' '}
                  caracteres
                </small>

              </div>

            )}


            {producto.max_fotos > 0 && (

              <div className="producto-detalle-opcion">

                <label htmlFor="foto">
                  Fotografía para tu producto
                </label>


                {!foto && (

                  <input
                    id="foto"
                    type="file"
                    accept="image/jpeg,image/png,image/webp"
                    onChange={manejarSeleccionFoto}
                  />

                )}


                {foto && (

                  <div>

                    {vistaPreviaFoto && (

                      <img
                        src={vistaPreviaFoto}
                        alt="Vista previa de la personalización"
                        style={{
                          width: '100%',
                          maxHeight: '300px',
                          objectFit: 'contain',
                          display: 'block',
                          marginBottom: '12px'
                        }}
                      />

                    )}


                    <p>
                      {foto.name}
                    </p>


                    <button
                      type="button"
                      onClick={eliminarFoto}
                    >
                      Cambiar fotografía
                    </button>

                  </div>

                )}

                <small>
                  Puedes subir hasta{' '}
                  {producto.max_fotos}{' '}
                  fotografía
                  {producto.max_fotos !== 1
                    ? 's'
                    : ''}
                  . JPG, PNG o WEBP.
                </small>

              </div>

            )}

          </div>


          {error && (

            <p>
              {error}
            </p>

          )}


          <div className="producto-detalle-stock">

            {producto.stock > 0
              ? `Disponible: ${producto.stock}`
              : 'Producto agotado'}

          </div>


          <button
            type="button"
            className="producto-detalle-boton"
            disabled={
              !producto.disponible ||
              producto.stock <= 0 ||
              guardandoPersonalizacion
            }
            onClick={
              manejarAgregarAlCarrito
            }
          >
            {guardandoPersonalizacion
              ? 'Guardando...'
              : 'Agregar al carrito'}
          </button>

        </div>

      </div>

    </section>
  )
}


export default ProductoDetalle