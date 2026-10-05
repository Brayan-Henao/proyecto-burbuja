const API_URL = 'http://localhost:5000/api/v1'


export async function crearPersonalizacion(datos) {

  const respuesta = await fetch(
    `${API_URL}/personalizaciones`,
    {
      method: 'POST',

      headers: {
        'Content-Type': 'application/json'
      },

      body: JSON.stringify(datos)
    }
  )


  const datosRespuesta =
    await respuesta.json()


  if (!respuesta.ok) {

    throw new Error(
      datosRespuesta?.error?.message ||
      'No se pudo crear la personalización.'
    )

  }


  return datosRespuesta
}


export async function subirFotoPersonalizacion(
  personalizacionId,
  archivo
) {

  const formulario = new FormData()

  formulario.append(
    'imagen',
    archivo
  )


  const respuesta = await fetch(
    `${API_URL}/personalizaciones/${personalizacionId}/fotos`,
    {
      method: 'POST',
      body: formulario
    }
  )


  const datosRespuesta =
    await respuesta.json()


  if (!respuesta.ok) {

    throw new Error(
      datosRespuesta?.error?.message ||
      'No se pudo subir la fotografía.'
    )

  }


  return datosRespuesta
}


export async function obtenerPersonalizacion(
  personalizacionId
) {

  const respuesta = await fetch(
    `${API_URL}/personalizaciones/${personalizacionId}`
  )


  const datosRespuesta =
    await respuesta.json()


  if (!respuesta.ok) {

    throw new Error(
      datosRespuesta?.error?.message ||
      'No se pudo obtener la personalización.'
    )

  }


  return datosRespuesta
}


export async function eliminarFotoPersonalizacion(
  fotoId
) {

  const respuesta = await fetch(
    `${API_URL}/personalizaciones/fotos/${fotoId}`,
    {
      method: 'DELETE'
    }
  )


  const datosRespuesta =
    await respuesta.json()


  if (!respuesta.ok) {

    throw new Error(
      datosRespuesta?.error?.message ||
      'No se pudo eliminar la fotografía.'
    )

  }


  return datosRespuesta
}