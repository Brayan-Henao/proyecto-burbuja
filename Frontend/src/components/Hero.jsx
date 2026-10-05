import './Hero.css'

function Hero() {
  return (
    <section className="hero">

      <video
        className="hero-video"
        autoPlay
        muted
        loop
        playsInline
      >
        <source
          src="/videos/video1.mp4"
          type="video/mp4"
        />
      </video>

      <div className="hero-overlay"></div>

      <div className="hero-content">

        <p className="hero-subtitle">
          REGALOS PERSONALIZADOS
        </p>

        <h1>
          Convierte tus recuerdos
          <br />
          en algo único
        </h1>

        <p className="hero-description">
          Creamos detalles personalizados para hacer
          inolvidables tus momentos especiales.
        </p>

        <a
          href="/tienda"
          className="hero-button"
        >
          Ver tienda
        </a>

      </div>

    </section>
  )
}

export default Hero