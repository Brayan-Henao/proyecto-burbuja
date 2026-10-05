import { useEffect, useState } from 'react'

import {
  BrowserRouter,
  Routes,
  Route,
} from 'react-router-dom'

import Header from './components/Header'
import Hero from './components/Hero'
import Categorias from './components/Categorias'
import ProductosDestacados from './components/ProductosDestacados'
import ProductoDetalle from './components/ProductoDetalle'
import PorQueBurbuja from './components/PorQueBurbuja'
import PersonalizacionCTA from './components/PersonalizacionCTA'
import Footer from './components/Footer'

import { obtenerProductos } from './services/productosService'


function Inicio() {

  const [productos, setProductos] = useState([])

  const [cargandoProductos, setCargandoProductos] =
    useState(true)

  const [errorProductos, setErrorProductos] =
    useState(null)


  useEffect(() => {

    obtenerProductos()
      .then((datos) => {

        console.log(
          'Productos recibidos:',
          datos
        )

        setProductos(datos.data)

      })
      .catch((error) => {

        console.error(
          'Error obteniendo productos:',
          error
        )

        setErrorProductos(
          'No fue posible cargar los productos.'
        )

      })
      .finally(() => {

        setCargandoProductos(false)

      })

  }, [])


  return (
    <>
      <Header />

      <main>

        <Hero />

        <Categorias />

        <ProductosDestacados
          productos={productos}
          cargando={cargandoProductos}
          error={errorProductos}
        />

        <PorQueBurbuja />

        <PersonalizacionCTA />

      </main>

      <Footer />
    </>
  )
}


function Tienda() {

  const [productos, setProductos] = useState([])

  const [cargandoProductos, setCargandoProductos] =
    useState(true)

  const [errorProductos, setErrorProductos] =
    useState(null)


  useEffect(() => {

    obtenerProductos()
      .then((datos) => {

        setProductos(datos.data)

      })
      .catch((error) => {

        console.error(
          'Error obteniendo productos:',
          error
        )

        setErrorProductos(
          'No fue posible cargar los productos.'
        )

      })
      .finally(() => {

        setCargandoProductos(false)

      })

  }, [])


  return (
    <>
      <Header />

      <main>

        <ProductosDestacados
          productos={productos}
          cargando={cargandoProductos}
          error={errorProductos}
        />

      </main>

      <Footer />
    </>
  )
}


function App() {

  return (
    <BrowserRouter>

      <Routes>

        <Route
          path="/"
          element={<Inicio />}
        />

        <Route
          path="/tienda"
          element={<Tienda />}
        />

        <Route
          path="/producto/:id"
          element={<ProductoDetalle />}
        />

      </Routes>

    </BrowserRouter>
  )
}


export default App