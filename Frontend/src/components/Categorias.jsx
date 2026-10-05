import './Categorias.css'

const categorias = [
  'Relicarios',
  'Burbujas',
  'Fotograbados',
  'Vasos y mugs',
  'Lámparas',
  'Lupa / Burbuja proyectora',
  'Imanes de nevera',
]

function Categorias() {
  return (
    <section className="categorias">

      <div className="categorias-header">
        <p>DESCUBRE BURBUJA</p>

        <h2>
          Encuentra el detalle perfecto
        </h2>

        <span>
          Productos creados para convertir
          momentos especiales en recuerdos únicos.
        </span>
      </div>

      <div className="categorias-grid">
        {categorias.map((categoria) => (
          <article
            className="categoria-card"
            key={categoria}
          >
            <div className="categoria-image">
              <span>Burbuja</span>
            </div>

            <h3>{categoria}</h3>

            <a href="/tienda">
              Ver productos
            </a>
          </article>
        ))}
      </div>

    </section>
  )
}

export default Categorias