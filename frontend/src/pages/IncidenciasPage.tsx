import { useEffect, useState } from 'react';
import { incidenciaService } from '../api/incidencias';
import { lineaService } from '../api/linea';
import { paradaService } from '../api/parada';
import { paradaLineaService } from '../api/parada_linea';

export default function IncidenciasPage() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [lineas, setLineas] = useState<any[]>([]);
  const [paradas, setParadas] = useState<any[]>([]);
  
  // Estados para el formulario
  const [titulo, setTitulo] = useState('');
  const [descripcion, setDescripcion] = useState('');
  const [lineaId, setLineaId] = useState('');
  const [paradaId, setParadaId] = useState('');
  
  // Estados para el listado e incidencias
  const [incidencias, setIncidencias] = useState<any[]>([]); 
  const [loading, setLoading] = useState(false);
  
  // Estados para los filtros
  const [filterLineaId, setFilterLineaId] = useState('');
  const [filterParadaId, setFilterParadaId] = useState('');
  const [filterParadas, setFilterParadas] = useState<any[]>([]);

  // Funciones de ayuda
  const cargarParadasDeLinea = async (id: number) => {
    const relaciones = await paradaLineaService.get_parada_lineas_by_linea_id(id);
    const paradasIds = relaciones.map((rel: any) => rel.parada_id);
    return await Promise.all(
      paradasIds.map((pid: number) => paradaService.get_parada_by_id(pid))
    );
  };

  const getIncidencias = async () => {
    setLoading(true);
    try {
      if (filterParadaId) {
        const data = await incidenciaService.get_incidencias_by_parada_id(parseInt(filterParadaId));
        setIncidencias(data);
      } else if (filterLineaId) {
        const data = await incidenciaService.get_incidencias_by_linea_id(parseInt(filterLineaId));
        setIncidencias(data);
      } else {
        const data = await incidenciaService.get_incidencias();
        setIncidencias(data);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Cargar líneas al inicio y las incidencias globales
  useEffect(() => {
    lineaService
      .get_lineas()
      .then((data) =>
        setLineas(
          [...data].sort((a, b) =>
            String(a.labelLinea ?? a.nombre ?? '').localeCompare(String(b.labelLinea ?? b.nombre ?? ''))
          )
        )
      )
      .catch(console.error);
    getIncidencias();
  }, []);

  // Efecto para recargar incidencias cuando cambian los filtros
  useEffect(() => {
    getIncidencias();
  }, [filterLineaId, filterParadaId]);

  // Efecto para cargar paradas del FORMULARIO
  useEffect(() => {
    if (lineaId) {
      setParadaId('');
      cargarParadasDeLinea(parseInt(lineaId))
        .then(setParadas)
        .catch(console.error);
    } else {
      setParadas([]);
      setParadaId('');
    }
  }, [lineaId]);

  // Efecto para cargar paradas del FILTRO
  useEffect(() => {
    if (filterLineaId) {
      setFilterParadaId('');
      cargarParadasDeLinea(parseInt(filterLineaId))
        .then(setFilterParadas)
        .catch(console.error);
    } else {
      setFilterParadas([]);
      setFilterParadaId('');
    }
  }, [filterLineaId]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!titulo || !descripcion || !lineaId) {
      alert("Por favor, rellena los campos obligatorios.");
      return;
    }

    const payload = {
      titulo,
      descripcion,
      linea_id: parseInt(lineaId),
      parada_id: paradaId ? parseInt(paradaId) : null
    };

    try {
      await incidenciaService.create_incidencia(payload);
      alert("Incidencia reportada correctamente");
      setIsModalOpen(false);
      // Limpiar el formulario
      setTitulo(''); setDescripcion(''); setLineaId(''); setParadaId('');
      // Refrescar las incidencias mostradas
      getIncidencias();
    } catch (err) {
      console.error(err);
      alert("Error al reportar la incidencia. Revisa la consola.");
    }
  };

  return (
    <div className="space-y-6 relative">
      <div className="flex justify-between items-center border-b border-neutral-800 pb-4">
        <h1 className="text-2xl font-bold tracking-tight text-neutral-100">Gestión de Incidencias</h1>
        <button 
          onClick={() => setIsModalOpen(true)}
          className="bg-red-600 hover:bg-red-500 text-white font-medium px-5 py-2 transition-all hover:-translate-y-1"
        >
          Reportar Incidencia
        </button>
      </div>

      <div className="bg-neutral-900 border border-neutral-800 p-6 mb-6">
        <h2 className="text-lg font-semibold text-neutral-300 mb-4">Filtrar Incidencias</h2>
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1">
            <label className="block text-sm font-medium text-neutral-400 mb-1">Por Línea</label>
            <select 
              value={filterLineaId}
              onChange={(e) => setFilterLineaId(e.target.value)}
              className="w-full bg-neutral-950 border border-neutral-800 text-white p-2.5 focus:border-red-500 outline-none transition-colors"
            >
              <option value="">Todas las líneas</option>
              {lineas.map(linea => (
                <option key={linea.id} value={linea.id}>
                  {linea.nombre || linea.numero ? `Línea ${linea.numero || linea.nombre}` : `${linea.labelLinea}`}
                </option>
              ))}
            </select>
          </div>
          <div className="flex-1">
            <label className="block text-sm font-medium text-neutral-400 mb-1">Por Parada</label>
            <select 
              value={filterParadaId}
              onChange={(e) => setFilterParadaId(e.target.value)}
              disabled={!filterLineaId}
              className={`w-full p-2.5 outline-none transition-colors border ${
                !filterLineaId 
                  ? 'bg-neutral-900 border-neutral-800 text-neutral-600 cursor-not-allowed' 
                  : 'bg-neutral-950 border-neutral-800 text-white focus:border-red-500'
              }`}
            >
              <option value="">{!filterLineaId ? "-- Elige línea primero --" : "Todas las paradas"}</option>
              {filterParadas.map(parada => (
                <option key={parada.id} value={parada.id}>
                  {parada.nombre || `Parada ${parada.id}`}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {loading ? (
        <div className="text-center py-20 text-neutral-400">Cargando incidencias...</div>
      ) : incidencias.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {incidencias.map((inc) => (
            <div key={inc.id} className="bg-neutral-900 border border-neutral-800 border-t-4 border-t-red-600 p-5 hover:border-red-500 hover:border-t-red-500 transition-colors">
              <div className="flex justify-between items-start mb-3">
                <h3 className="text-xl font-bold text-white">{inc.titulo}</h3>
              </div>
              <p className="text-neutral-400 text-sm mb-4 line-clamp-3">{inc.descripcion}</p>
              
              <div className="pt-3 border-t border-neutral-800 text-xs text-neutral-500 space-y-1">
                <p>
                  <span className="font-semibold text-neutral-400">Línea afectada:</span> {
                    lineas.find(l => l.id === inc.linea_id)?.labelLinea || 
                    lineas.find(l => l.id === inc.linea_id)?.numero || 
                    `${inc.linea}`
                  }
                </p>
                {inc.parada_id && (
                  <p>
                    <span className="font-semibold text-neutral-400">Parada:</span> ID {inc.parada_id}
                  </p>
                )}
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="bg-neutral-900 border border-neutral-800 p-6 flex flex-col items-center justify-center min-h-[300px]">
          <h2 className="text-xl mb-2 text-neutral-400 font-semibold">Panel de incidencias</h2>
          <p className="text-neutral-500 text-center max-w-md mb-6">Aquí se mostrarán los reportes registrados sobre el estado del tráfico o incidencias técnicas de los autobuses. Actualmente no hay incidencias para estos filtros.</p>
        </div>
      )}

      {/* Modal de Creación */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 px-4">
          <div className="bg-neutral-900 border border-neutral-700 p-8 w-full max-w-lg shadow-2xl relative">
            <h2 className="text-2xl font-bold text-white mb-6">Nueva Incidencia</h2>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-neutral-400 mb-1">Título *</label>
                <input 
                  type="text" 
                  required
                  value={titulo}
                  onChange={(e) => setTitulo(e.target.value)}
                  className="w-full bg-neutral-950 border border-neutral-800 text-white p-2.5 focus:border-red-500 outline-none transition-colors"
                  placeholder="Ej: Retraso por obras"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-neutral-400 mb-1">Descripción *</label>
                <textarea 
                  required
                  value={descripcion}
                  onChange={(e) => setDescripcion(e.target.value)}
                  rows={4}
                  className="w-full bg-neutral-950 border border-neutral-800 text-white p-2.5 focus:border-red-500 outline-none transition-colors resize-none"
                  placeholder="Detalles de la incidencia..."
                ></textarea>
              </div>

              <div>
                <label className="block text-sm font-medium text-neutral-400 mb-1">Línea Afectada *</label>
                <select 
                  required
                  value={lineaId}
                  onChange={(e) => setLineaId(e.target.value)}
                  className="w-full bg-neutral-950 border border-neutral-800 text-white p-2.5 focus:border-red-500 outline-none transition-colors"
                >
                  <option value="">-- Selecciona una línea --</option>
                  {lineas.map(linea => (
                    <option key={linea.id} value={linea.id}>
                      {linea.nombre || linea.numero ? `Línea ${linea.numero || linea.nombre}` : `${linea.labelLinea}`}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-neutral-400 mb-1">Parada (Opcional)</label>
                <select 
                  value={paradaId}
                  onChange={(e) => setParadaId(e.target.value)}
                  disabled={!lineaId}
                  className={`w-full p-2.5 outline-none transition-colors border ${
                    !lineaId 
                      ? 'bg-neutral-900 border-neutral-800 text-neutral-600 cursor-not-allowed' 
                      : 'bg-neutral-950 border-neutral-800 text-white focus:border-red-500'
                  }`}
                >
                  <option value="">
                    {!lineaId ? "-- Selecciona primero una línea --" : "-- Ninguna / Aplica a toda la línea --"}
                  </option>
                  {paradas.map(parada => (
                    <option key={parada.id} value={parada.id}>
                      {parada.nombre || `Parada ${parada.id}`}
                    </option>
                  ))}
                </select>
                {!lineaId && (
                  <p className="text-xs text-neutral-500 mt-1">Debes seleccionar una línea para ver sus paradas.</p>
                )}
              </div>

              <div className="flex gap-4 mt-8 pt-4 border-t border-neutral-800">
                <button 
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="flex-1 bg-neutral-800 hover:bg-neutral-700 text-white p-3 font-medium transition-colors"
                >
                  Cancelar
                </button>
                <button 
                  type="submit"
                  className="flex-1 bg-red-600 hover:bg-red-500 text-white p-3 font-medium transition-colors"
                >
                  Confirmar Reporte
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
