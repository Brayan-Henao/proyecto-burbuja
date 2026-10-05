import './Header.css'

function Header() {
  return (
    <header className="site-header">

      <div className="header-main">

        <span className="header-language">
          ES
        </span>

        <a
          href="/"
          className="header-logo"
        >
          BURBUJA
        </a>

        <div className="header-actions">

          <button
            type="button"
            aria-label="Buscar"
          >
            🔍
          </button>

          <button
            type="button"
            aria-label="Mi cuenta"
          >
            👤
          </button>

          <button
            type="button"
            aria-label="Carrito"
          >
            🛍
          </button>

        </div>

      </div>

      <nav className="main-navigation">

        <a href="/">
          Inicio
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

        <a href="/contacto">
          Contacto
        </a>

      </nav>

    </header>
  )
}

export default Header