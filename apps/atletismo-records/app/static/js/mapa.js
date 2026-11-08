/* Mapa interactivo de los recintos donde se han marcado records mundiales. */

(function () {
  "use strict";

  const RECINTOS = JSON.parse(document.getElementById("datos-recintos").textContent);

  const mapa = L.map("mapa", {
    worldCopyJump: true,
    scrollWheelZoom: false
  }).setView([25, 10], 2);

  L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 18,
    attribution:
      '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
  }).addTo(mapa);

  // Desplazar el zoom con Ctrl, para no interferir con el scroll de la pagina
  mapa.on("click", function () {
    mapa.scrollWheelZoom.enable();
  });
  mapa.on("mouseout", function () {
    mapa.scrollWheelZoom.disable();
  });

  // Agrupa los records por recinto
  const porRecinto = new Map();
  RECINTOS.forEach(function (recinto) {
    porRecinto.set(recinto.id, recinto);
  });

  const marcas = [];

  porRecinto.forEach(function (recinto) {
    if (recinto.lat === null || recinto.lon === null) {
      return;
    }

    // El radio del marcador crece con la altitud del recinto
    const altitud = recinto.altitud_estimada || 0;
    const radio = Math.max(9, Math.min(24, 9 + altitud / 120));

    const clase = recinto.modalidades && recinto.modalidades.indexOf("calle") !== -1
      ? "marcador calle"
      : "marcador";

    const icono = L.divIcon({
      className: "",
      html: '<div class="' + clase + '" style="width:' + radio + "px;height:" + radio + 'px"></div>',
      iconSize: [radio, radio],
      iconAnchor: [radio / 2, radio / 2],
      popupAnchor: [0, -radio / 2]
    });

    const marcasTexto = (recinto.pruebas || [])
      .map(function (p) {
        return p.prueba + " - " + p.marca + " (" + p.atleta + ")";
      })
      .join("<br>");

    const popup =
      "<b>" + recinto.nombre + "</b>" +
      '<span class="detalle">' + recinto.ciudad + "</span>" +
      '<span class="detalle">Altitud: ' + altitud + " m</span>" +
      '<hr style="margin:.5rem 0;border:none;border-top:1px solid #dfe3ea">' +
      marcasTexto;

    const posicion = [recinto.lat, recinto.lon];
    marcas.push(posicion);

    L.marker(posicion, { icon: icono })
      .addTo(mapa)
      .bindPopup(popup);
  });

  // Ajusta el encuadre a los marcadores visibles
  if (marcas.length) {
    mapa.fitBounds(marcas);
  }
})();
