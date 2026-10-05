// Cliente de la API local. Toda respuesta del backend es {ok, datos} o {ok:false, error:{codigo, mensaje, ref}}.
export class ErrorApp extends Error {
  constructor(error, status) {
    super(error?.mensaje || "Error desconocido");
    this.codigo = error?.codigo || "ERROR";
    this.ref = error?.ref;
    this.status = status;
  }
}

async function pedir(metodo, ruta, cuerpo) {
  let r;
  try {
    r = await fetch(ruta, {
      method: metodo,
      headers: cuerpo ? { "Content-Type": "application/json" } : {},
      body: cuerpo ? JSON.stringify(cuerpo) : undefined,
    });
  } catch (e) {
    throw new ErrorApp({ codigo: "SIN_CONEXION", mensaje: "No se pudo conectar con el servidor local. ¿Sigue corriendo python3 app/app.py?" }, 0);
  }
  const tipo = r.headers.get("Content-Type") || "";
  if (!tipo.includes("application/json")) {
    if (!r.ok) throw new ErrorApp({ codigo: "HTTP_" + r.status, mensaje: "Respuesta inesperada del servidor." }, r.status);
    return await r.text();
  }
  const j = await r.json();
  if (!j.ok) throw new ErrorApp(j.error, r.status);
  return j.datos;
}

export const api = {
  get: (ruta) => pedir("GET", ruta),
  post: (ruta, cuerpo) => pedir("POST", ruta, cuerpo || {}),
  borrar: (ruta) => pedir("DELETE", ruta),
  texto: async (ruta, cuerpo) => {
    const r = await fetch(ruta, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(cuerpo) });
    if ((r.headers.get("Content-Type") || "").includes("application/json")) {
      const j = await r.json();
      throw new ErrorApp(j.error, r.status);
    }
    return await r.text();
  },
};
