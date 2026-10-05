const API_URL = 'http://localhost:5000/api/v1'


export async function obtenerProductos() {

  const respuesta = await fetch(
    `${API_URL}/productos`
  )


  if (!respuesta.ok) {

    throw new Error(
      'No se pudieron obtener los productos.'
    )

  }


  const datos =
    await respuesta.json()


  return datos
}


export async function obtenerProductoPorId(
  productoId
) {

  const respuesta = await fetch(
    `${API_URL}/productos/${productoId}`
  )


  if (!respuesta.ok) {

    throw new Error(
      'No se pudo obtener el producto.'
    )

  }


  const datos =
    await respuesta.json()


  return datos
}