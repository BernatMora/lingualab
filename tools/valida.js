// valida.js — comprova que el literal `initialTexts` d'un index.html és vàlid i complet.
// Ús: node tools/valida.js ../index.html
const fs = require("fs");
const ruta = process.argv[2];
const h = fs.readFileSync(ruta, "utf8");
const i = h.indexOf("const initialTexts");
if (i < 0) { console.error("no trobo initialTexts"); process.exit(1); }
const s = h.indexOf("[", i);
let fons = 0, e = -1;
for (let k = s; k < h.length; k++) {
  const c = h[k];
  if (c === "[") fons++;
  else if (c === "]") { fons--; if (fons === 0) { e = k + 1; break; } }
}
if (e < 0) { console.error("el literal no es tanca"); process.exit(1); }
let arr;
try {
  arr = new Function("return " + h.slice(s, e))();
} catch (err) {
  console.error("el literal no és vàlid: " + err.message);
  process.exit(1);
}
// title i type poden venir del META a l'hora d'executar-se, així que no són obligatoris
const caps = ["id", "level", "en", "es", "keys"];
const incomplets = arr.filter((x) => !caps.every((c) => typeof x[c] === "string" && x[c].length > 0));
if (incomplets.length) {
  console.error("objectes incomplets: " + incomplets.map((x) => x.id || "?").join(", "));
  process.exit(1);
}
const ids = new Set(arr.map((x) => x.id));
if (ids.size !== arr.length) { console.error("hi ha ids repetits"); process.exit(1); }
const expressions = arr.reduce(
  (n, x) => n + x.keys.split("\n").filter((l) => l.includes(":")).length, 0);
const nivells = [...new Set(arr.map((x) => x.level))].sort().join("/");
console.log("OK textos=" + arr.length + " expressions=" + expressions + " nivells=" + nivells);
