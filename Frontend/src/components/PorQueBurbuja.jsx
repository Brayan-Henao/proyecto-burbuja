import './PorQueBurbuja.css'

const razones = [
  {
    numero: '01',
    titulo: 'Personalización',
    texto: 'Creamos cada detalle pensando en la historia y la persona que lo recibirá.',
  },
  {
    numero: '02',
    titulo: 'Recuerdos únicos',
    texto: 'Convertimos fotografías y momentos especiales en regalos para conservar.',
  },
  {
    numero: '03',
    titulo: 'Cuidamos cada detalle',
    texto: 'Desde la personalización hasta la presentación, cada pedido es preparado con dedicación.',
  },
]

function PorQueBurbuja() {
  return (
    <section className="por-que-burbuja">

      <div className="por-que-header">
        <p>LA ESENCIA DE BURBUJA</p>

        <h2>
          Un regalo puede guardar
          <br />
          mucho más que un recuerdo.
        </h2>
      </div>

      <div className="razones-grid">
        {razones.map((razon) => (
          <article
            className="razon-card"
            key={razon.numero}
          >
            <span>{razon.numero}</span>

            <h3>{razon.titulo}</h3>

            <p>{razon.texto}</p>
          </article>
        ))}
      </div>

    </section>
  )
}

export default PorQueBurbuja