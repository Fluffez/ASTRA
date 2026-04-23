#ifndef CONSTANTS_HPP
#define CONSTANTS_HPP

namespace Constants {
    const double GRAVITY = -9.80665;
    const double PI = 3.141592653589793;
    
    // ISA Atmosfer Sabitleri
    const double RHO_0 = 1.225;        // Deniz seviyesi yoğunluk (kg/m3)
    const double T0 = 288.15;          // Deniz seviyesi sıcaklık (K)
    const double L = 0.0065;           // Sıcaklık düşüş oranı (K/m)
    const double R = 287.05;           // Hava gaz sabiti (J/kgK)
    const double SOS_0 = 340.29;       // Deniz seviyesi ses hızı (m/s)
}

#endif
