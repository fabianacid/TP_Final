# Instrucciones para Integrar Capítulos 4 y 5 en Overleaf

## 📁 Archivos Generados

```
test_results/
├── capitulos_4_y_5.tex                    ← Contenido LaTeX completo
├── INSTRUCCIONES_OVERLEAF.md              ← Este archivo
└── graficos/
    ├── grafico_rmse_mape.pdf              ← Gráfico comparativo modelos ML
    ├── grafico_ticker_performance.pdf     ← Rendimiento por ticker
    ├── grafico_matriz_confusion.pdf       ← Matriz confusión sentimiento
    ├── grafico_latencia_componentes.pdf   ← Latencia por componente
    ├── grafico_pruebas_carga.pdf          ← Pruebas de escalabilidad
    └── *.png                              ← Versiones PNG para preview
```

## 🚀 Pasos para Integrar en Overleaf

### 1. Subir Archivos a Overleaf

1. Abre tu proyecto en Overleaf: https://www.overleaf.com
2. En el panel izquierdo, haz clic en **"Upload"** (ícono de carpeta con flecha)
3. Sube **TODOS los archivos PDF** de la carpeta `graficos/`:
   - grafico_rmse_mape.pdf
   - grafico_ticker_performance.pdf
   - grafico_matriz_confusion.pdf
   - grafico_latencia_componentes.pdf
   - grafico_pruebas_carga.pdf

4. **Importante**: Crea una carpeta llamada `graficos` en Overleaf y coloca todos los PDFs ahí
   - Clic derecho en el panel izquierdo → "New Folder" → Nombrar "graficos"
   - Arrastra los PDFs a esa carpeta

### 2. Copiar el Contenido LaTeX

1. Abre el archivo `capitulos_4_y_5.tex` con cualquier editor de texto
2. Copia **TODO el contenido**
3. En Overleaf, ubica el punto donde quieres insertar los capítulos (después del Capítulo 3)
4. Pega el contenido completo

### 3. Verificar Referencias de Imágenes

Las imágenes se referencian así en el archivo .tex:

```latex
\includegraphics[width=0.9\textwidth]{graficos/grafico_rmse_mape.pdf}
```

**Asegúrate que**:
- La carpeta se llame exactamente `graficos` (sin tildes, sin espacios)
- Los nombres de archivos coincidan exactamente (case-sensitive)

### 4. Compilar el Documento

1. En Overleaf, haz clic en **"Recompile"** (botón verde)
2. Si hay errores de compilación, revisa:
   - Que todas las imágenes estén en la carpeta `graficos/`
   - Que los nombres de archivos sean exactos
   - Que tengas los paquetes necesarios (ver sección siguiente)

### 5. Paquetes LaTeX Necesarios

Asegúrate de que tu documento incluya estos paquetes en el preámbulo:

```latex
\usepackage{graphicx}        % Para imágenes
\usepackage{booktabs}        % Para tablas profesionales
\usepackage{multirow}        % Para celdas combinadas
\usepackage[table]{xcolor}   % Para colores en tablas
\usepackage{caption}         % Para captions de figuras/tablas
\usepackage{float}           % Para posicionamiento de figuras
```

Si ya los tienes, perfecto. Si no, agrégalos antes de `\begin{document}`.

## 📊 Contenido Incluido

### Capítulo 4: Ensayos y Resultados (8 páginas aprox.)

**4.1. Evaluación de Modelos ML**
- Tabla comparativa de modelos (Random Forest, XGBoost, LSTM, Prophet, Ensemble)
- Gráfico comparativo RMSE/MAPE
- Tabla de resultados por ticker
- Gráfico de rendimiento por ticker
- Tabla de validación cruzada

**4.2. Evaluación NLP**
- Tabla de métricas de precisión (83.6%)
- Matriz de confusión (gráfico)
- Tabla comparativa de modelos NLP
- Tabla de correlación sentimiento-precio

**4.3. Pruebas End-to-End**
- Tabla de resultados funcionales (30 pruebas, 100% éxito)
- Tabla de latencia por iteración
- Tabla y gráfico de latencia por componente
- Tabla y gráfico de pruebas de carga
- Tabla de validación de requisitos no funcionales

**4.4. Casos de Uso**
- 4 casos de uso detallados (inversor principiante, trader, gestor, alertas)
- Tabla resumen de casos de uso

### Capítulo 5: Conclusiones y Trabajo Futuro (2 páginas aprox.)

**5.1. Resultados Obtenidos**
- Tabla de cumplimiento de objetivos
- Logros principales
- Limitaciones identificadas
- Contribuciones al estado del arte

**5.2. Mejoras Futuras**
- Mejoras de corto, mediano y largo plazo
- Tabla de roadmap de implementación
- Líneas de investigación propuestas
- Conclusiones finales

## ✅ Checklist de Verificación

Antes de compilar, verifica:

- [ ] Todos los PDFs están en la carpeta `graficos/`
- [ ] Los nombres de archivos son exactos (sin espacios, sin cambios)
- [ ] El preámbulo tiene los paquetes necesarios
- [ ] El contenido se pegó después del capítulo correcto
- [ ] Las referencias cruzadas funcionan (`\ref{fig:rmse_mape}`, etc.)
- [ ] Los labels de figuras y tablas no están duplicados con otros capítulos

## 🔧 Solución de Problemas

### Problema: "File not found" para imágenes

**Solución**:
1. Verifica que la ruta sea `graficos/nombre_archivo.pdf`
2. Revisa que el nombre del archivo sea exacto
3. En Overleaf, abre la carpeta `graficos/` y confirma que el archivo esté ahí

### Problema: Tablas muy anchas

**Solución**:
Cambia el tamaño de la tabla con:
```latex
\begin{table}[htbp]
\centering
\small  % o \footnotesize para tablas más pequeñas
...
```

### Problema: Referencias cruzadas no funcionan

**Solución**:
Compila **DOS VECES** en Overleaf. La primera genera los labels, la segunda los resuelve.

### Problema: Figuras en posición incorrecta

**Solución**:
Cambia el parámetro de posicionamiento:
```latex
\begin{figure}[H]  % H = exactamente aquí (requiere package float)
% o
\begin{figure}[!htbp]  % fuerza la posición preferida
```

## 📧 Contacto

Si tienes problemas para integrar los capítulos, revisa:
1. El log de compilación en Overleaf (ícono de advertencia)
2. Que los nombres de archivos sean exactos (case-sensitive)
3. Que la estructura de carpetas sea correcta

## 🎓 Resultado Final

Una vez integrado correctamente, tendrás:
- ✅ Capítulo 4 completo con 5 gráficos profesionales
- ✅ Capítulo 5 completo con conclusiones y trabajo futuro
- ✅ 15+ tablas formateadas profesionalmente
- ✅ Referencias cruzadas funcionando
- ✅ Documento listo para entregar

¡Buena suerte con tu tesis! 🚀
