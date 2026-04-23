import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { lineaService } from '../api/linea';

export default function LineasPage() {
  const [lineas, setLineas] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    lineaService.get_lineas()
      .then(data => {
        setLineas(data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Error al cargar líneas", err);
        setLoading(false);
      });
  }, []);

  const filteredLineas = lineas.filter(linea => {
    const nombre = linea.nombre || `Línea ${linea.labelLinea}`;
    return nombre.toLowerCase().includes(searchQuery.toLowerCase());
  });

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center border-b border-neutral-800 pb-4">
        <h1 className="text-2xl font-bold tracking-tight text-neutral-100">Líneas de Autobus</h1>
        <button className="bg-blue-600 hover:bg-blue-500 text-white font-medium px-5 py-2 transition-all hover:-translate-y-1">
          Actualizar Líneas
        </button>
        <input
          type="text"
          placeholder="Buscar línea..."
          className="ml-4 px-3 py-2 bg-neutral-800 text-neutral-200 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
      </div>

      {loading ? (
        <p className="text-neutral-400">Cargando datos...</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredLineas.length === 0 ? (
            <p className="text-neutral-500">No hay líneas que coincidan con la búsqueda.</p>
          ) : (
            filteredLineas.map(linea => (
              <div key={linea.id} className="bg-neutral-900 border border-neutral-800 hover:border-blue-500 p-5 transition-colors">
                <h3 className="text-xl font-bold mb-2">{linea.nombre || `Línea ${linea.labelLinea}`}</h3>
                <p className="text-neutral-400 text-sm">Información detallada sobre esta línea de transporte.</p>
                <div className="mt-4 pt-4 border-t border-neutral-800 text-right">
                  <Link to={`/lineas/${linea.id}`} className="bg-neutral-800 hover:bg-neutral-700 text-neutral-300 px-4 py-2 text-sm transition-colors">
                    Ver Detalles
                  </Link>
                </div>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}
