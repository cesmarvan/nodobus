import L from 'leaflet';
import { useEffect, useState } from 'react';
import { CircleMarker, GeoJSON, MapContainer, Marker, Popup, TileLayer } from 'react-leaflet';
import { Link, useParams } from 'react-router-dom';
import { lineaService } from '../api/linea';
import { paradaService } from '../api/parada';
import { paradaLineaService } from '../api/parada_linea';
import { fetcherService } from '../api/fetcher';

// Fix the default marker icon missing in Vite
import iconRetinaUrl from 'leaflet/dist/images/marker-icon-2x.png';
import iconMarkerUrl from 'leaflet/dist/images/marker-icon.png';
import iconShadowUrl from 'leaflet/dist/images/marker-shadow.png';

L.Icon.Default.mergeOptions({
  iconRetinaUrl,
  iconUrl: iconMarkerUrl,
  shadowUrl: iconShadowUrl,
});

// Haversine distance in kilometers
function getDistanceFromLatLonInKm(lat1: number, lon1: number, lat2: number, lon2: number) {
  const R = 6371; // Radius of the earth in km
  const dLat = deg2rad(lat2 - lat1);
  const dLon = deg2rad(lon2 - lon1);
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) *
    Math.sin(dLon / 2) * Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c;
}

function deg2rad(deg: number) {
  return deg * (Math.PI / 180);
}

// Algoritmo de estimación de ETA (Opción 2 simplificada para frontend)
function calculateETA(paradaTarget: any, todosAutobuses: any[], todasParadas: any[]) {
  if (!todosAutobuses || todosAutobuses.length === 0) return null;

  const [lonTarget, latTarget] = paradaTarget.localizacion.coordinates;
  const VELOCIDAD_MEDIA_KMH = 15; // 15 km/h media de un autobús urbano
  const PENALIZACION_PARADA_MIN = 0.5; // 30s asumiendo subida/bajada de pasajeros

  let minEta = Infinity;

  todosAutobuses.forEach(bus => {
    if (bus.latitudE6 == null || bus.longitudE6 == null) return;
    const busLat = bus.latitudE6 / 1000000;
    const busLon = bus.longitudE6 / 1000000;

    const distanciaKm = getDistanceFromLatLonInKm(busLat, busLon, latTarget, lonTarget);
    
    // Contar posible número de paradas intermedias:
    // Se buscan aquellas paradas que estén "de camino" (aprox. dentro del área entre el bus y el destino)
    let paradasIntermedias = 0;
    todasParadas.forEach(p => {
      if (p.id === paradaTarget.id) return;
      if (!p.localizacion || !p.localizacion.coordinates) return;
      
      const [pLon, pLat] = p.localizacion.coordinates;
      const dToTarget = getDistanceFromLatLonInKm(pLat, pLon, latTarget, lonTarget);
      const dToBus = getDistanceFromLatLonInKm(pLat, pLon, busLat, busLon);
      
      // Si la suma de distancias al bus y al destino es solo un poco mayor que la distancia directa
      // entonces podemos asumir que la parada queda de camino
      if (dToTarget < distanciaKm && dToBus < distanciaKm) {
        if (Math.abs((dToTarget + dToBus) - distanciaKm) < 0.8) {
          paradasIntermedias++;
        }
      }
    });

    const tiempoPorDistanciaMin = (distanciaKm / VELOCIDAD_MEDIA_KMH) * 60;
    const etaTotalMin = tiempoPorDistanciaMin + (paradasIntermedias * PENALIZACION_PARADA_MIN);

    if (etaTotalMin < minEta) {
      minEta = etaTotalMin;
    }
  });

  return minEta !== Infinity ? Math.ceil(minEta) : null;
}

