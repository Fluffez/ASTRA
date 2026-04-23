#ifndef TELEMETRY_HPP
#define TELEMETRY_HPP

#include "Vector3D.hpp"

/**
 * @brief Telemetri verisi - Merminin belirli bir andaki tüm durumunu saklar.
 * Roketsan'da veriler bu şekilde paketlenir.
 */
struct TelemetryData {
    double timestamp;
    Vector3D position;
    Vector3D velocity;
    double machNumber;
    double airDensity;
    double dynamicPressure; // q = 0.5 * rho * v^2 (Mühendislik için kritik)
};

#endif
