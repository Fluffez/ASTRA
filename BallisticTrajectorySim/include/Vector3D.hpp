#ifndef VECTOR3D_HPP
#define VECTOR3D_HPP

#include <cmath>

struct Vector3D {
    double x, y, z;
    Vector3D(double x = 0.0, double y = 0.0, double z = 0.0) : x(x), y(y), z(z) {}
    Vector3D operator+(const Vector3D& other) const { return {x + other.x, y + other.y, z + other.z}; }
    Vector3D operator-(const Vector3D& other) const { return {x - other.x, y - other.y, z - other.z}; }
    Vector3D operator*(double scalar) const { return {x * scalar, y * scalar, z * scalar}; }
    double length() const { return std::sqrt(x * x + y * y + z * z); }
    Vector3D normalize() const {
        double len = length();
        if (len > 0) return *this * (1.0 / len);
        return {0, 0, 0};
    }
};

#endif
