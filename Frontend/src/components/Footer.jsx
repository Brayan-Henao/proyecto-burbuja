import './Footer.css'

function Footer() {
  return (
    <footer className="site-footer">

      <div className="footer-main">

        <div className="footer-brand">
          <a href="/" className="footer-logo">
            BURBUJA
          </a>

          <p>
            Regalos personalizados para
            convertir momentos especiales
            en recuerdos únicos.
          </p>
        </div>

        <div className="footer-column">
          <h3>Ayuda</h3>

          <a href="/contacto">
            Contacto
          </a>

          <a href="/preguntas">
            Preguntas frecuentes
          </a>

          <a href="/envios">
            Envíos
          </a>
        </div>

        <div className="footer-column">
          <h3>Burbuja</h3>

          <a href="/nuestra-historia">
            Nuestra historia
          </a>

          <a href="/tienda">
            Tienda
          </a>

          <a href="/para-ella">
            Para Ella
          </a>

          <a href="/para-el">
            Para Él
          </a>
        </div>

        <div className="footer-column">
          <h3>Síguenos</h3>

          <a href="#">
            Instagram
          </a>

          <a href="#">
            Facebook
          </a>

          <a href="#">
            TikTok
          </a>
        </div>

      </div>

      <div className="footer-bottom">
        <span>
          © 2026 Burbuja. Todos los derechos reservados.
        </span>

        <span>
          Regalos personalizados
        </span>
      </div>

    </footer>
  )
}

export default Footer