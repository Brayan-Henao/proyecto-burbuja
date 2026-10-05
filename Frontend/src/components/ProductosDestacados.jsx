import { Link } from 'react-router-dom'

import './ProductosDestacados.css'


const API_BASE_URL = 'http://localhost:5000'


function ProductosDestacados({
  productos,
  cargando,
  error
}) {

  if (cargando) {

    return (
      <section className="productos-destacados">

        <div className="productos-header">

          <div>
            <p>SELECCIÓN BURBUJA</p>
            <h2>Productos destacados</h2>
          </div>

        </div>

        <p>Cargando productos...</p>

      </section>
    )
  }


  if (error) {

    return (
      <section className="productos-destacados">

        <div className="productos-header">

          <div>
            <p>SELECCIÓN BURBUJA</p>
            <h2>Productos destacados</h2>
          </div>

        </div>

        <p>{error}</p>

      </section>
    )
  }


  return (
    <section className="productos-destacados">

      <div className="productos-header">

        <div>
          <p>SELECCIÓN BURBUJA</p>
          <h2>Productos destacados</h2>
        </div>

        <Link to="/tienda">
          Ver todos los productos
        </Link>

      </div>


      <div className="productos-grid">

        {productos.map((producto) => {

          const imagenProducto =
            producto.imagenes &&
            producto.imagenes.length > 0
              ? `${API_BASE_URL}${producto.imagenes[0].url_imagen}`
              : null


          return (

            <Link
              to={`/producto/${producto.id}`}
              className="producto-card"
              key={producto.id}
            >

              <div className="producto-image">

                {imagenProducto ? (

                  <img
                    src={imagenProducto}
                    alt={producto.nombre}
                  />

                ) : (

                  <span>
                    {producto.categoria}
                  </span>

                )}

              </div>


              <div className="producto-info">

                <p>
                  {producto.categoria}
                </p>

                <h3>
                  {producto.nombre}
                </h3>

                <strong>
                  $
                  {Number(
                    producto.precio
                  ).toLocaleString('es-CO')}
                </strong>

              </div>

            </Link>

          )

        })}

      </div>

    </section>
  )
}


export default ProductosDestacados