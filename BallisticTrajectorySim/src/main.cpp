#include <iostream>
#include <fstream>
#include "include/Projectile.hpp"

int main() {
    // Başlangıç Koşulları
    Vector3D startPos(0, 0, 0);
    double launchSpeed = 850.0; 
    double launchAngle = 45.0 * Constants::PI / 180.0;
    Vector3D startVel(launchSpeed * cos(launchAngle), launchSpeed * sin(launchAngle), 0);
    
    // HEDEF: 20 km menzilde, 500 metre solda bir hedef
    Vector3D target(20000.0, 0, 500.0);
    
    // Rüzgar: Z ekseninde 10 m/s (Füze bunu yenmek zorunda)
    Vector3D wind(0, 0, 10.0); 

    Projectile missile(startPos, startVel, target, wind, 43.0, 0.22, 0.018, true);

    double dt = 0.01;
    double time = 0.0;
    
    std::ofstream dataFile("trajectory_data.csv");
    if (!dataFile.is_open()) {
        std::cerr << "Dosya acilamadi!" << std::endl;
        return 1;
    }

    dataFile << "Time,X,Y,Z,Velocity,Density,Mach,DynamicPressure\n";

    std::cout << "Gudumlu Fuze Simulasyonu baslatildi..." << std::endl;

    while (missile.state.pos.y >= 0) {
        TelemetryData tData = missile.getTelemetry(time);
        
        dataFile << tData.timestamp << "," 
                 << tData.position.x << "," 
                 << tData.position.y << "," 
                 << tData.position.z << "," 
                 << tData.velocity.length() << ","
                 << tData.airDensity << ","
                 << tData.machNumber << ","
                 << tData.dynamicPressure << "\n";
        
        missile.update(dt);
        time += dt;
        
        if (time > 500.0) break;
    }
    dataFile.close();
    std::cout << "Simulasyon bitti. Hedef Sapmasi: " << (missile.state.pos - target).length() << " m\n";
    return 0;
}
