import './PersonalizacionCTA.css'

function PersonalizacionCTA() {
  return (
    <section className="personalizacion-cta">

      <div className="personalizacion-content">

        <p>HAZLO TUYO</p>

        <h2>
          Crea un recuerdo
          <br />
          completamente único.
        </h2>

        <p className="personalizacion-texto">
          Elige tu producto, agrega tus fotografías,
          grabados o mensajes y crea un detalle
          pensado especialmente para esa persona.
        </p>

        <a
          href="/tienda"
          className="personalizacion-button"
        >
          Comenzar a personalizar
        </a>

      </div>

    </section>
  )
}

export default PersonalizacionCTA