
--
-- Servidor: localhost:3306
-- Tiempo de generación: 17-09-2024 a las 03:59:31
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.0.30


CREATE TABLE `carteras` (
  `id` int(11) NOT NULL,
  `nombre` varchar(20) NOT NULL,
  `valor` int(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `extractos` (
  `id` int(255) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  `salida_dinero` varchar(255) NOT NULL,
  `entrada_dinero` varchar(255) DEFAULT NULL,
  `valor_movido` int(255) NOT NULL,
  `fecha_de_creacion` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `metas` (
  `id` int(255) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  `valor_meta` int(255) NOT NULL,
  `cuota_fija` int(255) NOT NULL,
  `valor_restante` int(255) DEFAULT NULL,
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

ALTER TABLE `carteras`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `extractos`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `metas`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `carteras`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=0;

ALTER TABLE `extractos`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=0;

ALTER TABLE `metas`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=0;
COMMIT;

