#ifndef PROJECTILE_HPP
#define PROJECTILE_HPP

#include "Vector3D.hpp"
#include "Constants.hpp"
#include "Telemetry.hpp"

/**
 * @brief State structure for RK4 solver
 */
struct State {
    Vector3D pos;
    Vector3D vel;
};

class Projectile {
public:
    State state;
    Vector3D targetPos;    // Hedef koordinatları
    Vector3D windVelocity;
    double mass;
    double baseDragCoeff;
    double area;
    bool isGuided;         // Güdüm açık/kapalı

    Projectile(Vector3D pos, Vector3D vel, Vector3D target, Vector3D wind, double m, double cd, double a, bool guided = true)
        : targetPos(target), windVelocity(wind), mass(m), baseDragCoeff(cd), area(a), isGuided(guided) {
        state.pos = pos;
        state.vel = vel;
    }

    double getAirDensity(double h) const {
        if (h < 0) h = 0;
        if (h > 11000) h = 11000;
        double T = Constants::T0 - Constants::L * h;
        return Constants::RHO_0 * std::pow(T / Constants::T0, ((-Constants::GRAVITY) / (Constants::R * Constants::L)) - 1.0);
    }

    double getDynamicDragCoeff(double velocityMag) const {
        double mach = velocityMag / Constants::SOS_0;
        if (mach > 0.8 && mach < 1.2) return baseDragCoeff * 2.8;
        if (mach >= 1.2) return baseDragCoeff * 1.5;
        return baseDragCoeff;
    }

    /**
     * @brief Proportional Navigation (PN) Güdüm Algoritması
     * Hedefe kilitlenip rotayı düzeltir.
     */
    Vector3D calculateGuidanceAcceleration() const {
        if (!isGuided) return {0, 0, 0};

        Vector3D relativePos = targetPos - state.pos;
        Vector3D los = relativePos.normalize();
        double closingSpeed = state.vel.length();
        
        // Basit Güdüm Kanunu (N=3.0)
        Vector3D guidanceDir = los * 3.0 - state.vel.normalize();
        Vector3D guidanceAcc = guidanceDir * (closingSpeed * 0.4);

        // Fiziksel Limit: Füze maksimum 5G manevra yapabilir
        double maxG = 5.0 * 9.81;
        if (guidanceAcc.length() > maxG) {
            guidanceAcc = guidanceAcc.normalize() * maxG;
        }

        return guidanceAcc;
    }

    State derivative(const State& s) const {
        Vector3D gravityAcc(0, Constants::GRAVITY, 0);
        Vector3D relativeVel = s.vel - windVelocity;
        double vMag = relativeVel.length();

        if (vMag < 0.001) return {s.vel, gravityAcc};

        double currentRho = getAirDensity(s.pos.y);
        double currentCd = getDynamicDragCoeff(vMag);
        double dragMag = 0.5 * currentRho * (vMag * vMag) * currentCd * area;
        Vector3D dragAcc = relativeVel.normalize() * (-dragMag / mass);

        Vector3D guidanceAcc = calculateGuidanceAcceleration();

        return {s.vel, gravityAcc + dragAcc + guidanceAcc};
    }

    void update(double dt) {
        State k1 = derivative(state);
        State s2 = {state.pos + k1.pos * (dt * 0.5), state.vel + k1.vel * (dt * 0.5)};
        State k2 = derivative(s2);
        State s3 = {state.pos + k2.pos * (dt * 0.5), state.vel + k2.vel * (dt * 0.5)};
        State k3 = derivative(s3);
        State s4 = {state.pos + k3.pos * dt, state.vel + k3.vel * dt};
        State k4 = derivative(s4);

        state.pos = state.pos + (k1.pos + k2.pos * 2.0 + k3.pos * 2.0 + k4.pos) * (dt / 6.0);
        state.vel = state.vel + (k1.vel + k2.vel * 2.0 + k3.vel * 2.0 + k4.vel) * (dt / 6.0);
    }

    TelemetryData getTelemetry(double t) const {
        double vMag = state.vel.length();
        double rho = getAirDensity(state.pos.y);
        return {t, state.pos, state.vel, vMag / Constants::SOS_0, rho, 0.5 * rho * vMag * vMag};
    }
};

#endif