export default function LineaDetallePage() {
  const { id } = useParams<{ id: string }>();
  const [linea, setLinea] = useState<any>(null);
  const [autobuses, setAutobuses] = useState<any[]>([]);
  const [paradas, setParadas] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  // Sevilla coordinates
  const sevillePosition: [number, number] = [37.3891, -5.9845];

  const fetchRealTimeBuses = async (labelLinea: string) => {
    try {
      const formattedLabel = String(labelLinea).length === 1 ? String(labelLinea).padStart(2, '0') : labelLinea;
      const data = await fetcherService.get_real_time_buses(formattedLabel);
      console.log("Successfully fetched buses:", data);
      return data.result || [];
    } catch (error) {
      console.error("Error fetching real-time buses from backend:", error);
      return [];
    }
  };

  const fetchLineaData = async () => {
    try {
      if (!id) return;
      const lineaIdNum = Number(id);
      
      const [lineaData, paradaLineasData] = await Promise.all([
        lineaService.get_linea_by_id(lineaIdNum),
        paradaLineaService.get_parada_lineas_by_linea_id(lineaIdNum)
      ]);
      
      // Fetch details for each parada
      const paradaPromises = paradaLineasData.map((pl: any) =>
        paradaService.get_parada_by_id(pl.parada_id).catch(() => null)
      );
      
      const paradasData = await Promise.all(paradaPromises);
      setParadas(paradasData.filter(Boolean));
      
      // Fetch initial real-time buses
      const busesData = await fetchRealTimeBuses(lineaData.labelLinea);
      setAutobuses(busesData);
      
      setLinea(lineaData);
    } catch (err) {
      console.error("Error fetching data:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLineaData();
  }, [id]);

  // Set up automatic bus fetching every 10 seconds
  useEffect(() => {
    if (!linea?.labelLinea) return;

    // Fetch immediately
    const fetchBuses = async () => {
      const busesData = await fetchRealTimeBuses(linea.labelLinea);
      setAutobuses(busesData);
    };

    fetchBuses();

    // Set up interval for every 10 seconds
    const interval = setInterval(fetchBuses, 10000);

    // Clean up interval on unmount or when linea changes
    return () => clearInterval(interval);
  }, [linea?.labelLinea]);

  const handleRefreshBuses = async () => {
    if (linea?.labelLinea) {
      const busesData = await fetchRealTimeBuses(linea.labelLinea);
      setAutobuses(busesData);
    }
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <p className="text-neutral-400">Cargando mapa de la línea...</p>
      </div>
    );
  }

  if (!linea) {
    return (
      <div className="space-y-6">
        <p className="text-red-400">Error: No se ha encontrado la línea.</p>
        <Link to="/" className="text-blue-500 hover:text-blue-400">Volver a Líneas</Link>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center border-b border-neutral-800 pb-4">
        <div>
          <Link to="/" className="text-blue-500 hover:text-blue-400 text-sm mb-2 inline-block">
            &larr; Volver a Líneas
          </Link>
          <h1 className="text-3xl font-bold tracking-tight text-neutral-100 flex items-center gap-3">
            <span 
              className="w-8 h-8 rounded-sm inline-flex items-center justify-center text-white text-base" 
              style={{ backgroundColor: linea.color || '#3b82f6' }}
            >
              {linea.labelLinea}
            </span>
            {linea.nombreLinea || linea.nombre}
          </h1>
          <p className="text-neutral-400 mt-1">Destino: {linea.destino}</p>
        </div>
        <button 
          onClick={handleRefreshBuses}
          className="bg-neutral-800 hover:bg-neutral-700 text-neutral-200 font-medium px-4 py-2 transition-all hover:text-white"
        >
          Actualizar ahora
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Panel de Info / Buses */}
        <div className="lg:col-span-1 bg-neutral-900 border border-neutral-800 p-5 space-y-4">
          <h2 className="text-lg font-semibold text-neutral-200 border-b border-neutral-800 pb-2">
            Autobuses ({autobuses.length})
          </h2>
          <div className="space-y-3 max-h-[500px] overflow-y-auto pr-2">
            {autobuses.length === 0 ? (
              <p className="text-neutral-500 text-sm">No hay autobuses en circulación.</p>
            ) : (
              autobuses.map((bus) => (
                <div key={`bus-panel-${bus.vehiculo}`} className="bg-neutral-950 p-3 border border-neutral-800 text-sm">
                  <p className="font-medium text-blue-400">Vehículo: {bus.vehiculo}</p>
                  <p className="text-neutral-400">Sentido: {bus.sentido === 1 ? 'Ida' : 'Vuelta'}</p>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Mapa */}
        <div className="lg:col-span-3 border border-neutral-800 h-[600px] z-0">
          <MapContainer 
            center={sevillePosition} 
            zoom={13} 
            style={{ height: "100%", width: "100%", zIndex: 1 }}
          >
            <TileLayer
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            
            {/* Dibujar la ruta de la línea */}
            {linea.recorrido && (
              <GeoJSON 
                data={linea.recorrido} 
                style={{ 
                  color: linea.color || '#3b82f6', 
                  weight: 5,
                  opacity: 0.7 
                }} 
              />
            )}

            {/* Dibujar las paradas como círculos (nodos) */}
            {paradas.map((parada) => {
              if (!parada.localizacion || !parada.localizacion.coordinates) return null;
              
              const [lon, lat] = parada.localizacion.coordinates;
              const eta = calculateETA(parada, autobuses, paradas);

              return (
                <CircleMarker 
                  key={`parada-${parada.id}`} 
                  center={[lat, lon]}
                  radius={6}
                  pathOptions={{ 
                    color: '#ffffff', 
                    weight: 2,
                    fillColor: linea.color || '#3b82f6', 
                    fillOpacity: 1 
                  }}
                >
                  <Popup>
                    <div className="text-neutral-900 border-none p-0 m-0">
                      <strong>{parada.nombre}</strong><br/>
                      {eta !== null ? (
                        <span className="text-blue-600 font-semibold mt-1 inline-block">
                          Próximo bus: {eta} {eta === 1 ? 'minuto' : 'minutos'}
                        </span>
                      ) : (
                        <span className="text-neutral-500 mt-1 inline-block">Calculando ETA...</span>
                      )}
                    </div>
                  </Popup>
                </CircleMarker>
              );
            })}

            {/* Dibujar los buses (posición leída desde la API temporal de TUSSAM) */}
            {autobuses.map((bus) => {
              if (bus.latitudE6 == null || bus.longitudE6 == null) return null;
              
              const lat = bus.latitudE6 / 1000000;
              const lon = bus.longitudE6 / 1000000;

              const busIcon = L.divIcon({
                className: 'custom-bus-node',
                html: `<div style="width: 16px; height: 16px; background-color: #ef4444; border: 2px solid white;"></div>`,
                iconSize: [16, 16],
                iconAnchor: [8, 8]
              });

              return (
                <Marker key={`bus-${bus.vehiculo}`} position={[lat, lon]} icon={busIcon}>
                  <Popup>
                    <div className="text-neutral-900 border-none p-0 m-0">
                      <strong>Vehículo: {bus.vehiculo}</strong><br/>
                      Línea: {linea.labelLinea}<br/>
                      Sentido: {bus.sentido === 1 ? 'Ida' : 'Vuelta'}
                    </div>
                  </Popup>
                </Marker>
              );
            })}
          </MapContainer>
        </div>
      </div>
    </div>
  );
}