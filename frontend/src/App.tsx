

import { BrowserRouter, Link, Route, Routes, useLocation } from 'react-router-dom';
import IncidenciasPage from './pages/IncidenciasPage';
import LineaDetallePage from './pages/LineaDetallePage.tsx';
import LineasPage from './pages/LineasPage';

function NavLinks() {
  const location = useLocation();

  const getLinkClass = (path: string) => {
    const baseClass = "px-4 py-2 text-sm font-medium transition-colors border-b-2 ";
    return location.pathname === path
      ? baseClass + "border-blue-500 text-blue-400 bg-blue-950/30"
      : baseClass + "border-transparent text-neutral-400 hover:text-neutral-200 hover:border-neutral-600 hover:bg-neutral-800/50";
  };

  return (
    <nav className="flex items-center gap-2 mt-4 overflow-x-auto">
      <Link to="/" className={getLinkClass("/")}>
        Líneas y Autobuses
      </Link>
      <Link to="/incidencias" className={getLinkClass("/incidencias")}>
        Incidencias
      </Link>
    </nav>
  );
}

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-neutral-950 text-neutral-200 font-sans selection:bg-blue-900 selection:text-white pb-12">
        <header className="bg-neutral-900 border-b border-neutral-800 sticky top-0 z-10 pt-4 px-6 md:px-12">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 bg-blue-600 flex items-center justify-center font-bold text-white">N</div>
              <span className="text-xl font-bold tracking-tight text-white">NodoBus</span>
            </div>
            <div className="text-xs font-mono text-neutral-500">
              Microservicios v1.0
            </div>
          </div>
          
          <NavLinks />
        </header>

        <main className="max-w-7xl mx-auto px-6 md:px-12 py-8 mt-4">
          <Routes>
            <Route path="/" element={<LineasPage />} />
            <Route path="/incidencias" element={<IncidenciasPage />} />
            <Route path="/lineas/:id" element={<LineaDetallePage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
